
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .services import send_invoice_sms
from .whatsapp import send_invoice_whatsapp
from .models import Invoice, InvoiceItem
from customers.models import Customer
from products.models import Product


def invoice_list(request):
    invoices = Invoice.objects.select_related("customer").order_by("-created_at")

    return render(
        request,
        "invoices/invoice_list.html",
        {"invoices": invoices},
    )


def create_invoice(request):
    customers = Customer.objects.all().order_by("first_name")
    products = Product.objects.all().order_by("name")

    if request.method != "POST":
        return render(
            request,
            "invoices/create_invoice.html",
            {"customers": customers, "products": products},
        )

    customer_id = request.POST.get("customer")
    product_ids = request.POST.getlist("product")
    quantities = request.POST.getlist("quantity")

    try:
        if not customer_id:
            raise ValidationError("Please select a customer.")

        customer = Customer.objects.get(pk=customer_id)

        if not product_ids or len(product_ids) != len(quantities):
            raise ValidationError(
                "Please select at least one product and enter its quantity."
            )

        # Combine repeated products into one total quantity.
        requested_quantities = {}

        for product_id, quantity_text in zip(product_ids, quantities):
            if not product_id:
                raise ValidationError("Please select a product for every row.")

            try:
                quantity = int(quantity_text)
            except (TypeError, ValueError):
                raise ValidationError("Every quantity must be a whole number.")

            if quantity < 1:
                raise ValidationError("Every quantity must be at least 1.")

            requested_quantities[product_id] = (
                requested_quantities.get(product_id, 0) + quantity
            )

        invoice = None

        with transaction.atomic():
            # Lock product records where supported by the database.
            locked_products = Product.objects.select_for_update().filter(
                pk__in=requested_quantities.keys()
            )
            product_map = {str(p.pk): p for p in locked_products}

            if len(product_map) != len(requested_quantities):
                raise ValidationError(
                    "One or more selected products no longer exist."
                )

            # Validate every product before creating the invoice.
            for product_id, quantity in requested_quantities.items():
                product = product_map[product_id]

                if quantity > product.quantity_in_stock:
                    raise ValidationError(
                        f"Not enough stock for {product.name}. "
                        f"Available: {product.quantity_in_stock}; "
                        f"requested: {quantity}."
                    )

            # Preserve the existing invoice numbering style.
            last_invoice = Invoice.objects.order_by("-id").first()
            number = last_invoice.id + 1 if last_invoice else 1
            invoice_number = f"INV{number:03d}"

            invoice = Invoice.objects.create(
                invoice_number=invoice_number,
                customer=customer,
            )

            for product_id, quantity in requested_quantities.items():
                product = product_map[product_id]

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=quantity,
                    price=product.selling_price,
                )

                product.quantity_in_stock -= quantity
                product.save(update_fields=["quantity_in_stock"])

        # Notifications happen after the database transaction succeeds.
        # Notification failures must not undo or misreport a saved invoice.
        try:
            send_invoice_sms(invoice)
        except Exception as exc:
            print(f"Invoice saved, but SMS notification failed: {exc}")

        try:
            send_invoice_whatsapp(invoice)
        except Exception as exc:
            print(f"Invoice saved, but WhatsApp notification failed: {exc}")

        return redirect("invoice_detail", pk=invoice.pk)

    except (ValidationError, Customer.DoesNotExist, ValueError) as exc:
        if isinstance(exc, ValidationError):
            error = "; ".join(exc.messages)
        elif isinstance(exc, Customer.DoesNotExist):
            error = "The selected customer was not found."
        else:
            error = "Please check the customer, products, and quantities."

        return render(
            request,
            "invoices/create_invoice.html",
            {
                "customers": customers,
                "products": products,
                "error": error,
            },
        )


def invoice_detail(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related("customer").prefetch_related(
            "items__product"
        ),
        pk=pk,
    )

    return render(
        request,
        "invoices/invoice_detail.html",
        {"invoice": invoice},
    )


def send_whatsapp(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related("customer"),
        pk=pk,
    )

    customer = invoice.customer
    phone = customer.phone.replace(" ", "").replace("-", "").strip()

    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+"):
        phone = phone[1:]

    import urllib.parse
    from django.http import HttpResponseRedirect

    message = (
        f"Hello {customer.first_name},\n\n"
        f"Thank you for shopping with BudTech Enterprise.\n"
        f"Invoice No: {invoice.invoice_number}\n"
        f"Total: KSh {invoice.total_amount():,.2f}\n\n"
        "Thank you for your business."
    )

    url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"
    return HttpResponseRedirect(url)
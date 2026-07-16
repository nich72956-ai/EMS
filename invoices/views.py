from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
import urllib.parse

from .services import send_invoice_sms
from .whatsapp import send_invoice_whatsapp
from .models import Invoice, InvoiceItem
from customers.models import Customer
from products.models import Product


def invoice_list(request):
    invoices = Invoice.objects.all()

    return render(
        request,
        'invoices/invoice_list.html',
        {'invoices': invoices}
    )


def create_invoice(request):

    if request.method == "POST":

        customer_id = request.POST.get('customer')
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        customer = Customer.objects.get(id=customer_id)
        product = Product.objects.get(id=product_id)

        # Check stock availability
        if quantity > product.quantity_in_stock:
            return render(
                request,
                'invoices/create_invoice.html',
                {
                    'customers': Customer.objects.all(),
                    'products': Product.objects.all(),
                    'error': 'Not enough stock available.'
                }
            )

        # Generate invoice number
        last_invoice = Invoice.objects.order_by('id').last()

        if last_invoice:
            number = last_invoice.id + 1
        else:
            number = 1

        invoice_number = f"INV{number:03d}"

        try:
            with transaction.atomic():

                # Create invoice
                invoice = Invoice.objects.create(
                    invoice_number=invoice_number,
                    customer=customer
                )

                # Add invoice item
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=quantity,
                    price=product.selling_price
                )

                # Reduce stock
                product.quantity_in_stock -= quantity
                product.save()

            # Send notifications after successful save
            print("ABOUT TO SEND SMS")
            send_invoice_sms(invoice)
            send_invoice_whatsapp(invoice)
            print("SMS FUNCTION FINISHED")

            return redirect('invoice_list')

        except Exception as e:
            return render(
                request,
                'invoices/create_invoice.html',
                {
                    'customers': Customer.objects.all(),
                    'products': Product.objects.all(),
                    'error': f'Error creating invoice: {e}'
                }
            )

    customers = Customer.objects.all()
    products = Product.objects.all()

    return render(
        request,
        'invoices/create_invoice.html',
        {
            'customers': customers,
            'products': products,
        }
    )


def invoice_detail(request, pk):

    invoice = get_object_or_404(Invoice, pk=pk)

    return render(
        request,
        'invoices/invoice_detail.html',
        {
            'invoice': invoice
        }
    )
def send_whatsapp(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    customer = invoice.customer
    phone = customer.phone.replace(" ", "").strip()

    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+254"):
        phone = phone[1:]

    message = f"""
Hello {customer.first_name},

Thank you for shopping with BudTech Enterprise.

Invoice No: {invoice.invoice_number}

Your invoice has been created successfully.

Thank you for your business.
"""

    url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"

    return HttpResponseRedirect(url)


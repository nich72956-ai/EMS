from django.shortcuts import render
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

from products.models import Product, Category
from customers.models import Customer
from suppliers.models import Supplier
from purchases.models import Purchase
from invoices.models import Invoice, InvoiceItem


def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_customers = Customer.objects.count()
    total_suppliers = Supplier.objects.count()
    total_purchases = Purchase.objects.count()
    total_invoices = Invoice.objects.count()

    total_stock = sum(
        product.quantity_in_stock
        for product in Product.objects.all()
    )

    low_stock = Product.objects.filter(
        quantity_in_stock__lte=10
    ).count()

    # Calculate total revenue
    total_revenue = InvoiceItem.objects.aggregate(
        revenue=Sum(
            ExpressionWrapper(
                F("quantity") * F("price"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
    )["revenue"] or 0

    context = {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_customers": total_customers,
        "total_suppliers": total_suppliers,
        "total_purchases": total_purchases,
        "total_invoices": total_invoices,
        "total_stock": total_stock,
        "low_stock": low_stock,
        "total_revenue": total_revenue,
    }

    return render(request, "core/dashboard.html", context)
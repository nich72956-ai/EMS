from django.shortcuts import render
from django.db.models import Count

from products.models import Product
from customers.models import Customer
from suppliers.models import Supplier
from purchases.models import Purchase
from invoices.models import Invoice


def reports_dashboard(request):
    invoices = Invoice.objects.all()

    # Calculate total revenue
    total_revenue = sum(invoice.total_amount() for invoice in invoices)

    # Monthly invoice counts for the chart
    monthly_sales = (
        Invoice.objects
        .values("created_at__month")
        .annotate(total=Count("id"))
        .order_by("created_at__month")
    )

    context = {
        "total_products": Product.objects.count(),
        "total_customers": Customer.objects.count(),
        "total_suppliers": Supplier.objects.count(),
        "total_purchases": Purchase.objects.count(),
        "total_invoices": invoices.count(),
        "total_revenue": total_revenue,
        "low_stock": Product.objects.filter(quantity_in_stock__lte=10),

        # Chart data
        "months": [item["created_at__month"] for item in monthly_sales],
        "sales": [item["total"] for item in monthly_sales],
    }

    return render(
        request,
        "reports/dashboard.html",
        context,
    )
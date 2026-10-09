
from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from .forms import SupplierForm
from purchases.models import Purchase


def supplier_list(request):
    suppliers = Supplier.objects.all().order_by("company_name")
    return render(
        request,
        "suppliers/supplier_list.html",
        {"suppliers": suppliers},
    )


def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("supplier_list")
    else:
        form = SupplierForm()

    return render(
        request,
        "suppliers/add_supplier.html",
        {"form": form},
    )


def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)

        if form.is_valid():
            form.save()
            return redirect("supplier_list")
    else:
        form = SupplierForm(instance=supplier)

    return render(
        request,
        "suppliers/edit_supplier.html",
        {"form": form, "supplier": supplier},
    )


def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    has_purchases = Purchase.objects.filter(supplier=supplier).exists()

    if request.method == "POST":
        if has_purchases:
            return render(
                request,
                "suppliers/delete_supplier.html",
                {
                    "supplier": supplier,
                    "has_purchases": True,
                    "error_message": (
                        "This supplier cannot be deleted because purchase "
                        "records are linked to it. Preserve the purchase "
                        "history and keep this supplier record."
                    ),
                },
            )

        supplier.delete()
        return redirect("supplier_list")

    return render(
        request,
        "suppliers/delete_supplier.html",
        {
            "supplier": supplier,
            "has_purchases": has_purchases,
        },
    )
from django.shortcuts import render, redirect
from .models import Purchase
from .forms import PurchaseForm
from products.models import Product


def purchase_list(request):
    purchases = Purchase.objects.all()

    return render(
        request,
        'purchases/purchase_list.html',
        {'purchases': purchases}
    )


def add_purchase(request):

    if request.method == "POST":

        form = PurchaseForm(request.POST)

        if form.is_valid():

            purchase = form.save()

            product = purchase.product
            product.quantity_in_stock += purchase.quantity
            product.save()

            return redirect('purchase_list')

    else:
        form = PurchaseForm()

    return render(
        request,
        'purchases/add_purchase.html',
        {'form': form}
    )
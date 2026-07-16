from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Product
from .forms import ProductForm


def generate_sku():
    """
    Generate the next SKU in the format:
    BUD000001
    BUD000002
    """
    last_product = Product.objects.order_by("-id").first()

    if not last_product or not last_product.sku:
        return "BUD000001"

    try:
        last_number = int(last_product.sku.replace("BUD", ""))
        return f"BUD{last_number + 1:06d}"
    except ValueError:
        return "BUD000001"


def product_list(request):
    search = request.GET.get("search")

    products = Product.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    paginator = Paginator(products, 5)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    return render(request, "products/product_list.html", {
        "products": products
    })


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)

            if not product.sku:
                product.sku = generate_sku()

            product.save()

            return redirect("product_list")
    else:
        form = ProductForm()

    return render(request, "products/add_product.html", {
        "form": form
    })


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "products/add_product.html", {
        "form": form
    })


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(request, "products/delete_product.html", {
        "product": product
    })
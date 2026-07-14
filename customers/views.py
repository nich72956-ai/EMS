from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from .forms import CustomerForm
from django.db.models import Q

def customer_list(request):
    query = request.GET.get('q')

    if query:
        customers = Customer.objects.filter(
            Q(customer_code__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query)
        )
    else:
        customers = Customer.objects.all()

    context = {
        'customers': customers,
        'query': query
    }

    return render(request, 'customers/customer_list.html', context)
from .forms import CustomerForm
from django.shortcuts import redirect


def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('customer_list')

    else:
        form = CustomerForm()

    return render(request, 'customers/add_customer.html', {'form': form})
from django.shortcuts import get_object_or_404


def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            return redirect('customer_list')

    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/edit_customer.html', {'form': form})
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')

    return render(request, 'customers/delete_customer.html', {'customer': customer})
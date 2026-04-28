from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Purchase, RewardRedemption


def home(request):
    customer = None

    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        name = request.POST.get("name", "").strip()
        qty = int(request.POST.get("quantity", "0"))
        staff = request.POST.get("staff_name", "").strip()

        customer, created = Customer.objects.get_or_create(
            phone=phone,
            defaults={"name": name}
        )

        if name and not customer.name:
            customer.name = name
            customer.save()

        if qty > 0:
            Purchase.objects.create(
                customer=customer,
                quantity=qty,
                staff_name=staff
            )

        return redirect("customer_detail", customer_id=customer.id)

    return render(request, "loyalty/home.html", {"customer": customer})


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    return render(request, "loyalty/customer_detail.html", {
        "customer": customer,
        "balance": customer.total_active_qty(),
        "free_available": customer.free_available(),
        "purchases": customer.purchases.order_by("-created_at"),
        "rewards": customer.rewards.order_by("-redeemed_at"),
    })


def redeem(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if customer.free_available() > 0:
        RewardRedemption.objects.create(customer=customer, quantity=1)

    return redirect("customer_detail", customer_id=customer.id)
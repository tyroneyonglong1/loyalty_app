from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Purchase, RewardRedemption


def customer_lookup(request):
    phone = request.GET.get("phone", "").strip()
    customer = Customer.objects.filter(phone=phone).first()

    if customer:
        return JsonResponse({
            "exists": True,
            "name": customer.name,
            "customer_id": customer.id,
        })

    return JsonResponse({"exists": False})


def home(request):
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        name = request.POST.get("name", "").strip()

        customer = Customer.objects.filter(phone=phone).first()

        if not customer:
            customer = Customer.objects.create(phone=phone, name=name)

        return redirect("customer_detail", customer_id=customer.id)

    return render(request, "loyalty/home.html")


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    return render(request, "loyalty/customer_detail.html", {
        "customer": customer,
        "balance": customer.total_active_qty(),
        "free_available": customer.free_available(),
        "purchases": customer.purchases.order_by("-created_at"),
        "rewards": customer.rewards.order_by("-redeemed_at"),
    })


@login_required
def staff_panel(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":
        qty = int(request.POST.get("quantity", "0"))

        if qty > 0:
            Purchase.objects.create(
                customer=customer,
                quantity=qty,
                staff_name=request.user.username
            )

        return redirect("customer_detail", customer_id=customer.id)

    return render(request, "loyalty/staff_panel.html", {
        "customer": customer,
        "balance": customer.total_active_qty(),
        "free_available": customer.free_available(),
    })


@login_required
def redeem(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST" and customer.free_available() > 0:
        RewardRedemption.objects.create(
            customer=customer,
            quantity=1,
            staff_name=request.user.username
        )

    return redirect("customer_detail", customer_id=customer.id)
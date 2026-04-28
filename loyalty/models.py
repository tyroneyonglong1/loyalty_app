from django.db import models


class Customer(models.Model):
    phone = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_active_qty(self):
        bought = sum(p.quantity for p in self.purchases.all())
        redeemed = sum(r.quantity * 10 for r in self.rewards.all())
        return bought - redeemed

    def free_available(self):
        return self.total_active_qty() // 10

    def __str__(self):
        return self.phone


class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="purchases")
    quantity = models.PositiveIntegerField()
    staff_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RewardRedemption(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="rewards")
    quantity = models.PositiveIntegerField(default=1)
    staff_name = models.CharField(max_length=100, blank=True)
    redeemed_at = models.DateTimeField(auto_now_add=True)
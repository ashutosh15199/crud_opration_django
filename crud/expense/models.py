from django.db import models

from .userModel import CustomUser
class Transection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    transection_type = models.CharField(
        max_length=100, choices=(("CREDIT", "CREDIT"), ("DEBIT", "DEBIT"))
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def format_amount(self):
        if self.amount >= 1_00_00_000:  # 1 Crore
            return f"{self.amount / 1_00_00_000:.2f} Cr"
        elif self.amount >= 1_00_000:  # 1 Lakh
            return f"{self.amount / 1_00_000:.2f} L"
        return f"{self.amount:.2f}"  # Default as normal number

    def __str__(self):
        return f"{self.title} - {self.transection_type} - {self.format_amount()}"

       
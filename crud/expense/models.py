from django.db import models
class Transection(models.Model):
    title = models.CharField(max_length=100)
    amount=models.FloatField()
    transection_type=models.CharField(max_length=100,choices=(("CREDIT","CREDIT"),("DEBIT","DEBIT")))

    def save(self,*args,**kwargs):
        if self.transection_type=="DEBIT" and self.amount>0:
            self.amount=self.amount*-1
        super().save(*args,**kwargs)

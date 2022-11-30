from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json
import os

class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # User는 django.contrib.auth.models가 제공하는 모델
    modify_date = models.DateTimeField(null=True, blank=True)
    pcode = models.CharField(max_length=10)
    pname = models.TextField()
    unitprice = models.IntegerField(default=0)
    discountrate = models.DecimalField(max_digits=11, decimal_places=2,default=0)
    mainfunc = models.CharField(max_length=100, default="")
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    detailfunc = models.CharField(max_length=200, default="")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.pcode} {self.pname} {self.unitprice} {self.discountrate} {self.mainfunc}"


class SalesInfo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True)
    scode = models.CharField(max_length=10, null=False, blank=False)
    sale_date = models.DateTimeField(null=False, blank=False)
    qty = models.IntegerField(default=1)
    amt = models.IntegerField(default=0)
    main_inst = models.CharField(max_length=4, default="")
    detail_inst = models.TextField(default="")

class Sales_History(models.Model):
    udate = models.DateTimeField(null=True, blank=True)
    scode = models.CharField(max_length=10)
    sale_date = models.DateTimeField(null=False, blank=False)
    qty = models.IntegerField(default=1)
    amt = models.IntegerField(default=0)
    main_inst = models.CharField(max_length=4, default="")
    detail_inst = models.TextField(default="")
    uexplain = models.CharField(max_length=20, null=False)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
from itertools import product
from PIL import Image
from django.db import models
import uuid
from django.utils import timezone
from user.models import BaseUser

TYPE=([1,'coin'],[2,'jewelry'],[3,'gold_bullion'])
UNIT=([1,'ons'],[2,'methghal'],[3,'geram'])
PAYMENT=([1,'cash'],[2,'credit'])

class Product(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    user=models.ForeignKey(BaseUser,on_delete=models.CASCADE,related_name='product_user')
    name=models.CharField(max_length=55)
    type=models.IntegerField(choices=TYPE)
    weight=models.FloatField(default=0.0)
    unit=models.IntegerField(choices=UNIT)
    inventory=models.IntegerField()
    date=models.DateField(default=timezone.now)
    image=models.ImageField(default='def.jpg',upload_to='product_image')
    description=models.CharField(max_length=255,blank=True,null=True)

    def save(self,*args,**kwargs):
        super().save()
        img=Image.open(self.image.path)
        if img.height>500 or img.width>500:
            img.thumbnail((500,500))
            img.save(self.image.path)
        img.close()
    
    def __str__(self) -> str:
        return "{} ({})".format(self.name,self.id)


class Factor(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    seller=models.ForeignKey(BaseUser,on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=155)
    payment_type = models.IntegerField(choices=PAYMENT, default=1)
    total_price = models.CharField(max_length=255)
    tax =models.CharField(max_length=255)
    discount = models.CharField(max_length=255)
    comment = models.CharField(max_length=755,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id}"
    

class ProductSold(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    factor=models.ForeignKey(Factor,on_delete=models.CASCADE,related_name='product_sold')
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=155)
    price=models.CharField(max_length=155)
    number=models.IntegerField()

    def __str__(self) :
        return f"{self.id}"
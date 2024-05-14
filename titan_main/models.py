from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    pap = models.FloatField(default=0.0)
    isk = models.FloatField(default=0.0)
    skill = models.FloatField(default=0.0)
    lp = models.FloatField(default=0.0)
    used_lp = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    item_name = models.CharField(max_length=100, unique=True)
    item_price = models.FloatField()
    item_description = models.TextField()
    item_image = models.URLField()

    def __str__(self):
        return self.item_name


class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    order_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=10)
    lp_cost = models.FloatField()
    item_name = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_quantity = models.PositiveIntegerField()
    nickname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.order_id


class Apply(models.Model):
    apply_id = models.CharField(max_length=100, unique=True)
    apply_time = models.DateTimeField(auto_now_add=True)
    apply_status = models.CharField(max_length=10)
    nickname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    kill_record = models.JSONField()
    apply_description = models.TextField()

    def __str__(self):
        return self.apply_id

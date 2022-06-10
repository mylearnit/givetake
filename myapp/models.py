
from django.db import models
from treebeard.mp_tree import MP_Node
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    total_give_help = models.FloatField(default=0)
    total_pmf = models.FloatField(default=0)
    total_received_help = models.FloatField(default=0)
    mobile = models.CharField(max_length=20, blank=True)
    gpay = models.CharField(max_length=200, blank=True)

class BinaryTree(MP_Node):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    is_paid = models.ManyToManyField('User', related_name='+')
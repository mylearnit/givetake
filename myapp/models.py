
from django.db import models
from treebeard.mp_tree import MP_Node
from django.contrib.auth.models import AbstractUser
import random
class User(AbstractUser):
    total_give_help = models.FloatField(default=0)
    total_pmf = models.FloatField(default=0)
    total_received_help = models.FloatField(default=0)
    mobile = models.CharField(max_length=20, blank=True)
    gpay = models.CharField(max_length=200, blank=True)

class BinaryTree(MP_Node):
    id = models.IntegerField(primary_key=True, editable=False)

    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    payment = models.ManyToManyField('User', related_name='+', through='PaymentDetails')
    def save(self, *args, **kwargs):
        # https://stackoverflow.com/a/47323224/2351696
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = random.randint(10000000, 90000000)
                is_id_exist = BinaryTree.objects.filter(id=id).exists()
                
            self.id = id

        super().save(*args, **kwargs)



class PaymentDetails(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    binarytree = models.ForeignKey('BinaryTree', on_delete=models.CASCADE)
    # marked by admin
    is_paid = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    # marked by user
    screenshotfile = models.ImageField(upload_to='screenshotfile/', blank=True, null=True)
    payment_done_requested = models.BooleanField(default=False)
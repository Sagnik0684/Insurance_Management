from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Customer/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=10,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
    
class CustomerPolicy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=100)
    policy_name = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=100)
    start_date = models.DateField()
    renewal_date = models.DateField()

    def __str__(self):
        return f'{self.policy_name} ({self.policy_number})'
    

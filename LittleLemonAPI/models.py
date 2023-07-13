from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser, Group
# from django.conf import settings

# User = settings.AUTH_USER_MODEL

# class CustomGroup(Group):
#     description = models.TextField(blank=True)

# class User(AbstractBaseUser):
#     GROUP_CHOICES = (
#         ("customer", "Customer"),
#         ("delivery_crew", "Delivery Crew"),
#         ("manager", "Manager"),
#         ("admin", "Admin")
#     )
    # email = models.EmailField(verbose_name="email", max_length=70, unique=True)
    # username = models.CharField(max_length=30, unique=True)
    # date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    # last_login = models.DateTimeField(verbose_name='date joined', auto_now=True)
    # is_active = models.BooleanField(default=True)
    # group = models.ManyToManyField(CustomGroup, max_length=20, choices=GROUP_CHOICES, default='customer')
    # group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='customer')
    # groups = models.ManyToManyField(Group, blank=True, related_name='custom_users_groups')
    # user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_users_permissions')
    # pass

    # USERNAME_FIELD = "username"

# Group.add_to_class("Manager", Group(name='Manager'))
# Group.add_to_class("Delivery Crew", Group(name='Delivery Crew'))


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self)-> str:
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    inventory = models.SmallIntegerField(db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1, db_index=True)
    
    class Meta:
        verbose_name_plural = "Menu Items"
        # ordering = ("-category",)
    
    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(null=False, blank=False, default=1),
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ("menuitem", "user")
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ("order","menuitem")

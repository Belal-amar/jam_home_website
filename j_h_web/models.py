from django.db import models
from django.db import models
import re



class UserManager(models.Manager):
    def user_validator(self,postData):
        errors={}
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not postData['fname']:
            errors["missing_field_first_name"]="please fill in First name."
        else:
            if len(postData['fname']) < 2:
                errors["first_name_length"]="First name should be at least 2 charchters"

        if not postData['lname']:
            errors["missing_field_last_name"]="please fill in Last name."
        else:
            if len(postData['lname']) < 2:
                errors["last_name_length"]="Last name should be at least 2 charchters"

        if not postData['email']:
            errors["missing_field_email"]="please fill in Email."
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors["email"]="invalid Email address!"

        if not postData['password'] or not postData['c_pw']:
            errors["missing_field_password"]="Please enter password & confirm password"
        else:
            if len(postData['password']) <8:
                errors["password_length"]="password should be at least 8 charachters"

            else:
                if postData['password']!=postData['c_pw']:
                    errors["password_confirm"]="password not match!"

        users = User.objects.filter(email = postData['email'])
        if users:
            errors['Email']="The email is alredy exist !"


        return errors
        
    def login_validator(self,postData):
        errors={}
        if not postData['email']:
            errors["confirm"]="Invalid Email or Password"
        return errors




class User(models.Model):
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
    is_admin=models.BooleanField(default=False)
    contact=models.CharField(max_length=15)
    email=models.EmailField(max_length=200,unique=True)
    password=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.TextField()

class Product(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.TextField()
    quantity=models.PositiveBigIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")



class Order(models.Model):
    user=models.ForeignKey(User,related_name="uorder",on_delete=models.CASCADE)
    order_at=models.DateTimeField(auto_now_add=True)
    shipping_address=models.CharField(max_length=250)
    status=models.CharField(max_length=20,default="Staged")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Orderitem(models.Model):
    order=models.ForeignKey(Order,related_name="orderprod",on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        def hasNumbers(inputString):
            return any(char.isdigit() for char in inputString)
        errors = {}
        if(postData['form_type'] == "registration_form"):
            if len(postData['first_name']) < 2 or hasNumbers(postData['first_name']):
                errors["first_name"] = "First Name should be at least 2 characters with letters only"
            if len(postData['last_name']) < 2 or hasNumbers(postData['last_name']):
                errors["last_name"] = "Last Name should be at least 2 characters with letters only"
            if not EMAIL_REGEX.match(postData['user_email']):
                errors['user_email'] = "Email should be in a valid format"
            user= User.objects.filter(email=postData['user_email'])
            if user:
                errors['user_email_taken'] = "This email is already registered"
            if len(postData['user_password']) < 8 or postData['user_confirm_pw'] != postData['user_password']:
                errors['user_password'] = "Passwords should be at least 8 characters and should match"
        elif(postData['form_type'] == "login_form"):
            if not EMAIL_REGEX.match(postData['user_email']):
                errors['user_email'] = "Email should be in a valid format"
            if len(postData['user_password']) < 8:
                errors['user_password'] = "Password should be at least 8 characters"
        return errors

class WishManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['wish_title']) < 3:
            errors["wish_title"] = "A wish must consist of at least 3 characters!"
        if len(postData['wish_desc']) < 3:
            errors["wish_desc"] = "A description must be provided!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hashed_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    wish_title = models.CharField(max_length=255)
    desc = models.TextField()
    granted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upload_by = models.ForeignKey(User, related_name="wishes", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_wishes")
    objects = WishManager()
from django.db import models
import re

from django.db.models.deletion import CASCADE

class ValidationTest(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be more than two characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be more than two characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        emaildupcheck = User.objects.filter(email=postData['email'])
        if emaildupcheck == postData['email']:
            errors['email'] = "That email address already exists. Did you forget your password?"
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters."
        if not postData['confirm-pw'] == postData['password']:
            errors['confirm-pw'] = "Password mismatch. Maybe a typo? Please try again!"
        
        return errors

class TripManager(models.Manager):
    def validator(self,postData,postFiles):
        errors={}
        if not postData["name"]:
            errors["name"] = "tour's name should be no empty entries "
        if not postData["end_date"]:
            errors["end_date"] = "End Date should be no empty entries "
        if not postData["start_date"]:
            errors["start_date"] = "Start Date should be no empty entries "
        if 'image' in postFiles:
            if not postFiles["image"].name.endswith((".jpg",".png",".gif","jpeg")):
                errors["image"] = "should be ends with jpg ,png,gif or jpeg "
        else:
            errors['image']="Sorry, image field cannot be empty"
        if len(postData['description']) < 3:
            errors["description"] = " Description should be more than 3 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidationTest()

class Trip(models.Model):
    name = models.CharField(max_length=255)
    description=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    image=models.ImageField(upload_to='images/', null=True, blank=True)
    # one to many relationship (one user can create many trips)
    created_user = models.ForeignKey(User, related_name="created_trips", on_delete=models.CASCADE)
    # many to many relationship (one user can create many trips and one trip can be added for many users)
    users=models.ManyToManyField(User, related_name="added_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=TripManager()

class Review(models.Model):
    riv = models.TextField()
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, related_name="reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Comment(models.Model):
    comment = models.TextField()
    poster = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    on_reviews = models.ForeignKey(Review, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


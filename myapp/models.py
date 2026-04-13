from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Business(models.Model):
    name = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    pincode = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=200)
    established_year = models.CharField(max_length=200)
    liscence_number = models.CharField(max_length=200)
    plantype = models.CharField(max_length=200)
    status = models.CharField(max_length=200, default='pending')
    starting_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    USER = models.OneToOneField(User,on_delete=models.CASCADE)

class Users(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    photo = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    dob = models.DateField()
    USER=models.OneToOneField(User,on_delete=models.CASCADE)


class Station(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    photo = models.CharField(max_length=200)
    BUSINESS = models.ForeignKey(Business, on_delete=models.CASCADE)


class Slot(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=200)
    from_time = models.TimeField()
    to_time = models.TimeField()
    STATION = models.ForeignKey(Station, on_delete=models.CASCADE)


class Subscription(models.Model):
    plan_type = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)


class Payment(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=200)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)
    SUBSCRIPTION = models.ForeignKey(Subscription, on_delete=models.CASCADE)


class Reports(models.Model):
    SUBSCRIPTION = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    PAYMENT = models.ForeignKey(Payment, on_delete=models.CASCADE)

class Complaint(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=200)
    complaint = models.CharField(max_length=200)
    reply = models.CharField(max_length=200)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)



class Booking(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=200)
    tokens=models.CharField(max_length=200)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)
    SLOT = models.ForeignKey(Slot, on_delete=models.CASCADE)
    expected_time=models.TimeField(default='10:00:00')


class Token(models.Model):
    count = models.CharField(max_length=200)
    BOOKING = models.ForeignKey(Booking, on_delete=models.CASCADE)

class Review(models.Model):
    Rating = models.CharField(max_length=200)
    Review = models.CharField(max_length=200)
    date = models.DateField(max_length=200)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)












import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# Create your views here.
from myapp.models import Subscription, Complaint, Users, Business, Review, Station, Slot, Booking


def login_get(request):
    return render(request,'login.html')

#
# def login_post(request):
#     username=request.POST['username']
#     password=request.POST['password']
#     check =authenticate(request,username=username,password=password)
#     if check is not None:
#         login (request,check)
#         if check.groups.filter(name='Admin').exists():
#             return redirect('/myapp/admin_home_get/')
#         elif check.groups.filter(name='Business').exists():
#             return redirect('/myapp/business_home_get/')
#         else:
#             return redirect ('/myapp/login_get/')
#     else:
#         return redirect ('/myapp/login_get/')



def login_post(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    check = authenticate(request, username=username, password=password)

    if check is None:
        messages.error(request, "Invalid username or password")
        return redirect('/myapp/login_get/')

    if check.groups.filter(name='Admin').exists():
        login(request, check)
        messages.success(request,"Admin Login Succsesfull")
        return redirect('/myapp/admin_home_get/')

    if check.groups.filter(name='Business').exists():
        try:
            biz = Business.objects.get(USER=check)
        except Business.DoesNotExist:
            messages.error(request, "Business Account Not Found")
            return redirect('/myapp/login_get/')

        today = date.today()

        if biz.status == "blocked":
            messages.error(request, "Your account is blocked by Admin.")
            return redirect('/myapp/login_get/')

        if biz.expiry_date is None or biz.expiry_date < today:
            messages.error(request, "Subscription expired. Please renew.")
            return redirect('/myapp/login_get/')

        login(request, check)
        messages.success(request, 'Login Successful')
        return redirect('/myapp/business_home_get/')


    messages.error(request, "No permission to login.")
    return redirect('/myapp/login_get/')



@login_required(login_url='/myapp/login_get/')
def Logout_get(request):
    logout (request)
    messages.success(request,'Logout Successful')
    return redirect('/myapp/login_get/')


@login_required(login_url='/myapp/login_get/')
def admin_home_get (request):
    return render(request,'admin/admin_home.html')



@login_required(login_url='/myapp/login_get/')
def changepassword_get(request):
    return render(request,'admin/changepassword.html')

def changepassword_post(request):
    currentpass=request.POST['currentpass']
    newpass=request.POST['newpass']
    confirmpass=request.POST['confirmpass']
    data=request.user
    if data.check_password(currentpass):
        if newpass==confirmpass:
            data.set_password(newpass)
            data.save()
            return redirect('/myapp/login_get/#a')
        else:
            return redirect('/myapp/changepassword_get/#a')
    else:
        return redirect('/myapp/changepassword_get/#a')


@login_required(login_url='/myapp/login_get/')
def AddSubscription_get(request):
    return render(request,'admin/addsubcriptioncharge.html')

def AddSubscription_post(request):
    plantype=request.POST['plantype']
    amount = request.POST['amount']

    a=Subscription()
    a.plan_type=plantype
    a.amount=amount
    a.save()
    messages.success(request,'Subscription Added Successfully')
    return redirect('/myapp/view_subscription_get/#a')

@login_required(login_url='/myapp/login_get/')
def EditSubscription_get(request,id):
    a=Subscription.objects.get(id=id)
    return render(request,'admin/edit_subcriptioncharge.html',{'data':a})

def EditSubscription_post(request):
    id=request.POST['id']
    plantype=request.POST['plantype']
    amount = request.POST['amount']

    a=Subscription.objects.get(id=id)
    a.plan_type=plantype
    a.amount=amount
    a.save()
    messages.success(request,'Subscription Updated')
    return redirect('/myapp/view_subscription_get/')

@login_required(login_url='/myapp/login_get/')
def view_subscription_get(request):
    a=Subscription.objects.all()
    return render(request,'admin/view_subscription_charge.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def delete_subscription_get(request,id):
    Subscription.objects.get(id=id).delete()
    messages.success(request,'Subscription Deleted Successfully')
    return redirect('/myapp/view_subscription_get/')

@login_required(login_url='/myapp/login_get/')
def viewRegisteredBusiness_get(request):
    a=Business.objects.all()
    return render(request,'admin/view_registered_business.html',{'data':a})

def blockbussiness(request,id):
    Business.objects.filter(id=id).update(status='blocked')
    return redirect('/myapp/viewRegisteredBusiness_get/#a')
def unblockbussiness(request,id):
    Business.objects.filter(id=id).update(status='unblocked')
    return redirect('/myapp/viewRegisteredBusiness_get/#a')

@login_required(login_url='/myapp/login_get/')
def SubscriptionPaymentReport_get(request):
    return render(request,'admin/subscription_payment_report.html')

@login_required(login_url='/myapp/login_get/')
def viewComplaintFromUser_get(request):
    a=Complaint.objects.all()
    return render(request,'admin/view_complaint_from_user.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def delete_complaint(request, id):
    Complaint.objects.filter(id=id).delete()
    return redirect('/myapp/viewComplaintFromUser_get/#a')



@login_required(login_url='/myapp/login_get/')
def SentReplyToUser_get(request,id):
    return render(request,'admin/sent_reply_to_user.html',{'id':id})

def SentReplyToUser_post(request):
    id=request.POST['id']
    reply=request.POST['reply']
    a=Complaint.objects.get(id=id)
    a.reply=reply
    a.date=datetime.now().date()
    a.status='Replied'
    a.save()
    return redirect('/myapp/viewComplaintFromUser_get/#a')


@login_required(login_url='/myapp/login_get/')
def viewAppReviews_get(request):
    a=Review.objects.all()
    return render(request,'admin/view_app_reviews.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def delete_review(request, id):
    Review.objects.filter(id=id).delete()
    return redirect('/myapp/viewAppReviews_get/#a')

#
# # @login_required(login_url='/myapp/login_get/')
# def businesssignup_get(request):
#     return render(request,'business/signup.html')
#
# def businesssignup_post(request):
#     name =request.POST['name']
#     logo = request.FILES['logo']
#     email = request.POST['email']
#     pincode = request.POST['pincode']
#     mobile_number = request.POST['mobile_number']
#     established_year = request.POST['established_year']
#     liscence_number = request.POST['liscence_number']
#     password = request.POST['password']
#
#     b=User.objects.create_user(username=email,password=password)
#     b.groups.add(Group.objects.get(name='Business'))
#
#     fs=FileSystemStorage()
#     date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
#     fs.save(date,logo)
#     path=fs.url(date)
#
#     a=Business()
#     a.name=name
#     a.logo=path
#     a.email=email
#     a.pincode=pincode
#     a.mobile_number=mobile_number
#     a.established_year=established_year
#     a.liscence_number=liscence_number
#     a.USER=b
#     a.save()
#     return redirect('/myapp/login_get/')


@login_required(login_url='/myapp/login_get/')
def business_home_get(request):
    return render(request,'business/business_home.html')


@login_required(login_url='/myapp/login_get/')
def businessviewprofile_get(request):
    a=Business.objects.get(USER=request.user)
    return render(request,'business/businessviewprofile.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def editprofile_get(request,id):
    a=Business.objects.get(id=id)
    return render(request,'business/editprofile.html',{'data':a})

def editprofile_post(request):
    id=request.POST['id']
    name =request.POST['name']
    email = request.POST['email']
    pincode = request.POST['pincode']
    mobile_number = request.POST['mobile_number']
    established_year = request.POST['established_year']
    liscence_number = request.POST['liscence_number']

    a=Business.objects.get(id=id)

    if 'logo' in request.FILES:
        logo = request.FILES['logo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(date, logo)
        path = fs.url(date)
        a.logo = path
        a.save()

    a.name=name
    a.email=email
    a.pincode=pincode
    a.mobile_number=mobile_number
    a.established_year=established_year
    a.liscence_number=liscence_number
    a.save()
    messages.success(request,'Profile Updated Successfully')
    return redirect('/myapp/businessviewprofile_get/#a')

@login_required(login_url='/myapp/login_get/')
def add_servicestation_get(request):
    return render(request,'business/addservicestation.html')

def add_servicestation_post(request):
    name = request.POST['name']
    email = request.POST['email']
    mobile_number = request.POST['mobile_number']
    city = request.POST['city']
    state = request.POST['state']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    photo = request.FILES['photo']

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,photo)
    path=fs.url(date)

    a=Station()
    a.name=name
    a.email=email
    a.mobile_number=mobile_number
    a.city=city
    a.state=state
    a.latitude=latitude
    a.longitude=longitude
    a.photo=path
    a.BUSINESS=Business.objects.get(USER=request.user)
    a.save()
    messages.success(request,'Service Station Added Successfully')
    return redirect('/myapp/view_servicestation_get/#a')


@login_required(login_url='/myapp/login_get/')
def edit_servicestation_get(request,id):
    a=Station.objects.get(id=id)
    return render(request,'business/editservicestation.html',{'data':a})

def edit_servicestation_post(request):
    id=request.POST['id']
    name = request.POST['name']
    email = request.POST['email']
    mobile_number = request.POST['mobile_number']
    city = request.POST['city']
    state = request.POST['state']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']

    a = Station.objects.get(id=id)

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(date, photo)
        path = fs.url(date)
        a.photo = path
        a.save()

    a.name = name
    a.email = email
    a.mobile_number = mobile_number
    a.city = city
    a.state = state
    a.latitude = latitude
    a.longitude = longitude
    a.save()
    messages.success(request,'ServiceStation Updated Successfully')
    return redirect('/myapp/view_servicestation_get/#a')


@login_required(login_url='/myapp/login_get/')
def view_servicestation_get(request):
    a=Station.objects.filter(BUSINESS__USER_id=request.user.id)
    return render(request,'business/viewservicestation.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def delete_servicestation_get(request,id):
    Station.objects.get(id=id).delete()
    messages.success(request,'ServiceStation Deleted Successfully')
    return redirect('/myapp/view_servicestation_get/#a')


@login_required(login_url='/myapp/login_get/')
def add_slotcreation_get(request,id):
    return render(request,'business/addslotcreation.html',{'id':id})

def add_slotcreation_post(request):
    id=request.POST['id']
    print(id)
    from_time = request.POST['from_time']
    to_time = request.POST['to_time']

    a=Slot()
    a.from_time = from_time
    a.to_time = to_time
    a.date = datetime.now().date()
    a.status = 'pending'
    a.STATION_id=id
    a.save()
    messages.success(request,'Slot Added Successfully')
    return redirect(f'/myapp/view_slotcreation_get/{id}#a')




@login_required(login_url='/myapp/login_get/')
def view_slotcreation_get(request,id):
    a=Slot.objects.filter(STATION_id=id)
    request.session['sid']=id
    return render(request,'business/viewslotcreation.html', {'data': a,'id':id})


@login_required(login_url='/myapp/login_get/')
def edit_slotcreation_get(request,id):
    a=Slot.objects.get(id=id)
    return render(request,'business/business_editslot.html',{'data':a})

def edit_slotcreation_post(request):
    id=request.POST['id']
    from_time = request.POST['from_time']
    to_time = request.POST['to_time']

    a=Slot.objects.get(id=id)
    a.from_time = from_time
    a.to_time = to_time
    a.save()
    messages.success(request,'Slot Updated Successfully')
    return redirect(f"/myapp/view_slotcreation_get/{request.session['sid']}#a")



@login_required(login_url='/myapp/login_get/')
def delete_slotcreation_get(request,id):
    Slot.objects.get(id=id).delete()
    messages.success(request,'Slot Deleted Successfully')
    return redirect(f"/myapp/view_slotcreation_get/{request.session['sid']}#a")


@login_required(login_url='/myapp/login_get/')
def view_slotbooking(request,sid):
    print(sid,"jjjjjjjj")
    a = Booking.objects.filter(SLOT__STATION_id=sid).order_by('tokens')
    return render(request,'business/viewslotBooking.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def sent_appreviews_get(request):
    return render(request,'business/SentAppReviews.html')

def sent_appreviews_post(request):
    rating=request.POST['rating']
    review=request.POST['review']

    a=Review()
    a.Rating=rating
    a.Review =review
    a.date= datetime.now().date()
    a.USER=request.user
    a.save()
    messages.success(request, 'Success! Your review has been submitted')
    return redirect('/myapp/sent_appreviews_get/')

@login_required(login_url='/myapp/login_get/')
def businesschangepassword_get(request):
    return render(request,'business/businesschangepassword.html')

def businesschangepassword_post(request):
    currentpass=request.POST['currentpass']
    newpass=request.POST['newpass']
    confirmpass=request.POST['confirmpass']
    data=request.user
    if data.check_password(currentpass):
        if newpass==confirmpass:
            data.set_password(newpass)
            data.save()
            messages.success(request,'Password Changed Successfully')
            return redirect('/myapp/login_get/')
        else:
            messages.error(request,'New And Confirm Password Do not Match')
            return redirect('/myapp/businesschangepassword_get/')
    else:
        messages.error(request,'Current Password Do not Match')
        return redirect('/myapp/businesschangepassword_get/')





from datetime import date, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.shortcuts import redirect, render
import razorpay

from .models import Business


PLAN_AMOUNT = {
    "1_month": 500,
    "3_month": 1200,
    "1_year": 4000,
}




def businesssignup_get(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'business/signup.html',{'subscriptions': subscriptions})


def businesssignup_post(request):
    if request.method != "POST":
        return redirect('/myapp/businesssignup_get/')

    plan_id = request.POST.get("plan")

    try:
        # Get the selected subscription from database
        subscription = Subscription.objects.get(id=plan_id)
        amount = int(float(subscription.amount) * 100)  # Convert to paise for Razorpay
        plan_type = subscription.plan_type
    except Subscription.DoesNotExist:
        messages.error(request, "Invalid plan selected")
        return redirect('/myapp/businesssignup_get/')
    except ValueError:
        messages.error(request, "Invalid amount format")
        return redirect('/myapp/businesssignup_get/')

    # Handle image upload
    image_path = ""
    if "image" in request.FILES:
        photo = request.FILES["image"]
        fs = FileSystemStorage()
        ext = photo.name.split(".")[-1].lower()
        filename = f"{request.POST.get('email','user').replace('@','_').replace('.','_')}_{int(__import__('time').time())}.{ext}"
        fs.save(filename, photo)
        image_path = fs.url(filename)

    # Create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    # Send all form data to payment page
    data = dict(request.POST)
    clean_data = {k: v[0] for k, v in data.items()}

    # Add plan details to clean_data
    clean_data['plan_type'] = plan_type
    clean_data['plan_amount'] = subscription.amount

    return render(request, "business/payment.html", {
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "order_id": order["id"],
        "data": clean_data,
        "image_path": image_path
    })


# def businesssignup_post(request):
#
#     if request.method != "POST":
#         return redirect('/myapp/businesssignup_get/')
#
#     plan = request.POST.get("plan")
#     if plan not in PLAN_AMOUNT:
#         messages.error(request, "Invalid plan selected")
#         return redirect('/myapp/signup_get/')
#
#     amount = PLAN_AMOUNT[plan] * 100
#
#     image_path = ""
#     if "image" in request.FILES:
#         photo = request.FILES["image"]
#         fs = FileSystemStorage()
#         ext = photo.name.split(".")[-1].lower()
#         filename = f"{request.POST.get('email','user').replace('@','_').replace('.','_')}_{int(__import__('time').time())}.{ext}"
#         fs.save(filename, photo)
#         image_path = fs.url(filename)
#
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#     order = client.order.create({
#         "amount": amount,
#         "currency": "INR",
#         "payment_capture": 1
#     })
#
#     # Send all form data to payment page
#     # (Since you said no model changes, we keep your hidden input approach)
#     data = dict(request.POST)
#     # request.POST gives list values; convert to simple string
#     clean_data = {k: v[0] for k, v in data.items()}
#
#     return render(request, "business/payment.html", {
#         "razorpay_key": settings.RAZORPAY_KEY_ID,
#         "amount": amount,
#         "order_id": order["id"],
#         "data": clean_data,
#         "image_path": image_path
#     })


@transaction.atomic
def payment_success(request):
    """
    Called after Razorpay payment success.
    - Verifies signature
    - Creates user + business
    - Sets subscription dates
    """
    if request.method != "POST":
        return redirect('/myapp/businesssignup_get/')

    # Razorpay response
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    # Verify Razorpay signature (IMPORTANT)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })
    except Exception:
        messages.error(request, "Payment verification failed.")
        return redirect('/myapp/businesssignup_get/')

    # Get your form values
    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    mobile_number = request.POST.get("mobile_number", "")
    pincode = request.POST.get("pincode", "")
    established_year = request.POST.get("established_year", "")
    liscence_number = request.POST.get("liscence_number", "")
    plan = request.POST.get("plan", "")
    password = request.POST.get("password", "")
    image_path = request.POST.get("image_path", "")

    # Subscription dates
    start_date = date.today()
    if plan == "1_month":
        expiry_date = start_date + timedelta(days=30)
    elif plan == "3_month":
        expiry_date = start_date + timedelta(days=90)
    else:
        expiry_date = start_date + timedelta(days=365)

    # Create or get user
    user, created = User.objects.get_or_create(
        username=email,
        defaults={"email": email}
    )
    if created:
        user.set_password(password)
        user.save()
        # add to Business group (create group manually in admin)
        try:
            group = Group.objects.get(name="Business")
            user.groups.add(group)
        except Group.DoesNotExist:
            pass
    else:
        # prevent duplicate Business
        if Business.objects.filter(USER=user).exists():
            messages.warning(request, "Business already registered.")
            return redirect('/myapp/login_get/')

    business = Business()
    business.name = name
    business.logo = image_path
    business.email = email
    business.pincode = pincode
    business.mobile_number = mobile_number
    business.established_year = established_year
    business.liscence_number = liscence_number
    business.plantype = plan
    business.starting_date = start_date
    business.expiry_date = expiry_date

    business.status = "Active"

    business.USER = user
    business.save()

    messages.success(request, "Registered successfully. Subscription activated.")
    return redirect('/myapp/login_get/')


def businessview_subscription(request):
    a=Business.objects.get(USER=request.user)
    return render(request,'business/viewSubscription.html',{'data':a})

from datetime import date, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
import razorpay

from .models import Business

PLAN_AMOUNT = {
    "1_month": 500,
    "3_month": 1200,
    "1_year": 4000,
}


@login_required
def businessrenew_get(request):
    """
    Show renew plan page
    """
    biz = Business.objects.get(USER=request.user)
    return render(request, "business/renew.html", {"biz": biz})


@login_required
def businessrenew_post(request):
    """
    Create Razorpay order for renewal and open payment page
    """
    if request.method != "POST":
        return redirect("/myapp/businessrenew_get/")

    plan = request.POST.get("plan")
    if plan not in PLAN_AMOUNT:
        messages.error(request, "Invalid plan selected")
        return redirect("/myapp/businessrenew_get/")

    amount = PLAN_AMOUNT[plan] * 100  # paise

    # Create razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    # Pass only required data (no model change)
    data = {
        "plan": plan,
    }

    return render(request, "business/renewpayment.html", {
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "order_id": order["id"],
        "data": data,
    })


@transaction.atomic
@login_required
def businessrenew_success(request):
    """
    Verify payment and update Business subscription.
    EXTENDS plan from current expiry_date if still active.
    """
    if request.method != "POST":
        return redirect("/myapp/businessrenew_get/")

    # Razorpay response
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_signature = request.POST.get("razorpay_signature")
    plan = request.POST.get("plan")

    if plan not in PLAN_AMOUNT:
        messages.error(request, "Invalid plan.")
        return redirect("/myapp/businessrenew_get/")

    # Verify Razorpay signature
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })
    except Exception:
        messages.error(request, "Payment verification failed.")
        return redirect("/myapp/businessrenew_get/")

    biz = Business.objects.get(USER=request.user)

    today = date.today()

    # ✅ Base start: if subscription not expired, extend from existing expiry_date
    if biz.expiry_date and biz.expiry_date >= today:
        base_date = biz.expiry_date
    else:
        base_date = today

    # calculate new expiry
    if plan == "1_month":
        new_expiry = base_date + timedelta(days=30)
    elif plan == "3_month":
        new_expiry = base_date + timedelta(days=90)
    else:
        new_expiry = base_date + timedelta(days=365)

    # Update business subscription
    biz.plantype = plan
    biz.starting_date = today
    biz.expiry_date = new_expiry
    biz.status = "active"
    biz.save()

    messages.success(request, f"Subscription renewed successfully! New expiry: {new_expiry}")
    return redirect("/myapp/businessview_subscription/")




#Users


def user_login(request):
    username=request.POST['username']
    password=request.POST['password']
    check=authenticate(request,username=username,password=password)
    if check is not None:
        login(request,check)
        if check.groups.filter(name='user').exists():
            return JsonResponse({'status':'ok','lid':str(check.id)})
        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status':'no'})


def user_signup(request):
    name=request.POST['name']
    email=request.POST['email']
    photo=request.FILES['photo']
    phoneno=request.POST['phoneno']
    city=request.POST['city']
    state=request.POST['state']
    gender=request.POST['gender']
    dob=request.POST['dob']
    password=request.POST['password']
    confirm_password=request.POST['confirm_password']
    if password!=confirm_password:
        return JsonResponse({'status':'Password doesnot match'})

    b=User.objects.create_user(username=email,password=password)
    b.groups.add(Group.objects.get(name='user'))
    b.save()


    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,photo)
    path=fs.url(date)

    a=Users()
    a.name=name
    a.email=email
    a.photo=path
    a.phone_number=phoneno
    a.city=city
    a.state=state
    a.gender=gender
    a.dob=dob
    a.USER=b
    a.save()
    return JsonResponse({'status':'ok'})


def user_viewprofile(request):
    lid=request.POST['lid']
    a=Users.objects.get(USER=lid)
    return JsonResponse({'status':'ok',
                         'name':a.name,
                         'email':a.email,
                         'photo':a.photo,
                         'phoneno':a.phone_number,
                         'city':a.city,
                         'state':a.state,
                         'gender':a.gender,
                         'dob':a.dob,
                         })


def user_editprofile(request):
    lid=request.POST['lid']
    name=request.POST['name']
    email=request.POST['email']
    phoneno=request.POST['phoneno']
    city=request.POST['city']
    state=request.POST['state']
    gender=request.POST['gender']
    dob=request.POST['dob']

    a=Users.objects.get(USER=lid)
    if 'photo' in request.FILES:
        photo = request.POST['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(date, photo)
        path = fs.url(date)
        a.photo = path

    b=User.objects.get(id=lid)
    b.username=email
    b.save()

    a.name=name
    a.email=email
    a.phone_number=phoneno
    a.city=city
    a.state=state
    a.gender=gender
    a.dob=dob
    a.save()
    return JsonResponse({'status':'ok'})




def user_viewbusiness(request):
    a=Business.objects.all()
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'name':i.name,
                  'logo':i.logo,
                  'email':i.email,
                  'pincode':i.pincode,
                  'phoneno':i.mobile_number,
                  'established_year':i.established_year,
                  'liscence_number':i.liscence_number,
                  'plantype':i.plantype,
                  'status':i.status,
                  'starting_date':i.starting_date,
                  'expiry_date':i.expiry_date,
                  })
        print(l)
    return JsonResponse({'status':'ok','data':l})



def user_viewservicestation(request):
    bid=request.POST['bid']
    a=Station.objects.filter(BUSINESS_id=bid)
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'name':i.name,
                  'email':i.email,
                  'phoneno':i.mobile_number,
                  'city':i.city,
                  'state':i.state,
                  'latitude':i.latitude,
                  'longitude':i.longitude,
                  'photo':i.photo,
                  })
        print(l)
    return JsonResponse({'status':'ok','data':l})


def user_viewfreeslots(request):
    sid=request.POST['sid']
    a = Slot.objects.filter(STATION_id=sid).exclude(status='Booked')
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'date':i.date,
                  'status':i.status,
                  'from_time':i.from_time,
                  'to_time':i.to_time,
                  'station':i.STATION.name,
                  })
    return JsonResponse({'status':'ok','data':l})


def userbook_slot(request):
    sid = request.POST['sid']
    lid = request.POST['lid']

    b=Booking()
    b.status='pending'
    b.date=datetime.now().today()
    b.SLOT_id=sid
    b.USERS=Users.objects.get(USER_id=lid)
    b.save()
    return JsonResponse({'status':'ok'})


# def BusinessApprove_BookingRequest(request,id,sid):
#
#     Slot.objects.filter(id=sid).update(status='Booked')
#     s=Slot.objects.get(id=id)
#
#     a = Booking.objects.get(id=id)
#     b = Booking.objects.count()
#
#     if b == 0 :
#         a.expected_time=s.from_time
#
#     a.status = 'Approved'
#     a.tokens = b + 1
#     a.save()
#
#     return redirect('/myapp/business_home_get/')
#
#
# def check_out_user(request,id):
#     a=Booking.objects.get(id=id)
#     s=Booking.objects.filter(id=id).SLOT.id
#
#     a.expected_time = s.to_time-datetime.now().today()
#     a.save()
#     return redirect('/myapp/business_home_get/')





# from django.shortcuts import get_object_or_404, redirect
# from datetime import datetime, timedelta
#
#
# def BusinessApprove_BookingRequest(request, id, sid,ssid):
#
#     request.session['bokid']=ssid
#     print(request.session['bokid'],"ffffffffffffffffffffff")
#
#
#     booking = get_object_or_404(Booking, id=id)
#     slot = get_object_or_404(Slot, id=sid)
#
#     if booking.status == 'Approved':
#         return redirect('/myapp/business_home_get/')
#
#     slot.status = 'Booked'
#     slot.save()
#
#     approved_bookings = Booking.objects.filter(
#         date=booking.date,
#         status='Approved',
#         SLOT__STATION=slot.STATION
#     ).order_by('tokens')
#
#     if not approved_bookings.exists():
#         booking.tokens = 1
#         booking.expected_time = slot.from_time
#     else:
#         last_booking = approved_bookings.last()
#         last_slot = last_booking.SLOT
#
#         last_expected_dt = datetime.combine(booking.date, last_booking.expected_time)
#         last_slot_from_dt = datetime.combine(booking.date, last_slot.from_time)
#         last_slot_to_dt = datetime.combine(booking.date, last_slot.to_time)
#
#         last_duration = last_slot_to_dt - last_slot_from_dt
#         new_expected_dt = last_expected_dt + last_duration
#
#         booking.tokens = approved_bookings.count() + 1
#         booking.expected_time = new_expected_dt.time()
#
#     booking.status = 'Approved'
#     booking.save()
#
#     return redirect(f"/myapp/view_slotbooking/{request.session['bokid']}#a")

from django.shortcuts import get_object_or_404, redirect
from datetime import datetime

def BusinessApprove_BookingRequest(request, id, sid, ssid):
    request.session['bokid'] = ssid

    booking = get_object_or_404(Booking, id=id)
    slot = get_object_or_404(Slot, id=sid)

    if booking.status == 'Approved':
        return redirect('/myapp/business_home_get/')

    booking.status = 'Approved'
    booking.save()

    slot.status = 'Booked'
    slot.save()

    # same date + same station ഉള്ള എല്ലാ approved bookings earliest slot order-ിൽ
    approved_bookings = Booking.objects.filter(
        date=booking.date,
        status='Approved',
        SLOT__STATION=slot.STATION
    ).select_related('SLOT').order_by('SLOT__from_time', 'id')

    prev_end_dt = None
    token_no = 1

    for b in approved_bookings:
        slot_from_dt = datetime.combine(b.date, b.SLOT.from_time)
        slot_to_dt = datetime.combine(b.date, b.SLOT.to_time)
        duration = slot_to_dt - slot_from_dt

        b.tokens = token_no

        if token_no == 1:
            b.expected_time = b.SLOT.from_time
            prev_end_dt = datetime.combine(b.date, b.expected_time) + duration
        else:
            b.expected_time = prev_end_dt.time()
            prev_end_dt = datetime.combine(b.date, b.expected_time) + duration

        b.save()
        token_no += 1

    return redirect(f"/myapp/view_slotbooking/{request.session['bokid']}#a")


from datetime import datetime
from django.shortcuts import get_object_or_404, redirect


from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect

def check_out_user(request, id):
    booking = get_object_or_404(Booking, id=id)

    if booking.status != 'Approved':
        return redirect('/myapp/business_home_get/')

    now = datetime.now().replace(second=0, microsecond=0)

    # current booking complete
    booking.status = 'Completed'
    booking.save()

    # 🔥 VERY NEXT TOKEN മാത്രം എടുക്കുക
    next_booking = Booking.objects.filter(
        date=booking.date,
        status='Approved',
        SLOT__STATION=booking.SLOT.STATION,
        tokens__gt=booking.tokens
    ).order_by('tokens').first()

    if next_booking:
        # ✅ ONLY expected_time change
        next_booking.expected_time = now.time()
        next_booking.save()

        # ❌ from_time touch ചെയ്യരുത്

        # notification
        try:
            email = next_booking.USERS.email

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('serviq.team@gmail.com', 'zgkslniekvrjyeie')

            subject = "ServiQ Booking updates"
            msg = f"Subject: {subject}\n\nYour service slot is now active. You may visit anytime from now until the end of your scheduled slot.."

            server.sendmail("serviq.team@gmail.com", email, msg)
            server.quit()

        except Exception as e:
            print(e)

    return redirect(f"/myapp/view_slotbooking/{request.session['bokid']}#a")

# def check_out_user(request, id):
#     print("------ CHECK OUT STARTED ------")
#
#     booking = get_object_or_404(Booking, id=id)
#     print("Booking ID:", booking.id)
#     print("Booking Status:", booking.status)
#
#     if booking.status != 'Approved':
#         print("Booking not approved. Redirecting.")
#         return redirect('/myapp/business_home_get/')
#
#     slot = booking.SLOT
#     booking_date = booking.date
#
#     print("Booking Date:", booking_date)
#     print("Slot From:", slot.from_time)
#     print("Slot To:", slot.to_time)
#     print("Expected Start Time:", booking.expected_time)
#
#     now = datetime.now()
#     actual_checkout_dt = datetime(
#         now.year,
#         now.month,
#         now.day,
#         now.hour,
#         now.minute,
#         0,
#         0
#     )
#
#     print("Actual Checkout Datetime:", actual_checkout_dt)
#
#     next_bookings = Booking.objects.filter(
#         date=booking.date,
#         status='Approved',
#         SLOT__STATION=slot.STATION
#     ).exclude(id=booking.id).order_by('expected_time')
#
#     print("Next Bookings Count:", next_bookings.count())
#
#     # current checkout time മുതൽ next bookings update ചെയ്യും
#     next_start_dt = actual_checkout_dt
#
#     for next_booking in next_bookings:
#         print("Updating Booking:", next_booking.id)
#
#         # old duration keep cheyyan
#         old_from_dt = datetime.combine(booking_date, next_booking.SLOT.from_time)
#         old_to_dt = datetime.combine(booking_date, next_booking.SLOT.to_time)
#         duration = old_to_dt - old_from_dt
#
#         print("Old From:", old_from_dt)
#         print("Old To:", old_to_dt)
#         print("Duration:", duration)
#
#         # next booking expected time = previous checkout / previous end
#         next_booking.expected_time = next_start_dt.time()
#         next_booking.save()
#
#         # if you want from_time also same as expected_time
#         next_booking.SLOT.from_time = next_start_dt.time()
#         # next_booking.SLOT.to_time = (next_start_dt + duration).time()
#         next_booking.SLOT.save()
#
#         print("New Expected Time:", next_booking.expected_time)
#         print("New From Time:", next_booking.SLOT.from_time)
#         print("New To Time:", next_booking.SLOT.to_time)
#
#         # next booking start for following token
#         next_start_dt = next_start_dt + duration
#
#     booking.status = 'Completed'
#     booking.save()
#
#     print("Booking marked as Completed")
#
#     immediate_next = Booking.objects.filter(
#         date=booking.date,
#         status='Approved',
#         SLOT__STATION=slot.STATION
#     ).exclude(id=booking.id).order_by('expected_time').first()
#
#     if immediate_next:
#         email = immediate_next.USERS.email
#
#         message = "Previous booking has completed. Your service will start soon. Check App for the updated time"
#
#         try:
#             server = smtplib.SMTP('smtp.gmail.com', 587)
#             server.starttls()
#             server.login('serviq.team@gmail.com', 'zgkslniekvrjyeie')
#
#             subject = "ServiQ Booking updates"
#             body = message
#             msg = f"Subject: {subject}\n\n{body}"
#
#             server.sendmail("serviq.team@gmail.com", email, msg)
#             server.quit()
#
#             messages.success(request, 'Notification sent to next user')
#
#         except Exception as e:
#             print(e)
#             messages.warning(request, 'Failed to send email')
#
#     return redirect(f"/myapp/view_slotbooking/{request.session['bokid']}#a")
# ----------------------


# def check_out_user(request, id):
#     print("------ CHECK OUT STARTED ------")
#
#     booking = get_object_or_404(Booking, id=id)
#     print("Booking ID:", booking.id)
#     print("Booking Status:", booking.status)
#
#     if booking.status != 'Approved':
#         print("Booking not approved. Redirecting.")
#         return redirect('/myapp/business_home_get/')
#
#     slot = booking.SLOT
#     booking_date = booking.date
#
#     print("Booking Date:", booking_date)
#     print("Slot From:", slot.from_time)
#     print("Slot To:", slot.to_time)
#     print("Expected Start Time:", booking.expected_time)
#
#     # expected start datetime
#     expected_start_dt = datetime.combine(booking_date, booking.expected_time)
#     print("Expected Start Datetime:", expected_start_dt)
#
#     # slot end datetime (WHEN THE SLOT WAS SUPPOSED TO END)
#     slot_to_dt = datetime.combine(booking_date, slot.to_time)
#     print("Slot End Datetime (scheduled):", slot_to_dt)
#
#     now = datetime.now()
#     print("Current Time:", now)
#
#     actual_checkout_dt = datetime(
#         now.year,
#         now.month,
#         now.day,
#         now.hour,
#         now.minute,
#         0,
#         0
#     )
#     print("Actual Checkout Datetime:", actual_checkout_dt)
#
#     # IMPORTANT FIX: Calculate time saved = scheduled end time - actual checkout time
#     # If you finish at 9:56 and slot was supposed to end at 9:30:
#     # 9:30 - 9:56 = -26 minutes (negative means you finished LATE)
#     # But in your case at 9:56, slot ended at 9:30, so:
#     # 9:30 - 9:56 = -26 minutes (you're 26 minutes late!)
#     time_saved = slot_to_dt - actual_checkout_dt
#     print("Time Saved (positive=early, negative=late):", time_saved)
#
#     # For your example at 9:56 checkout with slot end at 9:30:
#     # time_saved = -26 minutes (you're late by 26 minutes)
#     # So next tokens should be DELAYED by 26 minutes, not advanced!
#
#     next_bookings = Booking.objects.filter(
#         date=booking.date,
#         status='Approved',
#         SLOT__STATION=slot.STATION,
#         tokens__gt=booking.tokens
#     ).order_by('tokens')
#
#     print("Next Bookings Count:", next_bookings.count())
#
#     for next_booking in next_bookings:
#         print("Updating Booking:", next_booking.id)
#
#         current_expected_dt = datetime.combine(booking_date, next_booking.expected_time)
#         print("Current Expected Time:", current_expected_dt)
#
#         # FIX: Add the time_saved (which is negative if late, positive if early)
#         # If time_saved = -26 minutes (late):
#         # new time = 10:00 + (-26 minutes) = 10:26 (DELAYED)
#         # If time_saved = +10 minutes (early):
#         # new time = 10:00 - (+10 minutes) = 9:50 (EARLIER)
#         new_expected_dt = current_expected_dt - time_saved
#         print("New Expected Time:", new_expected_dt)
#
#         next_booking.expected_time = new_expected_dt.time()
#         next_booking.save()
#
#     booking.status = 'Completed'
#     booking.save()
#
#     print("Booking marked as Completed")
#     print("------ CHECK OUT FINISHED ------")
#
#     return redirect(f"/myapp/view_slotbooking/{request.session['bokid']}")



def BusinessReject_BookingRequest(request,id,ssid):
    request.session['bokid']=ssid
    a=Booking.objects.get(id=id)
    a.status='Rejected'
    a.save()
    return redirect(f"/myapp/view_slotbooking/{request.session['bokid']}")


def user_viewbookedservice(request):
    lid=request.POST['lid']
    a=Booking.objects.filter(USERS__USER_id=lid)
    l = []
    for i in a:
        l.append({'id': i.id,
                  'date': i.date,
                  'token': i.tokens,
                  'Expected_Time': i.expected_time,
                  'Station_Name': i.SLOT.STATION.name,
                  'from_time': i.SLOT.from_time,
                  'to_time': i.SLOT.to_time,
                  'status': i.status,
                  })
    print(l)
    return JsonResponse({'status': 'ok','data':l})


def userCancel_booking(request):
    bid = request.POST['bid']
    Booking.objects.filter(id=bid).update(status='Cancelled')
    return JsonResponse({'status':'ok'})


def view_userCancelledBooking(request):
    lid=request.POST['lid']
    a=Booking.objects.filter(USERS__USER_id=lid,status='Cancelled')
    l = []
    for i in a:
        l.append({'id': i.id,
                  'date': i.date,
                  'token': i.tokens,
                  'Station_Name': i.SLOT.STATION.name,
                  'from_time': i.SLOT.from_time,
                  'to_time': i.SLOT.to_time,
                  'status': i.status,
                  })
    print(l)
    return JsonResponse({'status': 'ok','data':l})


def sent_appreview(request):
    lid=request.POST['lid']
    rating=request.POST['rating']
    review=request.POST['review']
    a=Review()
    a.Review=review
    a.Rating=rating
    a.date=datetime.now().date()
    a.USER_id = lid
    a.save()
    return JsonResponse({'status': 'ok'})


def appchangepassword(request):
    lid=request.POST['lid']
    currentpassword=request.POST['current']
    newpassword=request.POST['new']
    confirmpassword=request.POST['confirm']
    user=User.objects.get(id=lid)
    print(lid,currentpassword,newpassword,confirmpassword)
    if user.check_password(currentpassword):
        if newpassword==confirmpassword:
            print('hrlkef')
            user.set_password(newpassword)
            user.save()
            print('dfjdnjk')
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status':'no'})




def sentcomplaint(request):
    complaint=request.POST['complaint']
    lid=request.POST['lid']
    a=Complaint()
    a.complaint=complaint
    a.date=datetime.now().date()
    a.status='pending'
    a.reply='pending'
    a.USERS=Users.objects.get(USER=lid)
    a.save()
    return JsonResponse({'status': 'ok'})


def viewComplaintReply(request):
    lid=request.POST['lid']
    a=Complaint.objects.filter(USERS__USER_id=lid)
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'date':i.date,
                  'status':i.status,
                  'complaint':i.complaint,
                  'reply':i.reply,
                  })
        print(l)
    return JsonResponse({'status': 'ok','data':l})


def forgetpassword_get(req):
    return render(req,'forgotpassword.html')

def forgetpassword_post(req):
    if req.method == 'POST':
        email = req.POST.get('forget','').strip()
        try:
            user=User.objects.get(username=email)
        except User.DoesNotExist:
            messages.warning(req,'Email does not exist')
            return redirect('/myapp/login_get/')
        import random
        psw = random.randint(1000,9999)

        user.set_password(str(psw))
        user.save()

        try:
            server=smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('serviq.team@gmail.com', 'zgkslniekvrjyeie')

            subject = "Password Reset - ServiQ"
            body = "Your new password is: "+str(psw)
            msg = f"Subject: {subject}\n\n{body}"

            server.sendmail("serviq.team@gmail.com",email, msg)
            server.quit()

            messages.success(req,'New Password Send Successful')
            return  redirect('/myapp/login_get/')
        except Exception as e:
            messages.warning(req,'Faild to Send')
            return  redirect('/myapp/login_get/')


    messages.warning(req,'Faild to Send')
    return redirect('/myapp/login_get/')



def android_forget_password(req):
    email = req.POST['username']
    if not email:
        return JsonResponse({'status': 'error'})

    try:
        user = User.objects.get(username=email)
        print(email)

        # generate new password
        import random
        new_pass = str(random.randint(1000, 9999))
        user.password = make_password(new_pass)
        user.save()

        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "serviq.team@gmail.com"
        app_password = "zgkslniekvrjyeie"  # Replace with your actual app password

        # Create email message
        subject = "Your New Password"
        body = f"Your new password is:{new_pass}"
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(body, "plain"))

        # send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)
        server.quit()
        return JsonResponse({'status': 'ok'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error'})
    except Exception as e:
        return JsonResponse({'status': 'error'})

















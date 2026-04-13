"""
URL configuration for SLSM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
path('login_get/',views.login_get),
path('login_post/',views.login_post),
path('Logout_get/',views.Logout_get),

path('admin_home_get/',views.admin_home_get),

path('changepassword_get/',views.changepassword_get),
path('changepassword_post/',views.changepassword_post),

path('AddSubscription_get/',views.AddSubscription_get),
path('AddSubscription_post/',views.AddSubscription_post),

path('EditSubscription_get/<id>',views.EditSubscription_get),
path('EditSubscription_post/',views.EditSubscription_post),
path('view_subscription_get/',views.view_subscription_get),
path('delete_subscription_get/<id>',views.delete_subscription_get),

path('viewRegisteredBusiness_get/',views.viewRegisteredBusiness_get),

path('SubscriptionPaymentReport_get/',views.SubscriptionPaymentReport_get),

path('viewComplaintFromUser_get/',views.viewComplaintFromUser_get),

path('SentReplyToUser_get/<id>',views.SentReplyToUser_get),
path('SentReplyToUser_post/',views.SentReplyToUser_post),
path('payment_success/',views.payment_success),

path('viewAppReviews_get/',views.viewAppReviews_get),


path('businesssignup_get/',views.businesssignup_get),
path('businesssignup_post/',views.businesssignup_post),
path('businessview_subscription/',views.businessview_subscription),
path('businessrenew_get/',views.businessrenew_get),
path('businessrenew_post/',views.businessrenew_post),
path('businessrenew_success/',views.businessrenew_success),


path('business_home_get/',views.business_home_get),


path('businessviewprofile_get/',views.businessviewprofile_get),
path('editprofile_get/<id>',views.editprofile_get),
path('editprofile_post/',views.editprofile_post),

path('add_servicestation_get/',views.add_servicestation_get),
path('add_servicestation_post/',views.add_servicestation_post),

path('edit_servicestation_get/<id>',views.edit_servicestation_get),
path('edit_servicestation_post/',views.edit_servicestation_post),

path('view_servicestation_get/',views.view_servicestation_get),

path('delete_servicestation_get/<id>',views.delete_servicestation_get),

path('view_slotcreation_get/<id>',views.view_slotcreation_get),
path('delete_slotcreation_get/<id>',views.delete_slotcreation_get),

path('add_slotcreation_get/<id>',views.add_slotcreation_get),
path('add_slotcreation_post/',views.add_slotcreation_post),


path('view_slotbooking/<sid>',views.view_slotbooking),

path('user_viewservicestation/',views.user_viewservicestation),
path('sent_appreviews_get/',views.sent_appreviews_get),
path('sent_appreviews_post/',views.sent_appreviews_post),

path('user_viewbookedservice/',views.user_viewbookedservice),
path('user_signup/',views.user_signup),

path('user_editprofile/',views.user_editprofile),
path('user_viewbusiness/',views.user_viewbusiness),
path('user_viewfreeslots/',views.user_viewfreeslots),

path('blockbussiness/<id>',views.blockbussiness),
path('unblockbussiness/<id>',views.unblockbussiness),

path('user_login/',views.user_login),
path('user_viewprofile/',views.user_viewprofile),

path('sent_appreview/',views.sent_appreview),
path('appchangepassword/',views.appchangepassword),

path('businesschangepassword_get/',views.businesschangepassword_get),
path('businesschangepassword_post/',views.businesschangepassword_post),

path('edit_slotcreation_get/<id>',views.edit_slotcreation_get),
path('edit_slotcreation_post/',views.edit_slotcreation_post),


path('viewComplaintReply/',views.viewComplaintReply),

path('sentcomplaint/',views.sentcomplaint),


path('forgetpassword_get/',views.forgetpassword_get),
path('forgetpassword_post/',views.forgetpassword_post),
path('android_forget_password/',views.android_forget_password),


path('userbook_slot/',views.userbook_slot),
path('userCancel_booking/',views.userCancel_booking),
path('view_userCancelledBooking/',views.view_userCancelledBooking),


path('BusinessApprove_BookingRequest/<id>/<sid>/<ssid>',views.BusinessApprove_BookingRequest),
path('BusinessReject_BookingRequest/<id>/<ssid>',views.BusinessReject_BookingRequest),
path('check_out_user/<id>',views.check_out_user),


path('delete_complaint/<int:id>', views.delete_complaint),

path('delete_review/<int:id>', views.delete_review),

]



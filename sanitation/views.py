from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
import requests
from requests.auth import HTTPBasicAuth
import json
from .mpesa_credentials import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


# Create your views here.
@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user=request.user
    profile =Profile.objects.get(username=current_user)
    return render(request,'profile/user_profile.html',{"profile":profile})


@login_required(login_url='/accounts/login/')
def user_profile(request,username):
    user = User.objects.get(username=username)
    profile =Profile.objects.get(username=user)

@login_required(login_url='/accounts/login/')
def create_profile(request):
    current_user=request.user
    if request.method=="POST":
        form =ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()
        return HttpResponseRedirect('/')
    else:
        form = ProfileForm()
        return render(request,'profile/profile_form.html',{"form":form})
    

@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user=request.user
    if request.method=="POST":
        instance = Profile.objects.get(username=current_user)
        form =ProfileForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()

        return redirect('index')

    elif Profile.objects.get(username=current_user):
         profile = Profile.objects.get(username=current_user)
         form = ProfileForm(instance=profile)
    else:
        form = ProfileForm()

    return render(request,'profile/update_profile.html',{"form":form})


def payment(request):
    if request.method == 'POST':
        form=PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name=form.save(commit=False)
            phone_Number=form.save(commit=False)
            amount=form.save(commit=False)
            account=form.save(commit=False)
            payment.save()
            return redirect(hood)
    else:
        form=PaymentForm()
    return render(request, 'payment.html', locals())

def toilet(request):


    this_user_id_number=User.objects.all()
    if request.method == 'POST':

        form=ToiletForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            account_number=form.save(commit=False)
            toilet_tag=form.save(commit=False)
            # toilet.save()
            return redirect(index)
    else:
        form=ToiletForm()
    return render(request, 'toilet.html', locals())




def getAccessToken(request):
    consumer_key='cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
    consumer_secret='2nHEyWSD4VjpNh2g'
    api_URL='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r=requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token=json.loads(r.text)
    validated_mpesa_access_token=mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)
def lipa_na_mpesa_online(request):
    access_token=MpesaAccessToken.validated_mpesa_access_token
    api_url="https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers={"Authorization": "Bearer %s" % access_token}
    request={
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254717654230,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254717654230,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Obindi",
        "TransactionDesc": "Testing stk push"
    }
    response=requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')

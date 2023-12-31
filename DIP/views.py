from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
from . import decode_jwt
import base64
import requests
from . import models
from .forms import MyForm

# Home page
def index(request):
    context = {}
    try:
        code = request.GET.get('code')
        userData = getTokens(code)
        context['name'] = userData['name']
        context['status'] = 1
        print(f'{context=}')
        response = render(request, 'index.html', context)
        response.set_cookie('sessiontoken', userData['id_token'], max_age=60 * 60 * 24, httponly=True)
        return response
    except:
        token = getSession(request)
        if token is not None:
            userData = decode_jwt.lambda_handler(token, None)
            context['name'] = userData['name']
            context['status'] = 1
            print(f'2){context=}')
            return render(request, 'index.html', context)
        return render(request, 'index.html', {'status': 0})


# About page
def about(request):
    return render(request, "about.html")
# Wallet page
def wallet(request):
    return render(request, "wallet.html")
# Sponsor application(PDF) page
def sponsors(request):
    return render(request, "sponsors.html")
# Signup page
def drivers(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = MyForm()
    return render(request, "drivers.html", {'form': form})

# Dashboard page
def dashboard(request):
    return render(request, "dashboard.html")
def getTokens(code):
    TOKEN_ENDPOINT = config('TOKEN_ENDPOINT')
    REDIRECT_URL = config('REDIRECT_URL')
    CLIENT_ID = config('CLIENT_ID')
    CLIENT_SECRET = config('CLIENT_SECRET')

    encodeData = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "ISO-8859-1")).decode("ascii")

    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encodeData}'
    }

    body = {
        'grant_type': 'authorization-code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_url': REDIRECT_URL,
    }

    response = requests.post(TOKEN_ENDPOINT, data=body,headers=headers)

    id_token = response.json()['id_token']

    userData = decode_jwt.lambda_handler(id_token, None)

    if not userData:
        return False

    user = {
        'id_token': id_token,
        'name': userData['name'],
        'email': userData['email'],
    }
    return user

def getSession(request):
    try:
        response = request.COOKIES["sessiontoken"]
        return response
    except:
        return None

def signout(request):
    response = render(request, 'index.html', {'status': 0})
    response.delete_cookie('sessiontoken')
    return response

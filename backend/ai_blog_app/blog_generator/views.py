from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
import json
from pytube import YouTube

# Create your views here.
@login_required
def index(request):
  return render(request, 'index.html')


def user_login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid username or password!!'
      return render(request, 'login.html', {'error_message': error_message})
  return render(request, 'login.html')

def user_signup(request):
  if request.method == 'POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    repeatPassword = request.POST['repeatPassword']

    if password == repeatPassword:
      try:
        user = User.object.create_user(username, email, password)
        user.save()
        login(request, user)
        return redirect('/')
      except:
        error_message = 'Error on creating account!!'
        return render(request, 'signup.html', {'error_message': error_message})
    else:
      error_message = 'Password don\'t match!!'
      return render(request, 'signup.html', {'error_message': error_message})
  return render(request, 'signup.html')

def user_logout(request):
  logout(request)
  return redirect('/')

@csrf_exempt
def generate_blog(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      yt_link = data['link']
      return JsonResponse({'content': yt_link})
    except (KeyError, json.JSONDecodeError):
      return JsonResponse({'error': 'Invalid data sent'}, status=400)
    
    # get the title
    title = yt_title(yt_link)

  else:
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# get the Youtube title  
def yt_title(link):
  yt = YouTube(link)
  return yt.title
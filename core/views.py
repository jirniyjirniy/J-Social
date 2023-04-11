from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django_countries import countries

from .models import Profile, Posts


# from .forms import Forms


@login_required(login_url='signin')
def index(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_objects)

    posts = Posts.objects.all()

    context = {
        'user_profile': user_profile,
        'posts': posts,
    }

    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return HttpResponseRedirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return HttpResponseRedirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                user_login = auth.authenticate(username=username, password1=password1)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

                return redirect('settings')
        else:
            messages.info(request, 'Passwords Not Matching')
            return HttpResponseRedirect('/signup')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('/signin')
    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    context = {
        'countries': countries,
        'user_profile': user_profile,
    }

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profile_image
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', context)


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Posts.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

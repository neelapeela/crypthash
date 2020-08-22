from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Progress, Level
import operator

# Create your views here.

userlist = Progress.objects.all()
userlist = sorted(userlist, key= lambda x: x.points)

messages = {
    'levelstatus': "",
    'notification': "You are currently logged out. New here? Register.",
    'lb': userlist
}

def home(request):
    if request.user.is_authenticated:
        userinfo = Progress.objects.get(username= request.user.username)
        messages['userinfo'] = userinfo
        completedlist = list(userinfo.completedlist)
        messages['completedlist'] = completedlist

    if request.method == 'POST':
        if 'answer-button' not in request.POST:
            name = list(request.POST.keys())
            print(name)
            levelname = name[1]
            messages['levelstatus'] = ""
            if levelname not in completedlist:
                userinfo.is_playing = True
                userinfo.save()
                currentlevel = Level.objects.get(level = levelname)
                userinfo.level = levelname
                userinfo.save()
                messages['currentlevel'] = currentlevel

        elif 'answer-button' in request.POST:
            currentlevel = Level.objects.get(level = userinfo.level)
            answer = request.POST['answertext']
            if answer == currentlevel.answer:
                userinfo.completedlist += userinfo.level
                completedlist = list(userinfo.completedlist)
                messages['completedlist'] = completedlist

                userinfo.is_playing = False
                userinfo.level = 'none'
                userinfo.points = userinfo.points + currentlevel.points
                userinfo.completed += 1
                userinfo.save()
                messages['levelstatus'] = "Level completed. Good job, there."
            else:
                messages['levelstatus'] = "Wrong answer."


        return render(request, 'index.html', messages)

    else:
        messages['levelstatus'] = ""
        return render(request, 'index.html', messages)

def register(request):

    if request.method == 'POST':
        if 'registration' in request.POST:
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            if User.objects.filter(username=username).exists():
                messages['notification'] = "Username exists. Get creative!"
                return render(request, "register.html", messages)
            elif User.objects.filter(email=email).exists():
                messages['notification'] = "Account with the same email already exists"
                return render(request, "register.html", messages)
            else:
                user = User.objects.create_user(
                    username=username, first_name=name, email=email, password=password)
                user.save()

                messages['notification'] = "You have been registered. Log in."

                global user_progress
                user_progress = Progress(username=username)
                user_progress.save()

                messages['userprogress'] = user_progress

            return render(request, 'register.html', messages)

        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages['notification'] = "You are logged in, " + \
                    request.user.username
                request.session.set_expiry(1209600)
                return redirect("/")
            else:
                messages['notification'] = "Invalid credentials."

        if 'logout' in request.POST:
            auth.logout(request)
            messages['notification'] = "You are currently logged out. New here? Register."
            return render(request, 'register.html', messages)

    else:
        if request.user.is_authenticated:
            messages['notification'] = "You are logged in, " + \
                    request.user.username
        else:
            messages['notification'] = "You are currently logged out. New here? Register."
        return render(request, 'register.html', messages)


def dashboard(request):
    userinfo = Progress.objects.get(username= request.user.username)
    messages['userinfo'] = userinfo
    return render(request, 'index.html', messages)


def leaderboard(request):
    messages['lb']= Progress.objects.all
    return render(request, 'leaderboard.html', messages)


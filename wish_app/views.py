from django.shortcuts import render, redirect
from .models import User, Wish
from django .contrib import messages
import bcrypt

def index(request):
    return render(request, "login-register.html")

def addToDatabase(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    if(request.POST['form_type'] == "registration_form"):
        password = request.POST['user_password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['user_email'],hashed_pw=pw_hash)
        request.session['userid'] = User.objects.last().id
        return redirect("/wishes")
    elif(request.POST['form_type'] == "login_form"):
        user = User.objects.filter(email=request.POST['user_email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['user_password'].encode(), logged_user.hashed_pw.encode()):
                request.session['userid'] = logged_user.id
                print("checked pw")
                return redirect("/wishes")
    return redirect("/")

def showWishes(request):
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "wishes": Wish.objects.all()
        }
    return render(request, "wishes.html", context)

def logOut(request):
    request.session.clear()
    return redirect('/')

def addWish(request):
    context = {
        "user": User.objects.get(id=request.session['userid'])
        }
    return render(request, "addWish.html", context)

def removeWish(request, wish_id):
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.delete()
    return redirect("/wishes")

def addWishToDataBase(request):
    if request.POST['button'] == 'cancel':
        print("user canceled edit")
        return redirect("/wishes")
    errors = Wish.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wishes/new")
    this_user = User.objects.get(id=request.session['userid'])
    Wish.objects.create(wish_title=request.POST['wish_title'],desc=request.POST['wish_desc'],upload_by=this_user)
    return redirect("/wishes")

def editWish(request, wish_id):
   
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "wish": Wish.objects.get(id=wish_id)
        }
    return render(request, "editWish.html", context)

def editWishInDataBase(request, wish_id):
    if request.POST['button'] == 'cancel':
        print("user canceled edit")
        return redirect("/wishes")
    errors = Wish.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wishes/new")
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.wish_title = request.POST['wish_title']
    this_wish.desc = request.POST['wish_desc']
    this_wish.save()
    return redirect("/wishes")

def grantWish(request, wish_id):
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.granted = True
    this_wish.save()
    return redirect("/wishes")

def likeWish(request, wish_id):
    this_wish = Wish.objects.get(id=wish_id)
    this_user = User.objects.get(id=request.session['userid'])
    this_user.liked_wishes.add(this_wish)
    return redirect("/wishes")

def showStats(request):
    total_wishes_granted = 0
    for wish in Wish.objects.all():
        if (wish.granted == True):
            total_wishes_granted = total_wishes_granted + 1
    user_granted_wish = 0
    user_pending_wish = 0
    this_user = User.objects.get(id=request.session['userid'])
    for wish in this_user.wishes.all():
        if (wish.granted == True):
            user_granted_wish = user_granted_wish + 1
        else: user_pending_wish = user_pending_wish +1
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "total_wishes_granted": total_wishes_granted,
        "user_granted_wish": user_granted_wish,
        "user_pending_wish": user_pending_wish
        }
    return render(request, "showStats.html", context)
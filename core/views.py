from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import LikePost, Profile, Post
from django.contrib.auth.decorators import login_required
#Create your views here

@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    posts = Post.objects.all()

    return render(request, "index.html", {"user_profile":user_profile, "posts": posts})

def signup(request):
    if request.method == "POST":
        #Register User
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        #Check if passwords are the same  
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect('signup')
            else:
                #Create user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                #Login and redirect to settings
                user_login = auth.authenticate(username = username , password = password)
                auth.login = auth.login(request, user_login)
                #Create Profile 
                user_model =  User.objects.get(username = username)
                new_profile = Profile.objects.create(user=user_model, id_user = user_model.id)
                new_profile.save()
                return redirect("settings") # Redirect to Settings #
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
            #Show an error

    else:
        return render(request, "signup.html")
    
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Incorrect username or password")
            return redirect('signin')
    else:
        return render(request, "signin.html")
    
@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url="signin")
def settings(request):
    user_profile = Profile.objects.get(user = request.user)
    if request.method == "POST":
        if request.FILES.get("image") == None:
            image = user_profile.profileimg
            firstName = request.POST["firstName"]
            lastName = request.POST["lastName"]
            bio = request.POST["bio"]
            location = request.POST["location"]
            workingat = request.POST["workingat"]


            print("Hi dude")
            user_profile.profileimg = image
            user_profile.firstName = firstName
            user_profile.lastName = lastName
            user_profile.bio = bio
            user_profile.location = location    
            user_profile.workingat = workingat
            user_profile.save()
        if request.FILES.get("image") !=None:
            print("Hi man")
            image = request.FILES.get("image")
            firstName = request.POST["firstName"]
            lastName = request.POST["lastName"]
            bio = request.POST["bio"]
            location = request.POST["location"]
            workingat = request.POST["workingat"]

            user_profile.profileimg = image
            user_profile.firstName = firstName
            user_profile.lastName = lastName
            user_profile.bio = bio
            user_profile.location = location    
            user_profile.workingat = workingat
            user_profile.save()
        return redirect("settings")
    return render(request, 'setting.html', {"user_profile":user_profile} )

@login_required(login_url="signin")
def upload(request):
    if request.method =="POST":
        user = request.user.username 
        image = request.FILES.get("image_uploaded") 
        caption = request.POST["caption"]
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect("/")
    else:
        return redirect("/")
@login_required(login_url="signin")   
def like_post(request):
    username = request.user.username
    post_id = request.GET.get("post_id")
    print(post_id)

    post = Post.objects.get(id = post_id)
    like_filter = LikePost.objects.filter(id = post_id, username = username).first()
    if like_filter is None:
        new_like  = LikePost.objects.create(post_id = post_id, username = username)
        new_like.save()
        post.num_of_likes +=1
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.num_of_likes-=1
        post.save()
        return redirect("/")




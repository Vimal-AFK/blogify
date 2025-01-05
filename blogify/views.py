from django.shortcuts import render, get_object_or_404 ,redirect
from .models import post
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home (request):
    context = {
        'posts':post.objects.all(),
    }
    return render(request,'home.html',context)

def search(request):
    query = request.GET.get('search_key', '')  # Get the search key from the GET request
    posts = post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)  # Filter posts based on the search query

    context = {
        'query': query,
        'posts': posts,
    }
    return render(request, 'home.html', context)

def about_us(request):
    return render(request,'about.html')

def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            post_title = request.POST.get('title','')
            post_content = request.POST.get('content','')
            post_category = request.POST.get('category','')
            post_author = request.POST.get('author', '')

            post_obj = post(title=post_title,content=post_content,category=post_category,author = post_author)
            post_obj.save()
            return redirect('post_success')

    return render(request,'create.html')

def post_success (request):
    return render (request,'success.html')


def post_detail(request, slug):
    post_detail = get_object_or_404(post, slug=slug)
    related_category = post_detail.category
    
    # Fetch related posts (excluding the current post)
    related_posts = post.objects.filter(category=related_category).exclude(id=post_detail.id)
    
    # Fetch all posts (unrelated posts)
    unrelated_posts = post.objects.exclude(category=related_category)
    
    context = {
        'related_posts': related_posts,
        'unrelated_posts': unrelated_posts,
        'post_detail': post_detail,
    }
    
    return render(request, 'detail.html', context)


def user_dashboard(request):
    context = {
        'posts':post.objects.filter(author=request.user)
    }
    return render (request,'dashboard.html',context)

def post_update(request,id):
    print('id is :',id)
    post_to_update = get_object_or_404(post,id=id)
    if request.method == 'POST':
        u_title = request.POST.get('title')
        u_content = request.POST.get('content')
        u_category = request.POST.get('category')

        post_to_update.title = u_title
        post_to_update.content = u_content
        post_to_update.category = u_category
        post_to_update.save()

        return redirect('profile')
    return render (request,'post_update.html',{'data':post_to_update})

def post_delete(request,id):
    post_to_delete = get_object_or_404(post,id=id)
    post_to_delete.delete()
    return redirect('profile')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if password == confirm_password:
            new_user = User.objects.create_user(username=username,password=password,)
            new_user.save()
            messages.success(request,'Account created successfully. Now you can Login')
            return redirect('login')
        else:
            messages.warning(request,'Password Mismatched')
            return redirect('signup')
    else:
        user_form = UserCreationForm()
        return render (request,'signup.html', {'form':user_form}) 
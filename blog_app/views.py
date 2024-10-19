from django.shortcuts import render, redirect
from .models import Post, Comment, Category
from django.contrib.auth.models import User, auth
from django.contrib import messages
import math
import random

# Create your views here.
def index(request):
    category_id = request.GET.get('category')
    page = request.GET.get('page')

    if category_id:
        posts = Post.objects.filter(category_id=category_id)
        is_filter = True
        cat = Category.objects.get(id=category_id).name
    else:
        if page:
            posts = Post.objects.all()
            if page == 1:
                posts = posts[:4]
            else:
                posts = posts[((4*int(page))-4):(4*int(page))]
        else:
            posts = Post.objects.all()
            posts = posts[:4]
            page = 1
        is_filter = False
        cat = None


    comments = Comment.objects.all()
    categories = Category.objects.all()

    context = {
        'posts': posts,
        'total_pages': [i for i in range(1, (math.ceil(len(Post.objects.all()) / 4))+2)],
        'comments': comments,
        'categories': categories,
        'pageno': page,
        'featured': Post.objects.get(is_featured=1),
        'filter': is_filter,
        'curr_cat': cat
    }

    return render(request, 'index.html', context)

def post(request, pk):
    post = Post.objects.get(pk=pk)
    # comments = Comment.objects.get(post=pk)
    context = {
        'posts': post,
        # 'comments': comments,
        'curr_categories': Category.objects.get(id=post.category_id),
        'others': Category.objects.all()

    }
    return render(request, 'post.html', context)

def create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        passwd = request.POST.get('password')
        passwd2 = request.POST.get('password2')

        if passwd == passwd2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'A user with this email already exists', extra_tags='mail')
                return redirect('create')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'A user with this name already exists', extra_tags='user')
                return redirect('create')
            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = passwd
                )
                user.save()
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match', extra_tags='info')
            return redirect('create')
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('password')
        user = auth.authenticate(
            username=username,
            password = passwd
        )
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Incorrect Password or User does not exist")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            categories = Category.objects.filter(name__icontains=query)
            
            if categories.exists():
                posts = Post.objects.filter(category_id=categories[0].id)
                if list(posts) > 4:
                        posts = random.sample(list(posts), 4)
                context = {
                    'categories': Category.objects.all(),
                    'posts': posts,
                    'query': query
                }
                return render(request, 'index.html', context)
            else:
                posts = Post.objects.filter(post_by__icontains=query)
                if posts.exists():
                    if list(posts) > 4:
                        posts = random.sample(list(posts), 4)
                    context = {
                        'categories': Category.objects.all(),
                        'posts': posts,
                        'query': query
                    }
                    return render(request, 'index.html', context)
                else:
                    messages.info(request, 'No results found for your search.')
        else:
            messages.info(request, 'Please enter a search query.')
    
    return redirect('index')

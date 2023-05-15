
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User
from django.http import  JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .forms import PostForm, ProfileRegistrationForm, CommentForm

from .models import Post, Profile, Comment


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('home')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
def user_logout(request):
    logout(request)
    return redirect('home')


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Save the post in the user's profile
            profile = Profile.objects.get(user=request.user)
            profile.posts.add(post)

            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def home(request):
    posts = Post.objects.order_by('?')  # Random order
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data['post_id']
            post = Post.objects.get(pk=post_id)
            Comment.objects.create(post=post, user=request.user, content=form.cleaned_data['content'])
            return redirect('home')
    else:
        form = CommentForm()
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'home.html', context)



@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'like':
            post.likes.add(request.user)
        elif action == 'unlike':
            post.likes.remove(request.user)

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    context = {'profile': profile}
    return render(request, 'profile.html', context)




@login_required(login_url='login')
def like_post(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        likes_count = post.likes.count()
        return JsonResponse({'likes_count': likes_count})

    return HttpResponse(status=405)


@login_required(login_url='login')
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    posts = profile.posts.all()

    context = {
        'user': user,
        'profile': profile,
        'posts': posts
    }

    return render(request, 'profile.html', context)


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment(content=content, post=post, user=request.user)
        comment.save()

        # You can return a JSON response with the comment data
        return JsonResponse({
            'content': comment.content,
            'username': comment.user.username
        })
    else:
        return redirect('post_detail', pk=post.pk)


def follow_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    user = request.user

    if user.is_authenticated:
        if user in profile.followers.all():
            # User is already following the profile, so unfollow
            profile.followers.remove(user)
        else:
            # User is not following the profile, so follow
            profile.followers.add(user)

    # Store the previous URL in the session
    request.session['previous_url'] = request.META.get('HTTP_REFERER', '/')

    return redirect(request.session.get('previous_url'))

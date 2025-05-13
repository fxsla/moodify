# api/views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import get_object_or_404
from .models import Post, User, Comment

# using a custom model that has just one extra field to store the xp of the user (didn't want to create a new table just to store this)
User = get_user_model()

# simple login view
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'login was successful', 'username': user.username, 'id': user.id, 'xp': user.xp, 'is_superuser': user.is_superuser}, status=200)
        else:
            return JsonResponse({'message': 'invalid user credentials.'}, status=400)

    return JsonResponse({"message": "method not allowed."}, status=400)

# simple signup view
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':    
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'xp': user.xp
            }, status=200)
        except Exception as e:
            return JsonResponse({'message': 'failed to signup'}, status=500)
    
    return JsonResponse({"message": "method not allowed."}, status=400)

# simple logout view using django to logout
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message': 'Loged out'}, status=200)
        else:
            return JsonResponse({'message': 'failed to logout'}, status=400)
    return JsonResponse({'message': 'invalid request method'}, status=400)


# creates a post in database and formats it and returns all the data back
@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        username = data.get('author')
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return JsonResponse({'message':'title or content must not be empty'}, status=400)
        
        author = get_object_or_404(User, username=username)

        post = Post.objects.create(author=author, title=title, content=content)
        
        return JsonResponse({
            'id':post.id,
            'author':post.author.username,
            'title':post.title,
            'content':post.content,
            'created_at': post.created_at.isoformat(),
        }, status=200)
    else:
        return JsonResponse({'message':'invalid request method'}, status=400)

# fetches all the posts in database for the home view and formats and returns all the data thats needed
@csrf_exempt
def fetch_posts(request):
    if request.method == 'GET':
        try:
            posts = Post.objects.all().order_by('-created_at')
            data = [{
                'id': post.id,
                'author': post.author.username,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at.isoformat(),
                'xp':post.author.xp,
            }for post in posts]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'message':'failed to fetch posts'}, status=400)
    else:
        return JsonResponse({'message': 'invalid request method'}, status=400)


# adds exp, used in the pinia store
@csrf_exempt
def add_xp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('id')
            xp_to_add = data.get('xp')

            user = get_object_or_404(User, id=user_id)

            user.xp += xp_to_add
            user.save()
            return JsonResponse({'message': 'added successfuly'}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'failed to add xp'}, status=400)
    else:
        return JsonResponse({'messsage': 'incorrect request method'}, status=400)

# gets a single post when the user clicks on one from the home page
@csrf_exempt
def get_single_post(request, id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(pk=id)
            data = {
                'id': post.id,
                'author': post.author.username,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at.isoformat(),
                'xp':post.author.xp,
            }
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'message':'failed to fetch posts'}, status=400)
    else:
        return JsonResponse({'message': 'invalid request method'}, status=400)



# also creates messages (when request is post), just combined into one view
@csrf_exempt
def fetch_comments(request, id):

    if request.method == 'GET':
        post = get_object_or_404(Post, pk=id)

        comments = Comment.objects.filter(post=post).order_by('-created_at')

        comment_data = [{
            'id': comment.id,
            'author': comment.author.username,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'xp': comment.author.xp,
        } for comment in comments]
        return JsonResponse(comment_data, safe=False)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        user_id = data.get('user_id')
        post = get_object_or_404(Post, id=id)
        user = get_object_or_404(User, id=user_id)
        comment = Comment.objects.create(post=post, content=content, author=user)

        return JsonResponse({
            'id': comment.id,
            'post_id': post.id,
            'content': comment.content,
            'author': comment.author.username,
            'created_at': comment.created_at.isoformat(),
        }, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=400)


# deletes a post with a given id, admin accounts and post owners will call this
@csrf_exempt
def delete_post(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        print(id)
        post.delete()
        return JsonResponse({'message':'deleted'},status=200)
    else:
        
        return JsonResponse({'message':'failed to delete'}, status=400)
    

# deletes a comment with a given id, called by admin accounts and comment owners
@csrf_exempt
def delete_comment(request, id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return JsonResponse({'message':'deleted'},status=200)
    else:
        return JsonResponse({'message':'failed to delete'}, status=400)
    
        




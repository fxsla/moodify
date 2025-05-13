from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model that includes default Django user plus an xp field
class User(AbstractUser):
    xp = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    
# Post model to store details of the posts, each post is linked with a user
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Comment model to store the details of the comments, each comment is linked to a user and post.
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.author.username} on {self.post.title}"
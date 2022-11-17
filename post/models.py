from email.policy import default
from django.db import models
from account.models import User

class Post(models.Model):

    POST_TYPE = (
        ("public","public"),
        ("private","private"),
        ("friends_only","friends_only")
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_body = models.TextField()
    type = models.CharField(max_length=25, choices=POST_TYPE, default='public')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.post_body

class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_body = models.TextField()


    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Like(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


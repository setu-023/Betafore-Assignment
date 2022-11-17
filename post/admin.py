from django.contrib import admin

from post.models import Comment, Post, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Following, Follower, Like

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(Follower)
admin.site.register(Like)

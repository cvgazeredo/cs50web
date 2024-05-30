from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    text = models.CharField(max_length=255)
    date = models.DateTimeField(editable=True, auto_now_add=True) 

    def __str__(self):
        return f"Text: {self.text}, User: {self.user}, Date: {self.date}, " 

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="id_post")
    userliked = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="liked")

    def __str__(self):
        return f"This user: {self.userliked} liked this post: {self.post}, from {self.user}" 

class Following(models.Model): #SEGUINDO
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_main")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"This main user: {self.user}, is following this user: {self.following}"  

class Follower(models.Model): #SEGUIDORES
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="main_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"This main user: {self.user}, is followed by this user: {self.follower}" 



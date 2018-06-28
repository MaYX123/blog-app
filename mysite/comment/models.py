from django.db import models


class Comment(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('myblog.Post', on_delete=models.CASCADE)

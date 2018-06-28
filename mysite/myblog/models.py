from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
import datetime
import markdown


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    summary = models.CharField(max_length=400, blank=True)
    views = models.PositiveIntegerField(default=0)

    # 1 category -> many posts: if the category has a post, the category can't be deleted.
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # many posts <-> many tags
    tags = models.ManyToManyField(Tag, blank=True)
    # 1 author -> many posts: if the author has a post, the author can't be deleted.
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('myblog:detail', kwargs={'slugtitle': self.slug})

    def views_add(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        """
        重写save()。如果在admin中不输入summary，那么在save时自动生成summary。
        """
        if not self.summary:
            body_tmp = markdown.markdown(self.body,
                                         extensions=[
                                             'markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                         ])
            self.summary = strip_tags(body_tmp)[:84]
        # 调用实例的父类save方法
        super(Post, self).save(*args, **kwargs)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

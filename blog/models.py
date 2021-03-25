from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
CustomUser = settings.AUTH_USER_MODEL

STATUS_CHOICES = (
    ('D', 'Draft'),
    ('P', "publish")
)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to="waveline/blog_photos/", blank=True,
                              null=True, width_field='width_field', height_field='height_field')
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default='D')
    liked = models.ManyToManyField(
        CustomUser, default=None, blank=True, related_name='likes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={
            'slug': self.slug
        })

    @property
    def num_likes(self):
        return self.liked.all().count()

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    like_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(
        choices=LIKE_CHOICES, max_length=6, default='Unlike')

    def __str__(self):
        return str(self.like_post)

    class Meta:
        verbose_name_plural = 'Post Likes'


class Comment(models.Model):
    author = models.CharField(max_length=20, default='Anonymous')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='my_comments')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '{}'.format(self.content)

    class Meta:
        verbose_name_plural = "Lists of Comments"


class SideBar(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('Home Sidebar')

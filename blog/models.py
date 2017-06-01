import os.path

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def upload_location(post, filename):
    # ext = os.path.splitext(filename)[-1]
    # return "%s/%s.%s" %(post.pk, post.slug, ext)
    return "%s/%s" %(post.pk, filename)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=upload_location,
        null=True, 
        blank=True,
        width_field="width_field",
        height_field="height_field",
        )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, editable=False)
    text = models.TextField()
    trip_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"pk":self.pk})


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
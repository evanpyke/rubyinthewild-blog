import os.path

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from .choices import *


def upload_location(post, filename):
    ext = os.path.splitext(filename)[-1]
    return "%s/%s%s" %(post.pk, post.slug, ext)




class Post(models.Model):
    author = models.ForeignKey('auth.User')

    post_type = models.ForeignKey('Type')

    category = models.ForeignKey('Category')

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
    gear = models.ManyToManyField('Gear', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self, pub=True):
        if pub:
            self.published_date = timezone.now()
        else:
            self.published_date = None
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"post_type":self.post_type, "slug":self.slug})


class Comment(models.Model):
    post = models.OneToOneField(Post, related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Gear(models.Model):
    brand = models.CharField(max_length=20, blank=True)
    model = models.CharField(max_length=30, blank=True)
    short_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=60)
    category = models.ManyToManyField('Category')

    def __str__(self):
        return self.full_name

class Category(models.Model):
    name = models.CharField(max_length=16)
    
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-pk")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().pk)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

def create_full_name(instance, new_name=None):
    pass

def pre_save_gear_receiver(sender, instance, *args, **kwargs):
    if not instance.full_name:
        instance.full_name = create_full_name(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
# pre_save.connect(pre_save_gear_receiver, sender=Gear)
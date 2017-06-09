import os.path

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def upload_location(post, filename):
    ext = os.path.splitext(filename)[-1]
    return "%s/%s%s" %(post.pk, post.slug, ext)


class Post(models.Model):
    author = models.ForeignKey('auth.User')

    post_type = models.ForeignKey('Type', to_field='name')

    category = models.ForeignKey('Category', null=True, blank=True)

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


    def __str__(self):
        return self.title

    def publish(self, pub=True):
        if pub:
            self.published_date = timezone.now()
        else:
            self.published_date = None
        self.save()


    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"post_type":self.post_type, "slug":self.slug})

    def is_review(self):
        return str(self.post_type) == 'review'

    def pack_list(self):
        packlist = []
        for item in self.gear.all():
            packlist.append(item.short_name)
        packlist = list(set(packlist))
        return packlist


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
    full_name = models.CharField(max_length=60, editable=False)
    category = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return self.full_name

    def unique_short_names(self):
        items = []
        for item in self.objects.all():
            items += str(item.short_name)
        items = list(set(items))

        return items

    def review_url(self):
        qs = Post.objects.filter(gear=self.pk, category='review')


class Category(models.Model):
    name = models.CharField(max_length=16, primary_key=True)
    
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=16, primary_key=True)

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

def post_save_post_receiver(sender, instance, *args, **kwargs):
    category_gear = Gear.objects.filter(category=instance.category)
    instance.gear = category_gear

def pre_save_gear_receiver(sender, instance, *args, **kwargs):
    instance.full_name = str(instance.brand) + ' ' + str(instance.model)


pre_save.connect(pre_save_post_receiver, sender=Post)
post_save.connect(post_save_post_receiver, sender=Post)
pre_save.connect(pre_save_gear_receiver, sender=Gear)
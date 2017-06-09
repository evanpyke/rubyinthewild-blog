from django.contrib import admin
from django.utils import timezone
from .models import Category, Comment, Gear, Post, Type

# Register your models here.

def approve_comment(modeladmin, request, queryset):
    queryset.update(approved_comment=True)
approve_comment.short_description = "Approve selected comments"

def disapprove_comment(modeladmin, request, queryset):
    queryset.update(approved_comment=False)
disapprove_comment.short_description = "Remove approval of selected comments"

def publish_post(modeladmin, request, queryset):
    queryset.update(published_date=timezone.now())
publish_post.short_description = "Publish selected posts"

class PostModelAdmin(admin.ModelAdmin):
    actions = [publish_post,]
    list_display = ['title', 'created_date', 'published_date', 'author']
    list_filter = (('author', admin.RelatedOnlyFieldListFilter), 'category', 'post_type')
    search_fields = ('title', 'text')

    class Meta:
        model = Post

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['text', 'approved_comment']
    actions = [approve_comment, disapprove_comment]
    # list_filter = (('author', admin.RelatedOnlyFieldListFilter), )
    # search_fields = ('text', 'author')

    class Meta:
        model = Comment

class GearModelAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'brand']
    list_filter = ('category', 'brand')

admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Gear, GearModelAdmin)
admin.site.register(Type)
admin.site.register(Category)

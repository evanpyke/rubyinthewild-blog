from django.contrib import admin
from .models import Post, Comment

# Register your models here.

def approve_comment(modeladmin, request, queryset):
    queryset.update(approved_comment=True)
approve_comment.short_description = "Approve selected comments"

def disapprove_comment(modeladmin, request, queryset):
    queryset.update(approved_comment=False)
disapprove_comment.short_description = "Remove approval of selected comments"

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_date', 'published_date', 'author']
    list_filter = (('author', admin.RelatedOnlyFieldListFilter), )
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

admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment, CommentModelAdmin)


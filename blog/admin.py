from django.contrib import admin
from .models import Post, Comment

# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_date', 'published_date', 'author']
    list_filter = (('author', admin.RelatedOnlyFieldListFilter), )
    search_fields = ('title', 'text')
#    prepopulated_fields = {'slug': ('title',), }
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment)


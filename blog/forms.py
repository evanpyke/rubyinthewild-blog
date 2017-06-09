from django import forms
from .models import Post, Comment, Gear

class PostForm(forms.ModelForm):
    # gear_choices = ()
    # for item in Gear.objects.all():
    #     gear_choices += ((item.full_name, item.full_name),)

    # gear = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=gear_choices, initial='DeLorme inReach SE')

    class Meta:
        model = Post
        fields = ('title', 'text', 'post_type', 'category', 'image')

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('author', 'text',)
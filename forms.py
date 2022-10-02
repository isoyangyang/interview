from django.forms import ModelForm, TextInput
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post']
        labels = {
            'post': ''
        }
        widgets = {
            'post': TextInput(attrs={
                'class': "form-control",
                'style': 'width: 100%;',
                'placeholder': 'Post'
            })
        }

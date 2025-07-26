from django import forms
from django.forms import inlineformset_factory
from .models import BlogPost, BlogPostBlock

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заглавие',}),
        }

        labels = {
            'title': 'Заглавие'
        }


class BlogPostBlockForm(forms.ModelForm):
    class Meta:
        model = BlogPostBlock
        fields = ['text', 'image', 'order']

        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Текст'})
        }

        labels = {
            'text': 'Текст',
            'image': 'Снимка',
            'order': 'Подредба'
        }


BlogPostBlockFormSet = inlineformset_factory(
    BlogPost,
    BlogPostBlock,
    form=BlogPostBlockForm,
    extra=1,
    can_delete=True
)
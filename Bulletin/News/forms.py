from django import forms
from News.models import Post,Comment

class PostForm(forms.ModelForm):
    docfile = forms.FileField(
        label='Select a file',
        help_text='Max-size : 42 Mb',
        required= False,
    )

    class Meta():
        model=Post
        fields=('title','text','docfile')

        widgets={
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):

    class Meta():
        model=Comment
        fields = ('text',)

    widgets={
        'author':forms.TextInput(attrs={'class':'textinputclass'}),
        'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
    }

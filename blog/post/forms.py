from django import forms
from post.models import Category

class PostForm(forms.Form):
    title = forms.CharField(max_length=200)
    category = forms.ModelChoiceField(queryset = Category.objects.all())
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=200, required=False)

class SignInForm(forms.Form):
    userid = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)
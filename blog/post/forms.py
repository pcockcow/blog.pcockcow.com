from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=200)
    category = forms.CharField(max_length=200)
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=200)

class SignInForm(forms.Form):
    userid = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)
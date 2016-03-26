from django.shortcuts import render
from django.http import HttpResponseRedirect
from post.forms import PostForm, SignInForm
from post.models import Post, Category, Tag
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(req):
    posts = Post.objects.all().order_by("-id")
    return render(req, 'index.html', { "posts": posts })


def detail(req, post_id):
    post = Post.objects.get(pk=post_id)
    return render(req, 'detail.html', { "post": post })


@login_required(login_url='/signIn/')
def post(req):
    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            formData = form.cleaned_data
            articles = Post(
                author =  User.objects.get(username=req.user.username),
                title = formData['title'],
                category = Category.objects.get(name=formData['category']),
                content = formData['content']
            )
            articles.save()

        return HttpResponseRedirect('/')

    else:
        form = PostForm()

    return render(req, 'write.html', {'form': form})


def signIn(req):
    if req.method == 'POST':
        form = SignInForm(req.POST)

        if form.is_valid():
            formData = form.cleaned_data
            user = authenticate(username=formData["userid"], password=formData["password"])

            if user is not None:
                if user.is_active:
                    login(req, user)
                    next = req.POST["next"]

                    if not next:
                        next = "/"

                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect("/signIn/")
            else:
                return HttpResponseRedirect("/signIn/")
        else:
            return HttpResponseRedirect("/signIn/")
    else:
        nextURL=req.GET.get("next","")
        form = SignInForm()

    return render(req, 'signIn.html', {'form':form, 'nextURL':nextURL})


def signOut(req):
    logout(req)
    return HttpResponseRedirect('/')


def leftMenu(req):
    category = Category.objects.all()
    recent = Post.objects.order_by("created_date")[:5]
    user = req.user
    userNm = ""

    if user.is_authenticated():
        userNm = user.username

    return {"categorys": category, "recents": recent, "username":userNm}
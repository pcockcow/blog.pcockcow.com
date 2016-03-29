from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from post.forms import PostForm, SignInForm
from post.models import Post, Category, Tag
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os, uuid, json


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

@csrf_exempt
@login_required(login_url='/signIn/')
def imgUpload(req):
    if req.method == "POST":
        img_path = handle_uploaded_file(req.META["HTTP_FILE_NAME"], req.body)
        resp_data = "&bNewLine=true&sFileName=" + req.META["HTTP_FILE_NAME"] + "&sFileURL=http://"+req.META['HTTP_HOST']+"/"+img_path
        return HttpResponse(resp_data)

def handle_uploaded_file(filename, file):
    img_dir = "media/"
    ext = os.path.splitext(filename)[1]
    file_name = str(uuid.uuid4())
    img_path = img_dir + file_name + ext

    with open(img_path, 'wb+') as outfile:
        outfile.write(file)

    return img_path

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

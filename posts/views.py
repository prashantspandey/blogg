import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect,Http404
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def posts_create(request,*args,**kwargs):
    clickedcreate = True
    context = {'clickedcreate':clickedcreate}
    return render(request, 'post_form.html',context)

def posts_sudocreate(request,*args,**kwargs):
    posttitle = request.POST['title']
    postcontent = request.POST['content']
    postdraftornot = request.POST['draftornot']
    postpublishdate = request.POST['publishdate']
    newpost = Post()
    newpost.title = posttitle
    newpost.content = postcontent
    newpost.draft = postdraftornot
    newpost.publish = postpublishdate
    newpost.save()

    return HttpResponseRedirect(
        newpost.get_absolute_url())



    # context ={'posttitle':posttitle , 'postcontent':postcontent,'postdraftornot':postdraftornot,
    #           'postpublishdate':postpublishdate,}
    # return render(request, 'try.html',context)



def posts_detail(request,slug):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = urllib.parse.quote_plus(instance.content)
    context = {'instance': instance, 'title': instance.title,'share_string':share_string,'slug':slug}
    return render(request, "post_detail.html", context)


def posts_list(request):
    clickedhome = True
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    page_request_var = 'page'
    paginator = Paginator(queryset_list, 5)
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {'object_list': queryset, 'title': "All Posts", 'page_request_var': page_request_var,'today':today,'clickedhome':clickedhome,}
    return render(request, "post_list.html", context)

def posts_sudoupdate(request,*args,**kwargs):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if request.POST:
        slug = request.POST['slugg']
        editedtitle = request.POST['title']
        editedcontent = request.POST['content']
        editeddraft = request.POST['draftornot']
        editedpublish = request.POST['publishdate']
        instance = get_object_or_404(Post, slug=slug)
        instance.title = editedtitle
        instance.content = editedcontent
        instance.draft = editeddraft
        instance.publish = editedpublish
        instance.save()


    # form = PostForm(request.POST or None, request.FILES or None, instance=instance)  # instance loads data to form
    # if form.is_valid():
    #     instance = form.save(commit=False)
    #     instance.save()
    #     messages.success(request, 'Successfully Updated')
    #     return HttpResponseRedirect(
    #         instance.get_absolute_url())  # takes us to post after updating it (coming from models)
    #
        return HttpResponseRedirect(
            instance.get_absolute_url())

def posts_update(request, slug):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    else:
        instance = get_object_or_404(Post, slug=slug)
        edit = True
        context ={'instance': instance,'edit':edit,'slu':slug,}
        return render(request, 'post_form.html',context)


def posts_delete(request,slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)

    instance.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect("list")


def posts_search(request):
    clickedsearch = True
    qu = request.GET['search']
    qs = Post.objects.filter(Q(title__contains=qu)| Q(content__contains=qu)).distinct()

    context = {'result': qs, 'results_for': qu,'clickedresult':clickedsearch}

    return render(request, "search_list.html", context)

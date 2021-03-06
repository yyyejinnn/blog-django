from unicodedata import category
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category, Post, Tag

# Create your views here.
class PostList(ListView):
    model = Post
    ordering = "-pk"

    def get_context_data(self, **kwargs):  # 재정의 ex)post_list
        context = super(PostList, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()

        return context


def category_page(request, slug):  # FBV
    if slug == "no_category":
        category = "미분류"
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        "blog/post_list.html",
        {  # 직접 html에 넘겨주기 때문에 직접 정의해줘야함
            "post_list": post_list,
            "categories": Category.objects.all(),
            "no_category_post_count": Post.objects.filter(category=None).count(),
            "category": category,
        },
    )


def tag_page(request, slug):  # FBV
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()  # 역참조

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": post_list,
            "tag": tag,
            "no_category_post_count": Post.objects.filter(category=None).count(),
            "category": category,
        },
    )

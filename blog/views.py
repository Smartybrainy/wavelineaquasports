from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Post, SideBar, Like
from .forms import CommentForm


class PostListView(ListView):

    def get(self, *args, **kwargs):
        queryset = Post.objects.filter(status="P").order_by('-date_created')
        side_bar = SideBar.objects.all()

        paginator = Paginator(queryset, 5)
        page = self.request.GET.get('page')
        queryset = paginator.get_page(page)

        context = {
            'object_list': queryset,
            'side_bar': side_bar
        }
        return render(self.request, 'blog/post_list.html', context)


def post_detail(request, slug):
    queryset = get_object_or_404(Post, slug=slug)
    # Comment form
    commnet_form = CommentForm(request.POST or None)
    print(request.POST)
    if commnet_form.is_valid():
        print(commnet_form.is_valid())
        messages.info(request, "comment added")
        new_comment = commnet_form.save(commit=False)
        new_comment.post = queryset
        new_comment.save()
        return redirect('blog:post-detail', queryset.slug)

    context = {
        'comment_form': CommentForm,
        'object': queryset
    }
    return render(request, 'blog/post_detail.html', context)


def post_search(request):
    search_qs = request.GET['qs']
    if search_qs is not None:
        qs = Post.objects.filter(
            Q(title__icontains=search_qs) | Q(content__icontains=search_qs)
        )
        context = {'queryset': qs}
        return render(request, 'blog/search_result.html', context)


class PostLikes(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        post_id = request.POST.get('like_id')
        post_obj = Post.objects.get(pk=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
            post_obj.save()

        like, created = Like.objects.get_or_create(
            user=user, like_post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = "Unlike"
            else:
                like.value = 'Like'
        like.save()

        data = {
            'likes': post_obj.liked.all().count(),
            'value': like.value
        }
        return JsonResponse(data, safe=False)

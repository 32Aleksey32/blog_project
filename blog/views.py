from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .pagination import paginate_page
from .serializers import PostSerializer


class Signup(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration/signup.html'

    def get(self, request):
        form = UserCreationForm()
        return Response({'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('index')
        return Response({'form': form})


class PostList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        query = request.GET.get('q', '')
        queryset = Post.objects.all()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(text__icontains=query))
        page_obj = paginate_page(queryset, request)
        return Response({'page_obj': page_obj, 'query': query})


class PostCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_create.html'

    def get(self, request):
        serializer = PostSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save(author=request.user)
        return redirect('index')


class PostDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_detail.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response({'serializer': serializer, 'post': post})


class PostEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_edit.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response({'serializer': serializer, 'post': post})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'post': post})
        serializer.save()
        return redirect('post-detail', post_id=post_id)


class PostDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_delete.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer()
        return Response({'serializer': serializer, 'post': post})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return redirect('index')


class LikePost(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.likes += 1
        post.save()
        next_url = request.POST.get('next', 'index')
        return HttpResponseRedirect(next_url)


class DislikePost(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.likes -= 1
        post.save()
        next_url = request.POST.get('next', 'index')
        return HttpResponseRedirect(next_url)

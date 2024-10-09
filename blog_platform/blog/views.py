from django.shortcuts import render
from .models import Post
from .models import Comment
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.shortcuts import render, get_object_or_404


def post_list(request):
    posts = Post.objects.all()
    print(f"Posts: {posts}") 
    return render(request, 'blog/post_list.html', {'posts': posts})
'''
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})
'''
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  
    comments = post.comment_set.all()  
    if request.method == 'POST':
        comment_content = request.POST.get('content')
        if comment_content:
            Comment.objects.create(content=comment_content, post=post, author=request.user)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required


def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user != post.author:
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})



def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('post_list')  

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'blog/post_form.html', {'form': post})

@login_required
def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user != post.author:
        return redirect('post_list')
    if request.user == post.author:
        post.delete()
    return redirect('post_list')

@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(content=content, author=request.user, post=post)
    return redirect('post_detail', post_id=post.id)

from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post


# class based view for the home page
# by default looks for a template of the form:
#   <app>/<model>_<viewtype>.html
# for our class PostListView this would be:
#   ccf/post_list.html
# we can pass our own name by setting attribute template_name
class PostListView(ListView):
    # model that is going to be displayed as a list
    model = Post
    template_name = 'ccf/home.html'
    # specify the name for our list objects that we use in our template
    # the class based view will by default pass all objects of our model
    # i.e. Post.objects.all()
    context_object_name = 'posts'
    # order our posts by date in reversed order (using a '-') to get the
    # newest posts first i.e. at the top of the page
    ordering = ['-date_posted']
    # turn on paginator and show a limited number of pages
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'ccf/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # used by UserPassesTestMixin
    def test_func(self):
        # get current post
        post = self.get_object()
        # user must be the author of the post to delete it
        return self.request.user == post.author


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # used by UserPassesTestMixin
    def test_func(self):
        # get current post
        post = self.get_object()
        # user must be the author of the post to update it
        return self.request.user == post.author


# function based view for the home page
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'ccf/home.html', context)


# function based view for the about page
def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'ccf/about.html', context)

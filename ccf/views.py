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
from .models import Client


# class based view for the home page
# by default looks for a template of the form:
#   <app>/<model>_<viewtype>.html
# for our class ClientListView this would be:
#   ccf/client_list.html
# we can pass our own name by setting attribute template_name
class ClientListView(ListView):
    # model that is going to be displayed as a list
    model = Client
    template_name = 'ccf/home.html'
    # specify the name for our list objects that we use in our template
    # the class based view will by default pass all objects of our model
    # i.e. Client.objects.all()
    context_object_name = 'clients'
    # order our clients by date in reversed order (using a '-') to get the
    # newest clients first i.e. at the top of the page
    ordering = ['-date_added']
    # turn on paginator and show a limited number of pages
    paginate_by = 5


class UserClientListView(ListView):
    model = Client
    template_name = 'ccf/user_clients.html'
    context_object_name = 'clients'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Client.objects.filter(therapist=user).order_by('-date_added')


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = '/'

    # used by UserPassesTestMixin
    def test_func(self):
        # get current client
        client = self.get_object()
        # user must be the therapist of the client to delete it
        return self.request.user == client.therapist


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['friendly_name']

    def form_valid(self, form):
        form.instance.therapist = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['friendly_name']

    def form_valid(self, form):
        form.instance.therapist = self.request.user
        return super().form_valid(form)

    # used by UserPassesTestMixin
    def test_func(self):
        # get current client
        client = self.get_object()
        # user must be the therapist of the client to update it
        return self.request.user == client.therapist


# function based view for the home page
def home(request):
    context = {
        'clients': Client.objects.all()
    }
    return render(request, 'ccf/home.html', context)


# function based view for the about page
def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'ccf/about.html', context)

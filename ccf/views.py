from django.utils import (
    timezone
)
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
from django.utils.decorators import classonlymethod
from django.urls import (
    reverse
)
from bootstrap_datepicker_plus.widgets import (
    DatePickerInput,
)

import ccf.symbols
from .models import (
    Client, Note, Treatment, Medical,
)
from .filters import (
    ClientFilter,
)

# class based view for the home page
# class based views by default look for a template of the form:
#   <app>/<model>_<viewtype>.html
# for our class ClientListView this would be:
#   ccf/client_list.html
# we can however pass our own name by setting attribute template_name
class ClientListView(LoginRequiredMixin, ListView):
    # model that is going to be displayed as a list
    model = Client
    # our template name
    template_name = 'ccf/home.html'
    # the default name for the objests to pass to the template is 'object'
    # we specify our own name for our list objects that we use in our template
    # the class based view will by default pass all objects of our model
    # i.e. Client.objects.all()
    context_object_name = 'clients'
    # order our clients by date in reversed order (using a '-') to get the
    # newest clients first i.e. at the top of the page
    # todo:order alphabetically
    # todo:show compact, scrollable list
    ordering = ['-date_added']
    # turn on paginator and show a limited number of pages
    paginate_by = 5


class UserClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'ccf/user_clients.html'
    context_object_name = 'clients'
    paginate_by = 5
    # todo:show compact, scrollable list

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        clients = Client.objects.filter(therapist=user).order_by('display_name')
        self.filterset = ClientFilter(self.request.GET, queryset=clients)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['form'] = self.filterset.form
        pass
        return context


class ClientDataView:
    model = Client
    fields = [
        'display_name',
        'full_name',
        'address',
        'mobile',
        'phone',
        'email',
        'profession',
        'dob',
    ]
    optional_fields = [
        'full_name',
        'address',
        'mobile',
        'phone',
        'email',
        'profession',
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for f in self.optional_fields:
            form.fields[f].required = False
        form.fields['dob'].widget = DatePickerInput()
        form.fields['dob'].label = 'Date of birth'
        return form

    def form_valid(self, form):
        form.instance.therapist = self.request.user
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # add all Notes, Treatments & Medical details for this client
        context['notes'] = (
            Note.objects
            .filter(client=context['client'])
            .order_by('-date_updated')
        )
        context['treatments'] = (
            Treatment.objects
            .filter(client=context['client'])
            .order_by('-date_treated')
        )
        try:
            medical_data = Medical.objects.filter(client=context['client'])[0]
        except IndexError:
            medical_data = None
        context['medical'] = medical_data
        # add number of tab we want to activate
        context['tab_to_open'] = context['view'].kwargs['tab']
        return context


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'ccf/generic_confirm_delete.html'

    # page to redirect to after client is deleted; user list view
    def get_success_url(self):
        return reverse('ccf:user-clients', args=[self.request.user.username])

    # used by UserPassesTestMixin
    def test_func(self):
        # get current client
        client = self.get_object()
        # user must be the therapist of the client to delete the client
        return self.request.user == client.therapist


class ClientCreateView(ClientDataView, LoginRequiredMixin, CreateView):
    template_name = 'ccf/generic_add_update_form.html'


class ClientUpdateView(ClientDataView, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'ccf/generic_add_update_form.html'

    # used by UserPassesTestMixin
    def test_func(self):
        # get current client
        client = self.get_object()
        # user must be the therapist of the client to update client details
        return self.request.user == client.therapist


class MedicalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Medical
    template_name = 'ccf/generic_add_update_form.html'
    context_object_name = 'medical'
    fields = [
        'conditions',
        'medication',
        'appearance',
        'peels',
    ]
    optional_fields = [
        'conditions',
        'medication',
        'appearance',
        'peels',
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # account for optional fields
        for f in self.optional_fields:
            form.fields[f].required = False
        return form

    def form_valid(self, form):
        form.instance.therapist = self.request.user
        return super().form_valid(form)

    # used by UserPassesTestMixin
    def test_func(self):
        # current user must be the therapist of the client to update it
        medical = self.get_object()
        client = medical.client
        return self.request.user == client.therapist


class GenericDataView:
    fields = [
        'title',
        'content',
    ]
    optional_fields = [
        'content',
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for f in self.optional_fields:
            form.fields[f].required = False
        return form

    def form_valid(self, form):
        # we have to set the ID of the client and the data,
        # the form takes care of the other fields
        form.instance.client_id = self.kwargs.get('client_id')
        form.instance.date_updated = timezone.now()
        return super().form_valid(form)

    # used by UserPassesTestMixin
    def test_func(self):
        # get current client
        _object = self.get_object()
        if isinstance(_object, Client):
            client = _object
        else:
            client = _object.client
        # user must be the therapist of the client to access a note
        return self.request.user == client.therapist


class NoteDataView(GenericDataView):
    model = Note


class NoteCreateView(NoteDataView, LoginRequiredMixin, CreateView):
    template_name = 'ccf/generic_add_update_form.html'


class NoteUpdateView(NoteDataView, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'ccf/generic_add_update_form.html'


class NoteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ccf/generic_detail.html'
    model = Note
    fields = "__all__"

    # example how to override the as_view method in class based views
    @classonlymethod
    def as_view(cls, **initkwargs):
        self = cls(**initkwargs)
        view = super(NoteDetailView, cls).as_view(**initkwargs)
        return view


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'ccf/generic_confirm_delete.html'

    # page to redirect to after client is deleted; user list view
    def get_success_url(self):
        return reverse(
            'ccf:client-detail',
            kwargs={
                'pk': self.object.client_id,
                'tab': ccf.symbols.CLIENT_TAB_NOTES,
            }
        )

    # used by UserPassesTestMixin
    def test_func(self):
        # get current client
        _object = self.get_object()
        if isinstance(_object, Client):
            client = _object
        if isinstance(_object, Note):
            client = _object.client
        # user must be the therapist of the client to access a note
        return self.request.user == client.therapist


class TreatmentDataView(GenericDataView):
    model = Treatment


class TreatmentCreateView(TreatmentDataView, LoginRequiredMixin, CreateView):
    template_name = 'ccf/generic_add_update_form.html'


class TreatmentUpdateView(TreatmentDataView, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'ccf/generic_add_update_form.html'


class TreatmentDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ccf/generic_detail.html'
    model = Treatment
    fields = "__all__"

    # example how to override the as_view method in class based views
    @classonlymethod
    def as_view(cls, **initkwargs):
        self = cls(**initkwargs)
        view = super(TreatmentDetailView, cls).as_view(**initkwargs)
        return view


class TreatmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Treatment
    template_name = 'ccf/generic_confirm_delete.html'

    # page to redirect to after client is deleted; user list view
    def get_success_url(self):
        return reverse(
            'ccf:client-detail',
            kwargs={
                'pk': self.object.client_id,
                'tab': ccf.symbols.CLIENT_TAB_TREATMENTS,
            }
        )

    # used by UserPassesTestMixin
    def test_func(self):
        # get current client
        _object = self.get_object()
        if isinstance(_object, Client):
            client = _object
        if isinstance(_object, Treatment):
            client = _object.client
        # user must be the therapist of the client to access a treatment
        return self.request.user == client.therapist


# function based view for the about page
def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'ccf/about.html', context)

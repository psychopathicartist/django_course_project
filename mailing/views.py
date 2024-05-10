from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from blog.models import Blog
from mailing.forms import MailingForm, ClientForm, MessageForm, PermMailingForm
from mailing.models import Mailing, Client, Message, Log


class MainView(TemplateView):
    template_name = "mailing/main.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['total_mailings'] = Mailing.objects.all().count()
        context_data['started_mailings'] = Mailing.objects.filter(status='Запущена').count()
        context_data['all_clients'] = Client.objects.all().distinct('email').count()
        blog_posts = Blog.objects.all()
        three_posts = list(blog_posts)[:3]
        context_data['blogs'] = three_posts
        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm('mailing.change_status'):
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(author=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    login_url = reverse_lazy('users:login')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user.is_superuser or self.request.user == mailing.author


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse('mailing:view', args=[self.kwargs.get('pk')])

    def test_func(self):
        mailing = self.get_object()
        return self.request.user.is_superuser or self.request.user == mailing.author

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')
    login_url = reverse_lazy('users:login')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user.is_superuser or self.request.user == mailing.author


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm('mailing.change_status'):
            return Client.objects.all()
        else:
            return Client.objects.filter(author=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    login_url = reverse_lazy('users:login')

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or self.request.user == client.author


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse('mailing:client_view', args=[self.kwargs.get('pk')])

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or self.request.user == client.author


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    login_url = reverse_lazy('users:login')

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or self.request.user == client.author


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Message.objects.all()
        else:
            return Message.objects.filter(author=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    login_url = reverse_lazy('users:login')

    def test_func(self):
        message = self.get_object()
        return self.request.user.is_superuser or self.request.user == message.author


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse('mailing:message_view', args=[self.kwargs.get('pk')])

    def test_func(self):
        message = self.get_object()
        return self.request.user.is_superuser or self.request.user == message.author


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    login_url = reverse_lazy('users:login')

    def test_func(self):
        message = self.get_object()
        return self.request.user.is_superuser or self.request.user == message.author


class LogListView(LoginRequiredMixin, TemplateView):
    template_name = "mailing/log_list.html"
    login_url = reverse_lazy('users:login')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        if user.is_superuser:
            context_data['logs'] = Log.objects.all()
        else:
            logs = []
            mailings = Mailing.objects.filter(author=user)
            for mailing in mailings:
                author_logs = Log.objects.filter(mailing=mailing)
                for author_log in author_logs:
                    logs.append(author_log)
            context_data['logs'] = logs
        return context_data


class MailingEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = PermMailingForm
    permission_required = 'mailing.change_status'
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse('mailing:view', args=[self.kwargs.get('pk')])

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .models import Links, Tags
from .forms import LinkForm

class ExtraContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        context.update(self.extra())
        return context

    def extra(self):
        return dict()

class AddLink(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'

    model = Links
    form_class = LinkForm
    template_name = "links/add-link.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect("/user-links/")

    def success_url(self):
        return redirect("/user-links/")

class ListUserLink(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'

    model = Links
    context_object_name = "links"
    template_name = "links/list-user-links.html"

    def get_queryset(self):
        return Links.objects.filter(user=self.request.user)

class ShowTagLinks(ListView):
    model = Links
    context_object_name = "links"
    template_name = "links/show-tag-links.html"

    def get_queryset(self):
        return Links.objects.filter(tags=self.kwargs['pk'])

class ListLink(ListView):
    model = Links
    context_object_name = "links"
    template_name = "links/list-links.html"

    def get_queryset(self):
        return Links.objects.all()


class ShowLink(DetailView):
    model = Links
    context_object_name = "links"
    template_name = "links/show-link.html"


class UpdateLink(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'

    model = Links
    form_class = LinkForm
    template_name = "links/update-link.html"

    def get_success_url(self):
        return reverse('user-links')


def Jump(request, short_url):
    short = get_object_or_404(Links, short_url=short_url)
    Links.objects.filter(id=short.id).update(jump=int(short.jump) + 1)
    return HttpResponseRedirect(short.original_url)


def DelLink(request, pk):
    if not request.user.is_active:
        return HttpResponseRedirect('/accounts/login/')
    else:
        try:
            link = Links.objects.get(id=pk)
            link.delete()
            return HttpResponseRedirect("/user-links/")
        except Links.DoesNotExist:
            return HttpResponseNotFound("<p>Ссылка не найдена.</p>")
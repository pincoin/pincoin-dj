from django.urls import reverse_lazy
from django.views import generic


class HomeView(generic.RedirectView):
    url = reverse_lazy('admin:index')

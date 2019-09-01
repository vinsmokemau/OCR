"""."""
from django.views.generic import (
    TemplateView,
    FormView,
)
from .forms import ImageForm
from django.urls import reverse_lazy


class HomeView(FormView):
    """This view recibe form fields and send an email."""

    template_name = 'home.html'
    form_class = ImageForm
    success_url = reverse_lazy('cms:home')

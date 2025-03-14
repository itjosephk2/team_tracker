from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from people_management.models import Person


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('security:login')  # Uses URL name instead of hardcoding
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['people'] = Person.objects.all()
        return context 

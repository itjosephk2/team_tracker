from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from people_management.models import Person


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'  # This should now use reverse_lazy('security:login') if you're using namespaces
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['people'] = Person.objects.only('id', 'first_name', 'last_name')  
        return context

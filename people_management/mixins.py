from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = []
    def dispatch(self, request, *args, **kwargs):
        person = getattr(request.user, "person", None)
        if not person or person.role not in self.allowed_roles:
            return redirect(reverse('dashboard:dashboard'))
        return super().dispatch(request, *args, **kwargs)

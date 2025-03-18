from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from people_management.models import Person, Contract

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    View for the main dashboard, displaying relevant data based on user roles.

    - Employees: See only their own details and contracts.
    - Managers: See their assigned team members and their contracts.
    - HR/Admins: See all employees and all contracts.

    Access Control:
    - Users must be logged in (redirects to login page if not authenticated).
    - Managers can only access their direct team.
    - Employees do not see the people management table.
    """
    login_url = reverse_lazy('security:login')
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        """
        Get context data for the dashboard template.

        This method adds the following context variables based on the logged-in user's role:
        
        - person: The logged-in user's personal details.
        - people: A list of employees visible to the user:
            - HR/Admin: All employees.
            - Manager: Employees in the manager's team.
            - Employee: None (or personal details only).
        - contracts: A list of contracts visible to the user:
            - HR/Admin: All contracts.
            - Manager: Contracts for employees in the manager's team.
            - Employee: Only the contracts associated with the user.

        Returns:
            dict: A dictionary with keys 'person', 'people', and 'contracts' for the template.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Ensure the user is linked to a Person record
        person = getattr(user, 'person', None)
        context['person'] = person

        # Role-based filtering for people
        if person:
            if person.role == "hr_admin":
                # HR Admins see all employees
                context['people'] = Person.objects.all()
            elif person.role == "manager":
                # Managers see only their assigned team members
                context['people'] = Person.objects.filter(manager=person)
            else:
                # Employees only see their own details, no people list
                context['people'] = None

            # Role-based filtering for contracts
            if person.role == "hr_admin":
                # HR Admins see all contracts
                context['contracts'] = Contract.objects.all()
            elif person.role == "manager":
                # Managers see contracts for their team members (assuming Contract has a ForeignKey to Person)
                context['contracts'] = Contract.objects.filter(person__manager=person)
            else:
                # Employees see only their own contracts
                context['contracts'] = Contract.objects.filter(person=person)
        else:
            # Fallback: if person is None, no contracts should be shown
            context['contracts'] = None

        return context
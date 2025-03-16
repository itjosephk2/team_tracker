from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from people_management.models import Person

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    View for the main dashboard, displaying relevant data based on user roles.

    - Employees: See only their own details.
    - Managers: See their assigned team members.
    - HR/Admins: See all employees.

    Access Control:
    - Users must be logged in (redirects to login page if not authenticated).
    - Managers can only access their direct team.
    - Employees do not see the people management table.
    """

    login_url = reverse_lazy('security:login')  # Redirect unauthorized users
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        """
        Adds relevant user and role-based data to the dashboard.

        Context Variables:
        - `person`: The logged-in user's personal details.
        - `people`: A list of employees based on the user's role:
            - HR/Admin: See all employees.
            - Manager: See only their assigned team.
            - Employee: This is set to None (no access to employee list).

        Returns:
            dict: Context data for rendering the dashboard template.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Ensure the user is linked to a Person record
        person = getattr(user, 'person', None)
        context['person'] = person

        # Debugging: Print user role info
        if person:
            print(f"User: {user.username}, Role: {person.role}, Manager: {person.manager}")

        # Role-based filtering
        if person:
            if person.role == "hr_admin":
                # HR Admins see all employees
                context['people'] = Person.objects.all()
                print("HR Admin - showing all employees")

            elif person.role == "manager":
                # Managers see only their assigned team members
                context['people'] = Person.objects.filter(manager=person)
                print(f"Manager - showing team members for {person.first_name} {person.last_name}")

            else:
                # Employees only see their own details, no people list
                context['people'] = None
                print("Employee - no team data shown")

        return context

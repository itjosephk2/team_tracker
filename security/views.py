from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group, Permission
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from django import forms
from people_management.models import Person
from .forms import CustomUserCreationForm, CustomLoginForm, UserForm


def is_hr_admin(user):
    """Helper function to check if a user is an HR Admin."""
    return user.groups.filter(name="HR Admin").exists()


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "security/auth/register.html"
    success_url = reverse_lazy("security:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = form.cleaned_data.get("is_staff")
        user.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("dashboard"))
        return super().dispatch(request, *args, **kwargs)


class LoginInterface(LoginView):
    form_class = CustomLoginForm
    template_name = "security/auth/login.html"


class LogoutInterface(LogoutView):
    next_page = reverse_lazy("security:login")


class ListUsers(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"
    template_name = "security/user_list.html"


class ViewUserDetails(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "user"
    template_name = "security/user_detail.html"


class CreateNewUser(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "security/user_form.html"
    success_url = reverse_lazy("security:user_list")

    def test_func(self):
        return is_hr_admin(self.request.user)


class UpdateUser(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "security/user_form.html"
    success_url = reverse_lazy("security:user_list")

    def test_func(self):
        return is_hr_admin(self.request.user)


class DeleteUser(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "security/user_confirm_delete.html"
    success_url = reverse_lazy("security:user_list")

    def test_func(self):
        return is_hr_admin(self.request.user)


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]


@permission_required("auth.view_group", raise_exception=True)
def group_list(request):
    groups = Group.objects.all()
    return render(request, "security/group_list.html", {"groups": groups})


@permission_required("auth.change_group", raise_exception=True)
def group_edit(request, pk=None):
    group = get_object_or_404(Group, pk=pk) if pk else Group()

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect("security:group_list")
    else:
        form = GroupForm(instance=group)

    return render(request, "security/group_form.html", {"form": form, "group": group})


@permission_required("auth.delete_group", raise_exception=True)
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == "POST":
        group.delete()
        return redirect("security:group_list")

    return render(request, "security/group_confirm_delete.html", {"group": group})

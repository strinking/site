from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic

from .models import RestrictProcessing
from stats.models import RoleMembership


class ProfileDetailView(UserPassesTestMixin, generic.DetailView):
    model = User

    raise_exception = True
    permission_denied_message = "You are not allowed to view this profile at the time."

    def test_func(self):
        """Test function used by `UserPassesTestMixin`.

        Used to disallow viewing profiles where users
        have set `restrict_processing` as required by GDPR.

        Returns:
            True:
                If the user whose profile is being visited
                does not have `restrict_processing` set or
                has it set to `False` (which is the default).
            False:
                If the user set `restrict_processing` to
                `True` through the profile change form.
        """

        profile_user = self.get_object()
        try:
            restrict_processing_row = RestrictProcessing.objects.get(user=profile_user)
        except RestrictProcessing.DoesNotExist:
            return True
        else:
            restricted = restrict_processing_row.restrict_processing
            # restricted == False: returns True, user can access
            # restricted == True: returns False, user can not access
            return not restricted

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["discord_role_membership"] = RoleMembership.objects.filter(
            guild_id=settings.DISCORD_GUILD_ID, user_id=self.get_object().id
        ).order_by(
            "-role__position"
        ).exclude(
            role__name="@everyone"
        )
        return context


class ProfileDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('home:index')

    raise_exception = True
    permission_denied_message = "You are not allowed to delete a profile that isn't yours."

    def test_func(self):
        return self.request.user == self.get_object()

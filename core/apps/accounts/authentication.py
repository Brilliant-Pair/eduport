from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameAuthentication(BaseBackend):
    def authenticate(self, request, username, password=None):
        try:
            user = User.objects.filter(Q(email=username) | Q(username=username)).first()

            if user and user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

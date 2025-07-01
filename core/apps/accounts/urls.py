from django.urls import path

from .views import (
    ActivateAccountView,
    LoginView,
    LogoutView,
    RegisterView,
    ResendActivateEmailView,
)

app_name = "accounts_app"


urlpatterns = [
    path("sign-in/", LoginView.as_view(), name="sign-in"),
    path("sign-out/", LogoutView.as_view(), name="sign-out"),
    path("sign-up/", RegisterView.as_view(), name="sign-up"),
    path(
        "verify/activate/<uidb64>/<token>/",
        ActivateAccountView.as_view(),
        name="activate",
    ),
    path("verify/resend/", ResendActivateEmailView.as_view(), name="re-activate"),
]

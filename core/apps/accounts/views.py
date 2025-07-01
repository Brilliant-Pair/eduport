import uuid

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import View

from .forms import LoginForm, RegisterForm, ResendActivateForm
from .tasks.mail import send_verification_email

# Create your views here.

User = get_user_model()


class LoginView(View):
    template_name = "accounts/sign_in.html"
    success_url = reverse_lazy("home_app:home")

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, _("You are already logged in!"))
            return redirect(self.success_url)

        form = LoginForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)

                if form.cleaned_data.get("remember"):
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)

                messages.success(request, _("You're logged in!"))

                return redirect(self.success_url)

        return render(request, self.template_name, context={"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.warning(request, _("You're logged out!"))
        return redirect("home_app:home")


class RegisterView(View):
    template_name = "accounts/sign_up.html"
    success_url = reverse_lazy("accounts_app:sign-in")

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, _("You are already logged in!"))
            return redirect(self.success_url)
        form = RegisterForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            email = cleaned_data.get("email")
            username = self._generate_username(email)
            password = cleaned_data.get("password1")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            # send verification email
            mail_subject = "Please activate your account"
            email_template = "emails/account_verification_email.html"
            send_verification_email.delay(
                user.pk, get_current_site(request).domain, mail_subject, email_template
            )
            #  send_verification_email.delay(user.pk, get_current_site(request).domain, mail_subject, email_template)

            messages.success(
                request,
                _(
                    "Your account has been created. Please check your email to verify your account."
                ),
            )
            return redirect(self.success_url)

        return render(request, self.template_name, context={"form": form})

    def _generate_username(self, email):
        base_username = email.split("@")[0]
        return f"{base_username}-{uuid.uuid4().hex[:8]}"


class ActivateAccountView(View):

    def get(self, request, uidb64, token):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect("home_app:home")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Congratulations! Your account is activated.")

        else:
            messages.error(request, "Invalid activation link.")

        return redirect("home_app:home")


class ResendActivateEmailView(View):
    template_name = "accounts/resend_activate.html"
    success_url = reverse_lazy("accounts_app:sign-in")

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect("home_app:home")

        form = ResendActivateForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = ResendActivateForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data.get("email"))

            if user.is_active:
                messages.info(
                    request, _("Your account is already activated. Please log in.")
                )
                return redirect(self.success_url)

            # send verification email
            mail_subject = "Please activate your account"
            email_template = "emails/account_verification_email.html"

            send_verification_email(
                user.pk, get_current_site(request).domain, mail_subject, email_template
            )
            #  send_verification_email.delay(user.pk, get_current_site(request).domain, mail_subject, email_template)

            messages.success(
                request,
                _("Please check your email to verify your account."),
            )
            return redirect(self.success_url)

        return render(request, self.template_name, context={"form": form})

import re

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, validate_slug
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LoginForm(forms.Form):
    login = forms.CharField(
        max_length=255,
        error_messages={
            "invalid": _("Enter a valid email address or username."),
            "required": _("Email or Username is required."),
        },
        widget=forms.TextInput(
            attrs={
                "class": "form-control border-0 bg-light rounded-end ps-1",
                "placeholder": "test@gmail.com",
                "dir": "rtl",
            }
        ),
    )
    password = forms.CharField(
        max_length=32,
        error_messages={
            "required": _("Password is required."),
        },
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-0 bg-light rounded-end ps-1",
                "placeholder": "********",
                "dir": "rtl",
            }
        ),
    )

    remember = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
    )

    def clean_login(self):
        login = self.cleaned_data.get("login")

        if "@" in login:
            try:
                validate_email(login)
            except ValidationError:
                raise ValidationError(_("Enter a valid email address."))
        else:
            if not re.fullmatch(r"^[-a-zA-Z0-9_]+$", login):
                raise ValidationError(_("Enter a valid username."))

        return login

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))

        return password

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get("login")
        password = cleaned_data.get("password")

        if login and password:
            user = authenticate(username=login, password=password)
            if not user:
                raise ValidationError(_("The username or password is incorrect"))
            self._user = user

    def get_user(self):
        return getattr(self, "_user", None)


class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control border-0 bg-light rounded-end ps-1",
                "placeholder": "test@gmail.com",
                "dir": "rtl",
            }
        ),
        error_messages={
            "invalid": _("Enter a valid email address."),
            "required": _("Email is required."),
        },
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-0 bg-light rounded-end ps-1",
                "placeholder": "********",
                "dir": "rtl",
            }
        ),
        error_messages={
            "required": _("Password is required."),
        },
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-0 bg-light rounded-end ps-1",
                "placeholder": "********",
                "dir": "rtl",
            }
        ),
        error_messages={
            "required": _("Password confirmation is required."),
        },
    )

    terms_agreed = forms.BooleanField(
        required=True,
        error_messages={
            "required": _("You must accept the terms to register."),
        },
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Email already exists."))
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))

        if not any(char.isupper() for char in password1):
            raise ValidationError(
                _("Password must contain at least one uppercase letter.")
            )

        if not any(char.islower() for char in password1):
            raise ValidationError(
                _("Password must contain at least one lowercase letter.")
            )

        special_chars = "@#$%!_"
        if not any(char in special_chars for char in password1):
            raise ValidationError(
                _("Password must contain at least one special character (@ # $ % ! _).")
            )

        if not re.fullmatch(r"[a-zA-Z0-9@#$%!_]+", password1):
            raise ValidationError(
                _(
                    "Password can only contain English letters, numbers, and special characters (@ # $ % ! _)."
                )
            )

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", _("Passwords do not match."))

        return cleaned_data


class ResendActivateForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control border-0 bg-light rounded-end ps-1",
                "placeholder": "test@gmail.com",
                "dir": "rtl",
            }
        ),
        error_messages={
            "invalid": _("Enter a valid email address."),
            "required": _("Email is required."),
        },
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_("Email not exists."))
        return email

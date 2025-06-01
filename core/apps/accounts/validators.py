import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_phone(value):
    """
    Validates that the provided phone number is a valid Iranian phone number.
    """

    phone_regex = re.compile(r"^(09)\d{9}$")

    if not phone_regex.match(value):
        raise ValidationError(_("Please enter a valid phone number."))

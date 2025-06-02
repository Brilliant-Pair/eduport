import pytest
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@pytest.mark.django_db
class TestUserManager:

    def test_email_validator_with_valid_email(self, user_manager):
        "Test that valid email pass the validation."
        valid_emails = ["test1@gmail.com", "test2@gmail.com", "test3@gmail.com"]

        for email in valid_emails:
            user_manager.email_validator(email)

    def test_email_validator_with_invalid_email(self, user_manager):
        "Test that invalid emails raise ValueError"
        invalid_emails = [
            "test@",
            "test@gmail",
            "test@gmail." "@test.com",
            "test@.com",
            "test@test..com",
        ]
        for email in invalid_emails:
            with pytest.raises(ValueError) as error:
                user_manager.email_validator(email)

            assert str(error.value) == str(_("You must provide a valid email address."))

    def test_create_user_with_minimal_required_fields(self, user_manager):
        user = user_manager.create_user(
            username="test", email="test@test.com", is_active=True
        )
        assert user.id
        assert user.uuid
        assert user.email == "test@test.com"
        assert user.username == "test"
        assert user.has_usable_password() is False
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_user_with_password(self, user_manager):
        user = user_manager.create_user(
            username="test", email="test@test.com", password="test"
        )

        assert user.id
        assert user.uuid
        assert user.email == "test@test.com"
        assert user.username == "test"
        assert user.has_usable_password() is True
        assert user.is_active is False
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_user_missing_username(self, user_manager):
        with pytest.raises(ValueError) as error:
            user_manager.create_user(email="test@test.com", username="")
        assert str(error.value) == str(_("Users must have an username."))

    def test_create_user_missing_email(self, user_manager):
        with pytest.raises(ValueError) as error:
            user_manager.create_user(email="", username="test")
        assert str(error.value) == str(_("Users must have an email address."))

    def test_create_superuser(self, user_manager):
        superuser = user_manager.create_superuser(
            username="test", email="test@test.com", password="test"
        )

        assert superuser.id
        assert superuser.uuid
        assert superuser.email == "test@test.com"
        assert superuser.username == "test"
        assert superuser.has_usable_password() is True
        assert superuser.is_active is True
        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_create_superuser_missing_password(self, user_manager):
        with pytest.raises(ValueError) as error:
            user_manager.create_superuser(
                username="test", email="test@test.com", password=""
            )
        assert str(error.value) == str(_("Superuser must have password."))

    def test_create_superuser_not_staff(self, user_manager):
        with pytest.raises(ValueError) as error:
            user_manager.create_superuser(
                username="test", email="test@test.com", password="test", is_staff=False
            )
        assert str(error.value) == str(
            _("Superusers must have 'is_staff' attribute set to True.")
        )

    def test_create_superuser_not_superuser(self, user_manager):
        with pytest.raises(ValueError) as error:
            user_manager.create_superuser(
                username="test",
                email="test@test.com",
                password="test",
                is_superuser=False,
            )
        assert str(error.value) == str(
            _("Superusers must have 'is_superuser' attribute set to True.")
        )


@pytest.mark.django_db
class TestUser:
    def test_create_normal_user(self, normal_user):
        assert normal_user.id is not None
        assert normal_user.uuid is not None
        assert normal_user.email is not None
        assert normal_user.username is not None
        assert normal_user.is_active == True
        assert normal_user.is_staff == False
        assert normal_user.is_superuser == False

    def test_create_staff_user(self, staff_user):
        assert staff_user.id is not None
        assert staff_user.uuid is not None
        assert staff_user.email is not None
        assert staff_user.username is not None
        assert staff_user.is_active == True
        assert staff_user.is_staff == True
        assert staff_user.is_superuser == False

    def test_create_superuser_user(self, super_user):
        assert super_user.id is not None
        assert super_user.uuid is not None
        assert super_user.email is not None
        assert super_user.username is not None
        assert super_user.is_active == True
        assert super_user.is_staff == True
        assert super_user.is_superuser == True

    def test_create_not_active_user(self, not_active_user):
        assert not_active_user.id is not None
        assert not_active_user.uuid is not None
        assert not_active_user.email is not None
        assert not_active_user.username is not None
        assert not_active_user.is_active == False
        assert not_active_user.is_staff == False
        assert not_active_user.is_superuser == False

    def test_user_str(self, normal_user):
        assert str(normal_user) == normal_user.email

    def test_update_user(self, normal_user):
        new_email = "test@test.com"
        new_username = "test"
        new_password = "test"

        normal_user.email = new_email
        normal_user.username = new_username
        normal_user.set_password(new_password)
        normal_user.save()

        updated_user = User.objects.get(id=normal_user.id)

        assert updated_user.email == new_email
        assert updated_user.username == new_username

    def test_delete_user(self, normal_user):
        id = normal_user.id
        normal_user.delete()

        with pytest.raises(User.DoesNotExist):
            User.objects.get(id=id)

    def test_normal_user_email_is_normalized(self, normal_user):
        assert normal_user.email == normal_user.email.lower()


@pytest.mark.django_db
class TestProfile:
    pass
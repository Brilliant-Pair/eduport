import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
    def test_create_complete_profile(self, complete_profile):
        assert complete_profile.id is not None
        assert complete_profile.user is not None
        assert complete_profile.first_name is not None
        assert complete_profile.last_name is not None
        assert complete_profile.avatar is not None
        assert complete_profile.caption is not None
        assert complete_profile.phone is not None
        assert complete_profile.gender is not None
        assert complete_profile.full_address is not None
        assert complete_profile.facebook is not None
        assert complete_profile.github is not None
        assert complete_profile.linkedin is not None
        assert complete_profile.twitter is not None
        assert complete_profile.github is not None
        assert complete_profile.website_url is not None
        assert complete_profile.is_public is not None

    def test_create__minimal_profile(self, empty_profile):
        assert empty_profile.id is not None
        assert empty_profile.user is not None

    def test_create_public_profile(self, public_profile):
        assert public_profile.id is not None
        assert public_profile.user is not None
        assert public_profile.is_public is True

    def test_create_private_profile(self, private_profile):
        assert private_profile.id is not None
        assert private_profile.user is not None
        assert private_profile.is_public is False

    def test_create_public_male(self, male_profile):
        assert male_profile.id is not None
        assert male_profile.user is not None
        assert male_profile.gender == "M"

    def test_create_private_female(self, female_profile):
        assert female_profile.id is not None
        assert female_profile.user is not None
        assert female_profile.gender == "F"

    def test_profile_str(self, complete_profile):
        assert str(complete_profile) == f"{complete_profile.user.username}'s Profile"

    def test_get_full_name_with_profile_names(self, complete_profile):
        assert (
            complete_profile.get_full_name()
            == f"{complete_profile.first_name} {complete_profile.last_name}"
        )

    def test_get_full_name_with_username(self, user_with_profile):
        user_with_profile.first_name = None
        user_with_profile.last_name = None
        assert user_with_profile.get_full_name() == f"{user_with_profile.user.username}"

    def test_superuser_profile(self, superuser_with_profile):
        assert superuser_with_profile.user.is_superuser is True
        assert superuser_with_profile.user.is_staff is True

    def test_phone_validation_valid(self, complete_profile):
        valid_phones = ["09919909312", "09171643342", "09933213441"]

        for phone in valid_phones:
            complete_profile.phone = phone
            complete_profile.full_clean()

    def test_phone_validation_invalid(self, complete_profile):
        valid_phones = ["+09919909312", "08171643342", "92933213441"]

        for phone in valid_phones:
            complete_profile.phone = phone
            with pytest.raises(ValidationError) as error:
                complete_profile.full_clean()


@pytest.mark.django_db
class TestInstructor:
    def test_create_instructor(self, instructor):
        assert instructor.id is not None
        assert instructor.status is not None
        assert instructor.birthdate is not None
        assert instructor.experience_year is not None
        assert instructor.job_title is not None
        assert instructor.job_start_date is not None
        assert instructor.job_end_date is not None
        assert instructor.resume is not None

    def test_create_active_instructor(self, active_instructor):
        assert active_instructor.id is not None
        assert active_instructor.status is True

    def test_create_not_active_instructor(self, inactive_instructor):
        assert inactive_instructor.id is not None
        assert inactive_instructor.status is False

    def test_create_instructor_factory(self, current_instructor):
        assert current_instructor.id is not None
        assert current_instructor.job_end_date is None

    def test_instructor_str(self, instructor):
        assert (
            str(instructor)
            == f"Teacher: {instructor.user.username} - {instructor.job_title}"
        )


@pytest.mark.django_db
class TestApplyInstructor:
    def test_create_apply_instructor(self, apply_instructor):
        assert apply_instructor.id is not None
        assert apply_instructor.first_name is not None
        assert apply_instructor.last_name is not None
        assert apply_instructor.phone is not None
        assert apply_instructor.gender is not None
        assert apply_instructor.email is not None
        assert apply_instructor.address is not None
        assert apply_instructor.resume is not None
        assert apply_instructor.status is not None

    def test_create_pending_apply_instructor(self, pending_apply):
        assert pending_apply.id is not None
        assert pending_apply.status == "PENDING"

    def test_create_approved_apply_instructor(self, approved_apply):
        assert approved_apply.id is not None
        assert approved_apply.status == "APPROVED"

    def test_create_rejected_apply_instructor(self, rejected_apply):
        assert rejected_apply.id is not None
        assert rejected_apply.status == "REJECTED"

    def test_str_apply_instructor(self, apply_instructor):
        assert (
            str(apply_instructor)
            == f"{apply_instructor.first_name} {apply_instructor.last_name} - {apply_instructor.status}"
        )

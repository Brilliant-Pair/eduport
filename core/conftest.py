import pytest
from apps.accounts.tests.factories import (
    ApplyInstructorFactory,
    InstructorFactory,
    ProfileFactory,
    UserFactory,
)
from django.contrib.auth import get_user_model
from pytest_factoryboy import register

register(UserFactory)
register(ProfileFactory)
register(InstructorFactory)
register(ApplyInstructorFactory)


@pytest.fixture
def normal_user(user_factory):
    return user_factory(normal=True)


@pytest.fixture
def not_active_user(user_factory):
    return user_factory(not_active=True)


@pytest.fixture
def staff_user(user_factory):
    return user_factory(staff=True)


@pytest.fixture
def super_user(user_factory):
    return user_factory(superuser=True)


@pytest.fixture
def user_manager():
    return get_user_model().objects


# @pytest.fixture
# def complete_profile(profile_factory):
#     return profile_factory()


# @pytest.fixture
# def empty_profile(profile_factory):
#     return profile_factory(minimal=True)


# @pytest.fixture
# def public_profile(profile_factory):
#     return profile_factory(public=True)


# @pytest.fixture
# def private_profile(profile_factory):
#     return profile_factory(private=True)


# @pytest.fixture
# def male_profile(profile_factory):
#     return profile_factory(male=True)


# @pytest.fixture
# def female_profile(profile_factory):
#     return profile_factory(female=True)


# @pytest.fixture
# def user_with_profile(normal_user, profile_factory):
#     return profile_factory(user=normal_user)


# @pytest.fixture
# def superuser_with_profile(super_user, profile_factory):
#     return profile_factory(user=super_user)


# @pytest.fixture
# def instructor(instructor_factory):
#     return instructor_factory()


# @pytest.fixture
# def active_instructor(instructor_factory):
#     return instructor_factory(active=True)


# @pytest.fixture
# def inactive_instructor(instructor_factory):
#     return instructor_factory(not_active=True)


# @pytest.fixture
# def current_instructor(instructor_factory):
#     return instructor_factory(still_working=True)

import pytest
from apps.accounts.tests.factories import (
    ApplyInstructorFactory,
    EducationFactory,
    ExperienceFactory,
    InstructorFactory,
    ProfileFactory,
    SkillFactory,
    UserFactory,
)
from django.contrib.auth import get_user_model
from pytest_factoryboy import register

register(UserFactory)
register(ProfileFactory)
register(InstructorFactory)
register(ApplyInstructorFactory)
register(SkillFactory)
register(EducationFactory)
register(ExperienceFactory)


# ------------------- User -----------------
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


# ------------------- Profile -----------------
@pytest.fixture
def complete_profile(profile_factory):
    return profile_factory()


@pytest.fixture
def empty_profile(profile_factory):
    return profile_factory(minimal=True)


@pytest.fixture
def public_profile(profile_factory):
    return profile_factory(public=True)


@pytest.fixture
def private_profile(profile_factory):
    return profile_factory(private=True)


@pytest.fixture
def male_profile(profile_factory):
    return profile_factory(male=True)


@pytest.fixture
def female_profile(profile_factory):
    return profile_factory(female=True)


@pytest.fixture
def user_with_profile(normal_user, profile_factory):
    return profile_factory(user=normal_user)


@pytest.fixture
def superuser_with_profile(super_user, profile_factory):
    return profile_factory(user=super_user)


# ------------------- Instructor -----------------
@pytest.fixture
def instructor(instructor_factory):
    return instructor_factory()


@pytest.fixture
def active_instructor(instructor_factory):
    return instructor_factory(active=True)


@pytest.fixture
def inactive_instructor(instructor_factory):
    return instructor_factory(not_active=True)


@pytest.fixture
def current_instructor(instructor_factory):
    return instructor_factory(still_working=True)


# ------------------- Apply Instructor -----------------
@pytest.fixture
def apply_instructor(apply_instructor_factory):
    return apply_instructor_factory()


@pytest.fixture
def pending_apply(apply_instructor_factory):
    return apply_instructor_factory(pending=True)


@pytest.fixture
def approved_apply(apply_instructor_factory):
    return apply_instructor_factory(approved=True)


@pytest.fixture
def rejected_apply(apply_instructor_factory):
    return apply_instructor_factory(rejected=True)


# ------------------- Skill -----------------


@pytest.fixture
def basic_skill(skill_factory):
    return skill_factory(basic=True)


@pytest.fixture
def intermediate_skill(skill_factory):
    return skill_factory(intermediate=True)


@pytest.fixture
def advanced_skill(skill_factory):
    return skill_factory(advanced=True)


# ------------------- Education -----------------
@pytest.fixture
def bachelor_education(education_factory):
    return education_factory(bachelor=True)


@pytest.fixture
def master_education(education_factory):
    return education_factory(master=True)


@pytest.fixture
def doctorate_education(education_factory):
    return education_factory(doctorate=True)


@pytest.fixture
def professional_education(education_factory):
    return education_factory(professional=True)


@pytest.fixture
def diploma_education(education_factory):
    return education_factory(diploma=True)


@pytest.fixture
def other_education(education_factory):
    return education_factory(other=True)


@pytest.fixture
def finished_education(education_factory):
    return education_factory()


@pytest.fixture
def ongoing_education(education_factory):
    return education_factory(still_studying=True)


# ------------------- Experience -----------------
@pytest.fixture
def intern_experience(experience_factory):
    return experience_factory(intern=True)


@pytest.fixture
def junior_experience(experience_factory):
    return experience_factory(junior=True)


@pytest.fixture
def mid_experience(experience_factory):
    return experience_factory(mid=True)


@pytest.fixture
def senior_experience(experience_factory):
    return experience_factory(senior=True)


@pytest.fixture
def finished_experience(experience_factory):
    return experience_factory()


@pytest.fixture
def ongoing_experience(experience_factory):
    return experience_factory(still_working=True)

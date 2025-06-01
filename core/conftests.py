from apps.accounts.tests.factories import ProfileFactory, UserFactory
from pytest_factoryboy import register

register(UserFactory)
register(ProfileFactory)


@pytest.fixture
def normal_user(user_factory):
    return user_factory()


@pytest.fixture
def super_user(user_factory):
    return user_factory(is_staff=True, is_superuser=True)


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

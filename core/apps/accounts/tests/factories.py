from datetime import date, timedelta

import factory
import factory.fuzzy
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from faker import Factory as FakerFactory

from ..models import (
    ApplyInstructor,
    Education,
    Experience,
    Instructor,
    Profile,
    Skill,
)

faker = FakerFactory.create()
farsi_faker = FakerFactory.create("fa_IR")

User = get_user_model()


def fake_farsi_phone_number():
    return f"09{str(faker.random_number(digits=9, fix_len=True))}"


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: faker.name())
    email = factory.LazyAttribute(lambda x: faker.email())

    class Params:
        normal = factory.Trait(is_active=True, is_staff=False, is_superuser=False)
        not_active = factory.Trait(is_active=False, is_staff=False, is_superuser=False)
        staff = factory.Trait(is_active=True, is_staff=True, is_superuser=False)
        superuser = factory.Trait(is_active=True, is_staff=True, is_superuser=True)

    # @classmethod``
    # def _create(cls, model_class, *args, **kwargs):
    #     manager = cls._get_manager(model_class)

    #     if "is_superuser" in kwargs:
    #         return manager.create_superuser(password=faker.password(),**kwargs)
    #     else:
    #         return manager.create_user(**kwargs)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    first_name = factory.LazyAttribute(lambda x: farsi_faker.first_name())
    last_name = factory.LazyAttribute(lambda x: farsi_faker.last_name())
    avatar = factory.django.ImageField(color=faker.color())
    caption = factory.LazyAttribute(lambda x: farsi_faker.sentence())
    phone = factory.LazyAttribute(lambda x: fake_farsi_phone_number())
    gender = factory.Iterator([Profile.Gender.MALE, Profile.Gender.FEMALE])
    full_address = factory.LazyAttribute(lambda x: farsi_faker.address())
    facebook = factory.LazyAttribute(
        lambda x: f"https://facebook.com/{faker.user_name()}"
    )
    github = factory.LazyAttribute(lambda x: f"https://github.com/{faker.user_name()}")
    linkedin = factory.LazyAttribute(
        lambda x: f"https://linkedin.com/in/{faker.user_name()}"
    )
    twitter = factory.LazyAttribute(
        lambda x: f"https://twitter.com/{faker.user_name()}"
    )
    website_url = factory.LazyAttribute(lambda x: faker.url())
    is_public = factory.Iterator([True, False])

    class Params:
        minimal = factory.Trait(
            first_name=None,
            last_name=None,
            caption=None,
            avatar=None,
            phone=None,
            gender=None,
            full_address=None,
            facebook=None,
            github=None,
            twitter=None,
            website_url=None,
        )
        public = factory.Trait(is_public=True)
        private = factory.Trait(is_public=False)
        male = factory.Trait(gender=Profile.Gender.MALE)
        female = factory.Trait(gender=Profile.Gender.FEMALE)


class InstructorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instructor

    user = factory.SubFactory(UserFactory)
    status = factory.Iterator([True, False])
    birthdate = factory.fuzzy.FuzzyDate(
        start_date=date(1960, 1, 1), end_date=date(2000, 1, 1)
    )
    experience_year = factory.fuzzy.FuzzyInteger(low=0, high=30)
    job_title = factory.LazyAttribute(lambda x: faker.job())
    job_start_date = factory.fuzzy.FuzzyDate(
        start_date=date(2010, 1, 1), end_date=date.today() - timedelta(days=365)
    )
    job_end_date = factory.LazyAttribute(
        lambda o: faker.date_between_dates(
            date_start=o.job_start_date, date_end=date.today()
        )
    )
    resume = factory.django.FileField(filename="resume.pdf")

    class Params:
        active = factory.Trait(status=True)
        not_active = factory.Trait(status=False)
        still_working = factory.Trait(job_end_date=None)


class ApplyInstructorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ApplyInstructor

    first_name = factory.LazyAttribute(lambda x: farsi_faker.first_name())
    last_name = factory.LazyAttribute(lambda x: farsi_faker.last_name())
    phone = factory.LazyAttribute(lambda x: fake_farsi_phone_number())
    gender = factory.Iterator(
        [ApplyInstructor.Gender.MALE, ApplyInstructor.Gender.FEMALE]
    )
    email = factory.LazyAttribute(lambda x: faker.email())
    address = factory.LazyAttribute(lambda x: faker.address())
    resume = factory.django.FileField(filename="resume.pdf")
    status = factory.Iterator([status[0] for status in ApplyInstructor.STATUS.choices])

    class Params:
        pending = factory.Trait(status=ApplyInstructor.STATUS.PENDING)
        approved = factory.Trait(status=ApplyInstructor.STATUS.APPROVED)
        rejected = factory.Trait(status=ApplyInstructor.STATUS.REJECTED)


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill

    instructor = factory.SubFactory(InstructorFactory)
    name = factory.LazyAttribute(lambda x: faker.job())
    level = factory.Iterator([level[0] for level in Skill.Level.choices])


    class Params:
        basic = factory.Trait(level=Skill.Level.BASIC)
        intermediate = factory.Trait(level=Skill.Level.INTERMEDIATE)
        advanced = factory.Trait(level=Skill.Level.ADVANCED)



class EducationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Education

    instructor = factory.SubFactory(InstructorFactory)
    major = factory.LazyAttribute(lambda x: faker.job())
    degree = factory.Iterator([degree[0] for degree in Education.Degree.choices])
    institution = factory.LazyAttribute(
        lambda x: f"University of {faker.company()}"
    )
    start = factory.fuzzy.FuzzyDate(
        start_date=date(2010, 1, 1), end_date=date.today() - timedelta(days=365)
    )
    end = factory.LazyAttribute(
        lambda o: faker.date_between_dates(date_start=o.start, date_end=date.today())
    )

    class Params:
        still_studying = factory.Trait(end=None)
        bachelor = factory.Trait(degree=Education.Degree.BACHELOR)
        master = factory.Trait(degree=Education.Degree.MASTER)
        doctorate = factory.Trait(degree=Education.Degree.DOCTORATE)
        professional = factory.Trait(degree=Education.Degree.PROFESSIONAL)
        diploma = factory.Trait(degree=Education.Degree.DIPLOMA)
        other = factory.Trait(degree=Education.Degree.OTHER)


class ExperienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Experience

    instructor = factory.SubFactory(InstructorFactory)
    job_title = factory.LazyAttribute(lambda x: faker.job())
    company = factory.LazyAttribute(lambda x: faker.last_name())
    level = factory.Iterator([level[0] for level in Experience.Level.choices])
    start = factory.fuzzy.FuzzyDate(
        start_date=date(2010, 1, 1), end_date=date.today() - timedelta(days=365)
    )
    end = factory.LazyAttribute(
        lambda o: faker.date_between_dates(date_start=o.start, date_end=date.today())
    )

    class Params:
        still_working = factory.Trait(end=None)
        intern = factory.Trait(level=Experience.Level.INTERN)
        junior = factory.Trait(level=Experience.Level.JUNIOR)
        mid = factory.Trait(level=Experience.Level.MID)
        senior = factory.Trait(level=Experience.Level.SENIOR)

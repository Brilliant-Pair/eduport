from datetime import date, timedelta

import factory
from django.contrib.auth import get_user_model
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


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: faker.username())
    email = factory.LazyAttribute(lambda x: faker.email())
    is_active = True
    is_staff = False
    is_superuser = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        if "is_superuser" in kwargs:
            return manager.create_superuser(**kwargs)
        else:
            return manager.create_user(**kwargs)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    first_name = factory.LazyAttribute(lambda x: farsi_faker.first_name())
    last_name = factory.LazyAttribute(lambda x: farsi_faker.last_name())
    avatar = factory.django.ImageField(color=faker.color())
    caption = factory.LazyAttribute(lambda x: farsi_faker.sentence())
    phone = factory.LazyAttribute(lambda x: farsi_faker.phone())
    gender = factory.Iterator([Profile.GENDER.MALE, Profile.GENDER.FEMALE])
    full_address = factory.LazyAttribute(farsi_faker.address())
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
        male = factory.Trait(gender=Profile.gender.MALE)
        female = factory.Trait(gender=Profile.gender.FEMALE)


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


class InstructorApplyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ApplyInstructor

    first_name = factory.LazyAttribute(lambda x: farsi_faker.first_name())
    last_name = factory.LazyAttribute(lambda x: farsi_faker.last_name())
    phone = factory.LazyAttribute(lambda x: farsi_faker.phone())
    gender = factory.Iterator(
        [ApplyInstructor.Gender.MALE, ApplyInstructor.Gender.FEMALE]
    )
    email = factory.LazyAttribute(lambda x: faker.email())
    address = factory.LazyAttribute(lambda x: faker.address())
    resume = factory.django.FileField(filename="resume.pdf")
    status = factory.Iterator([status[0] for status in ApplyInstructor.STATUS.choices])


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill

    instructor = factory.SubFactory(InstructorFactory)
    name = factory.LazyAttribute(lambda x: faker.skill())
    level = factory.Iterator([level[0] for level in Skill.Level.choices])


class EducationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Education

    instructor = factory.SubFactory(InstructorFactory)
    major = factory.LazyAttribute(lambda x: faker.major())
    degree = factory.Iterator([degree[0] for degree in Education.Degree.choices])
    institution = factory.LazyAttribute(
        lambda x: f"University of {faker.school_name()}"
    )
    start = factory.fuzzy.FuzzyDate(
        start_date=date(2010, 1, 1), end_date=date.today() - timedelta(days=365)
    )
    end = factory.LazyAttribute(
        lambda o: faker.date_between_dates(date_start=o.start, end=date.today())
    )

    class Params:
        still_studying = factory.Trait(end=None)


class ExperienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Experience

    instructor = factory.SubFactory(InstructorFactory)
    job_title = factory.LazyAttribute(lambda x: faker.job())
    company = factory.LazyAttribute(lambda x: faker.last_name())
    level = factory.Iterator([level[0] for level in Experience.Level.choices])
    start = factory.fuzzy.FuzzyDate(
        start_date=date(2010, 1, 1), end_date=date.today - timedelta(days=365)
    )
    end = factory.LazyAttribute(
        lambda o: faker.date_between_dates(date_start=o.start, end=date.today())
    )

    class Params:
        still_working = factory.Trait(end=None)

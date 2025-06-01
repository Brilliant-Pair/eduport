import factory
from django.contrib.auth import get_user_model
from faker import Factory as FakerFactory

from ..models import Profile

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

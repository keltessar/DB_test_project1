from faker import Faker
from .dataclasses import User

fake = Faker()

class UserGenerator:

    @staticmethod
    def create() -> User:
        return User (
            name=fake.first_name(),
            surname=fake.last_name(),
            country=fake.country()
        )
import pytest

from sqlalchemy import select, update
from .base_database import BaseDBManager
from .models import User
from bd_temp.bd_config import TestConfig


test_config = TestConfig()


@pytest.fixture(scope="session")
def db_manager():
    """Manager for the whole test session run"""
    manager = BaseDBManager(test_config.connection_string)

    yield manager

    manager.dispose()


@pytest.fixture(scope="function")
def db_session(db_manager):
    """Isolated session for each test"""
    with db_manager.get_session() as session:
        yield session


@pytest.fixture
def db_utils(db_session):
    """Utilities for managing database"""

    class DBUtils:
        def __init__(self, session):
            self.session = session

        def create_user(self, **kwargs):
            user = User(**kwargs)
            self.session.add(user)
            self.session.commit()
            return user

        def get_user(self, user_id):
            return self.session.query(User).get(user_id)

        def get_all_users(self):
            statement = select(User)
            result = self.session.execute(statement)
            return result.scalars().all()

        def update_user_country(self, user_id, new_country):
            """
            Update user's country who has param ID to new data from param Country
            :param user_id:
            :param new_country:
            :return:
            """
            user = self.get_user(user_id)
            if user:
                user.country = new_country
                self.session.commit()
                return user
            return False


        def find_users_by_name(self, name):
            return self.session.query(User).filter(
                User.Name.like(f"%{name}%")
            ).all()

        def delete_user(self, user_id):
            try:
                user = self.session.query(User).get(user_id)
                if user:
                    self.session.delete(user)
                    self.session.commit()
                return user
            except:
                raise Exception("There is no User with this Id in the Database!")

    return DBUtils(db_session)
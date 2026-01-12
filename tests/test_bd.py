import random
from tools.generators.user_data_generator import UserGenerator

class TestUserOperations:
    def test_create_user(self, db_utils, db_session):
        generated_user = UserGenerator.create()
        user = db_utils.create_user(
            name=generated_user.name,
            surname=generated_user.surname,
            country=generated_user.country
        )

        assert user.id is not None
        found_user = db_utils.get_user(user.id)
        print (f"User {found_user.name} {found_user.surname} from {found_user.country} has been created! It's Id is - {found_user.id}")
        assert found_user.country  == generated_user.country

    def test_delete_random_user(self, db_utils, db_session):
        users = db_utils.get_all_users()
        if users:
            deleted_user = random.choice(users)
            db_utils.delete_user(deleted_user.id)
            print (f"User {deleted_user.name} {deleted_user.surname} from {deleted_user.country} has been deleted! It's Id was - {deleted_user.id}")
            assert db_utils.get_user(deleted_user.id) is None
        else:
            raise Exception("There is no User with this Id in the Database!")



    def test_print_all_users(self,db_utils, db_session):
        users = db_utils.get_all_users()
        for user in users:
            print (user.id, user.name, user.surname, user.country)

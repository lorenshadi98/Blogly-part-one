from logging import lastResort
from unittest import TestCase

from app import app
from models import db, User
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for users"""

    def setUp(self):
        """Cleanup any existing users"""
        User.query.delete()

    def tearDown(self):
        """Cleanup any fouled transactions"""
        db.session.rollback()

    def test_create_new_user(self):
        """Test new user creation"""
        new_user = User(first_name="lorens", last_name="hadi",
                        user_image="https://i.pravatar.cc/100")
        db.session.add(new_user)
        db.session.commit()

        found_user = User.query.filter(User.id == new_user.id).first()

        self.assertEqual(found_user.first_name, "lorens")
        self.assertEqual(found_user.last_name, "hadi")
        self.assertEqual(found_user.user_image, "https://i.pravatar.cc/100")

    def test_edit_user(self):
        """Tests editing of user details with the same id."""
        new_user = User(first_name="steve", last_name="smith",
                        user_image="https://i.pravatar.cc/100")
        db.session.add(new_user)
        db.session.commit()

        found_user = User.query.filter(User.id == new_user.id).first()
        found_user.first_name = "billy"
        found_user.last_name = "bob"
        found_user.user_image = "https://i.pravatar.cc/100"

        self.assertEqual(found_user.first_name, "billy")
        self.assertEqual(found_user.last_name, "bob")
        self.assertEqual(found_user.user_image, "https://i.pravatar.cc/100")

    def test_delete_user(self):
        """Tests user deletion"""

        # Creates new user and adds it to database
        new_user = User(first_name="hilly", last_name="stevie",
                        user_image="https://i.pravatar.cc/100")
        db.session.add(new_user)
        db.session.commit()

        # deletes user created above
        User.query.filter(User.id == new_user.id).delete()
        db.session.commit()

        # attemps to search for the user we deleted. Should retrun none, since
        # it no longer exists
        search_result = User.query.filter(User.id == new_user.id).first()
        self.assertEqual(search_result, None)

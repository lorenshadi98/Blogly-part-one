from logging import lastResort
from unittest import TestCase

from app import app
from models import db, User
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for users application"""

    def setUp(self):
        """Add a sample user"""
        User.query.delete()
        new_user = User(first_name="lorens", last_name="hadi",
                        user_image="https://i.pravatar.cc/100")
        db.session.add(new_user)
        db.session.commit()
        self.user_id = User.id

    def tearDown(self):
        """Cleanup any fouled transactions"""
        db.session.rollback()

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("lorens", html)

    def test_user_details_page(self):
        with app.test_client() as client:
            test_user = User(first_name="stevie", last_name="billy",
                             user_image="https://i.pravatar.cc/100")
            db.session.add(test_user)
            db.session.commit()
            found_user = User.query.filter(User.id == test_user.id).first()
            resp = client.get(f"/users/{found_user.id}/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(test_user.first_name, html)

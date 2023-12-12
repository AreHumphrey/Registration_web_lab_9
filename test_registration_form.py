import unittest
from app import app, db
from models import Users, UserDetails


class RegistrationFormTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_registration_form_submission(self):

        data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'city': 'Москва',
            'birthday': '1990-01-01',
            'email': 'ivanov.ii@test.com',
            'phone_number': '1234567890'
        }

        response = self.app.post('/submit_registration', data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, '/submit_registration')

        user = Users.query.filter_by(email=data['email']).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, data['first_name'])

        user_details = UserDetails.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(user_details)
        self.assertEqual(user_details.city, data['city'])


if __name__ == '__main__':
    unittest.main()

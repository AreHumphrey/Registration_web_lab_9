import unittest
from app import app, db
from models import Users, User_details

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

    def test_registration_form_submission_true(self):
        data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'city': 'Москва',
            'birthday': '1990-01-01',
            'email': 'ivanov.ii@test.com',
            'phone_number': '9146668608'
        }

        response = self.app.post('/submit_registration', data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, '/submit_registration')

        user = Users.query.filter_by(email=data['email']).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, data['first_name'])

        users_details = User_details.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(users_details)
        self.assertEqual(users_details.city, data['city'])

    def test_invalid_email_submission(self):
        data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'city': 'Москва',
            'birthday': '1990-01-01',
            'email': 'invalid_email',
            'phone_number': '1234567890'
        }

        response = self.app.post('/submit_registration', data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.path, '/submit_registration')

        user = Users.query.filter_by(email=data['email']).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, data['first_name'])

        users_details = User_details.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(users_details)
        self.assertEqual(users_details.city, data['city'])

    def test_invalid_phone_submission(self):
        data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'city': 'Москва',
            'birthday': '1990-01-01',
            'email': 'ivanov.iii@test.com',
            'phone_number': '123'
        }

        response = self.app.post('/submit_registration', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_missing_required_fields_submission(self):
        data = {
            'first_name': 'Alice',
            'last_name': 'Smith'
        }

        response = self.app.post('/submit_registration', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_birthday_submission(self):
        user = Users(first_name='Jane', last_name='Doe', email='jane.doe@test.com', phone_number='9876543210')
        db.session.add(user)
        db.session.commit()

        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jane.doe@test.com',
            'phone_number': '1234567890'
        }

        response = self.app.post('/submit_registration', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

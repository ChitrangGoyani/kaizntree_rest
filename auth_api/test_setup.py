from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):
    # load these variables everytime we run any testcase
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.forgot_pass_url=reverse('forgotpass')
        self.logout_url=reverse('logout')
        self.user_data= {
            'username':'johnDoe',
            'email':'johndoe@email.com',
            'password':'supersecretpassword'
        }

        self.user_login_data= {
            'username':'johnDoe',
            'password':'supersecretpassword'
        }

        self.incorrect_login_data = {
            'username':'NotjohnDoe',
            'password':'Notsupersecretpassword'
        }

        self.forgot_pass_incorrect_data = {
            'email':'notjohndoe@email.com'
        }

        self.forgot_pass_correct_data = {
            'email':'johndoe@email.com'
        }
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
   

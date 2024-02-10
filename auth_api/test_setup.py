from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):
    # load these variables everytime we run any testcase
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.user_data= {
            'username':'johnDoe',
            'email':'johndoe@email.com',
            'password':'supersecretpassword'
        }

        self.user_login_data= {
            'username':'johnDoe',
            'password':'supersecretpassword'
        }
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
   

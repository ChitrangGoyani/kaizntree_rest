from .test_setup import TestSetup

class TestViews(TestSetup):
    def test_register_empty_data(self):
        res=self.client.post(self.register_url)
        self.assertEqual(res.status_code, 500)

    def test_register_correct_data(self):
        res=self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(res.data['user']['email'], self.user_data['email'])
        self.assertEqual(res.data['user']['username'], self.user_data['username'])
        self.assertEqual(res.status_code, 200)

    def test_login_empty_data(self):
        res=self.client.post(self.login_url)
        self.assertEqual(res.status_code, 500)

    def test_login_incorrect_data(self):
        res=self.client.post(self.login_url, self.incorrect_login_data, format='json')
        self.assertEqual(res.status_code, 404)

    def test_login_correct_data(self):
        self.client.post(self.register_url, self.user_data, format='json')
        res=self.client.post(self.login_url, self.user_login_data, format='json')
        self.assertEqual(res.status_code, 200)
    
    def test_logout(self):
        self.client.post(self.register_url, self.user_data, format='json')
        self.client.post(self.login_url, self.user_login_data, format='json')
        res=self.client.get(self.logout_url)
        self.assertEqual(res.status_code, 200)

    def test_forgot_password_incorrect_data(self):
        self.client.post(self.register_url, self.user_data, format='json')
        res=self.client.post(self.login_url, self.user_login_data, format='json')
        res=self.client.post(self.forgot_pass_url, self.forgot_pass_incorrect_data, format='json')
        self.assertEqual(res.status_code, 404)

    def forgot_password_correct_data(self):
        self.client.post(self.register_url, self.user_data, format='json')
        res=self.client.post(self.login_url, self.user_login_data, format='json')
        res=self.client.post(self.forgot_pass_url, self.forgot_pass_correct_data, format='json')
        self.assertEqual(res.status_code, 200)

    
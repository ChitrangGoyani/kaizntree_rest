from .test_setup import TestSetup

class TestViews(TestSetup):
    def test_register_fail(self):
        res=self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_register_pass(self):
        res=self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(res.data['user']['email'], self.user_data['email'])
        self.assertEqual(res.status_code, 201)

    def test_login_fail(self):
        res=self.client.post(self.login_url)
        self.assertEqual(res.status_code, 404)

    def test_login_pass(self):
        self.client.post(self.register_url, self.user_data, format='json')
        res=self.client.post(self.login_url, self.user_login_data, format='json')
        self.assertEqual(res.status_code, 200)
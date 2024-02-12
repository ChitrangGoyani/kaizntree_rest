from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetupItem(APITestCase):
    # load these variables everytime we run any testcase
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.forgot_pass_url=reverse('forgotpass')
        self.logout_url=reverse('logout')
        self.add_item_url=reverse('add_item')
        self.delete_item_url=reverse('delete_item')
        self.get_item_url=reverse('get_item')
        self.get_items_url=reverse('get_all')
        self.filter_items_url=reverse('filters')
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

        self.item_correct_data = {
            "name": "ProductOne",
            "sku": "PRONE",
            "tag": "ETSY",
            "category": "Raw Material",
            "in_stock": 2147,
            "stock_status": True,
            "available_stock": 2550
        }

        self.add_multiple_items = [
            {
                "name": "ProductOne",
                "sku": "PRONE",
                "tag": "ETSY",
                "category": "RawMaterial",
                "in_stock": 2147,
                "stock_status": True,
                "available_stock": 2550
            },
            {
                "name": "ProductTwo",
                "sku": "PRTWO",
                "tag": "SHOPIFY",
                "category": "Finished",
                "in_stock": 20,
                "stock_status": True,
                "available_stock": 40
            },
            {
                "name": "ProductThree",
                "sku": "PRTHREE",
                "tag": "AMZ",
                "category": "Finished",
                "in_stock": 20,
                "stock_status": True,
                "available_stock": 40
            },
        ]

        self.incorrect_stock = {
            "name": "ProductThree",
            "sku": "PRTHREE",
            "tag": "AMZ",
            "category": "Finished",
            "in_stock": 40,
            "stock_status": False,
            "available_stock": 20
        }

        self.correct_sku_length = {
            "name": "ProductThree",
            "sku": "PRTHREE",
            "tag": "AMZ",
            "category": "Finished",
            "in_stock": 40,
            "stock_status": False,
            "available_stock": 20
        }

        self.incorrect_lengths = {
            "name": "ProductThree",
            "sku": "PRTHREEYYYYYYYYYYYYYYYYYYYYYYYYYY",
            "tag": "AMZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ",
            "category": "Finisheddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
            "in_stock": 20,
            "stock_status": True,
            "available_stock": 40
        }

        self.filter_query_1 = "category=RawMaterial&tag=ETSY"
        self.filter_query_2 = "available_stock__gt=20"
        self.filter_query_3 = "instock__lte=20"
        self.filter_query_4 = "createdAt_before=2025-02-12T12:30:08.850Z&createdAt_after=2022-02-12T12:30:08.850Z"
        self.search_query_1 = "search=ProductOne"
        self.search_query_2 = "search=PRTHREE"

        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
   

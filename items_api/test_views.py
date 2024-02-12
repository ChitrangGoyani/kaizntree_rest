from .test_setup import TestSetupItem

class TestViewsItem(TestSetupItem):
    # User journey1: register -> login -> addItem -> getItem -> updateItem -> deleteItem -> logout
    def test_journey1(self):
        self.client.post(self.register_url, self.user_data, format='json')
        self.client.post(self.login_url, self.user_login_data, format='json')
        res=self.client.post(self.add_item_url, self.item_correct_data, format='json')
        self.assertEqual(res.status_code, 200) # successful add operation
        id = res.data['id']
        query = f'id={id}'
        res=self.client.get(self.get_item_url, QUERY_STRING=query, format='json')
        self.assertEqual(res.status_code, 200) # successful get single item
        self.client.delete(self.delete_item_url, QUERY_STRING=query, format='json')
        self.assertEqual(res.status_code, 200) # successful delete operation
        res=self.client.get(self.logout_url)
        self.assertEqual(res.status_code, 200) # successful logout
    
    # User journey2: register -> login -> addItems -> getItems -> logout
    def test_journey2(self):
        self.client.post(self.register_url, self.user_data, format='json')
        self.client.post(self.login_url, self.user_login_data, format='json')
        for item in self.add_multiple_items:
            res=self.client.post(self.add_item_url, item, format='json')
            self.assertEqual(res.status_code, 200) # successful add operations
        res=self.client.get(self.get_items_url)
        self.assertEqual(res.status_code, 200) # successful get all items
        res=self.client.get(self.logout_url)
        self.assertEqual(res.status_code, 200) # successful logout

    # User journey3: register -> login -> addItems -> filterItems -> searchItems -> logout
    def test_journey3(self):
        self.client.post(self.register_url, self.user_data, format='json')
        self.client.post(self.login_url, self.user_login_data, format='json')
        for item in self.add_multiple_items:
            res=self.client.post(self.add_item_url, item, format='json')
            self.assertEqual(res.status_code, 200) # successful add operations
        # filter queries
        res=self.client.get(self.filter_items_url, QUERY_STRING=self.filter_query_1, format='json')
        self.assertEqual(res.status_code, 200)
        res=self.client.get(self.filter_items_url, QUERY_STRING=self.filter_query_2, format='json')
        self.assertEqual(res.status_code, 200)
        res=self.client.get(self.filter_items_url, QUERY_STRING=self.filter_query_3, format='json')
        self.assertEqual(res.status_code, 200)
        res=self.client.get(self.filter_items_url, QUERY_STRING=self.filter_query_4, format='json')
        self.assertEqual(res.status_code, 200)
        # search queries
        res=self.client.get(self.filter_items_url, QUERY_STRING=self.search_query_1, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data[0]['name'], "ProductOne")
        res=self.client.get(self.filter_items_url, QUERY_STRING=self.search_query_2, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data[0]['sku'], "PRTHREE")
        res=self.client.get(self.logout_url)
        self.assertEqual(res.status_code, 200) # successful logout

    # Available stock < in stock
    def test_stock(self):
        self.client.post(self.register_url, self.user_data, format='json')
        self.client.post(self.login_url, self.user_login_data, format='json')
        res=self.client.post(self.add_item_url, self.incorrect_stock, format='json')
        self.assertEqual(res.status_code, 500)
    
    def test_lengths(self):
        self.client.post(self.register_url, self.user_data, format='json')
        self.client.post(self.login_url, self.user_login_data, format='json')
        res=self.client.post(self.add_item_url, self.incorrect_lengths, format='json')
        self.assertEqual(res.status_code, 500)
        

    
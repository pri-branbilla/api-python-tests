from app.models.item import ItemModel
from app.models.store import StoreModel
from app.models.user import UserModel
from app.tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '123').save_to_db()
                auth_response = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '123'
                }),
                                           headers={
                                               'Content-Type': 'application/json'
                                           })
                auth_token = json.loads(auth_response.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                header = {'Authorization': self.access_token}
                resp = client.get('/item/test', headers=header)
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 1.99, 1).save_to_db()
                header = {'Authorization': self.access_token}
                resp = client.get('/item/test', headers=header)
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({
                        'name': 'test',
                        'price': 1.99,
                }, json.loads(resp.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 1.99, 1).save_to_db()
                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', data={'price': 1.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({
                    'name': 'test',
                    'price': 1.99,
                }, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test', data={'price': 1.99, 'store_id': 1})
                resp = client.post('/item/test', data={'price': 1.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', data={'price': 1.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 1.99)
                self.assertDictEqual({
                    'name': 'test',
                    'price': 1.99,
                }, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1.99, 1).save_to_db()
                self.assertEqual(ItemModel.find_by_name('test').price, 1.99)
                resp = client.put('/item/test', data={'price': 2.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 2.99)
                self.assertDictEqual({
                    'name': 'test',
                    'price': 2.99,
                }, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1.99, 1).save_to_db()
                resp = client.get('/items')
                self.assertDictEqual({'items': [{'name': 'test', 'price': 1.99}]}, json.loads(resp.data))

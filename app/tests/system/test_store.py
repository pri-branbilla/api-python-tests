from app.models.store import StoreModel
from app.tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({
                    'name': 'test',
                    'items': []
                }, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'test' already exists."}, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.delete('/store/test')
                self.assertEqual(response.status_code, 204)

    def test_find_store(self):
        pass

    def test_store_not_found(self):
        pass

    def test_store_found_with_items(self):
        pass

    def test_store_list(self):
        pass

    def test_store_list_with_items(self):
        pass

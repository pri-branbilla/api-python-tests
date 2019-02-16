from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTestIntegration(BaseTest):
    def test_crud(self):
        with self.app_context():
            item = ItemModel('test', 19.99, 1)
            self.assertIsNone(ItemModel.find_by_name('test'), "Expected to be empty")
            item.save_to_db()
            self.assertIsNotNone(ItemModel.find_by_name('test'))
            item.delete_from_db()
            self.assertIsNone(ItemModel.find_by_name('test'), "Expected to be empty")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test', 19.99, 1)
            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'test_store')

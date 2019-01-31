from app.models.item import ItemModel
from app.tests.base_test import BaseTest


class ItemTestIntegration(BaseTest):
    def test_crud(self):
        with self.app_context():
            item = ItemModel('test', 19.99)
            self.assertIsNone(ItemModel.find_by_name('test'), "Expected to be empty")
            item.save_to_db()
            self.assertIsNotNone(ItemModel.find_by_name('test'))
            item.delete_from_db()
            self.assertIsNone(ItemModel.find_by_name('test'), "Expected to be empty")

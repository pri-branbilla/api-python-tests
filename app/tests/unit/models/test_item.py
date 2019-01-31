from unittest import TestCase
from app.models.item import ItemModel


class ItemModelTest(TestCase):
    def test_create_item(self):
        item = ItemModel('test', 19.99, 1)

        self.assertEqual(item.name, 'test', "Incorrect name")
        self.assertEqual(item.price, 19.99, "Incorrect price")
        self.assertEqual(item.store_id, 1, "Incorrect store")

    def test_json(self):
        item = ItemModel('test', 19.99, 1)
        expected = {'name': 'test', 'price': 19.99, 'store_id': 1}

        self.assertEqual(item.json(), expected, "Expected {}, but received {}".format(expected, item.json()))

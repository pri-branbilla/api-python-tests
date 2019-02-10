from app.models.item import ItemModel
from app.tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_create_item(self):
        item = ItemModel('test', 19.99, 1)

        self.assertEqual(item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")  # noqa: E501
        self.assertEqual(item.price, 19.99,
                         "The price of the item after creation does not equal the constructor argument.")  # noqa: E501
        self.assertEqual(item.store_id, 1,
                         "The store_id of the item after creation does not equal the constructor argument.")  # noqa: E501
        self.assertIsNone(item.store, "The item's store was not None even though the store was not created.")  # noqa: E501

    def test_item_json(self):
        item = ItemModel('test', 19.99, 1)
        expected = {
            'name': 'test',
            'price': 19.99
        }

        self.assertEqual(
            item.json(),
            expected,
            "The JSON export of the item is incorrect. Received {}, expected {}.".format(item.json(), expected))  # noqa: E501

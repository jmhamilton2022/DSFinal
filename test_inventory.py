import unittest
from inventory import Product, add_product, remove_product, update_quantity, stock_room, product_lookup, queue


class TestInventoryManagement(unittest.TestCase):

    def setUp(self):
        self.product = Product("001", "TestProduct", 20)
        add_product(self.product)

    def test_add_product(self):
        self.assertIn(self.product, stock_room)
        self.assertEqual(product_lookup["001"], self.product)

    def test_remove_product(self):
        remove_product("001")
        self.assertNotIn("001", product_lookup)
        self.assertNotIn(self.product, stock_room)

    def test_update_quantity(self):
        update_quantity("001", 5)
        self.assertEqual(self.product.quantity, 25)

        update_quantity("001", -10)
        self.assertEqual(self.product.quantity, 15)

    def test_low_stock_alert(self):
        update_quantity("001", -15)
        self.assertIn(self.product, queue)

        update_quantity("001", 20)
        self.assertNotIn(self.product, queue)

    def tearDown(self):
        stock_room.clear()
        product_lookup.clear()
        queue.clear()


if __name__ == '__main__':
    unittest.main()

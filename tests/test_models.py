    def test_update_a_product(self):
        """It should Update a product's details"""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)
        
        # Update the product
        product.name = "Updated Product"
        product.price = Decimal("19.99")
        product.update()
        
        updated_product = Product.find(product.id)
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.price, Decimal("19.99"))

    def test_delete_a_product(self):
        """It should Delete a product from the database"""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)

        # Delete the product
        product_id = product.id
        product.delete()
        
        deleted_product = Product.find(product_id)
        self.assertIsNone(deleted_product)

    def test_find_product_by_id(self):
        """It should Find a product by its ID"""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)

        found_product = Product.find(product.id)
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)

    def test_find_product_by_name(self):
        """It should Find products by their name"""
        Product(name="Widget", description="A useful widget", price=5.99, available=True, category=Category.TOOLS).create()
        Product(name="Widget", description="Another widget", price=7.99, available=True, category=Category.TOOLS).create()
        
        found_products = Product.find_by_name("Widget")
        self.assertEqual(len(found_products), 2)
        self.assertEqual(found_products[0].name, "Widget")
        self.assertEqual(found_products[1].name, "Widget")

    def test_find_product_by_category(self):
        """It should Find products by their category"""
        Product(name="Shirt", description="A stylish shirt", price=15.00, available=True, category=Category.CLOTHS).create()
        Product(name="Hammer", description="A heavy hammer", price=25.00, available=True, category=Category.TOOLS).create()

        cloth_products = Product.find_by_category(Category.CLOTHS)
        self.assertEqual(len(cloth_products), 1)
        self.assertEqual(cloth_products[0].name, "Shirt")

        tool_products = Product.find_by_category(Category.TOOLS)
        self.assertEqual(len(tool_products), 1)
        self.assertEqual(tool_products[0].name, "Hammer")

    def test_serialize_a_product(self):
        """It should serialize a Product into a dictionary"""
        product = ProductFactory()
        serial_product = product.serialize()
        self.assertEqual(serial_product["name"], product.name)
        self.assertEqual(serial_product["description"], product.description)
        self.assertEqual(Decimal(serial_product["price"]), product.price)
        self.assertEqual(serial_product["available"], product.available)
        self.assertEqual(serial_product["category"], product.category.name)

    def test_deserialize_a_product(self):
        """It should deserialize a Product from a dictionary"""
        data = {
            "name": "Gadget",
            "description": "A tech gadget",
            "price": "49.99",
            "available": True,
            "category": "ELECTRONICS"
        }
        product = Product()
        product.deserialize(data)
        self.assertEqual(product.name, "Gadget")
        self.assertEqual(product.description, "A tech gadget")
        self.assertEqual(product.price, Decimal("49.99"))
        self.assertEqual(product.available, True)
        self.assertEqual(product.category, Category.ELECTRONICS)

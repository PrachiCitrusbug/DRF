from django.test import TestCase

class TestExampleClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print(
            "\n\nsetUpTestData: Run once to set up non-modified data for all class methods.\n\n"
        )
        return super().setUpTestData()

    def setUp(self):
        print(
            "setUp: Run once for every test method to set up clean data. Every test function will get a fresh version of these objects."
        )
        return super().setUp()

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

    def tearDown(self):
        print(
            "tearDown: Hook method for deconstructing the test fixture after testing it.\n"
        )
        return super().tearDown()
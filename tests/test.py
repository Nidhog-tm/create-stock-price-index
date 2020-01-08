import unittest
import get_policy_number_list as app


class TestHandlerCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_lambda_handler(self):
        # d = app.SBI_Scraper('ID', 'passwordc')
        # json = d.get_fi_param()
        json = app.lambda_handler('a', 'b')
        print(json)


if __name__ == "__main__":
    unittest.main()

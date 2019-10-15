import unittest
import get_policy_number_list as app


class TestHandlerCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_lambda_handler(self):
        d = app.SBI_Scraper('ユーザID', 'パスワード')
        d.get_fi_param('6050')
        # app.SBI_Scraper.get_fi_param()


if __name__ == "__main__":
    unittest.main()

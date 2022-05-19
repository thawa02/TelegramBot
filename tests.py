import unittest
import main
import requests
from bs4 import BeautifulSoup


class TestGetNext(unittest.TestCase):
    """Test function get_next_page()"""
    def setUp(self):
        r = requests.get(main.site_address + main.start_address)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.nxt = main.get_next_page(soup)

    def test_work_of_get_next(self):
        self.assertIsInstance(self.nxt, str, "incorrect return of function get_next_page")
        self.assertNotEqual(self.nxt, main.start_address,
                            "function get_next_page does not work")

    def test_correct_address_after_get_next(self):
        r = requests.get(main.site_address + self.nxt)
        soup = BeautifulSoup(r.text, 'html.parser')
        for info in soup.select('#main'):
            title = info.select('.af-title')[0].text
            self.assertEqual(title, "Генератор фактов", "incorrect address after get_next_page")

    def tearDown(self):
        pass


class TestGetFact(unittest.TestCase):
    """Test function get_fact()"""
    def setUp(self):
        r = requests.get(main.site_address + main.start_address)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.fact = main.get_fact(soup)

    def test_correct_output_format_of_get_fact(self):
        self.assertIsInstance(self.fact, list, "incorrect return of function get_fact")
        self.assertTrue(len(self.fact) == 2, "incorrect size of return of function get_fact")

    def test_correct_output_types_of_get_fact(self):
        self.assertIsInstance(self.fact[0], str, "incorrect text in return of function get_fact")
        self.assertIsInstance(self.fact[1], str, "incorrect src text in return of function get_fact")

    def test_correct_picture_address_in_get_fact_output(self):
        self.assertTrue(self.fact[1][:36] == 'https://zagge.ru/wp-content/uploads/',
                        "incorrect address of picture")
        self.assertTrue(self.fact[1][-4:] == '.jpg', "incorrect address of picture")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

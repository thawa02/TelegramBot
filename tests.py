import unittest
import main
import requests
from bs4 import BeautifulSoup


class TestBot(unittest.TestCase):

    def setUp(self):
        self.address = "https://zagge.ru/"
        r = requests.get(self.address + "nils-bor-i-dom-s-truboj-s-pivom/")
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def test_get_next(self):
        nxt = main.get_next_page(self.page)
        self.assertIsInstance(nxt, str, "incorrect return of function get_next_page")
        self.assertNotEqual(nxt, "nils-bor-i-dom-s-truboj-s-pivom/",
                            "function get_next_page does not work")

        r = requests.get(self.address + nxt)
        self.soup = BeautifulSoup(r.text, 'html.parser')
        for info in self.soup.select('#main'):
            title = info.select('.af-title')[0].text
        self.assertEqual(title, "Генератор фактов", "incorrect address after get_next_page")

    def test_get_fact(self):
        fact = main.get_fact(self.soup)
        self.assertIsInstance(fact, list, "incorrect return of function get_fact")
        self.assertTrue(len(fact) == 2, "incorrect size of return of function get_fact")
        self.assertIsInstance(fact[0], str, "incorrect text in return of function get_fact")
        self.assertIsInstance(fact[1], str, "incorrect src text in return of function get_fact")
        self.aseertTrue(fact[1][:36] == 'https://zagge.ru/wp-content/uploads/2020/02/',
                        "incorrect address of picture")
        self.assertTrue(fact[1][-4:] == '.jpg', "incorrect address of picture")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

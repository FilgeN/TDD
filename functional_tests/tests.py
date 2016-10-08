from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(LiveServerTestCase):
    """docstring for NewVisitorTest"""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        import time
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edyta dowiedziala sie o nowej, wspanialej aplikacji w postaci listy rzeczy do zrobienia.
        # Postanowila wiec wejsc na strone glowa tej aplikacji.
        self.browser.get(self.live_server_url)

        # Zwrocila uwage ze tytul strony i naglowek zawieraja slowo 'Listy'
        self.assertIn('Listy', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Utworz', header_text)

        # Od razu jest zachecona, aby wpisac rzeczy do zrobienia
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Wpisz rzecz do zrobienia'
        )

        # W polu tesktowym wpisala "Kupic pawie piora"
        # ( malowanie jest hobby Edyty )
        input_box.send_keys('Kupic pawie piora')

        # Po nacisnieciu klawisza 'Enter' strona zostala uaktualniona i wyswietla
        # 1. Kupic pawie piora jako element listy rzeczy do zrobienia
        input_box.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Kupic pawie piora')

        # Na stronie nadal znajduje sie pole tekstowe zachęcajace do podania kolejnego zadania
        # Edyta wpisala: "Uzyc pawich pior do zrobienia przynety" (Edyta jest bardzo skrupulatna)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Uzyc pawich pior do zrobienia przynety')
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('2: Uzyc pawich pior do zrobienia przynety')

        # Teraz nowy uzytkownik Franek zaczyna korzystac z witryny

        ##Uzywamy nowej sesji przegladarki internetowej, aby miec pewnosc, ze zadne
        ##informacje z sesji Edyty nie zostana ujawnione - na przyklad przez cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Franek odwiedza strone glowna
        # Nie znajduje zadnych sladow listy Edyty
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupic pawie piora', page_text)
        self.assertNotIn('zrobienia przynety', page_text)

        import time
        time.sleep(1)
        # Franek tworzy nowa liste, wprowadzajac nowy element
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Kupic mleko')
        input_box.send_keys(Keys.ENTER)

        time.sleep(1)
        # Franek otrzymuje unikatowy adres URL prowadzacy do jego listy
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Ponownie niema zadnego sladu po liscie Edyty
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupic pawie piora', page_text)
        self.assertIn('Kupic mleko', page_text)

        # Usatysfakcjonowani, oboje klada sie spac
        # Edyta byla ciekawa, czy witryna zapamieta jej liste. Zwrocila uwage na wygenerowany dla niej
        # unikatowy adres URL, obok ktorego znajduje sie pewien tekst z wyjasnieniem
        self.fail('Zakonczenie testu!')

        # Przechodzi pod podany adres URL i widzi wyswietlona swoja liste rzeczy do zrobienia

        # Usatysfakcjonowana kladzie sie spac

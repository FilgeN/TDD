from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
	"""docstring for NewVisitorTest"""
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		#Edyta dowiedziala sie o nowej, wspanialej aplikacji w postaci listy rzeczy do zrobienia.
		#Postanowila wiec wejsc na strone glowa tej aplikacji.
		self.browser.get('http://localhost:8000')
		
		#Zwrocila uwage ze tytul strony i naglowek zawieraja slowo 'Listy'
		self.assertIn('Listy', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text 
		self.assertIn('lista', header_text)

		#Od razu jest zachecona, aby wpisac rzeczy do zrobienia
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			input_box.get_attribute('placeholder'),
			'Wpisz rzecz do zrobienia'
		)

		#W polu tesktowym wpisala "Kupic pedzle o rozmiarze 8,9" 
		#( malowanie jest hobby Edyty )
		input_box.send_keys('Kupic pawie piora')

		#Po nacisnieciu klawisza 'Enter' strona zostala uaktualniona i wyswietla
		# 1. Kupic pedzle o rozmiarze 8,9 jako element listy rzeczy do zrobienia
		input_box.send_keys(Keys.ENTER)
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		print( "blallblaslasladals\n" )
		print(  type(rows) )
		self.assertTrue(
			any(row.text == '1: Kupić pawie pióra' for row in rows),
			"Nowy element nie znajduje sie w tabeli!"
		)
		
		#Na stronie nadal znajduje sie pole tekstowe zachęcajace do podania kolejnego zadania
		#Edyta wpisala: "Uzyc pedzli do namalowania pejzazu" (Edyta jest bardzo skrupulatna)
		self.fail('Zakonczenie testu!')

		#Strona zostala ponownie uaktualniona i teraz wyswietla dwa elementy na liscie rzeczy do zrobienia
		
		#Edyta byla ciekawa, czy witryna zapamieta jej liste. Zwrocila uwage na wygenerowany dla niej
		#unikatowy adres URL, obok ktorego znajduje sie pewien tekst z wyjasnieniem
		
		#Przechodzi pod podany adres URL i widzi wyswietlona swoja liste rzeczy do zrobienia
		
		#Usatysfakcjonowana kladzie sie spac

if __name__=='__main__':
	unittest.main(warnings='ignore')

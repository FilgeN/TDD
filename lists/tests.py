from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

# Create your tests here.
class HomePagetest(TestCase):
	"""docstring for HomepAgetest"""

	def test_root_url_resolvers_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
		
	def test_home_page_return_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		excepted_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), excepted_html)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'Nowy element listy'

		response = home_page(request)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'Nowy element listy')
		
		self.assertIn('Nowy element listy', response.content.decode() )
		excepted_html = render_to_string(
			'home.html',
			{'new_item_text': 'Nowy element listy'}
		)
		self.assertEqual(response.content.decode(), excepted_html)

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item .text = 'Absolutnie pierwszy element listy'
		first_item.save()

		second_item = Item()
		second_item.text = 'Drugi element'
		second_item.save()

		saved_items = Item.objects.all() #zwraca QuerySet
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]

		self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element listy')
		self.assertEqual(second_saved_item.text, 'Drugi element')


	def test_home_page_only_saves_item_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(), 0)
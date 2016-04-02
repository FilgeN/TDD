from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

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
		
		self.assertIn('Nowy element listy', response.content.decode() )
		excepted_html = render_to_string(
			'home.html',
			{'new_item_text': 'Nowy element kisty'}
		)
		self.assertEqual(response.content.decode(), excepted_html)

	# def test_home_page_can_save_a_POST_request(self)
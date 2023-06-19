from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Snack


class SnackTests(TestCase):
    def setUp(self):
        self.purchaser = get_user_model().objects.create(username="tester",password="tester")
        self.snake = Snack.objects.create(title="rake", purchaser=self.purchaser )

    def test_list_page_status_code(self):
        url = reverse('snacks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_page_template(self):
        url = reverse('snacks')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_list_page_context(self):
        url = reverse('snacks')
        response = self.client.get(url)
        snacks = response.context['eat']
        self.assertEqual(len(snacks), 1)
        self.assertEqual(snacks[0].title, "rake")
        self.assertEqual(snacks[0].description, 'write your description')
        self.assertEqual(snacks[0].purchaser.username, "tester")

    def test_detail_page_status_code(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_page_template(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_detail_page_context(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        snacks = response.context['snack']
        self.assertEqual(snacks.title, "rake")
        self.assertEqual(snacks.purchaser.username, "tester")
        self.assertEqual(snacks.description, "write your description")
    
    def test_create_view(self):
        obj={
            'title':"test2",
            'purchaser':self.purchaser.id,
            'description': "info..."

        }

        url = reverse('snack_create')
        response = self.client.post(path=url,data=obj,follow=True)
        self.assertRedirects(response, reverse('snack_detail',args=[2]))    
    
    def test_update_view(self):
        obj={
            'title':"test2",
            'purchaser':self.purchaser.id,
            'description': "info..."

        }

        url = reverse('snack_update',args=[1])
        response = self.client.post(path=url,data=obj,follow=True)
        self.assertRedirects(response, reverse('snack_detail',args=[1]))        
    
    def test_delete_view(self):
        
        url = reverse('snack_delete',args=[1])
        response = self.client.post(path=url,follow=True)
        self.assertRedirects(response, reverse('snacks'))       
    
    def test_str_method(self):
        self.assertEqual(str(self.snake),"rake")

    def test_create_response(self):
        url = reverse('snack_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'snack_create.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_update_response(self):
        url = reverse('snack_update', args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response,'snack_update.html')
        self.assertTemplateUsed(response, 'base.html')


    def test_delete_response(self):
        url = reverse('snack_delete', args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response,'snack_delete.html')
        self.assertTemplateUsed(response, 'base.html')    
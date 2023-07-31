from django.test import TestCase
from django.shortcuts import reverse
from .models import Folder

class FshareTest(TestCase):

	def test_home_page(self):
		req=reverse('FileViewUrl')
		resp=self.client.get(req)
		folders=Folder.objects.all().filter(privacy='public') | Folder.objects.filter(privacy='authorize')
		
		self.assertEqual(resp.status_code,200)
		self.assertTemplateUsed('FshareTemplate/home.html')
		self.assertEqual(list(resp.context['folders']),list(folders))

	def test_file_detail_page(self):
		fod=Folder.objects.create(name='myfolder',privacy='authorize')
		req = reverse('FolderDetailViewUrl',kwargs={'fid':fod.id})

		resp = self.client.get(req)
		self.assertEqual(resp.status_code,200)
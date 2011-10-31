#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from models import *
import os
from django.contrib.auth.models import User
from django.db import models

try:
    from lxml import html
except:
    raise ImportError('Imagestore require lxml for self-testing')

class ImagestoreTest(TestCase):
    def setUp(self):
        self.image_file = open(os.path.join(os.path.dirname(__file__), 'test_img.jpg'))
        self.user = User.objects.create_user('zeus', 'zeus@example.com', 'zeus')
        self.client = Client()
        self.album = Album(name='test album', user=self.user)
        self.album.save()

    def _upload_test_image(self, username='zeus', password='zeus'):
        self.client.login(username=username, password=password)
        self.image_file = open(os.path.join(os.path.dirname(__file__), 'test_img.jpg'))
        response = self.client.get(reverse('imagestore:upload'))
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)
        values = dict(tree.xpath('//form[@method="post"]')[0].form_values())
        values['image'] = self.image_file
        values['album'] = Album.objects.filter(user=self.user)[0].id
        response = self.client.post(reverse('imagestore:upload'), values, follow=True)
        return response

    def _create_test_album(self, username='zeus', password='zeus'):
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('imagestore:create-album'))
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)
        values = dict(tree.xpath('//form[@method="post"]')[0].form_values())
        values['name'] = 'test album creation'
        response = self.client.post(reverse('imagestore:create-album'), values, follow=True)
        return response

    def test_empty_index(self):
        response = self.client.get(reverse('imagestore:index'))
        self.assertEqual(response.status_code, 200)

    def test_empty_album(self):
        self.album.is_public = False
        self.album.save()
        response = self.client.get(self.album.get_absolute_url())
        self.assertTrue(response.status_code == 403)
        self.client.login(username='zeus', password='zeus')
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(self.album.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        response = self.client.get(reverse('imagestore:user', kwargs={'username': 'zeus'}))
        self.assertEqual(response.status_code, 200)

    def test_album_creation(self):
        response = self._create_test_album()
        self.assertEqual(response.status_code, 200)

    def test_album_edit(self):
        response = self._create_test_album()
        album_id = Album.objects.get(name='test album creation').id
        self.client.login(username='zeus', password='zeus')
        response = self.client.get(reverse('imagestore:update-album', kwargs={'pk': album_id}))
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)
        values = dict(tree.xpath('//form[@method="post"]')[0].form_values())
        values['name'] = 'test album update'
        self.client.post(reverse('imagestore:update-album', kwargs={'pk': album_id}), values, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Album.objects.get(id=album_id).name == 'test album update')

    def test_album_delete(self):
        response = self._create_test_album()
        self.client.login(username='zeus', password='zeus')
        album_id = Album.objects.get(name='test album creation').id
        response = self.client.post(reverse('imagestore:delete-album', kwargs={'pk': album_id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Album.objects.filter(id=album_id)) == 0)


    def test_image_upload(self):
        response = self._create_test_album()
        response = self._upload_test_image()
        self.assertEqual(response.status_code, 200)
        img_url = Image.objects.get(user__username='zeus').get_absolute_url()
        response = self.client.get(img_url)
        self.assertEqual(response.status_code, 200)
        self.test_user()

    def test_tagging(self):
        response = self._create_test_album()
        self.client.login(username='zeus', password='zeus')
        response = self.client.get(reverse('imagestore:upload'))
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)
        values = dict(tree.xpath('//form[@method="post"]')[0].form_values())
        values['image'] = self.image_file
        values['tags'] = 'one, tow, three'
        values['album'] = Album.objects.filter(user=self.user)[0].id
        self.client.post(reverse('imagestore:upload'), values, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('imagestore:tag', kwargs={'tag': 'one'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['image_list']) == 1)

    def test_delete(self):
        User.objects.create_user('bad', 'bad@example.com', 'bad')
        response = self._create_test_album()
        self._upload_test_image()
        self.client.login(username='bad', password='bad')
        image_id = Image.objects.get(user__username='zeus').id
        response = self.client.post(reverse('imagestore:delete-image', kwargs={'pk': image_id}), follow=True)
        self.assertEqual(response.status_code, 404)
        self.client.login(username='zeus', password='zeus')
        response = self.client.post(reverse('imagestore:delete-image', kwargs={'pk': image_id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Image.objects.all()), 0)

    def test_update_image(self):
        self._upload_test_image()
        self.client.login(username='zeus', password='zeus')
        image_id = Image.objects.get(user__username='zeus').id
        response = self.client.get(reverse('imagestore:update-image', kwargs={'pk': image_id}), follow=True)
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)
        values = dict(tree.xpath('//form[@method="post"]')[0].form_values())
        values['tags'] = 'one, tow, three'
        values['title'] = 'changed title'
        values['album'] = Album.objects.filter(user=self.user)[0].id
        self.client.post(reverse('imagestore:update-image', kwargs={'pk': image_id}), values, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Image.objects.get(user__username='zeus').title == 'changed title')

    def test_prev_next_with_ordering(self):
        self.test_album_creation()
        for i in range(1, 6):
            self._upload_test_image()
            img = Image.objects.order_by('-id')[0]
            img.order = i
            img.save()
        # Swap two id's
        im1 = Image.objects.get(order=2)
        im2 = Image.objects.get(order=4)
        im1.order, im2.order = 4, 2
        im1.save()
        im2.save()
        response = self.client.get(Image.objects.get(order=3).get_absolute_url())
        self.assertEqual(response.context['next'], im1)
        self.assertEqual(response.context['previous'], im2)

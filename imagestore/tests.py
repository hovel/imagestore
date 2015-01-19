#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
import swapper
Image = swapper.load_model('imagestore', 'Image')
Album = swapper.load_model('imagestore', 'Album')
import os
import random
from django.contrib.auth.models import Permission, User
from imagestore.templatetags.imagestore_tags import imagestore_alt

try:
    from lxml import html
except:
    raise ImportError('Imagestore require lxml for self-testing')


class ImagestoreTest(TestCase):
    def setUp(self):
        self.image_file = open(os.path.join(os.path.dirname(__file__), 'test_img.jpg'), 'rb')
        self.user = User.objects.create_user('zeus', 'zeus@example.com', 'zeus')
        self.user.user_permissions.add(*Permission.objects.filter(content_type__app_label='imagestore'))
        self.client = Client()
        self.album = Album(name='test album', user=self.user)
        self.album.save()

    def _upload_test_image(self, username='zeus', password='zeus'):
        self.client.login(username=username, password=password)
        self.image_file = open(os.path.join(os.path.dirname(__file__), 'test_img.jpg'), 'rb')
        response = self.client.get(reverse('imagestore:upload'))
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)
        values = dict(tree.xpath('//form[@method="post"]')[0].form_values())
        values['image'] = self.image_file
        values['album'] = Album.objects.filter(user=self.user)[0].id
        values['some_int'] = random.randint(1, 100)
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
        img = Image.objects.get(user__username='zeus')
        img_url = img.get_absolute_url()
        response = self.client.get(img_url)
        self.assertEqual(response.status_code, 200)
        self.test_user()
        self.assertIsNotNone(img.some_int)

    def test_tagging(self):
        response = self._create_test_album()
        self.client.login(username='zeus', password='zeus')
        response = self.client.get(reverse('imagestore:upload'))
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)
        values = dict(tree.xpath('//form[@method="post"]')[0].form_values())
        values['image'] = self.image_file
        values['tags'] = 'one, tow, three'
        values['some_int'] = random.randint(1, 100)
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

    def test_album_order(self):
        self.album.delete()
        a1 = Album.objects.create(name='b2', order=1, user=self.user)
        a2 = Album.objects.create(name='a1', order=2, user=self.user)
        response = self.client.get(reverse('imagestore:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'][0].name, 'b2')
        self.assertEqual(response.context['object_list'][1].name, 'a1')
        a1.order, a2.order = 2, 1
        a1.save()
        a2.save()
        response = self.client.get(reverse('imagestore:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'][0].name, 'a1')
        self.assertEqual(response.context['object_list'][1].name, 'b2')

    def test_imagestore_alt(self):
        self._upload_test_image()
        image = Image.objects.all()[0]
        image.album = None
        image.title = ''
        image.save()

        # empty title, empty brief = empty result
        result = imagestore_alt(image)
        self.assertEqual(result, '')

        album = Album.objects.all()[0]
        album.brief = 'album brief'
        album.save()
        image.album = album
        image.save()
        counter = random.randint(0, 111)

        # empty title, not empty brief = brief in result
        result = imagestore_alt(image)
        self.assertIn(album.brief, result)
        self.assertNotIn(str(counter), result)  # insure next assertIn from mistake
        self.assertIn(result.count('\''), (0, 2))
        self.assertIn(result.count('\"'), (0, 2))

        # same behaviour plus counter
        result = imagestore_alt(image, counter)
        self.assertIn(album.brief, result)
        self.assertIn(str(counter), result)
        self.assertIn(result.count('\''), (0, 2))
        self.assertIn(result.count('\"'), (0, 2))

        # IMAGESTORE_BRIEF_TO_ALT_TEMPLATE affects on result format
        with self.settings(IMAGESTORE_BRIEF_TO_ALT_TEMPLATE = '{1}_{0}'):
            result = imagestore_alt(image, counter)
            self.assertIn('{1}_{0}'.format(album.brief, counter), result)

        # but does not affect on single and double quotes
        with self.settings(IMAGESTORE_BRIEF_TO_ALT_TEMPLATE = '{1}_\'_\"_{0}'):
            result = imagestore_alt(image, counter)
            self.assertIn(result.count('\''), (0, 2))
            self.assertIn(result.count('\"'), (0, 2))

        # quotes shall not pass
        album.brief = 'album \' \" brief'
        album.save()
        result = imagestore_alt(image, counter)
        self.assertIn(result.count('\''), (0, 2))
        self.assertIn(result.count('\"'), (0, 2))
        counter = '1 \'\" 2'
        result = imagestore_alt(image, counter)
        self.assertIn(result.count('\''), (0, 2))
        self.assertIn(result.count('\"'), (0, 2))

        # not empty title = title in result (only)
        image.title = 'image title'
        image.save()
        result = imagestore_alt(image, counter)
        self.assertIn(image.title, result)
        self.assertNotIn(album.brief, result)
        self.assertNotIn(str(counter), result)
        self.assertIn(result.count('\''), (0, 2))
        self.assertIn(result.count('\"'), (0, 2))

        # quotes escaped again
        image.title = 'image \' \" title'
        image.save()
        result = imagestore_alt(image, counter)
        self.assertIn(result.count('\''), (0, 2))
        self.assertIn(result.count('\"'), (0, 2))

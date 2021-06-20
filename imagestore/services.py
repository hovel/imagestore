import os
import re
import sys
from pathlib import Path
from typing import List

import swapper
from django.core.files import File

from imagestore.utils import valid_filepath



def fetch_from_local_path(path: Path) -> List[str]:
    """
    This function will replace all albums with the contents of the folder in
    the specified path
    """

    Image = swapper.load_model('imagestore', 'Image')
    Album = swapper.load_model('imagestore', 'Album')

    # list() use because queryset is lazy
    previous_images_ids = list(Image.objects.values_list('id', flat=True))

    log = []
    for dirpath, dirnames, filenames in os.walk(path):
        collected = []  # [[filepath, filename, filename_noext, is_cover]]

        for filename in filenames:
            filename_noext = os.path.splitext(filename)[0]
            if 'cover' in filename or ''.join(set(filename_noext)) == '0':
                is_cover = True
            else:
                is_cover = False
            filepath = os.path.join(dirpath, filename)
            if valid_filepath(filepath):
                collected.append(
                    [filepath, filename, filename_noext, is_cover])

        if not collected:
            continue

        # sort by int(filename_noext)
        def get_sort_key(x):
            if x[2].isdigit():
                key = (int(x[2]), x[2])
            else:
                key = (sys.maxsize, x[2])
            return key

        collected = sorted(collected, key=get_sort_key)

        album_path = dirpath
        album_name = os.path.basename(album_path)

        album_order = Album._meta.get_field('order').default
        order_pattern = re.compile(r'-(?P<order>\d+)')
        order_search = order_pattern.search(album_name)
        if order_search:
            album_order = order_search.group('order')
            album_name = order_pattern.sub('', album_name)

        album, created = Album.objects.update_or_create(
            name=album_name, defaults={'order': album_order})

        for filepath, filename, filename_noext, is_cover in collected:
            with open(filepath, mode='rb') as original:
                image = Image.objects.create(
                    album=album, image=File(original, name=filename))
                log.append(f'Saved {filepath}')

            if is_cover:
                album.head = image
                album.save()
                log.append(f'Set {filepath} as cover of {album_name}')

    Image.objects.filter(id__in=previous_images_ids).delete()
    Album.objects.filter(images__isnull=True).delete()

    return log

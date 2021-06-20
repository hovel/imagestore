import logging.config
import pathlib

from django.core.management import CommandParser, BaseCommand

from imagestore.services import fetch_from_local_path

logger = logging.getLogger(__file__)


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('path', type=pathlib.Path)

    def handle(self, *args, **options):
        path = options['path'].expanduser().resolve()
        log = fetch_from_local_path(path)
        logger.info(log)

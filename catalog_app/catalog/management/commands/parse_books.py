from concurrent.futures import ThreadPoolExecutor

from django.core.management.base import BaseCommand

from catalog.models import Book
from catalog.utils import _parse_books, _download_and_save_image


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("url", type=str)

    def handle(*args, **options) -> None:
        import time

        start = time.time()
        _parse_books(url=options.get("url"))
        with ThreadPoolExecutor(
            max_workers=13
        ) as executor:  # 6 threads * 2 + 1
            executor.map(_download_and_save_image, Book.objects.all())
        end = time.time()
        print(end - start)

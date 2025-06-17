import requests
import time
from django.core.management.base import BaseCommand
from market.models import Item

class Command(BaseCommand):
    help = 'Fetches all items from the DarkerDB API and populates the local database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting item population script...'))

        base_url = 'https://api.darkerdb.com/v1/items'
        page = 1
        limit = 50  # Берем максимальный лимит для скорости
        total_items_saved = 0

        while True:
            params = {
                'page': page,
                'limit': limit,
            }

            try:
                response = requests.get(base_url, params=params, timeout=10)
                response.raise_for_status()  # Вызовет ошибку, если статус не 2xx
            except requests.RequestException as e:
                self.stderr.write(self.style.ERROR(f'API request failed on page {page}: {e}'))
                break

            data = response.json()
            items_data = data.get('body', [])
            count_model = Item.objects.count()

            if not items_data or count_model >= 1885: # 1885
                # Если API вернуло пустой массив, значит предметы закончились
                self.stdout.write(self.style.SUCCESS(f'No more items found. Script finished.'))
                break

            items_to_create = []
            for item_data in items_data:
                # Используем update_or_create, чтобы не создавать дубликаты
                # и обновлять существующие записи, если они изменились.
                # Это делает скрипт безопасным для повторного запуска.
                defaults = {
                    'name': item_data.get('name'),
                    'archetype': item_data.get('archetype'),
                }
                item, created = Item.objects.update_or_create(
                    item_id=item_data['id'],
                    defaults=defaults
                )

                if created:
                    total_items_saved += 1

            self.stdout.write(self.style.SUCCESS(f'Page {page}: Processed {len(items_data)} items. New items saved: {total_items_saved}.'))

            page += 1

            time.sleep(5)

        self.stdout.write(self.style.SUCCESS(f'Total new items added to the database: {total_items_saved}.'))
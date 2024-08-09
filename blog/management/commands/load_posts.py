import csv

from django.core.management.base import BaseCommand

from blog.models import Post
from config.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Добавление постов в БД'

    def handle(self, **kwargs):
        file = f'{BASE_DIR}/blog/management/blog_post.csv'
        try:
            with open(file, 'r', encoding='UTF-8') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    Post.objects.get_or_create(
                        title=row[1],
                        text=row[2],
                        likes=row[3],
                        pub_date=row[4],
                        author_id=row[5]
                    )
            self.stdout.write(self.style.SUCCESS('Посты успешно добавлены в БД.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR("Ошибка: %s" % e))

import csv
from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Load movies from CSV'

    def handle(self, *args, **kwargs):
        with open('data/movies.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Movie.objects.get_or_create(
                    title=row['title'],
                    genre=row['genres'],
                    rating=float(row.get('rating', 4)),
                    image=row.get('image', 'https://via.placeholder.com/300')
                )
        self.stdout.write(self.style.SUCCESS("Movies Loaded Successfully"))

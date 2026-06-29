"""
Management command: python manage.py seed_data
Creates demo categories, products (with real image URLs), and an admin user.
"""
import urllib.request
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from legoshop.catalog.models import Category, Product
from legoshop.accounts.models import User

CATEGORIES = [
    {'name': 'City',         'slug': 'city',         'description': 'Build the city of your dreams.'},
    {'name': 'Technic',      'slug': 'technic',      'description': 'Advanced builds with moving parts.'},
    {'name': 'Star Wars',    'slug': 'star-wars',    'description': 'A galaxy far, far away.'},
    {'name': 'Creator',      'slug': 'creator',      'description': '3-in-1 creative sets.'},
    {'name': 'Architecture', 'slug': 'architecture', 'description': 'Iconic buildings of the world.'},
]

PRODUCTS = [
    {'name': 'City Police Station',    'slug': 'city-police-station',    'category': 'city',         'price': '49.99',  'pieces': 668,   'age_min': 6,  'stock': 15, 'description': 'A fully equipped police station with jail cells, a garage, and a helicopter pad.'},
    {'name': 'City Fire Truck',        'slug': 'city-fire-truck',        'category': 'city',         'price': '29.99',  'pieces': 380,   'age_min': 6,  'stock': 20, 'description': 'Race to the rescue with this detailed fire truck featuring an extendable ladder.'},
    {'name': 'City Hospital',          'slug': 'city-hospital',          'category': 'city',         'price': '89.99',  'pieces': 816,   'age_min': 7,  'stock': 8,  'description': 'A multi-storey hospital with an ambulance, operating room, and helipad.'},
    {'name': 'City Train Station',     'slug': 'city-train-station',     'category': 'city',         'price': '59.99',  'pieces': 907,   'age_min': 7,  'stock': 12, 'description': 'Busy city train station with ticket office and platform.'},
    {'name': 'Technic Supercar',       'slug': 'technic-supercar',       'category': 'technic',      'price': '149.99', 'pieces': 1580,  'age_min': 11, 'stock': 5,  'description': 'An incredibly detailed supercar with working gearbox and V8 engine.'},
    {'name': 'Technic Crane Truck',    'slug': 'technic-crane-truck',    'category': 'technic',      'price': '119.99', 'pieces': 1292,  'age_min': 10, 'stock': 7,  'description': 'A heavy-duty crane truck with extendable boom and outriggers.'},
    {'name': 'Technic Excavator',      'slug': 'technic-excavator',      'category': 'technic',      'price': '74.99',  'pieces': 920,   'age_min': 10, 'stock': 10, 'description': 'A powerful excavator with motorized functions.'},
    {'name': 'Millennium Falcon',      'slug': 'millennium-falcon',      'category': 'star-wars',    'price': '849.99', 'pieces': 7541,  'age_min': 16, 'stock': 3,  'description': 'The most iconic ship in the galaxy — 7,541 pieces of pure awesome.'},
    {'name': 'X-Wing Starfighter',     'slug': 'x-wing-starfighter',     'category': 'star-wars',    'price': '59.99',  'pieces': 474,   'age_min': 9,  'stock': 18, 'description': "Luke Skywalker's legendary X-Wing, ready for the attack on the Death Star."},
    {'name': 'Death Star',             'slug': 'death-star-2',           'category': 'star-wars',    'price': '499.99', 'pieces': 4016,  'age_min': 14, 'stock': 2,  'description': 'The ultimate weapon — recreated in 4,016 bricks with 23 minifigures.'},
    {'name': 'Medieval Castle',        'slug': 'medieval-castle',        'category': 'creator',      'price': '99.99',  'pieces': 1426,  'age_min': 9,  'stock': 9,  'description': 'Build a castle, a manor house, or a market — 3 builds in one box.'},
    {'name': 'Pirate Ship',            'slug': 'pirate-ship',            'category': 'creator',      'price': '79.99',  'pieces': 1264,  'age_min': 9,  'stock': 11, 'description': 'Sail the seas! Converts into a tavern or a lighthouse.'},
    {'name': 'Deep Sea Creatures',     'slug': 'deep-sea-creatures',     'category': 'creator',      'price': '34.99',  'pieces': 522,   'age_min': 7,  'stock': 25, 'description': 'Build an anglerfish, a crab, or a squid from one set.'},
    {'name': 'Eiffel Tower',           'slug': 'eiffel-tower',           'category': 'architecture', 'price': '209.99', 'pieces': 10001, 'age_min': 18, 'stock': 4,  'description': 'A stunning 1.5 metre tall replica of the iconic Parisian landmark.'},
    {'name': 'Colosseum',              'slug': 'colosseum',              'category': 'architecture', 'price': '549.99', 'pieces': 9036,  'age_min': 18, 'stock': 2,  'description': "The world's largest LEGO set — an epic recreation of Rome's ancient arena."},
    {'name': 'Empire State Building',  'slug': 'empire-state-building',  'category': 'architecture', 'price': '119.99', 'pieces': 1767,  'age_min': 16, 'stock': 6,  'description': "Art Deco masterpiece — a detailed scale model of New York's most iconic skyscraper."},
]


class Command(BaseCommand):
    help = 'Seed the database with demo LEGO products and an admin user'

    def handle(self, *args, **kwargs):
        self.stdout.write('🧱 Seeding database...')

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', email='admin@legoshop.local',
                password='admin123', role=User.ROLE_ADMIN,
            )
            self.stdout.write(self.style.SUCCESS('  ✅ Admin user created (admin / admin123)'))
        else:
            self.stdout.write('  ⏭  Admin user already exists')

        cat_map = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
            cat_map[cat.slug] = cat
            if created:
                self.stdout.write(f'  ✅ Category: {cat.name}')

        for p_data in PRODUCTS:
            cat_slug = p_data.pop('category')
            category = cat_map.get(cat_slug)
            product, created = Product.objects.get_or_create(
                slug=p_data['slug'],
                defaults={**p_data, 'category': category},
            )
            if created:
                self.stdout.write(f'  ✅ Product: {product.name}')

        self.stdout.write(self.style.SUCCESS('\n🎉 Done! Run: python manage.py runserver'))
        self.stdout.write('   Login: admin / admin123')

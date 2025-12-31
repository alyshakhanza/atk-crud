from django.core.management.base import BaseCommand
from app.models.user import UserAccount
from app.models.product import Category, Brand

class Command(BaseCommand):
    help = 'Seeds the database with initial data (User, Categories, Brands)'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # 1. SEED USER (Customer)
        # Menggunakan get_or_create agar tidak duplikat
        user, created = UserAccount.objects.get_or_create(
            email="customer1@gmail.com",
            defaults={
                "type": "CUSTOMER",
                "is_customer": True,
                "is_active": True
            }
        )

        if created:
            user.set_password("password123")
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.email}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {user.email} already exists. Skipped.'))

        # 2. SEED CATEGORIES
        categories = [
            "Aksesorie Seragam", "Alat Gambar", "Alat Tulis", "Bahan Perekat",
            "Dokumen", "Mainan", "Tali"
        ]

        for cat_name in categories:
            obj, created = Category.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Category: {cat_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category {cat_name} exists. Skipped.'))

        # 3. SEED BRANDS
        brands = [
            "Zebra", "Kenko", "Faber-Castell", "Joyko", "Pilot",
            "Pentel", "Sinar Dunia (SIDU)", "Paperline", "Artline",
            "Max", "Nachi Tape", "Agatis"
        ]

        for brand_name in brands:
            obj, created = Brand.objects.get_or_create(name=brand_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Brand: {brand_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Brand {brand_name} exists. Skipped.'))

        self.stdout.write(self.style.SUCCESS('Seeding completed!'))
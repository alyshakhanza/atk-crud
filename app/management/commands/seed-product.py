import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from app.models import Item, Category, Brand
from django.conf import settings

class Command(BaseCommand):
    help = "Seed initial data with images"

    def download_image(self, image_url, image_name):
        """
        Download image from URL and save it to local media directory.
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()

            # Cek jenis konten dari file yang diunduh
            content_type = response.headers['Content-Type']
            if 'image/jpeg' in content_type:
                ext = '.jpg'
            elif 'image/png' in content_type:
                ext = '.png'
            elif 'image/webp' in content_type:
                ext = '.webp'
            else:
                # Jika format tidak dikenal, simpan sebagai .jpg default
                ext = '.jpg'

            # Membuat nama file berdasarkan image_name dan ekstensi yang sesuai
            image_name_with_ext = image_name.replace(" ", "_").lower() + ext
            image_path = os.path.join(settings.MEDIA_ROOT, 'items', image_name_with_ext)

            # Menyimpan file gambar secara lokal
            with open(image_path, 'wb') as image_file:
                image_file.write(response.content)

            return image_path
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Failed to download {image_url}: {e}"))
            return None

    def handle(self, *args, **kwargs):
        # Seed Items with Images
        items = [
            {"name": "Amplop", "category": "Aksesorie Seragam", "brand": "Zebra", "description": "", "price": 10000, "stock": 100, "size": "Medium", "image_url": "https://drive.google.com/uc?id=10EqWRu987UdTQOCllJOxTXL27PVPNpdz"},
            {"name": "Buku Gambar", "category": "Alat Gambar", "brand": "Faber-Castell","description": "", "price": 25000, "stock": 50, "size": "Large", "image_url": "https://drive.google.com/uc?id=1CpI3QLTkxxpR31U_WAYEyXpXnaHljqp5"},
            {"name": "Cat Air", "category": "Alat Gambar", "brand": "Joyko", "description": "", "price": 5000, "stock": 200, "size": "Small", "image_url": "https://drive.google.com/uc?id=1fAOaG3ns0pGs1jIRdec-_ESoMLzL3mPc"},
            {"name": "Cutter", "category": "Alat Tulis", "brand": "Pilot", "description": "", "price": 15000, "stock": 80, "size": "Standard", "image_url": "https://drive.google.com/uc?id=1m9mkqrPxlP4HrWe75N6Yb8iL_TIHWcOA"},
            {"name": "Double Tape", "category": "Bahan Perekat", "brand": "Pentel", "description": "", "price": 3000, "stock": 150, "size": "Standard", "image_url": "https://drive.google.com/uc?id=1G4h5xfKVvH11qz2touDBZbBWxlCAkArd"},
            {"name": "Gunting", "category": "Alat Tulis", "brand": "Zebra", "description": "", "price": 7000, "stock": 120, "size": "Medium", "image_url": "https://drive.google.com/uc?id=1RUWPmGwCJ_4CrS2XQ4Tw39cqnugMB21Z"},
            {"name": "Isi Cutter", "category": "Alat Tulis", "brand": "Kenko", "description": "", "price": 4000, "stock": 90, "size": "Standard", "image_url": "https://drive.google.com/uc?id=1Nb78NeHPTsW80MByoqzp25wh0mKxZV8V"},
            {"name": "Isi Lem Tembak", "category": "Bahan Perekat", "brand": "Sinar Dunia (SIDU)", "description": "", "price": 8000, "stock": 110, "size": "Standard", "image_url": "https://drive.google.com/uc?id=1DlIsDYn_h_5NxWkkwzXlO51TYG23U8fx"},
            {"name": "Isi Pensil", "category": "Alat Tulis", "brand": "Paperline", "description": "", "price": 2000, "stock": 200, "size": "Pack", "image_url": "https://drive.google.com/uc?id=1QYOL8DNgCc_NaViwNLx6t3PWCBLVQ3LQ"},
            {"name": "Isi Spidol", "category": "Alat Tulis", "brand": "Artline", "description": "", "price": 2500, "stock": 180, "size": "Pack", "image_url": "https://drive.google.com/uc?id=1jStB1NVP2WaDmfaWUxzSmgfR-cLDgmIc"},
            {"name": "Jangka", "category": "Alat Tulis", "brand": "Max", "description": "", "price": 10000, "stock": 40, "size": "Medium", "image_url": "https://drive.google.com/uc?id=1_yc0dnAyfL70Tq9wDcw-xFlMt8IUMgyP"},
            {"name": "Kertas Folio", "category": "Dokumen", "brand": "Nachi Tape", "description": "", "price": 15000, "stock": 500, "size": "A4", "image_url": "https://drive.google.com/uc?id=1BAqr52PHzH9nS_N7-f3wXic_w3N-twQx"},
            {"name": "Kertas HVS", "category": "Dokumen", "brand": "Agatis", "description": "", "price": 12000, "stock": 300, "size": "A4", "image_url": "https://drive.google.com/uc?id=1MkEaPw0fSzbjtxvcXlbiQSKwyzY14dMA"},
            {"name": "Kertas Origami", "category": "Dokumen", "brand": "Zebra", "description": "", "price": 5000, "stock": 100, "size": "Pack", "image_url": "https://drive.google.com/uc?id=1Hs3CP_gpdb6Jl-8NU25Gp0deX1HCkkXQ"},
            {"name": "Krayon", "category": "Alat Gambar", "brand": "Kenko", "description": "", "price": 7000, "stock": 150, "size": "Pack", "image_url": "https://drive.google.com/uc?id=1Hdb8b5ZV4-ALi-534cvDrZvveP9fsk4W"},
            {"name": "Kuas Cat", "category": "Alat Gambar", "brand": "Faber-Castell", "description": "", "price": 15000, "stock": 60, "size": "Medium", "image_url": "https://drive.google.com/uc?id=1jguJs8WPkU4gbPIBwMAgMGrf4DUpB057"},
            {"name": "Lakban", "category": "Bahan Perekat", "brand": "Joyko", "description": "", "price": 5000, "stock": 100, "size": "Large", "image_url": "https://drive.google.com/uc?id=12n_Q9tlJmyeQEu1P_MoSolZjiehzaszx"},
            {"name": "Sterofoam", "category": "Bahan Perekat", "brand": "Pentel", "description": "", "price": 10000, "stock": 80, "size": "Medium", "image_url": "https://drive.google.com/uc?id=1A_mbrFby6VFeohkRsP2Yaxdb33uLwE7q"},
            {"name": "Lem", "category": "Bahan Perekat", "brand": "Sinar Dunia (SIDU)", "description": "", "price": 6000, "stock": 120, "size": "Small", "image_url": "https://drive.google.com/uc?id=173iez-vqy2ONPjvaEJ-j6h023VBLlamS"},
            {"name": "Lilin Mainan", "category": "Mainan", "brand": "Paperline", "description": "", "price": 3000, "stock": 200, "size": "Pack", "image_url": "https://drive.google.com/uc?id=1AzavilebQRaoLsRXf9PD9BZSew75Mki7"},
            {"name": "Map Kertas", "category": "Dokumen", "brand": "Artline", "description": "", "price": 4000, "stock": 150, "size": "Medium", "image_url": "https://drive.google.com/uc?id=1xKJqqdCbIG1AVl1HC1oKpfF734wUFALC"},
            {"name": "Materai", "category": "Dokumen", "brand": "Max", "description": "", "price": 10000, "stock": 500, "size": "Pack", "image_url": "https://drive.google.com/uc?id=1_Q12pFFYaOk8Ci9Sc4p2ukHgril3c7aF"},
            {"name": "Mika Film", "category": "Dokumen", "brand": "Nachi Tape", "description": "", "price": 7000, "stock": 250, "size": "A4", "image_url": "https://drive.google.com/uc?id=1yrDL66ak7nl1CWSTmsPGfZgbc9Z11JOY"},
            {"name": "Palet Cat", "category": "Alat Gambar", "brand": "Agatis", "description": "", "price": 15000, "stock": 30, "size": "Medium", "image_url": "https://drive.google.com/uc?id=1PBTCQSiUyhwGnhGBjl14VeBFBJCinupY"},
        ]

        for item_data in items:
            category = Category.objects.get(name=item_data["category"])
            brand = Brand.objects.get(name=item_data["brand"])

            # Download image
            image_name = item_data["name"]  # Name format: amplop.jpg
            image_path = self.download_image(item_data["image_url"], image_name)

            if image_path:
                item = Item.objects.create(
                    name=item_data["name"],
                    category=category,
                    brand=brand,
                    description="",
                    price=item_data.get("price", 0), 
                    stock=item_data.get("stock", 0), 
                    size=item_data.get("size", "Medium"),
                )

                # Save the image to Item model
                with open(image_path, 'rb') as img_file:
                    item.image.save(image_name.replace(" ", "_").lower(), ContentFile(img_file.read()), save=True)

                self.stdout.write(self.style.SUCCESS(f"Created item: {item_data['name']}"))

        self.stdout.write(self.style.SUCCESS("Item seeding finished"))

import csv
from django.core.management.base import BaseCommand
from properties.models import Property, Location, Image
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib.request
import socket

class Command(BaseCommand):
    help = 'Import properties from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        self.stdout.write(self.style.SUCCESS(f'Starting import from {csv_file}'))
        
        # Set timeout for URL requests
        socket.setdefaulttimeout(10)
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Create or get location
                    location, created = Location.objects.get_or_create(
                        city=row['city'],
                        state=row['state'],
                        country=row['country'],
                        defaults={
                            'address': row.get('address', ''),
                            'zip_code': row.get('zip_code', ''),
                        }
                    )
                    
                    # Create property
                    property_obj = Property.objects.create(
                        name=row['name'],
                        description=row['description'],
                        property_type=row['property_type'],
                        bedrooms=int(row['bedrooms']),
                        bathrooms=int(row['bathrooms']),
                        max_guests=int(row['max_guests']),
                        price_per_night=float(row['price_per_night']),
                        location=location
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created property: {property_obj.name}')
                    )
                    
                    # Handle images (optional - won't fail if images can't be downloaded)
                    image_urls = row.get('image_urls', '').split('|')
                    images_downloaded = 0
                    
                    for idx, url in enumerate(image_urls):
                        url = url.strip()
                        if url:
                            try:
                                # Try to download image from URL
                                img_temp = NamedTemporaryFile(delete=True)
                                urllib.request.urlretrieve(url, img_temp.name)
                                
                                # Create image object
                                image_obj = Image(property=property_obj)
                                image_obj.image.save(
                                    f"{property_obj.name}_{idx}.jpg",
                                    File(img_temp)
                                )
                                image_obj.save()
                                images_downloaded += 1
                                
                            except Exception as e:
                                # Just log the warning but continue with the import
                                self.stdout.write(
                                    self.style.WARNING(f'  → Could not download image {idx + 1} for {property_obj.name}: {str(e)}')
                                )
                    
                    if images_downloaded > 0:
                        self.stdout.write(
                            self.style.SUCCESS(f'  → Downloaded {images_downloaded} image(s) for {property_obj.name}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'  → No images downloaded for {property_obj.name} (property created without images)')
                        )
                
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to create property from row: {str(e)}')
                    )
                    continue
        
        self.stdout.write(self.style.SUCCESS('\n==========================================='))
        self.stdout.write(self.style.SUCCESS('Import completed successfully!'))
        self.stdout.write(self.style.SUCCESS('Note: Properties were created even if images failed to download.'))
        self.stdout.write(self.style.SUCCESS('You can add images manually through the admin panel.'))
        self.stdout.write(self.style.SUCCESS('==========================================='))
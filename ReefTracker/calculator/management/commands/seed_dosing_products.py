from django.core.management.base import BaseCommand
from calculator.models import DosingProduct 

class Command(BaseCommand):
    help = 'Seeds the database with standard reef dosing products'

    def handle(self, *args, **kwargs):
        # NOTE: PPMPerLiter represents how much 1ml of product raises 1 Liter of tank water.
        # You will need to verify the exact math for your specific calculator formula.
        products = [
            # CALCIUM PRODUCTS
            {
                'name': 'BRS Liquid Calcium Chloride',
                'category': 'CAL',
                'description': 'Standard Bulk Reef Supply Liquid Recipe',
                'PPMPerLiter': 37.85, 
            },
            {
                'name': 'Seachem Reef Fusion 1',
                'category': 'CAL',
                'description': 'Two-part calcium supplement',
                'PPMPerLiter': 25.0, 
            },
            
            # MAGNESIUM PRODUCTS
            {
                'name': 'BRS Liquid Magnesium Mix',
                'category': 'MAG',
                'description': 'Standard Bulk Reef Supply Liquid Recipe',
                'PPMPerLiter': 47.3,
            },
            {
                'name': 'Aquaforest Magnesium',
                'category': 'MAG',
                'description': 'Liquid magnesium supplement',
                'PPMPerLiter': 10.0,
            },
            {
                'name': "Randy's Recipe Calcium",
                'category': 'CAL',
                'description': 'DIY Recipe #1 (Calcium Chloride Dihydrate)',
                'PPMPerLiter': 37.0, 
            },
            {
                'name': 'AquaForest Ca Plus Liquid',
                'category': 'CAL',
                'description': 'Concentrated calcium (Based on 10ppm per 10ml/100L)',
                'PPMPerLiter': 100.0, 
            },
        ]

        self.stdout.write('Seeding Dosing Products...')
        
        count = 0
        for data in products:
            # get_or_create ensures we never create duplicates if you run the script twice
            product, created = DosingProduct.objects.get_or_create(
                name=data['name'], 
                category=data['category'],
                defaults={
                    'description': data['description'],
                    'PPMPerLiter': data['PPMPerLiter']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  + Added: {product.name}"))
                count += 1
            else:
                self.stdout.write(self.style.WARNING(f"  ~ Skipped: {product.name} (Already exists)"))

        self.stdout.write(self.style.SUCCESS(f'Finished! Added {count} new products.'))
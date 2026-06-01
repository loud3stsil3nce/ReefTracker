# aquariums/management/commands/seed_species.py

from django.core.management.base import BaseCommand
from aquariums.models import Species

class Command(BaseCommand):
    help = 'Seeds the database with common reef aquarium species'

    def handle(self, *args, **kwargs):
        # Data mapped perfectly to your CATEGORY_CHOICES
        species_data = [
            # FISH
            {'common_name': 'Ocellaris Clownfish', 'scientific_name': 'Amphiprion ocellaris', 'category': 'FISH'},
            {'common_name': 'Yellow Tang', 'scientific_name': 'Zebrasoma flavescens', 'category': 'FISH'},
            {'common_name': 'Blue Hippo Tang', 'scientific_name': 'Paracanthurus hepatus', 'category': 'FISH'},
            {'common_name': 'Royal Gramma', 'scientific_name': 'Gramma loreto', 'category': 'FISH'},
            {'common_name': 'Mandarinfish', 'scientific_name': 'Synchiropus splendidus', 'category': 'FISH'},
            {'common_name': 'Flame Angelfish', 'scientific_name': 'Centropyge loricula', 'category': 'FISH'},
            {'common_name': 'Six Line Wrasse', 'scientific_name': 'Pseudocheilinus hexataenia', 'category': 'FISH'},
            {'common_name': 'Banggai Cardinalfish', 'scientific_name': 'Pterapogon kauderni', 'category': 'FISH'},
            {'common_name': 'Firefish Goby', 'scientific_name': 'Nemateleotris magnifica', 'category': 'FISH'},
            
            # CORAL
            {'common_name': 'Hammer Coral', 'scientific_name': 'Euphyllia ancora', 'category': 'CORAL'},
            {'common_name': 'Torch Coral', 'scientific_name': 'Euphyllia glabrescens', 'category': 'CORAL'},
            {'common_name': 'Frogspawn Coral', 'scientific_name': 'Euphyllia divisa', 'category': 'CORAL'},
            {'common_name': 'Duncan Coral', 'scientific_name': 'Duncanopsammia axifuga', 'category': 'CORAL'},
            {'common_name': 'Zoanthids', 'scientific_name': 'Zoanthus spp.', 'category': 'CORAL'},
            {'common_name': 'Green Star Polyps', 'scientific_name': 'Pachyclavularia violacea', 'category': 'CORAL'},
            {'common_name': 'Pulsing Xenia', 'scientific_name': 'Xenia spp.', 'category': 'CORAL'},
            {'common_name': 'Montipora Cap', 'scientific_name': 'Montipora capricornis', 'category': 'CORAL'},
            
            # INVERT
            {'common_name': 'Skunk Cleaner Shrimp', 'scientific_name': 'Lysmata amboinensis', 'category': 'INVERT'},
            {'common_name': 'Peppermint Shrimp', 'scientific_name': 'Lysmata wurdemanni', 'category': 'INVERT'},
            {'common_name': 'Emerald Crab', 'scientific_name': 'Mithraculus sculptus', 'category': 'INVERT'},
            {'common_name': 'Astrea Snail', 'scientific_name': 'Astraea tecta', 'category': 'INVERT'},
            {'common_name': 'Trochus Snail', 'scientific_name': 'Trochus spp.', 'category': 'INVERT'},
            {'common_name': 'Rose Bubble Tip Anemone', 'scientific_name': 'Entacmaea quadricolor', 'category': 'INVERT'},
            
            # MACRO
            {'common_name': 'Chaetomorpha', 'scientific_name': 'Chaetomorpha linum', 'category': 'MACRO'},
            {'common_name': 'Dragon\'s Breath', 'scientific_name': 'Halymenia spp.', 'category': 'MACRO'},
            {'common_name': 'Caulerpa', 'scientific_name': 'Caulerpa prolifera', 'category': 'MACRO'},
        ]

        added_count = 0
        skipped_count = 0

        self.stdout.write('Starting database seed for Species...')

        for data in species_data:
            # We use get_or_create to prevent duplicates
            obj, created = Species.objects.get_or_create(**data)
            if created:
                added_count += 1
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(f'Success! Added {added_count} new species. Skipped {skipped_count} existing.'))
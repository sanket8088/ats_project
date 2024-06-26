# your_app/management/commands/create_test_data.py

import json
from django.core.management.base import BaseCommand
from ats.models import Candidate

class Command(BaseCommand):
    help = 'Creates sample data for Candidates model.'

    def handle(self, *args, **kwargs):
        with open('extra/test_candidates.json', 'r') as file:
            candidates = json.load(file)
        
        for candidate_data in candidates:
            try:
                Candidate.objects.create(**candidate_data)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating candidate: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully.'))

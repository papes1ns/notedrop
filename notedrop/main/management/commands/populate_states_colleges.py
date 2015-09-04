import csv
from django.core.management.base import BaseCommand, CommandError
from main.models import School


def buffer_states_from_csv(filename='data/states.csv'):
    states = {}
    with open(filename) as states_csv:
        next(states_csv, None)  # skip the header line
        cursor = csv.reader(states_csv)
        for row in cursor:
            states[row[1]] = row[0]
        states_csv.close()
    return states
            
class Command(BaseCommand):
    help = 'Import Schools'
    
    def handle(self, *args, **options):
        states = buffer_states_from_csv()
        print states
        # TODO map stats to school model

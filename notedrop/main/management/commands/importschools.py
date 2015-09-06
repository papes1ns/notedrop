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
    created_count = 0

    def handle(self, *args, **options):
        states = buffer_states_from_csv()

        with open('data/colleges.csv') as colleges_csv:
            next(colleges_csv, None)  # skip the header line
            cursor = csv.reader(colleges_csv)
            for row in cursor:
                name = row[0].replace('&', 'and').replace('\'', '').replace('-', ' ')
                obj, created = School.objects.get_or_create(
                    name=name,
                    city=row[1],
                    state=states[row[2]]
                )
                if created:
                    self.created_count += 1
            colleges_csv.close()
        print '{0} schools created'.format(self.created_count)

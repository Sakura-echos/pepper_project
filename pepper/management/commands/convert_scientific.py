from django.core.management.base import BaseCommand
from pepper.models import Sample

def scientific_to_decimal(value):
    if value is None:
        return None
    elif 'E-' in value:
        float_value = float(value)
        decimal_value = format(float_value, '.{}f'.format(abs(int(value.split('E-')[1]))))
        return decimal_value
    else:
        return value

class Command(BaseCommand):
    help = 'Converts scientific notation to decimal in the database'

    def handle(self, *args, **options):
        for sample in Sample.objects.all():
            sample.permeability_k1 = scientific_to_decimal(sample.permeability_k1)
            sample.permeability_k2 = scientific_to_decimal(sample.permeability_k2)
            sample.vesicle_number_density = scientific_to_decimal(sample.vesicle_number_density)
            sample.s_polydispersivity = scientific_to_decimal(sample.s_polydispersivity)
            sample.total_crystallinity = scientific_to_decimal(sample.total_crystallinity)
            sample.phenocrystallinity = scientific_to_decimal(sample.phenocrystallinity)
            sample.microcrystallinity = scientific_to_decimal(sample.microcrystallinity)
            sample.save()

        self.stdout.write(self.style.SUCCESS('Successfully converted scientific notation to decimal'))

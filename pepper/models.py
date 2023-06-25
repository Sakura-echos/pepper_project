from django.db import models

# Create your models here.
from django.db import models

class Sample(models.Model):
    publication = models.CharField(max_length=255)
    volcano = models.CharField(max_length=255)
    eruption = models.CharField(max_length=255)
    data_doi = models.CharField(max_length=255)
    chemistry = models.CharField(max_length=255)
    bulk_sio2 = models.CharField(max_length=255)
    bulk_na2o_k2o = models.CharField(max_length=255)
    glass_sio2 = models.CharField(max_length=255)
    glass_na2o_k2o = models.CharField(max_length=255)
    chemistry_doi = models.CharField(max_length=255)
    rock_experiment_type = models.CharField(max_length=255)
    subaerial_submarine = models.CharField(max_length=255)
    eff_exp = models.CharField(max_length=255)
    sample_no = models.CharField(max_length=255)
    bulk_porosity = models.CharField(max_length=255)
    connected_porosity = models.CharField(max_length=255)
    connectivity = models.CharField(max_length=255)
    permeability_k1 = models.CharField(max_length=255)
    permeability_k2 = models.CharField(max_length=255)
    vesicle_number_density = models.CharField(max_length=255)
    s_polydispersivity = models.CharField(max_length=255)
    total_crystallinity = models.CharField(max_length=255)
    phenocrystallinity = models.CharField(max_length=255)
    microcrystallinity = models.CharField(max_length=255)

    def __str__(self):
        return f"Sample {self.sample_no}"
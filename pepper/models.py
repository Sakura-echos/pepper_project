from django.db import models

# Create your models here.
from django.db import models

class Sample(models.Model):
    publication = models.CharField(max_length=255, blank=True)
    volcano = models.CharField(max_length=255, blank=True)
    eruption = models.CharField(max_length=255, blank=True)
    data_doi = models.CharField(max_length=255, blank=True)
    chemistry = models.CharField(max_length=255, blank=True)
    bulk_sio2 = models.CharField(max_length=255, blank=True)
    bulk_na2o_k2o = models.CharField(max_length=255, blank=True)
    glass_sio2 = models.CharField(max_length=255, blank=True)
    glass_na2o_k2o = models.CharField(max_length=255, blank=True)
    chemistry_doi = models.CharField(max_length=255, blank=True)
    rock_experiment_type = models.CharField(max_length=255, blank=True)
    subaerial_submarine = models.CharField(max_length=255, blank=True)
    eff_exp = models.CharField(max_length=255, blank=True)
    sample_no = models.CharField(max_length=255, blank=True)
    bulk_porosity = models.CharField(max_length=255, blank=True)
    connected_porosity = models.CharField(max_length=255, blank=True)
    connectivity = models.CharField(max_length=255, blank=True)
    permeability_k1 = models.CharField(max_length=255, blank=True)
    permeability_k2 = models.CharField(max_length=255, blank=True)
    vesicle_number_density = models.CharField(max_length=255, blank=True)
    s_polydispersivity = models.CharField(max_length=255, blank=True)
    total_crystallinity = models.CharField(max_length=255, blank=True)
    phenocrystallinity = models.CharField(max_length=255, blank=True)
    microcrystallinity = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Sample {self.sample_no}"

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    permission = models.IntegerField(default=1)
    token = models.CharField(max_length=255, null=True)

    def __init__(self, username, password, permission=1, token=None, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.permission = permission
        self.token = token

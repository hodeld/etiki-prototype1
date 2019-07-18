from django.db import models
from django.contrib.auth import get_user_model


class Country (models.Model):
    name = models.CharField(unique = True,  max_length=15)
    alpha3code = models.CharField(unique = True, verbose_name='alpha-3-code', max_length=3)
    def __str__(self):
        return self.name
    
class ActivityCategory  (models.Model):
    name = models.CharField(unique = True,  max_length=15)
    def __str__(self):
        return self.name
    
class Company (models.Model):
    name = models.CharField(unique = True, verbose_name='CompanyName', max_length=15)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Media (models.Model):
    name = models.CharField(unique = True, verbose_name='MediaType', max_length=15)
    def __str__(self):
        return self.name
        
class Reference (models.Model):
    name = models.CharField(unique = True, verbose_name='ReferenceName', max_length=15)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class SustainabilityCategory (models.Model):
    name = models.CharField(unique = True,  max_length=15)
    name_long = models.CharField(unique = True,  max_length=50)
    def __str__(self):
        return self.name

class SustainabilityTag (models.Model):
    name = models.CharField(unique = True,  max_length=15)
    name_long = models.CharField(unique = True,  max_length=50)
    def __str__(self):
        return self.name
      
class ImpactEvent (models.Model):
    created_at = models.DateTimeField(auto_now_add=True) #tz aware datetime
    updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True,null=True)
    
    date_impact = models.DateField()
    date_published = models.DateField(verbose_name='Date IE published')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    sust_categories = models.ForeignKey(SustainabilityCategory, on_delete=models.CASCADE)
    sust_tags = models.ManyToManyField('SustainabilityTag', blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    source_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
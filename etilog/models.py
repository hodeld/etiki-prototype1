from django.db import models
from django.contrib.auth import get_user_model


class Country (models.Model):
    numeric = models.PositiveSmallIntegerField(unique = True)
    name = models.CharField(unique = True,  max_length=15)
    alpha2code = models.CharField(unique = True, verbose_name='alpha-2-code', max_length=2)
    alpha3code = models.CharField(unique = True, verbose_name='alpha-3-code', max_length=3)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
    
class ActivityCategory  (models.Model):
    name = models.CharField(unique = True,  max_length=15)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
    
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
    class Meta:
        ordering = ['name', ]
        
class Reference (models.Model):
    name = models.CharField(unique = True, verbose_name='ReferenceName', max_length=15)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
        
class SustainabilityDomain (models.Model):
    impnr = models.PositiveSmallIntegerField(verbose_name='Import Number', blank=True,null=True)
    name = models.CharField(unique = True,  max_length=15)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
           
class SustainabilityCategory (models.Model):
    
    impnr = models.PositiveSmallIntegerField(verbose_name='Import Number', blank=True,null=True)
    name = models.CharField(unique = True,  max_length=15)
    name_long = models.CharField(unique = True,  max_length=50)
    sust_domain = models.ForeignKey(SustainabilityDomain, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]

class SustainabilityTag (models.Model):
    impnr = models.PositiveSmallIntegerField(verbose_name='Import Number', blank=True,null=True)
    name = models.CharField(unique = True,  max_length=35)
    sust_categories = models.ManyToManyField('SustainabilityCategory', blank=True)
    description = models.CharField(max_length=200, blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
      
class ImpactEvent (models.Model):
    created_at = models.DateTimeField(auto_now_add=True) #tz aware datetime
    updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True,null=True)
    
    date_impact = models.DateField()
    date_published = models.DateField(verbose_name='Date IE published')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    sust_category = models.ForeignKey(SustainabilityCategory, on_delete=models.CASCADE)
    sust_tags = models.ManyToManyField('SustainabilityTag', blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    source_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        name_str = self.company.name[:10] + '_' + self.date_impact.strftime('%y') + '_' + self.sust_category.name
        return name_str
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('admin:etilog_impactevent_change', args=(self.pk,))
    
    class Meta:
        ordering = ['date_impact', 'company']

    
    
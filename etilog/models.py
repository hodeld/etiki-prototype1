from django.db import models
from django.contrib.auth import get_user_model


class Country (models.Model):
    numeric = models.PositiveSmallIntegerField(unique = True)
    name = models.CharField(unique = True,  max_length=100)
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
    
    name = models.CharField(unique = True, verbose_name='CompanyName', max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
    
class Media (models.Model):
    name = models.CharField(unique = True, verbose_name='MediaType', max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
        verbose_name = 'medium'
        
class Reference (models.Model):
    name = models.CharField(unique = True, verbose_name='ReferenceName', max_length=50)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True,null=True, help_text = 'optional')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True,null=True)
    comment = models.CharField(max_length=200, blank=True,null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]

class Source(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) #tz aware datetime
    url = models.URLField()        
    comment = models.CharField(blank=True, null=True, max_length=200)
    def __str__(self):
        url_str = str(self.url)[:50]
        if self.comment:
            
            return self.comment + ': ' + url_str
        else:
            return url_str
    
class SustainabilityDomain (models.Model):
    impnr = models.PositiveSmallIntegerField(verbose_name='Import Number', blank=True,null=True)
    name = models.CharField(unique = True,  max_length=30)
    comment = models.CharField(max_length=200, blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
           
class SustainabilityCategory (models.Model):
    
    impnr = models.PositiveSmallIntegerField(verbose_name='Import Number', blank=True,null=True)
    name = models.CharField(unique = True,  max_length=40)
    name_long = models.CharField(unique = True,  max_length=50)
    sust_domain = models.ForeignKey(SustainabilityDomain, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]

class SustainabilityTag (models.Model):
    impnr = models.PositiveSmallIntegerField(verbose_name='Import Number', blank=True,null=True)
    name = models.CharField(unique = True,  max_length=35)
    sust_categories = models.ManyToManyField('SustainabilityCategory', blank=True)
    description = models.CharField(max_length=200, blank=True,null=True)
    comment = models.CharField(max_length=200, blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
      
class ImpactEvent (models.Model):
    created_at = models.DateTimeField(auto_now_add=True) #tz aware datetime
    updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True,null=True)
    
    date_published = models.DateField(verbose_name='Date IE published', 
                                      help_text = 'First time published. If only year is known put 1st of jan')
    date_impact = models.DateField(blank=True,null=True, help_text = 'optional date of impact')
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)   
       
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    sust_category = models.ForeignKey(SustainabilityCategory, on_delete=models.CASCADE)
    sust_tags = models.ManyToManyField('SustainabilityTag', blank=True)
    
    source_url = models.URLField(blank=True, null=True)
    sources = models.ManyToManyField('Source', blank=True, verbose_name = 'further sources', 
                                     related_name = 'impevents') #get Source.impevents.all()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)    
    
    summary = models.CharField(max_length=500, blank=True,null=True, 
                               help_text = 'abstract, title or first part of text')
    comment = models.CharField(max_length=500, blank=True,null=True)
    
    
    def __str__(self):
        name_str = self.company.name[:10] + '_' + self.date_published.strftime('%y') + '_' + self.sust_category.name
        return name_str
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('admin:etilog_impactevent_change', args=(self.pk,))
    
    @property
    def all_tags(self):
        return ', '.join([x.name for x in self.sust_tags.all()])
  
    class Meta:
        ordering = ['date_impact', 'company']

    
    
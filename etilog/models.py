from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re


def full_domain_validator(hostname):
    """
    Fully validates a domain name as compilant with the standard rules:
        - Composed of series of labels concatenated with dots, as are all domain names.
        - Each label must be between 1 and 63 characters long.
        - The entire hostname (including the delimiting dots) has a maximum of 255 characters.
        - Only characters 'a' through 'z' (in a case-insensitive manner), the digits '0' through '9'.
        - Labels can't start or end with a hyphen.
    """
    HOSTNAME_LABEL_PATTERN = re.compile("(?!-)[A-Z\d-]+(?<!-)$", re.IGNORECASE)
    if not hostname:
        return
    if len(hostname) > 255:
        raise ValidationError(("The domain name cannot be composed of more than 255 characters."))
    if hostname[-1:] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    for label in hostname.split("."):
        if len(label) > 63:
            raise ValidationError(
                _("The label '%(label)s' is too long (maximum is 63 characters).") % {'label': label})
        if not HOSTNAME_LABEL_PATTERN.match(label):
            raise ValidationError(("Unallowed characters in label '%(label)s'.") % {'label': label})
        
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
    
    name = models.CharField(unique = True, max_length=50)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    activity = models.ForeignKey(ActivityCategory, on_delete=models.PROTECT)
    domain = models.CharField(max_length=255, validators=[full_domain_validator], blank = True, null = True, help_text = 'companydomain.com')
    subsidiary_old = models.ManyToManyField('self', blank=True, verbose_name='owns', related_name = 'owner2')
    owner_old = models.ManyToManyField('self', blank=True, verbose_name='owned by')    
    supplier_old = models.ManyToManyField('self', blank=True, verbose_name='supplied by')  #verbose name was wrong
    recipient_old = models.ManyToManyField('self', blank=True, verbose_name='delivers to') #verbose name was wrong
    
    subsidiary_to_owner = models.ManyToManyField('self', blank=True, 
                                                 through='SubsidiaryOwner',
                                                 through_fields=('subsidiary_company', 'owner_company'),
                                                 symmetrical=False,
                                                 related_name='owner_to_subsidiary'
                                                 )
    supplier_to_recipient = models.ManyToManyField('self', blank=True, 
                                                 through='SupplierRecipient',
                                                 through_fields=('supplier_company', 'recipient_company'),
                                                 symmetrical=False,
                                                 related_name='recipient_to_supplier'
                                                 )
    
    comment = models.CharField(max_length=200, blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
        verbose_name = 'Organisation'

class SubsidiaryOwner(models.Model):   
    created_at = models.DateTimeField(auto_now_add=True) #tz aware datetime
    active = models.BooleanField(default = True)
    owner_company = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                      related_name='owner_company',
                                      verbose_name='owned by')    
    subsidiary_company = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                           related_name='subsidiary_company',                                          
                                          verbose_name='owns')
    
    def __str__(self):
        return self.subsidiary_company.name+'_ownedby_'+self.owner_company.name

class SupplierRecipient(models.Model):   
    created_at = models.DateTimeField(auto_now_add=True) #tz aware datetime
    active = models.BooleanField(default = True)
    recipient_company = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                      related_name='recipient_company',
                                      verbose_name='delivers to')    
    supplier_company = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                           related_name='supplier_company',                                          
                                          verbose_name='supplied by')
    
    def __str__(self):
        return self.supplier_company.name+'_suppliesto_'+self.recipient_company.name
    
     
class Media (models.Model):
    name = models.CharField(unique = True, verbose_name='MediaType', max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', ]
        verbose_name = 'medium'
        
class Reference (models.Model):
    name = models.CharField(unique = True, verbose_name='ReferenceName', max_length=50)
    mediaform = models.ForeignKey(Media, on_delete=models.PROTECT, default = 1) #newspaper
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True,null=True, help_text = 'optional')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True,null=True,
                                related_name = 'reference')
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
        
class SustainabilityTendency (models.Model):
    impnr = models.PositiveSmallIntegerField(verbose_name='Import Number', blank=True,null=True)
    name = models.CharField(unique = True,  max_length=30)
    comment = models.CharField(max_length=200, blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-name', ]
           
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
    sust_domains = models.ManyToManyField('SustainabilityDomain', blank=True)
    sust_tendency = models.ForeignKey(SustainabilityTendency, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True,null=True)
    comment = models.CharField(max_length=200, blank=True,null=True)
    def __str__(self):
        return self.name
    
    @property
    def get_categories(self):
        return '; '.join([x.name for x in self.sust_categories.all()])
    
    @property
    def get_domains(self):
        return '; '.join([x.name for x in self.sust_domains.all()])
    
    class Meta:
        ordering = ['name', ]
      
class ImpactEvent (models.Model):
    choices_res_html = [(0, 'not parsed'), 
                        (1, 'success'),
                        (2, 'error'),
                        (3, 'PDF'),
                        (4, 'ConnErr'),
                        (5, 'readabErr'),
                        (6, 'emptyText'), 
                        (7, 'timeout'), 
                        (8, 'doublepara'), 
                        (9, 'longtext'),
                        (10, 'inlongp'),
                        (11, 'parsed manually')                        
                       ]
    
    
    created_at = models.DateTimeField(auto_now_add=True) #tz aware datetime
    updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True,null=True)
    
    date_published = models.DateField(verbose_name='Date IE published', 
                                      help_text = 'First time published. If only year is known put 1st of jan')
    date_impact = models.DateField(blank=True,null=True, help_text = 'optional date of impact')
    date_text = models.CharField(max_length=100, blank=True,null=True)
    
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name = 'impevents')   
       
    reference = models.ForeignKey(Reference, on_delete=models.PROTECT)
    sust_category = models.ForeignKey(SustainabilityCategory, on_delete=models.SET_NULL, blank=True,null=True) #will be deleted
    sust_tags = models.ManyToManyField('SustainabilityTag', blank=True)
    sust_domain = models.ForeignKey(SustainabilityDomain, on_delete=models.PROTECT) 
    sust_tendency = models.ForeignKey(SustainabilityTendency, on_delete=models.PROTECT) #todo:on_delete=models.CASCADE)
    
    source_url = models.URLField(blank=True, null=True)
    sources = models.ManyToManyField('Source', blank=True, verbose_name = 'further sources', 
                                     related_name = 'impevents') #get Source.impevents.all()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)    
    
    summary = models.CharField(max_length=500, blank=True,null=True, 
                               help_text = 'abstract, title or first part of text')
    comment = models.CharField(max_length=500, blank=True,null=True)
    article_text = models.TextField(blank=True, null=True)
    article_title = models.CharField(max_length=150, blank=True, null=True)
    article_html = models.TextField(blank=True, null=True)
    result_parse_html = models.PositiveSmallIntegerField(choices = choices_res_html, default = 0)
    
    
    def __str__(self):
        name_str = self.company.name[:10] + '_' + self.date_published.strftime('%y') + '_' + self.sust_domain.name + '_' + self.sust_tendency.name
        return name_str
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('admin:etilog_impactevent_change', args=(self.pk,))
    
    @property
    def get_tags(self):
        return ', '.join([x.name for x in self.sust_tags.all()])
    
    @property
    def date_display(self):
        if self.date_impact:
            value = self.date_impact
        else:
            value = self.date_published
        return  value
    
    @property
    def country_display(self):
        if self.country:
            value = self.country
        else:
            value = self.company.country
        return  value
    
    @property
    def summary_display(self):
        if self.summary:
            value = self.summary
        else:
            value = self.article_title
        return  value
    
    
    class Meta:
        ordering = ['date_impact', 'company']

    
    
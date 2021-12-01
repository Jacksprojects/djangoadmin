from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import SlugField
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from ckeditor.fields import RichTextField
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField, ProcessedImageField
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager

# Choices for post status:
DRAFT = 'DR'
PUBLISHED = 'PB'
options = (
	(DRAFT, _('Draft')),
	(PUBLISHED, _('Published')),
)

class Organization(models.Model):
    """
    An organization object.
    """
    name = models.CharField(_("Nom de l'organisation"), max_length = 150)
    slug = SlugField(_("Slug"), unique=True)
    date_created = models.DateField(_("Date de création"))
    
    logo = ProcessedImageField(
        upload_to='organization/logo',
        processors=[ResizeToFill(150,150)],
        format='JPEG',
        options={'quality':90},
        null=True,
        blank=True
    )

    cover_image = ProcessedImageField(
        upload_to='organization/cover_image',
        processors=[ResizeToFill(900,500)],
        format='JPEG',
        options={'quality':80},
        null=True,
        blank=True
    )

    address = models.TextField(_("Adresse de la rue"))
    email = models.EmailField(_("Adresse e-mail"))
    fax = PhoneNumberField(_("Numéro de fax"))
    phone = PhoneNumberField(_("Numéro de téléphone"))

    extract = models.TextField(_("Extrait"), max_length = 300, blank=True, null=True)
    content = RichTextField(_("Contenu"), blank=True, null = True)
    tags = TaggableManager()

    author = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, editable=False)
    status = models.CharField(
		_("statut de l'organisation"), max_length=10, choices=options, default='DR'
    )

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')
        ordering = ('-name', )


    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organization-detail', kwargs = {'slug':self.slug})
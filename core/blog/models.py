from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import SlugField
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

# Choices for post status:
DRAFT = 'DR'
PUBLISHED = 'PB'
options = (
	(DRAFT, _('Draft')),
	(PUBLISHED, _('Published')),
)

class Post(models.Model):
	"""
	A blog post object.
	"""
	title = models.CharField(_("Titre"), max_length = 150)
	slug = SlugField(_("Slug"), unique=True)
	extract = models.TextField(_("Extrait"), max_length = 300, blank=True, null=True)
	content = RichTextField(_("Contenu"), blank=True, null = True)
	date_posted = models.DateTimeField(_("Date de publication"), default=timezone.now)
	last_modified = models.DateTimeField(_("Dernière modification"), auto_now=True)
	author = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, editable=False)
	tags = TaggableManager()
	status = models.CharField(
		_('Statut du poste'), max_length=10, choices=options, default='DR'
    )

	class Meta:
		verbose_name = _('Blog Post')
		verbose_name_plural = _('Blog Posts')
		ordering = ('-date_posted', )


	def save(self, *args, **kwargs):
		self.slug = self.slug or slugify(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs = {'slug':self.slug})
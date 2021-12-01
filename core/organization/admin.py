from django.utils.translation import ngettext
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin, messages
from django import forms
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from . import models
from blog.admin import user_admin_site, moderator_admin_site

DETAIL_DESCRIPTION = _('Cette section traite des informations de base sur votre organisation')
CONTACT_DESCRIPTION = _('Cette section concerne les coordonnées de votre organisation')
CONTENT_DESCRIPTION = _('Cette section porte sur le contenu de la page de profil de votre organisation.')
STATUS_DESCRIPTION = _("Votre article est-il publié ou à l'état de projet ?")

class OrganizationResource(resources.ModelResource):

    class Meta:
        model = models.Organization


# Create Organization model form in the admin
class ModeratorOrganizationAdmin(ImportExportModelAdmin):
    resource_class = OrganizationResource
    list_display = ['name', 'author', 'email', 'date_created', 'status']
    list_filter = ['status']
    search_fields = ['name']

    # Custom admin actions
    actions = ['make_published', 'make_draft']
    
    @admin.action(description=_('Marquer les articles sélectionnés comme publiés'))
    def make_published(self, request, queryset):
        updated = queryset.update(status='PB')
        self.message_user(request, ngettext(
            '%d article a été marqué avec succès comme publié.',
            '%d articles ont été marqués comme publiés avec succès.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description=_('Marquer les articles sélectionnés comme brouillons'))
    def make_draft(self, request, queryset):
        updated = queryset.update(status='DR')
        self.message_user(request, ngettext(
            '%d article a été marqué avec succès comme brouillon.',
            '%d les articles ont été marqués avec succès comme brouillon.',
            updated,
        ) % updated, messages.SUCCESS)

class UserOrganizationAdmin(ImportExportModelAdmin):
    resource_class = OrganizationResource
    list_display = ['name', 'email', 'date_created']
    search_fields = ['name']
    exclude = ['status']

    # Form composition
    fieldsets = (
        (_('Details'), {
            'fields': [('name', 'slug'), 'date_created', ('logo', 'cover_image'), 'tags'],
            'description': f'{DETAIL_DESCRIPTION}'
        }),
        (_('Content'), {
            'fields': [ 'extract', 'content'],
            'description': f'{CONTENT_DESCRIPTION}',
            'classes': ['wide']
        }),
        (_('Contact Details'), {
            'fields': ['address', 'email', 'fax', 'phone'],
            'description': f'{CONTACT_DESCRIPTION}',
            'classes': ['collapse']
        })
    )

    def get_queryset(self, request):
        qs = super(UserOrganizationAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='user').exists():
            qs = qs.filter(author = request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return True
    
    # Prevent users from creating more than one organization
    def has_add_permission(self, request):
        if request.user.groups.filter(name='user').exists():
            qs = super(UserOrganizationAdmin, self).get_queryset(request)
            qs = qs.filter(author = request.user)
            count = qs.count()
            
            if count >= 1:
                return False
            else:
                return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='user').exists():
            return obj is None or obj.author == request.user
        else:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='user').exists():
            return obj is None or obj.author == request.user
        else:
            return False

# Register models
admin.site.register(models.Organization)
moderator_admin_site.register(models.Organization, ModeratorOrganizationAdmin)
user_admin_site.register(models.Organization, UserOrganizationAdmin)
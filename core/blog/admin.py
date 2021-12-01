from django.utils.translation import ngettext
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin, messages
from django.contrib.admin.forms import AuthenticationForm
from django import forms
from . import models

from import_export.admin import ImportExportModelAdmin

# Create admin areas for users and moderators
class ModeratorAdminArea(admin.AdminSite):
    """
    Admin area for site moderators.
    """
    login_form = AuthenticationForm
    site_header = _('Content Moderation Area')
    site_title = _('Content Moderation Area')

    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        if request.user.groups.filter(name='moderator').exists():
            return True
        else: return False

class UserAdminArea(admin.AdminSite):
    """
    Admin area for site users.
    """
    login_form = AuthenticationForm
    site_header = _('Content Creation Area')
    site_title = _('Content Creation Area')

    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        if request.user.groups.filter(name='user').exists():
            return True
        else: return False


## Create Post model form in the admin
class ModeratorPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_posted', 'status']
    list_filter = ['author', 'status']

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


class UserPostAdmin(ImportExportModelAdmin):
    list_display = ['title', 'date_posted']
    exclude = ['status']
    filter_horizontal = ('tags',)
    group_fieldsets = True
    # Form composition
    fieldsets = (
        (_('Details'), {
            'fields': ['title', 'slug', 'tags', 'date_posted'],
        }),
        (_('Content'), {
            'fields': [ 'extract', 'content'],
            'classes': ['wide']
        }),
    )

    def get_queryset(self, request):
        qs = super(UserPostAdmin, self).get_queryset(request)
        if request.user.groups.filter(name='user').exists():
            qs = qs.filter(author = request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return True
    
    def has_add_permission(self, request):
        return True

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


# Register admin areas for users, moderators
moderator_admin_site = ModeratorAdminArea(name='ModeratorAdmin')
user_admin_site = UserAdminArea(name='UserAdmin')

# Register models with admin areas for users, moderators and admins
admin.site.register(models.Post)
moderator_admin_site.register(models.Post, ModeratorPostAdmin)
user_admin_site.register(models.Post, UserPostAdmin)

# Customize the global admin
admin.site.site_header = _('Admin Area')
admin.site.site_title = _('Admin Area')
from django.contrib import admin
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from .models import Webhook


class WebhookAdmin(admin.ModelAdmin):
    actions = ['register', 'delete']

    class Meta:
        model = Webhook

    def get_actions(self, request):
        actions = super(WebhookAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def register(self, request, queryset):
        queryset.register()
        name_plural = force_text(self.model._meta.verbose_name_plural)
        self.message_user(request, _("Register selected %s" % name_plural))
    register.short_description = ugettext_lazy("Register selected %(verbose_name_plural)s")

    def delete(self, request, queryset):
        """
        A custom delete action that explicitly calls delete() for each
        object. This causes the deletion API call to be fired.
        """
        for webhook in queryset:
            webhook.delete()
        name_plural = force_text(self.model._meta.verbose_name_plural)
        self.message_user(request, _("Deleted selected %s" % name_plural))
    delete.short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")


admin.site.register(Webhook, WebhookAdmin)

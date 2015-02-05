from django.contrib import admin
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from .models import Webhook


class WebhookAdmin(admin.ModelAdmin):
    actions = ['create', 'remove']

    class Meta:
        model = Webhook

    def get_actions(self, request):
        actions = super(WebhookAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def create(self, request, queryset):
        for webhook in queryset:
            webhook.create()
        name_plural = force_text(self.model._meta.verbose_name_plural)
        self.message_user(request, _("Created selected %s" % name_plural))
    create.short_description = ugettext_lazy("Create selected %(verbose_name_plural)s")

    def remove(self, request, queryset):
        for webhook in queryset:
            webhook.delete()
        name_plural = force_text(self.model._meta.verbose_name_plural)
        self.message_user(request, _("Deleted selected %s" % name_plural))
    remove.short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")


admin.site.register(Webhook, WebhookAdmin)

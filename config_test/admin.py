from django.contrib import admin
from feincms.admin import item_editor, tree_editor
from models import Page
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.templatetags.staticfiles import static

class PageAdmin(tree_editor.TreeEditor):
    fieldsets = [
        (None, {
            'fields': ['active', 'title'],
            }),
        ]
    list_display = ['active', 'title']
    raw_id_fields = ['parent']
    search_fields = ['title']

    def _actions_column(self, page):
        actions = super(PageAdmin, self)._actions_column(page)

        actions.append(
            '<a href="add/?parent=%s" title="%s">'
                    '<img src="%s" alt="%s" />'
                    '</a>' % (
                        page.pk,
                        _('Add child page'),
                        static('feincms/img/icon_addlink.gif'),
                        _('Add child page'),
                    )
                )
        return actions

    def response_add(self, request, obj, *args, **kwargs):
        response = super(PageAdmin, self).response_add(
            request, obj, *args, **kwargs)
        if ('parent' in request.GET
                and '_addanother' in request.POST
                and response.status_code in (301, 302)):
            # Preserve GET parameters if we are about to add another page
            response['Location'] += '?parent=%s' % request.GET['parent']

        return response

    def save_model(self, request, obj, form, change):
        if 'parent' in request.GET:
            obj.parent_id = request.GET['parent']
        obj.save()

admin.site.register(Page, PageAdmin)

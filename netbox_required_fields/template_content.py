"""
netbox_required_fields.template_content

Injects a small JS file into the <head> of an object's add/edit page when
the current model is listed in PLUGINS_CONFIG['netbox_required_fields']
['required_fields']. The script marks the listed fields' labels as required.

The current model is determined from request.resolver_match, since the
extension is registered globally (models = None) and is invoked on every
page - filtering by model happens here.

view_name format for core models (confirmed by NetBox's
utilities/views.py, get_viewname()):
    "{app_label}:{model_name}_{action}"
    e.g.: "dcim:site_add", "dcim:location_edit"

Third-party PLUGIN models get an extra namespace level - netbox/urls.py
wraps every plugin's URLs under "plugins" via
include((plugin_patterns, 'plugins')):
    "plugins:{plugin_name}:{model_name}_{action}"
    e.g.: "plugins:netbox_attachments:netboxattachment_add"
"""
from django.apps import apps
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from netbox.plugins import PluginTemplateExtension
from netbox.plugins.utils import get_plugin_config

_FORM_ACTION_SUFFIXES = ('_add', '_edit')


def _get_required_fields_map():
    """Read {model: [fields]} from PLUGINS_CONFIG (configuration.py)."""
    fields_map = get_plugin_config('netbox_required_fields', 'required_fields', default={})
    return fields_map or {}


class RequiredFieldsInjection(PluginTemplateExtension):
    # models = None -> this extension is registered globally; head() is
    # called on every page, so model filtering happens inside head().
    models = None

    def _get_current_model(self):
        """
        Determine app_label.model_name of the current page from the view
        name. Returns None if this isn't a create/edit form for a model.
        """
        request = self.context.get('request')
        if request is None:
            return None

        match = getattr(request, 'resolver_match', None)
        if match is None:
            return None

        view_name = match.view_name or ''
        for suffix in _FORM_ACTION_SUFFIXES:
            if view_name.endswith(suffix):
                base = view_name[:-len(suffix)]
                parts = base.split(':')
                # Plugin model: "plugins:{plugin_name}:{model_name}".
                if len(parts) == 3 and parts[0] == 'plugins':
                    app_label, model_name = parts[1], parts[2]
                # Core model: "{app_label}:{model_name}".
                elif len(parts) == 2:
                    app_label, model_name = parts
                else:
                    continue
                if app_label and model_name:
                    return f'{app_label}.{model_name}'
        return None

    def head(self):
        current_model = self._get_current_model()
        if current_model is None:
            return ''

        fields = _get_required_fields_map().get(current_model)
        if not fields:
            return ''

        script_url = static('netbox_required_fields/required-fields.js') + '?v=' + self._plugin_version()
        return mark_safe(
            '<script src="{url}" defer data-fields="{fields}"></script>'.format(
                url=script_url,
                fields=','.join(fields),
            )
        )

    @staticmethod
    def _plugin_version():
        """Plugin version from its AppConfig - used to cache-bust the static file."""
        try:
            return apps.get_app_config('netbox_required_fields').version or '0'
        except LookupError:
            return '0'


template_extensions = [RequiredFieldsInjection]

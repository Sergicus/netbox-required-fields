"""
netbox_required_fields

A small NetBox plugin that visually flags form fields as required when they
are enforced by server-side logic (CUSTOM_VALIDATORS, a custom form/model
clean(), etc.) but declared required=False on the Django ModelForm, so NetBox
core doesn't bold/asterisk them on its own. Purely a client-side hint -
no validation behaviour is added, changed, or bypassed.
"""
from netbox.plugins import PluginConfig


class RequiredFieldsConfig(PluginConfig):
    name = 'netbox_required_fields'
    verbose_name = 'Required Fields Highlighter'
    description = (
        'Marks form fields as required (using NetBox\'s own required-field '
        'styling) when they are enforced by custom validation but not by '
        'the Django form itself.'
    )
    version = '0.1.0'
    author = 'Serge G.'
    min_version = '4.6.0'
    max_version = '4.7.99'

    # Mapping of "app_label.model_name" -> list of form field names to mark
    # as required. See README.md for details and examples.
    default_settings = {
        'required_fields': {},
    }


config = RequiredFieldsConfig

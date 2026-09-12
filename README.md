# netbox-required-fields

A [NetBox](https://github.com/netbox-community/netbox) plugin that visually
marks form fields as required when they're enforced by your own validation
logic, but not by the underlying Django form.

## The problem

NetBox's own form rendering only bolds a field's label and adds the
required-field asterisk icon when the field is `required=True` on the
Django `ModelForm`. If you additionally enforce a field through
[`CUSTOM_VALIDATORS`](https://netboxlabs.com/docs/netbox/en/stable/customization/custom-validation/)
(or a custom form/model `clean()`), that field still renders exactly like an
optional one - users only find out it's required after they hit *Save* and
get a validation error.

## What it does

For fields you list in `PLUGINS_CONFIG`, on the add/edit page of the
corresponding model, this plugin adds NetBox's own `.required` CSS class to
the field's label - the same bold text + asterisk icon a genuinely
`required=True` field gets. That's it.

This is a purely cosmetic, client-side hint. It does not add, remove, or
bypass any validation - you still need to enforce the rule server-side
(`CUSTOM_VALIDATORS`, a form/model `clean()`, etc.). This plugin only makes
sure the user finds out about the requirement before submitting the form,
not after.

## Compatibility

| NetBox version | Plugin version |
| --------------- | --------------- |
| 4.6 - 4.7       | 0.1.x           |

## Installation

Install directly from GitHub into your NetBox virtual environment:

```bash
pip install git+https://github.com/Sergicus/netbox-required-fields.git
```

Enable it and configure which fields to mark in `configuration.py`:

```python
PLUGINS = [
    # ...
    "netbox_required_fields",
]

PLUGINS_CONFIG = {
    "netbox_required_fields": {
        "required_fields": {
            "dcim.site": ["tenant"],
            "dcim.rack": ["role"],
            "dcim.device": ["platform"],
        },
    },
}
```

<img width="760" height="971" alt="image" src="https://github.com/user-attachments/assets/069cbf6f-441d-4f3b-be6a-9e6a59608e2d" />


Then collect static files and restart NetBox:

```bash
python manage.py collectstatic --no-input
```

(Restart `netbox` and `netbox-rq`/`netbox-housekeeping` services, or your
container, as usual after a plugin change.)

If you're installing this alongside other plugins, add
`"netbox_required_fields"` to your existing `PLUGINS` list rather than
replacing it, and merge `"netbox_required_fields"` into your existing
`PLUGINS_CONFIG` dict.

## Configuration

The only setting is `required_fields`: a mapping of `"app_label.model_name"`
(lowercase, the same string NetBox itself uses in URLs and in
`CUSTOM_VALIDATORS`) to a list of form field names to mark as required.

Field names are the form field's own name (i.e. what you'd see in the
rendered `<select name="...">`/`<input name="...">`), which is usually the
same name you already pass to a validator like
`RequiredFieldsValidator(['tenant', 'role'])`. Only models present in this
dict are touched - everything else is left untouched.

### Field name mapping notes

A couple of NetBox fields aren't rendered as a single simple `<select>` or
`<input>`, so the name to put in the config differs slightly from the
model attribute your validator checks:

- **Generic-object ("scope") fields** - e.g. `Prefix.scope_type` /
  `VLANGroup.scope_type` are validated as a model attribute, but the form
  renders a single combined field named `scope` (content type + object
  pickers together). Use `"scope"` in the config, not `"scope_type"`.

If a field doesn't get marked and you're not sure why, check the rendered
HTML for the field's actual `name=`/`id=` attribute.

## How it works

The plugin registers a global `PluginTemplateExtension` (NetBox's supported
hook for injecting markup into `<head>`). On every request, it checks
whether the current page is an add/edit form for a model listed in
`required_fields`; if so, it injects one small `<script>` tag with the
field list passed through a `data-fields` attribute. The script itself just
finds each field's `<label>` and adds the `required` class - it accounts
for plain fields, TomSelect-enhanced fields, and compound (generic-object)
fields. No NetBox core template, view, or form is modified.

## Limitations

- Purely cosmetic - it does not perform or trigger any validation itself.
- If a field's label isn't associated via the standard `<label for="...">`
  mechanism (e.g. a fully custom widget), the script has nothing to attach
  the `required` class to and silently does nothing for that field.

## License

[MIT](LICENSE)

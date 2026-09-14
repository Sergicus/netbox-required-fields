# Changelog

## [0.1.1] - 2026-09-14

### Fixed

- Fields on third-party plugin models (e.g. `netbox_attachments.netboxattachment`)
  were never marked as required. NetBox wraps every plugin's URLs under an
  extra `plugins:` namespace level (`plugins:{plugin_name}:{model_name}_add`),
  which the model-detection logic didn't account for - it only handled the
  single-level namespace core models use (`{app_label}:{model_name}_add`),
  so the field-name lookup in `required_fields` always missed for plugin
  models and no script was injected at all.

## [0.1.0] - 2026-09-12

### Added

- Initial public release.
- `PLUGINS_CONFIG["netbox_required_fields"]["required_fields"]`: a mapping
  of `app_label.model_name` to a list of form field names to mark as
  required.
- Marks configured fields' labels with NetBox's native `.required` CSS
  class (bold text + asterisk icon), matching the styling of genuinely
  required fields.
- Handles plain fields, TomSelect-enhanced fields (`-ts-control` id
  suffix), and compound `MultiValueField`/generic-object fields (`_0` id
  suffix, e.g. a GFK "scope" selector).

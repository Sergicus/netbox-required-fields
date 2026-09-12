# Changelog

## [0.1.0] - 2026-09-12

### Added

- Initial public release, extracted from the internal `auto_name` plugin.
- `PLUGINS_CONFIG["netbox_required_fields"]["required_fields"]`: a mapping
  of `app_label.model_name` to a list of form field names to mark as
  required.
- Marks configured fields' labels with NetBox's native `.required` CSS
  class (bold text + asterisk icon), matching the styling of genuinely
  required fields.
- Handles plain fields, TomSelect-enhanced fields (`-ts-control` id
  suffix), and compound `MultiValueField`/generic-object fields (`_0` id
  suffix, e.g. a GFK "scope" selector).

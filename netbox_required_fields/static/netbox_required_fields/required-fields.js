/**
 * netbox_required_fields / required-fields.js
 */
(function () {
  'use strict';

  function getOwnScript() {
    return document.currentScript ||
      Array.prototype.slice.call(document.scripts).filter(function (s) {
        return s.src && s.src.indexOf('required-fields.js') !== -1;
      })[0];
  }

  function markRequired(fieldName) {
    var label = document.querySelector(
      'label[for="id_' + fieldName + '"],' +
      'label[for="id_' + fieldName + '-ts-control"],' +
      'label[for="id_' + fieldName + '_0"]'
    );
    if (label) {
      label.classList.add('required');
    }
  }

  function init() {
    var script = getOwnScript();
    var fieldsAttr = script && script.getAttribute('data-fields');
    if (!fieldsAttr) {
      return;
    }
    fieldsAttr.split(',').forEach(function (fieldName) {
      fieldName = fieldName.trim();
      if (fieldName) {
        markRequired(fieldName);
      }
    });
  }

  document.addEventListener('DOMContentLoaded', init);
  // Re-run after HTMX swaps (e.g. a quick-add modal re-rendering the form).
  document.addEventListener('htmx:afterSettle', init);
})();

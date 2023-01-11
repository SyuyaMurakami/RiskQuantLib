#% import 'macro.pyt' as macro %#
#%- for instrumentName, inheritTree in shortcutList -%#
{{ macro.shortcut(instrumentName,inheritTree) }}
#% endfor %#
#%- import 'macro.pyt' as macro -%#
#->module@moduleAutoImport
#%- for instrumentName in instrumentNameList %#
{{ macro.shortcut(instrumentName, instrumentInheritTreeSeries[loop.index0]) }}
#%- endfor %#

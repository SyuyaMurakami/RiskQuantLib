#%- import 'macro.pyt' as macro -%#
#%- set var = namespace(parentListAutoClassNameList = []) -%#
#%- for parentInstrumentName in parentInstrumentNameSeries -%#
#%- set var.parentListAutoClassNameList = var.parentListAutoClassNameList + [macro.instrumentListAutoClassName(parentInstrumentName)] -%#
#%- endfor -%#
{{ macro.scriptStart() }}
{{ macro.importModule(moduleName = 'numpy', shortcutName = 'np') }}
{{ macro.importModule(moduleName = 'pandas', shortcutName = 'pd') }}
#%- for dependence in dependenceList %#
{{ macro.importModule(moduleName = dependence) }}
#%- endfor %#
#%- for parentInstrumentName in parentInstrumentNameSeries %#
{{ macro.importModule(moduleName = macro.instrumentListAutoClassPath(parentInstrumentName,parentInheritListSeries[loop.index0]),submoduleName = var.parentListAutoClassNameList[loop.index0]) }}
#%- endfor %#
{{ macro.tag(tagName = "import", indentNum = 0) }}

{{ macro.classStart(className = macro.instrumentListAutoClassName(instrumentName), inheritList = var.parentListAutoClassNameList, nullElement = False) }}
{{ macro.indent(1) }}"""
{{ macro.indent(1) }}{{ macro.instrumentListAutoClassName(instrumentName) }} is an class used to store the source code generated automatically.
{{ macro.indent(1) }}"""
{{ macro.indent(1) }}__nullElement__ = None

{{ macro.tag(tagName = macro.instrumentListAutoClassName(instrumentName), indentNum = 1) }}
{{ macro.tag(tagName = macro.instrumentListAutoSetAttributeTagName(instrumentName), indentNum = 1) }}


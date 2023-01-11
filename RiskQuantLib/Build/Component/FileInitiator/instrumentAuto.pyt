#%- import 'macro.pyt' as macro -%#
#%- set var = namespace(parentAutoClassNameList = []) -%#
#%- for parentInstrumentName in parentInstrumentNameSeries -%#
#%- set var.parentAutoClassNameList = var.parentAutoClassNameList + [macro.instrumentAutoClassName(parentInstrumentName)] -%#
#%- endfor -%#
{{ macro.scriptStart() }}
{{ macro.importModule(moduleName = 'numpy', shortcutName = 'np') }}
{{ macro.importModule(moduleName = 'pandas', shortcutName = 'pd') }}
#%- for dependence in dependenceList %#
{{ macro.importModule(moduleName = dependence) }}
#%- endfor %#
#%- for parentInstrumentName in parentInstrumentNameSeries %#
{{ macro.importModule(moduleName = macro.instrumentAutoClassPath(parentInstrumentName,parentInheritListSeries[loop.index0]),submoduleName = var.parentAutoClassNameList[loop.index0]) }}
#%- endfor %#
{{ macro.tag(tagName = "import", indentNum = 0) }}

{{ macro.classStart(className = macro.instrumentAutoClassName(instrumentName), inheritList = var.parentAutoClassNameList, nullElement = False) }}
{{ macro.indent(1) }}"""
{{ macro.indent(1) }}{{ macro.instrumentAutoClassName(instrumentName) }} is an class used to store source python code generated automatically.
{{ macro.indent(1) }}"""
{{ macro.indent(1) }}__nullElement__ = None

{{ macro.tag(tagName = macro.instrumentAutoClassName(instrumentName), indentNum = 1) }}
{{ macro.tag(tagName = macro.instrumentAutoSetAttributeTagName(instrumentName), indentNum = 1) }}


#%- import 'macro.pyt' as macro -%#
#%- set var = namespace(parentListClassNameList = []) -%#
#%- for parentInstrumentName in parentInstrumentNameSeries -%#
#%- set var.parentListClassNameList = var.parentListClassNameList + [macro.instrumentListClassName(parentInstrumentName)] -%#
#%- endfor -%#
{{ macro.scriptStart() }}
{{ macro.importModule(moduleName = 'numpy', shortcutName = 'np') }}
{{ macro.importModule(moduleName = 'pandas', shortcutName = 'pd') }}
#%- for dependence in dependenceList %#
{{ macro.importModule(moduleName = dependence) }}
#%- endfor %#
#%- for parentInstrumentName in parentInstrumentNameSeries %#
{{ macro.importModule(moduleName = macro.instrumentListClassPath(parentInstrumentName,parentInheritListSeries[loop.index0]),submoduleName = var.parentListClassNameList[loop.index0]) }}
#%- endfor %#
{{ macro.importModule(moduleName = macro.instrumentClassPath(instrumentName,inheritList),submoduleName = macro.instrumentClassName(instrumentName)) }}
{{ macro.importModule(moduleName = macro.instrumentListAutoClassPath(instrumentName,inheritList),submoduleName = macro.instrumentListAutoClassName(instrumentName)) }}
{{ macro.tag(tagName = "import", indentNum = 0) }}

{{ macro.classStart(className = macro.instrumentListClassName(instrumentName), inheritList = var.parentListClassNameList + [macro.instrumentListAutoClassName(instrumentName)], nullElement = False) }}
{{ macro.indent(1) }}"""
{{ macro.indent(1) }}{{ macro.instrumentListClassName(instrumentName) }} is an instrument list class, used as nodes of data graph, and it is also the entrance of graph.
{{ macro.indent(1) }}"""
{{ macro.indent(1) }}elementClass = {{ macro.instrumentClassName(instrumentName = instrumentName) }}

{{ macro.instrumentListClassInit(instrumentName = instrumentName, instrumentType = instrumentType) }}

{{ macro.instrumentListClassAdd(instrumentName = instrumentName, instrumentType = instrumentType) }}

{{ macro.instrumentListClassAddSeries(instrumentName = instrumentName, instrumentType = instrumentType) }}

{{ macro.tag(tagName = macro.instrumentListClassName(instrumentName), indentNum = 1) }}


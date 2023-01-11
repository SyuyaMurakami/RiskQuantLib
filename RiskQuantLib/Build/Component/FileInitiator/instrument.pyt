#%- import 'macro.pyt' as macro -%#
#%- set var = namespace(parentClassNameList = []) -%#
#%- for parentInstrumentName in parentInstrumentNameSeries -%#
#%- set var.parentClassNameList = var.parentClassNameList + [macro.instrumentClassName(parentInstrumentName)] -%#
#%- endfor -%#
{{ macro.scriptStart() }}
{{ macro.importModule(moduleName = 'numpy', shortcutName = 'np') }}
{{ macro.importModule(moduleName = 'pandas', shortcutName = 'pd') }}
#%- for dependence in dependenceList %#
{{ macro.importModule(moduleName = dependence) }}
#%- endfor %#
#%- for parentInstrumentName in parentInstrumentNameSeries %#
{{ macro.importModule(moduleName = macro.instrumentClassPath(parentInstrumentName,parentInheritListSeries[loop.index0]),submoduleName = var.parentClassNameList[loop.index0]) }}
#%- endfor %#
{{ macro.importModule(moduleName = macro.instrumentAutoClassPath(instrumentName,inheritList),submoduleName = macro.instrumentAutoClassName(instrumentName)) }}
#%- for parentQuantLibInstrumentName in parentQuantLibInstrumentNameSeries %#
{{ macro.importModule(moduleName = 'QuantLib', submoduleName = parentQuantLibInstrumentName) }}
#%- endfor %#
{{ macro.tag(tagName = "import", indentNum = 0) }}

{{ macro.classStart(className = macro.instrumentClassName(instrumentName), inheritList = var.parentClassNameList + parentQuantLibInstrumentNameSeries + [macro.instrumentAutoClassName(instrumentName)], nullElement = False) }}
{{ macro.indent(1) }}"""
{{ macro.indent(1) }}{{ macro.instrumentClassName(instrumentName) }} is an instrument class, used as nodes of data graph.
{{ macro.indent(1) }}"""

#%- if parentQuantLibInstrumentNameSeries | length %#
{{ macro.instrumentClassInit(instrumentName = instrumentName, super = False, parentInstrumentNameList = var.parentClassNameList, instrumentType = instrumentType) }}

{{ macro.instrumentClassQuantLibInit(QuantLibInstrumentNameList = parentQuantLibInstrumentNameSeries) }}
#% else %#
{{ macro.instrumentClassInit(instrumentName = instrumentName, super = True, instrumentType = instrumentType) }}
#% endif %#
{{ macro.tag(tagName = macro.instrumentClassName(instrumentName), indentNum = 1) }}


#%- import 'macro.pyt' as macro -%#
#%- set var = namespace(parentPropertyClassNameList = []) -%#
#%- for parentPropertyName in parentPropertyNameSeries -%#
#%- set var.parentPropertyClassNameList = var.parentPropertyClassNameList + [macro.propertyClassName(parentPropertyName)] -%#
#%- endfor -%#
{{ macro.scriptStart() }}
#%- for parentPropertyName in parentPropertyNameSeries %#
{{ macro.importModule(moduleName = macro.propertyClassPath(parentPropertyName,parentInheritListSeries[loop.index0]),submoduleName = var.parentPropertyClassNameList[loop.index0]) }}
#%- endfor %#
{{ macro.tag(tagName = "import", indentNum = 0) }}

{{ macro.classStart(className = propertyName, inheritList = var.parentPropertyClassNameList, nullElement = False) }}
{{ macro.indent(1) }}"""
{{ macro.indent(1) }}{{ macro.propertyClassName(propertyName) }} is an attribute type class, used as terminal nodes of data graph. It represents the type of data.
{{ macro.indent(1) }}"""

{{ macro.propertyInit(propertyName) }}

{{ macro.tag(tagName = macro.propertyClassName(propertyName), indentNum = 1) }}


#%- import 'macro.pyt' as macro -%#
#->{{ macro.instrumentAutoSetAttributeTagName(instrumentName) }}
#%- for attributeName in attributeNameList %#
{{ macro.setAttribute(attributeName, macro.propertyClassPath(propertyNameList[loop.index0],propertyInheritTreeSeries[loop.index0]), macro.propertyClassName(propertyNameList[loop.index0])) }}
#%- endfor %#
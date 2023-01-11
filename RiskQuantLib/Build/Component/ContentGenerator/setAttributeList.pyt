#%- import 'macro.pyt' as macro -%#
#->{{ macro.instrumentListAutoSetAttributeTagName(instrumentName) }}
#%- for attributeName in attributeNameList %#
#%- if propertyNameList[loop.index0] == "series" %#
{{ macro.setAttributeDataFrame(attributeName,defaultValueList[loop.index0]) }}
#%- else %#
{{ macro.setAttributeList(attributeName,defaultValueList[loop.index0]) }}
#%- endif %#
#%- endfor %#
#: Capitalize the first letter of string :#
#% macro cap(text) -%#
{{ text[0] | upper }}{{ text[1:] }}
#%- endmacro %#

#: Capitalize the first letter of every string in a string list and join them into a string :#
#% macro capJoin(stringList, joinBy) -%#
#% for string in stringList -%#
{{ cap(string) + joinBy }}
#%- endfor %#
#%- endmacro %#

#: Split string by the capitalized letter :#
#% macro capSplit(text) -%#
#% for letter in text -%#
#% if loop.first -%#
{{ letter | upper }}
#%- elif letter is upper -%#
{{ ' ' + letter }}
#%- else -%#
{{ letter }}
#%- endif %#
#%- endfor %#
#%- endmacro %#

#: Indent control :#
#% macro indent(lengthOfIndent) -%#
#% for _ in range(lengthOfIndent) -%#
{{ '    ' }}
#%- endfor %#
#%- endmacro %#

#: This function add a tag, where code can be inserted :#
#% macro tag(tagName, indentNum = 0) -%#
{{ indent(indentNum) }}#<{{ tagName }}>
{{ indent(indentNum) }}#</{{ tagName }}>
#%- endmacro %#

#: Python script file start :#
#% macro scriptStart(indentNum = 0) -%#
{{ indent(indentNum) }}#!/usr/bin/python
{{ indent(indentNum) }}#coding = utf-8
#%- endmacro %#

#: Import python module :#
#% macro importModule(moduleName, shortcutName = '', submoduleName = '', indentNum = 0) -%#
#% if submoduleName | length -%#
{{ indent(indentNum) }}from {{ moduleName }} import {{ submoduleName  }}{{ (' as ' + shortcutName) if shortcutName!='' else '' }}
#%- else -%#
{{ indent(indentNum) }}import {{ moduleName }}{{ (' as ' + shortcutName) if shortcutName!='' else '' }}
#%- endif %#
#%- endmacro %#

#: Python class start :#
#% macro classStart(className, inheritList, nullElement = True, indentNum = 0) -%#
{{ indent(indentNum) }}class {{ className }}({{ inheritList | join(',') }}):
#%- if nullElement %#
{{ indent(indentNum) }}    __nullElement__ = None
#%- endif %#
#%- endmacro %#

#: This function is used to set some value as object attribute, and bound virtual terminal object into instrument :#
#% macro setAttribute(attributeName,propertyPath,propertyName, indentNum = 0) -%#
{{ indent(indentNum) }}def set{{ cap(attributeName) }}(self, {{ attributeName }}):
{{ indent(indentNum) }}    from {{ propertyPath }} import {{ propertyName }}
{{ indent(indentNum) }}    if not hasattr(self, '_{{ attributeName }}'):
{{ indent(indentNum) }}        self._{{ attributeName }} = {{ propertyName }}({{ attributeName }})
{{ indent(indentNum) }}        self._{{ attributeName }}.setBelongTo(self,'{{ attributeName }}')
{{ indent(indentNum) }}        self.{{ attributeName }} = self._{{ attributeName }}.value
{{ indent(indentNum) }}    else:
{{ indent(indentNum) }}        self._{{ attributeName }}.setValue({{ attributeName }})
{{ indent(indentNum) }}        self.{{ attributeName }} = self._{{ attributeName }}.value
#%- endmacro %#

#: This function is used to iterate through instrument list, set values as object attribute and bound virtual terminal object into instrument :#
#% macro setAttributeList(attributeName,defaultValue, indentNum = 0) -%#
{{ indent(indentNum) }}def set{{ cap(attributeName) }}(self,codeSeries,{{ attributeName }}Series,byAttr='code',update=False):
{{ indent(indentNum) }}    {{ attributeName }}Dict = dict(zip(codeSeries,{{ attributeName }}Series))
{{ indent(indentNum) }}    if byAttr=='code' and not update:
{{ indent(indentNum) }}        [i.set{{ cap(attributeName) }}({{ attributeName }}Dict[i.code]) if i.code in {{ attributeName }}Dict.keys() else i.set{{ cap(attributeName) }}({{ defaultValue }}) for i in self.all]
{{ indent(indentNum) }}    elif not update:
{{ indent(indentNum) }}        [i.set{{ cap(attributeName) }}({{ attributeName }}Dict[getattr(i,byAttr)]) if hasattr(i,byAttr) and getattr(i,byAttr) in {{ attributeName }}Dict.keys() else i.set{{ cap(attributeName) }}({{ defaultValue }}) for i in self.all]
{{ indent(indentNum) }}    else:
{{ indent(indentNum) }}        [i.set{{ cap(attributeName) }}({{ attributeName }}Dict[getattr(i,byAttr)]) if hasattr(i,byAttr) and getattr(i,byAttr) in {{ attributeName }}Dict.keys() else None for i in self.all]
#%- endmacro %#

#: This function is used to iterate through instrument list, set a pandas.Series object as attribute and bound virtual terminal object into instrument :#
#% macro setAttributeDataFrame(attributeName,defaultValue, indentNum = 0) -%#
{{ indent(indentNum) }}def set{{ cap(attributeName) }}(self,{{ attributeName }}DataFrame,byAttr='code',update=False):
{{ indent(indentNum) }}    {{ attributeName }}CodeList = {{ attributeName }}DataFrame.columns.to_list()
{{ indent(indentNum) }}    if byAttr=='code' and not update:
{{ indent(indentNum) }}        [i.set{{ cap(attributeName) }}({{ attributeName }}DataFrame[i.code]) if hasattr(i,'code') and i.code in {{ attributeName }}CodeList else i.set{{ cap(attributeName) }}({{ defaultValue }}) for i in self.all]
{{ indent(indentNum) }}    elif not update:
{{ indent(indentNum) }}        [i.set{{ cap(attributeName) }}({{ attributeName }}DataFrame[getattr(i,byAttr)]) if hasattr(i,byAttr) and getattr(i,byAttr) in {{ attributeName }}CodeList else i.set{{ cap(attributeName) }}({{ defaultValue }}) for i in self.all]
{{ indent(indentNum) }}    else:
{{ indent(indentNum) }}        [i.set{{ cap(attributeName) }}({{ attributeName }}DataFrame[getattr(i,byAttr)]) if hasattr(i,byAttr) and getattr(i,byAttr) in {{ attributeName }}CodeList else None for i in self.all]
#%- endmacro %#

#: This is the template of record instrument auto file path :#
#% macro instrumentAutoFilePath(instrumentName, inheritTree, sep) -%#
Auto{{ sep }}Instrument{{ sep }}{{ capJoin(inheritTree, sep) }}{{ cap(instrumentName)+sep if instrumentName }}{{ instrumentName if instrumentName else 'instrument' }}.py
#%- endmacro %#

#: This is the template of record instrument list auto file path :#
#% macro instrumentListAutoFilePath(instrumentName, inheritTree, sep) -%#
Auto{{ sep }}InstrumentList{{ sep }}{{ capJoin(inheritTree, "List" + sep) }}{{ cap(instrumentName) + "List" + sep if instrumentName }}{{ instrumentName  + "List" if instrumentName else 'instrumentList' }}.py
#%- endmacro %#

#: This is the template of record instrument file path :#
#% macro instrumentFilePath(instrumentName, inheritTree, sep) -%#
Instrument{{ sep }}{{ capJoin(inheritTree, sep) }}{{ cap(instrumentName)+sep if instrumentName }}{{ instrumentName if instrumentName else 'instrument' }}.py
#%- endmacro %#

#: This is the template of record instrument list file path :#
#% macro instrumentListFilePath(instrumentName, inheritTree, sep) -%#
InstrumentList{{ sep }}{{ capJoin(inheritTree, "List" + sep) }}{{ cap(instrumentName) + "List" + sep if instrumentName }}{{ instrumentName  + "List" if instrumentName else 'instrumentList' }}.py
#%- endmacro %#

#: This is the template of record instrument auto-class import path :#
#% macro instrumentAutoClassPath(instrumentName, inheritTree) -%#
RiskQuantLib.Auto.Instrument.{{ capJoin(inheritTree, ".") }}{{ cap(instrumentName)+'.' if instrumentName }}{{ instrumentName if instrumentName else 'instrument' }}
#%- endmacro %#

#: This is the template of record instrument list auto-class import path :#
#% macro instrumentListAutoClassPath(instrumentName, inheritTree) -%#
RiskQuantLib.Auto.InstrumentList.{{ capJoin(inheritTree, "List.") }}{{ cap(instrumentName)+"List." if instrumentName }}{{ instrumentName if instrumentName else 'instrument' }}List
#%- endmacro %#

#: This is the template of record instrument class import path :#
#% macro instrumentClassPath(instrumentName, inheritTree) -%#
RiskQuantLib.Instrument.{{ capJoin(inheritTree, ".") }}{{ cap(instrumentName)+'.' if instrumentName }}{{ instrumentName if instrumentName else 'instrument' }}
#%- endmacro %#

#: This is the template of record instrument list class import path :#
#% macro instrumentListClassPath(instrumentName, inheritTree) -%#
RiskQuantLib.InstrumentList.{{ capJoin(inheritTree, "List.") }}{{ cap(instrumentName)+"List." if instrumentName }}{{ instrumentName if instrumentName else 'instrument' }}List
#%- endmacro %#

#: This is the template of record instrument class name :#
#% macro instrumentClassName(instrumentName) -%#
{{ instrumentName if instrumentName else 'instrument' }}
#%- endmacro %#

#: This is the template of record instrument list class name :#
#% macro instrumentListClassName(instrumentName) -%#
{{ instrumentName if instrumentName else 'instrument' }}List
#%- endmacro %#

#: This is the template of record instrument auto-class name :#
#% macro instrumentAutoClassName(instrumentName) -%#
{{ instrumentName if instrumentName else 'instrument' }}Auto
#%- endmacro %#

#: This is the template of record instrument list auto-class name :#
#% macro instrumentListAutoClassName(instrumentName) -%#
{{ instrumentName if instrumentName else 'instrument' }}ListAuto
#%- endmacro %#

#: This is the template of record instrument auto-class set attribute tag name :#
#% macro instrumentAutoSetAttributeTagName(instrumentName) -%#
{{ instrumentAutoClassName(instrumentName) }}SetAttribute
#%- endmacro %#

#: This is the template of record instrument list auto-class set attribute tag name :#
#% macro instrumentListAutoSetAttributeTagName(instrumentName) -%#
{{ instrumentListAutoClassName(instrumentName) }}SetAttribute
#%- endmacro %#

#: This is the template of record attribute type path :#
#% macro propertyFilePath(propertyName, inheritTree, sep) -%#
Property{{ sep }}{{ capJoin(inheritTree, sep) }}{{ cap(propertyName)+sep if propertyName }}{{ propertyName if propertyName else 'property' }}.py
#%- endmacro %#

#: This is the template of record property class name :#
#% macro propertyClassName(propertyName) -%#
{{ propertyName if propertyName else 'property' }}
#%- endmacro %#

#: This is the template of record attribute type import path :#
#% macro propertyClassPath(propertyName, inheritTree) -%#
RiskQuantLib.Property.{{ capJoin(inheritTree, ".") }}{{ cap(propertyName)+"." if propertyName }}{{ propertyName if propertyName else 'property' }}
#%- endmacro %#

#: This is the template of shortcut :#
#% macro shortcut(instrumentName, inheritTree) -%#
{{ importModule(moduleName = instrumentListClassPath(instrumentName, inheritTree), submoduleName = instrumentClassName(instrumentName)+', '+instrumentListClassName(instrumentName)) }}
#%- endmacro %#

#: This is the template of shortcut of property :#
#% macro shortcutProperty(propertyName, inheritTree) -%#
{{ importModule(moduleName = propertyClassPath(propertyName, inheritTree), submoduleName = propertyClassName(propertyName)) }}
#%- endmacro %#

#: This is the __init__ function template of instrument list class :#
#% macro instrumentListClassInit(instrumentName, instrumentType = '', indentNum = 1) -%#
{{ indent(indentNum) }}#<init>
{{ indent(indentNum) }}def __init__(self):
{{ indent(indentNum) }}    super({{ instrumentListClassName(instrumentName) }},self).__init__()
{{ indent(indentNum) }}    self.listType = '{{ instrumentType }}{{ ' ' if instrumentType else '' }}List'
{{ indent(indentNum) }}#</init>
#%- endmacro %#

#: This is the addInstrument function template of instrument list class :#
#% macro instrumentListClassAdd(instrumentName, instrumentType = '', indentNum = 1) -%#
{{ indent(indentNum) }}#<add>
{{ indent(indentNum) }}def add{{ cap(instrumentName) }}(self,codeString,nameString,instrumentTypeString = '{{ instrumentType }}'):
{{ indent(indentNum) }}    tmpList = self.all+[{{ instrumentName }}(codeString,nameString,instrumentTypeString)]
{{ indent(indentNum) }}    self.setAll(tmpList)
{{ indent(indentNum) }}#</add>
#%- endmacro %#

#: This is the addInstrument function template of instrument list class :#
#% macro instrumentListClassAddSeries(instrumentName, instrumentType = '', indentNum = 1) -%#
{{ indent(indentNum) }}#<addSeries>
{{ indent(indentNum) }}def add{{ cap(instrumentName) }}Series(self,{{ instrumentName }}CodeSeries,{{ instrumentName }}NameSeries,instrumentTypeString = '{{ instrumentType }}'):
{{ indent(indentNum) }}    {{ instrumentName }}Series = [{{ instrumentClassName(instrumentName) }}(i,j,instrumentTypeString) for i,j in zip({{ instrumentName }}CodeSeries,{{ instrumentName }}NameSeries)]
{{ indent(indentNum) }}    tmpList = self.all + {{ instrumentName }}Series
{{ indent(indentNum) }}    self.setAll(tmpList)
{{ indent(indentNum) }}#</addSeries>
#%- endmacro %#

#: This is the __init__ function template of instrument class :#
#% macro instrumentClassInit(instrumentName, super = True ,parentInstrumentNameList = [], instrumentType = '', indentNum = 1) -%#
{{ indent(indentNum) }}#<init>
{{ indent(indentNum) }}def __init__(self,codeString,nameString,instrumentTypeString = '{{ instrumentType }}'):
#%- if super %#
{{ indent(indentNum) }}    super({{ instrumentClassName(instrumentName) }},self).__init__(codeString,nameString,instrumentTypeString)
#%- else %#
#%- for parentInstrumentName in parentInstrumentNameList %#
{{ indent(indentNum) }}    {{ parentInstrumentName }}.__init__(self,codeString,nameString,instrumentTypeString)
#%- endfor %#
#%- endif %#
{{ indent(indentNum) }}#</init>
#%- endmacro %#

#: This is function template of instrument class to initialize QuantLib pricing module :#
#% macro instrumentClassQuantLibInit(QuantLibInstrumentNameList, indentNum = 1) -%#
{{ indent(indentNum) }}#<initQuantLib>
{{ indent(indentNum) }}def iniPricingModule(self,*args):
#%- for QuantLibInstrumentName in QuantLibInstrumentNameList %#
{{ indent(indentNum) }}    {{ QuantLibInstrumentName }}.__init__(self,*args)
#%- endfor %#
{{ indent(indentNum) }}#</initQuantLib>
#%- endmacro %#

#: This is __init__ function template of property class :#
#% macro propertyInit(propertyName, indentNum = 1) -%#
{{ indent(indentNum) }}#<init>
{{ indent(indentNum) }}def __init__(self, value):
{{ indent(indentNum) }}    super({{ propertyName }},self).__init__(value)
{{ indent(indentNum) }}#</init>
#%- endmacro %#
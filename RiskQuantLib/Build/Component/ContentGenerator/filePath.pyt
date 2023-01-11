#%- import 'macro.pyt' as macro -%#
{
    "instrumentFilePath":{
            #%- for instrumentName in instrumentNameList %#
            "{{ macro.instrumentClassName(instrumentName) }}":"{{ macro.instrumentFilePath(instrumentName,instrumentInheritTreeSeries[loop.index0], sep) }}"
            #%- if not loop.last -%#
            ,
            #%- endif %#
            #%- endfor %#
    },
    "instrumentListFilePath":{
            #%- for instrumentName in instrumentNameList %#
            "{{ macro.instrumentListClassName(instrumentName) }}":"{{ macro.instrumentListFilePath(instrumentName,instrumentInheritTreeSeries[loop.index0], sep) }}"
            #%- if not loop.last -%#
            ,
            #%- endif %#
            #%- endfor %#
    },
    "instrumentAutoFilePath":{
            #%- for instrumentName in instrumentNameList %#
            "{{ macro.instrumentAutoClassName(instrumentName) }}":"{{ macro.instrumentAutoFilePath(instrumentName,instrumentInheritTreeSeries[loop.index0], sep) }}"
            #%- if not loop.last -%#
            ,
            #%- endif %#
            #%- endfor %#
    },
    "instrumentListAutoFilePath":{
            #%- for instrumentName in instrumentNameList %#
            "{{ macro.instrumentListAutoClassName(instrumentName) }}":"{{ macro.instrumentListAutoFilePath(instrumentName,instrumentInheritTreeSeries[loop.index0], sep) }}"
            #%- if not loop.last -%#
            ,
            #%- endif %#
            #%- endfor %#
    },
    "propertyFilePath":{
            #%- for propertyName in propertyNameList %#
            "{{ macro.propertyClassName(propertyName) }}":"{{ macro.propertyFilePath(propertyName,propertyInheritTreeSeries[loop.index0], sep) }}"
            #%- if not loop.last -%#
            ,
            #%- endif %#
            #%- endfor %#
    },
    "instrumentAutoSetAttributeTagPath":{
            #%- for instrumentName in instrumentNameList %#
            "{{ macro.instrumentAutoSetAttributeTagName(instrumentName) }}":"{{ macro.instrumentAutoFilePath(instrumentName,instrumentInheritTreeSeries[loop.index0], sep) }}"
            #%- if not loop.last -%#
            ,
            #%- endif %#
            #%- endfor %#
    },
    "instrumentListAutoSetAttributeTagPath":{
            #%- for instrumentName in instrumentNameList %#
            "{{ macro.instrumentListAutoSetAttributeTagName(instrumentName) }}":"{{ macro.instrumentListAutoFilePath(instrumentName,instrumentInheritTreeSeries[loop.index0], sep) }}"
            #%- if not loop.last -%#
            ,
            #%- endif %#
            #%- endfor %#
    }
}
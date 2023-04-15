#%- import 'macro.pyt' as macro -%#
#%- for src in srcOfChunk %#
#%- if canBeDebugged[loop.index0] %#
_srcPath = r"{{ srcPath }}"
from RiskQuantLib.Build.debugger import debugger as _debugger
_tmp = _debugger.importModuleFromFile(_srcPath)
{{ functionName[loop.index0] }} = _tmp.{{ functionName[loop.index0] }}
#%- else %#
{{ src }}
#%- endif %#
#%- endfor %#
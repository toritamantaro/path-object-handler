# pathobj-handler

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/pathobj_handler)](https://pepy.tech/project/pathobj_handler)

## Installation

```bash
$ pip install pathobj-handler
```

## Series  

### pathobj_handler.filestem.picker
* PickFilesBySuffix

### pathobj_handler.filesterm.filter

* FilterByCustomFunction
* FilterWithDateRange
* FilterWithRegExp

### pathobj_handler.filestem.renamer
* RenameFilesByCustomFunction
* RenamerWithReplaceStr
  
  
`PickFilesBySuffix` can retrieve file objects (`pathlib.Path`) as a generator in a given directory, and `FilterByCustomFunction` can filter file objects by their file names. 
  
`pathobj_hundler` classes form a process chain with the `make_pipeline` function. 
The chain can contain several filters, and each of the filters applies to a file object in an order. 




## Basic use

Listing `*.txt` or `*.text` files in the given directory tree:

```commandline
from pathobj_handler.filestem.picker import PickFilesBySuffix

fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)
dir_path = './resource'

fp_gen = fp(dir_path)
print(list(fp_gen))
```
>[WindowsPath('resource/sample/20240410T150525_DDDDDD111111_AAA.txt'), WindowsPath('resource/sample/20240411T150625_DDDDDD111111_BBB.txt'), WindowsPath('resource/sample/20240412T150725_DDDD
DD222222_AAA.txt'), WindowsPath('resource/sample/20240413T150825_DDDDDD333333_BBB.txt'), WindowsPath('resource/sample/fuga_01.txt'), WindowsPath('resource/sample/fuga_02.txt'), WindowsPath('resource/sample/hoge_01.text'), WindowsPath('resource/sample/hoge_02.text')]
<br>
  
Screening files in a given directory that contain the specified string in the filename:
```commandline
from pathobj_handler.tool import make_pipeline
from pathobj_handler.filestem.picker import PickFilesBySuffix
from pathobj_handler.filestem.filter import FilterByCustomFunction

fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)
dir_path = './resource'

# custom filter
def is_target(stem: str) -> bool:
    return 'hoge' in stem

fl_1 = FilterByCustomFunction(filter_method=is_target)

fp_filter = make_pipeline(fp, fl_1)
fp_gen = fp_filter(dir_path)
print(list(fp_gen))
```
>[WindowsPath('resource/sample/hoge_01.text'), WindowsPath('resource/sample/hoge_02.text')]
<br>
  
Multiple filters are chained with `make_pipeline`:
```commandline
from datetime import datetime
import re

from pathobj_handler.tool import make_pipeline
from pathobj_handler.filestem.picker import PickFilesBySuffix
from pathobj_handler.filestem.filter import FilterWithDateRange, FilterWithRegExp

fp = PickFilesBySuffix(['.txt', '.text'], recursive=True)
dir_path = './resource'

fl_1 = FilterWithDateRange(
    re_time=r'\d+T\d+',
    dt_from=datetime(2024, 4, 11),
    dt_to=datetime(2024, 4, 14),
)

fl_2 = FilterWithRegExp(
    re_list=['DDDDDD111111', 'DDDDDD333333']
)

fp_filter = make_pipeline(
    fp, 
    fl_1,
    fl_2,
)
fp_gen = fp_filter(dir_path)
print(list(fp_gen))
```
>[WindowsPath('resource/sample/20240411T150625_DDDDDD111111_BBB.txt'), WindowsPath('resource/sample/20240413T150825_DDDDDD333333_BBB.txt')]
<br>
  







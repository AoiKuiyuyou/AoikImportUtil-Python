# AoikImportUtil-Python
Import module by code, name, path, and import object.

Tested working with:
- Python: 2.5+, 3.0+

## Table of Contents
- [Setup](#setup)
  - [Setup via pip](#setup-via-pip)
  - [Setup via git](#setup-via-git)
- [Usage](#usage)
  - [Import module by code](#import-module-by-code)
  - [Import module by name](#import-module-by-name)
  - [Import module by path](#import-module-by-path)
  - [Import object](#import-object)

## Setup
- [Setup via pip](#setup-via-pip)
- [Setup via git](#setup-via-git)

### Setup via pip
Run:
```
pip install AoikImportUtil
```
or:
```
pip install git+https://github.com/AoiKuiyuyou/AoikImportUtil-Python
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikImportUtil-Python

cd AoikImportUtil-Python

python setup.py install
```

## Usage
- [Import module by code](#import-module-by-code)
- [Import module by name](#import-module-by-name)
- [Import module by path](#import-module-by-path)
- [Import object](#import-object)

### Import module by code
E.g.
```
import sys

from aoikimportutil import import_code

mod_obj = import_code(mod_name='a', mod_code='x = 1')

assert mod_obj is sys.modules['a']

assert mod_obj.x == 1
```

### Import module by name
E.g.
```
import sys

from aoikimportutil import import_name

mod_obj = import_name('os.path')

assert mod_obj is sys.modules['os.path']
```

### Import module by path
E.g.
```
import sys

from aoikimportutil import import_path

mod_obj = import_path('src/aoikimportutil/aoikimportutil.py', mod_name='a')

assert mod_obj is sys.modules['a']
```

### Import object
E.g.
```
import sys

from aoikimportutil import import_obj

mod_obj = import_obj('os.path')

assert mod_obj is sys.modules['os.path']

func_obj = import_obj('os.path::split')

assert func_obj is sys.modules['os.path'].split

class_obj = import_obj('os.path::split.__class__')

assert class_obj is sys.modules['os.path'].split.__class__

import_code = import_obj('src/aoikimportutil/aoikimportutil.py::import_code', mod_name='a')

assert import_code is sys.modules['a'].import_code
```

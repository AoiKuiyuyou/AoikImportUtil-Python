

# AoikImportUtil-Python
Import module by code, name, file path, or HTTP URL. Import any object, not only module.

Tested working with:
- Python: 2.5+, 3.0+

[Package on PyPI](https://pypi.python.org/pypi/AoikImportUtil)

## Table of Contents
- [Setup](#setup)
  - [Setup via pip](#setup-via-pip)
  - [Setup via git](#setup-via-git)
- [Usage](#usage)
  - [Import by module code](#import-by-module-code)
  - [Import by module name](#import-by-module-name)
    - [Specify a namespace dir](#specify-a-namespace-dir)
  - [Import by module file path](#import-by-module-file-path)
  - [Import by module file HTTP URL](#import-by-module-file-http-url)
  - [Load object from module](#load-object-from-module)
    - [Specify py protocol prefix](#specify-py-protocol-prefix)
    - [Specify chain of attributes](#specify-chain-of-attributes)
  - [Load object from module file on filesystem](#load-object-from-module-file-on-filesystem)
    - [Specify file protocol prefix](#specify-file-protocol-prefix)
  - [Load object from module file on HTTP server](#load-object-from-module-file-on-http-server)
  - [Load object from either local or remote](#load-object-from-either-local-or-remote)

## Setup

### Setup via pip
Run
```
pip install AoikImportUtil
```
or
```
pip install git+https://github.com/AoiKuiyuyou/AoikImportUtil-Python
```

### Setup via git
Clone this repo to local
```
git clone https://github.com/AoiKuiyuyou/AoikImportUtil-Python
```

Run the **setup.py** file in the local repo dir
```
python setup.py install
```
The effect is equivalent to installation via pip.

## Usage

### Import by module code
E.g.
```
from aoikimportutil import import_module_by_code
import sys

#/
mod_obj = import_module_by_code(mod_name='aoiktmp', mod_code='x = 1')

print(mod_obj is sys.modules['aoiktmp'])
## True

print(mod_obj.x)
## 1
```
- Use arg ```mod_name``` to specify the module name to load the module as.

### Import by module name
E.g.
```
from aoikimportutil import import_module_by_name
import sys

#/
mod_obj = import_module_by_name('datetime')

print(mod_obj is sys.modules['datetime'])
## True

#/
mod_obj2 = import_module_by_name('os.path')

print(mod_obj2 is sys.modules['os.path'])
## True
```

#### Specify a namespace dir
Modules will only be loaded from the specified namespace dir. Other namespace
 dirs listed in **sys.path** are ignored.

E.g.
```
from aoikimportutil import import_module_by_name
import sys

#/
mod_obj = import_module_by_name('aoikimportutil.aoikimportutil', ns_dir='src')

print(mod_obj is sys.modules['aoikimportutil.aoikimportutil'])
## True

#/
mod_obj2 = import_module_by_name('os', ns_dir='src')
## ImportError: No module named os
```
- The relative path above assumes your working dir is containing the ```src```
   dir.

### Import by module file path
E.g.
```
from aoikimportutil import import_module_by_path
import sys

#/
mod_obj = import_module_by_path(
    mod_path='src/aoikimportutil/aoikimportutil.py',
    mod_name='aoiktmp',
)

print(mod_obj is sys.modules['aoiktmp'])
## True
```
- Can use either absolute or relative path.
- The relative path above assumes your working dir is containing the ```src```
   dir.
- Use arg ```mod_name``` to specify the module name to load the module as.

### Import by module file HTTP URL
E.g.
```
from aoikimportutil import import_module_by_http
import sys

#/
mod_obj = import_module_by_http(
    uri='https://raw.githubusercontent.com/akheron/cpython/2.7/Lib/base64.py',
    mod_name='b64',
)

print(mod_obj is sys.modules['b64'])
## True
```
- Use arg ```mod_name``` to specify the module name to load the module as.
- The module file will be downloaded via HTTP, then loaded dynamically.
- Loading remote code is handy but be aware of the security implications.

### Load object from module
E.g.
```
from aoikimportutil import load_obj

mod_obj = load_obj('os.path')

func_obj = load_obj('os.path::split')
```
- ```os.path``` is the module to load.
- ```::``` is the separator between module part and attribute part.
- ```split``` is the attribute to load.  
  It can be a chain of attributes as well, as mentioned [here](#specify-chain-of-attributes).

#### Specify py protocol prefix
E.g.
```
from aoikimportutil import load_obj

func_obj = load_obj('py://os.path::split')
```

If no explicit protocol prefix is present, an ending ```.py``` in the module
 part makes the URI be interpreted as module file path instead of module name.

In the rare case that a module is named **py**, protocol prefix ```py://``` can
 be used to prevent the URI from being interpreted as file path.

#### Specify chain of attributes
E.g.
```
from aoikimportutil import load_obj

cls_obj = load_obj('os.path::split.__class__')

cls_name = load_obj('os.path::split.__class__.__name__')
```

### Load object from module file on filesystem
E.g.
```
from aoikimportutil import load_obj

#/
mod_obj = load_obj(
  uri='src/aoikimportutil/aoikimportutil.py',
  mod_name='aoiktmp',
)

#/
func_obj = load_obj(
  uri='src/aoikimportutil/aoikimportutil.py::import_module_by_name',
  mod_name='aoiktmp',
)
```
- ```src/aoikimportutil/aoikimportutil.py``` is the module to load.
- ```::``` is the separator between module part and attribute part.
- ```import_module_by_name``` is the attribute to load.  
  It can be a chain of attributes as well, as mentioned [here](#specify-chain-of-attributes).
- Both absolute path and relative path can be used.  
- The relative path in the example assumes your working dir is containing the **src** dir.
- Use arg ```mod_name``` to specify the module name to load the module as.

#### Specify file protocol prefix
E.g.
```
from aoikimportutil import load_obj

#/
func_obj = load_obj(
  mod_path='file://src/aoikimportutil/aoikimportutil.py::import_module_by_name',
  mod_name='aoiktmp',
)
```

If no explicit protocol prefix is present, an ending ```.py``` in the module
 part makes the URI be interpreted as module file path instead of module name.

In the rare case that a module file is not named with **.py** file extension,
 protocol prefix ```file://``` can be used to force the URI to be interpreted
 as file path.

### Load object from module file on HTTP server
E.g.
```
from aoikimportutil import load_obj_http

#/
mod_obj = load_obj_http(
    uri='https://raw.githubusercontent.com/akheron/cpython/2.7/Lib/base64.py',
    mod_name='b64',
)

#/
func_obj = load_obj_http(
    uri='https://raw.githubusercontent.com/akheron/cpython/2.7/Lib/base64.py::b64encode',
    mod_name='b64',
)

```
- ```base64.py``` is the module to load.
- ```::``` is the separator between module part and attribute part.
- ```b64encode``` is the attribute to load.  
  It can be a chain of attributes as well, as mentioned [here](#specify-chain-of-attributes).
- Use arg ```mod_name``` to specify the module name to load the module as.
- The module file will be downloaded via HTTP, then loaded dynamically.
- Loading remote code is handy but be aware of the security implications.

### Load object from either local or remote
E.g.
```
from aoikimportutil import load_obj_local_or_remote

#/
func_obj = load_obj_local_or_remote(
    uri='base64::b64encode',
)

#/
func_obj2 = load_obj_local_or_remote(
    uri='https://raw.githubusercontent.com/akheron/cpython/2.7/Lib/base64.py::b64encode',
    mod_name='b64',
)
```

- Protocol prefix ```http://``` or ```https://``` makes the URI be interpreted
   as HTTP URL, otherwise the URI is interpreted as module name or file path.

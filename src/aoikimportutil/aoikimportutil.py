# coding: utf-8
from __future__ import absolute_import

import imp
import sys


__version__ = '0.3.0'

__all__ = (
    'import_code',
    'import_name',
    'import_path',
    'import_obj',
)


# Define `exec_` and `raise_` that are 2*3 compatible.
#
# Modified from `six`:
# https://bitbucket.org/gutworth/six/src/cc9fce6016db076497454f9352e55b4758ccc07c/six.py?#cl-632
#
# --- BEG ---
if sys.version_info[0] == 2:
    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec("""exec _code_ in _globs_, _locs_""")

    exec_("""def raise_(exc, tb=None):
    raise exc, None, tb
""")
else:
    exec_ = eval('exec')

    def raise_(exc, tb=None):
        if tb is not None and exc.__traceback__ is not tb:
            raise exc.with_traceback(tb)
        else:
            raise exc
# --- END ---


def import_code(mod_code, mod_name):
    """Create a module object by code.
    @param mod_code: the code that the module contains.

    @param mod_name: module name.
    """
    mod_obj = imp.new_module(mod_name)

    mod_obj.__file__ = None

    exec_(mod_code, mod_obj.__dict__, mod_obj.__dict__)

    add_to_sys_modules(mod_name=mod_name, mod_obj=mod_obj)

    return mod_obj


def import_name(mod_name):
    """Import a module by module name.

    @param mod_name: module name.
    """
    try:
        mod_obj_old = sys.modules[mod_name]
    except KeyError:
        mod_obj_old = None

    if mod_obj_old is not None:
        return mod_obj_old

    __import__(mod_name)

    mod_obj = sys.modules[mod_name]

    return mod_obj


def import_path(mod_path, mod_name):
    """Import a module by module file path.

    @param mod_path: module file path.

    @param mod_name: module name.
    """
    mod_code = open(mod_path).read()

    mod_obj = import_code(
        mod_code=mod_code,
        mod_name=mod_name,
    )

    if not hasattr(mod_obj, '__file__'):
        mod_obj.__file__ = mod_path

    return mod_obj


def import_obj(
    uri,
    mod_name=None,
    mod_attr_sep='::',
    attr_chain_sep='.',
    retn_mod=False,
):
    """Load an object from a module.

    @param uri: an uri specifying which object to load.
    An `uri` consists of two parts: module URI and attribute chain,
     e.g. `a/b/c.py::x.y.z` or `a.b.c::x.y.z`

    # Module URI
    E.g.  `a/b/c.py` or `a.b.c`.
    Can be either a module name or a file path.
    Whether it is a file path is determined by whether it ends with `.py`.

    # Attribute chain
    E.g. `x.y.z`.

    @param mod_name: module name.
    Must be given when `uri` specifies a module file path, not a module name.

    @param mod_attr_sep: the separator between module name and attribute name.

    @param attr_chain_sep: the separator between parts of attribute name.

    @retn_mod: whether return module object.
    """
    if mod_attr_sep is None:
        mod_attr_sep = '::'

    uri_parts = split_uri(uri=uri, mod_attr_sep=mod_attr_sep)

    protocol, mod_uri, attr_chain = uri_parts

    if protocol == 'py':
        mod_obj = import_name(mod_uri)

    else:
        if not mod_name:
            msg = (
                'Argument `mod_name` must be given when loading by file path.'
            )

            raise ValueError(msg)

        mod_obj = import_path(mod_uri, mod_name=mod_name)

    if not attr_chain:
        if retn_mod:
            return mod_obj, None
        else:
            return mod_obj

    if attr_chain_sep is None:
        attr_chain_sep = '.'

    attr_obj = get_attr_chain(
        obj=mod_obj,
        attr_chain=attr_chain,
        sep=attr_chain_sep,
    )

    if retn_mod:
        return mod_obj, attr_obj
    else:
        return attr_obj


def add_to_sys_modules(mod_name, mod_obj=None):
    """Add a module object to `sys.modules`.

    @param mod_name: module name, used as key to `sys.modules`.
    If `mod_name` is `a.b.c` while modules `a` and `a.b` are not existing,
    empty modules will be created for `a` and `a.b` as well.

    @param mod_obj: a module object.
    If None, an empty module object will be created.
    """
    mod_snames = mod_name.split('.')

    parent_mod_name = ''

    parent_mod_obj = None

    for mod_sname in mod_snames:
        if parent_mod_name == '':
            current_mod_name = mod_sname
        else:
            current_mod_name = parent_mod_name + '.' + mod_sname

        if current_mod_name == mod_name:
            current_mod_obj = mod_obj
        else:
            current_mod_obj = sys.modules.get(current_mod_name, None)

        if current_mod_obj is None:
            current_mod_obj = imp.new_module(current_mod_name)

        sys.modules[current_mod_name] = current_mod_obj

        if parent_mod_obj is not None:
            setattr(parent_mod_obj, mod_sname, current_mod_obj)

        parent_mod_name = current_mod_name

        parent_mod_obj = current_mod_obj


def split_uri(uri, mod_attr_sep='::'):
    """Split given URI into a tuple of (protocol, module URI, attribute chain).

    @param mod_attr_sep: the separator between module name and attribute name.
    """
    uri_parts = uri.split(mod_attr_sep, 1)

    if len(uri_parts) == 2:
        mod_uri, attr_chain = uri_parts
    else:
        mod_uri = uri_parts[0]

        attr_chain = None

    if mod_uri.startswith('py://'):
        protocol = 'py'

        mod_uri = mod_uri[5:]

    elif mod_uri.startswith('file://'):
        protocol = 'file'

        mod_uri = mod_uri[7:]

    # If no protocol prefix is present, and the uri ends with `.py`, then
    # consider the uri as module file path instead of module name.
    elif mod_uri.endswith('.py'):
        protocol = 'file'

    else:
        protocol = 'py'

    info = (protocol, mod_uri, attr_chain)

    return info


def get_attr_chain(obj, attr_chain, sep='.'):
    """Get the last attribute of given attribute chain.
    E.g. `get_attr_chain(x, 'a.b.c')` is equivalent to `x.a.b.c`.

    @param obj: an object

    @param attr_chain: a chain of attribute names

    @param sep: separator for the chain of attribute names
    """
    if sep is None:
        sep = '.'

    attr_names = attr_chain.split(sep)

    new_obj = obj

    for attr_name in attr_names:
        new_obj = getattr(new_obj, attr_name)

    return new_obj

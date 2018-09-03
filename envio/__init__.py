import os
import logging

try:
    import json
except ImportError:
    import simplejson as json


# truthy and falsey values
BOOL_TRUE = ['true', 't', 'yes', 'on', '1']
BOOL_FALSE = ['false', 'f', 'no', 'off', '0']


class EnvioParseError(Exception): pass


def get_var(name, default=None, var_type=str, many=False, delimmiter=','):
    """Get environment variable from running process. A default value can be
    provided. If no default is provided, then the env variable is assumed to
    be required. The values can be coerced into a type by using the var_type
    argument. lists as delimmitted values are also supported and their values
    can also be coerced into a value.
    """

    types = (str, bool, int, float, 'json')
    if var_type not in types:
        msg = 'value <%s> not in supported types: [%s]' %(var_type, types)
        raise EnvioParseError(msg)

    var = os.getenv(name)
    using_default = False

    if var is None:
        if default is not None:
            var = default
            using_default = True
        else:
            msg = 'Variable <%s> is required. Supply a default if needed' %name
            raise EnvioParseError(msg)

    if many == True:
        return parse_list(var, var_type, using_default, delimmiter)
    else:
        return parse_var(var, var_type, using_default)


def parse_list(x, var_type, using_default, delimmiter):
    try:
        vars = x.split(delimmiter)
        list_exception = None
        return [parse_var(x.strip(), var_type, using_default) for x in vars]
    except Exception as e:
        msg = 'Could not parse value <%s> as list' % x
        list_exception = EnvioParseError(msg, e)
    raise list_exception


def parse_var(x, var_type, using_default):
    if var_type == bool:
        return str_to_bool(x)
    elif var_type == int:
        return str_to_int(x)
    elif var_type == float:
        return str_to_float(x)
    elif var_type == 'json':
        return str_to_dict(x)
    else:
        return x


def str_to_bool(x):
    """Try to cast a value to a boolean.
    """
    y = x.lower()
    if y in BOOL_TRUE:
        return True
    elif y in BOOL_FALSE:
        return False
    else:
        msg = 'Could not parse value <%s> as boolean' %x
        raise EnvioParseError(msg)


def str_to_int(x):
    try:
        x = int(x)
        return x
    except Exception as e:
        msg = 'Could not parse value <%s> as integer' %x
        r = EnvioParseError(msg, e)
    raise r


def str_to_float(x):
    try:
        x = float(x)
        return x
    except Exception as e:
        msg = 'Could not parse value <%s> as float' %x
        r = EnvioParseError(msg, e)
    raise r


def str_to_dict(x):
    try:
        x = json.loads(x)
        return x
    except Exception as e:
        msg = 'Could not parse into json value: %s' %x
        json_exception = EnvioParseError(msg, e)
    raise json_exception

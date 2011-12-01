def str2bool(value):
    """
    >>> str2bool('True')
    True
    >>> str2bool('true')
    True
    >>> str2bool('On')
    True
    >>> str2bool('on')
    True
    >>> str2bool(True)
    True
    >>> str2bool('false')
    False
    >>> str2bool('False')
    False
    >>> str2bool('Off')
    False
    >>> str2bool('off')
    False
    >>> str2bool('')
    False
    >>> str2bool(False)
    False
    >>> str2bool('foo')
    True
    """

    boolDict = {
        'false': False,
        'true': True,
        'on': True,
        'off': False}

    try:
        return boolDict[value.lower()]
    except (KeyError, AttributeError):
        return bool(value)


def kwargs2commandline(kwargs, boolflags=[]):
    """ Returns a string with the given key,value pairs formatted as command line options.
    we use this to convert fabrics task arguments back to command line options for ezjail-admin.

    >>> kwargs2commandline(dict(m='True', r='8.2-RELEASE'), boolflags=['m'])
    ' -r 8.2-RELEASE -m'

    >>> kwargs2commandline(dict(P='false', m='True', h='foo'), boolflags=['m', 'P'])
    ' -h foo -m'

    >>> kwargs2commandline(dict(P='true', h='foo'), boolflags=['m', 'P'])
    ' -h foo -P'

    >>> kwargs2commandline(dict())
    ''
    """
    result = ""
    for key, value in kwargs.items():
        if key in boolflags:
            if str2bool(value):
                result += " -%s" % key
        else:
            result += " -%s %s" % (key, value)
    return result

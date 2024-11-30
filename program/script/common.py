import re


class Block(object):
    """
    SMELL ALERT! This is a way to conflate a Python class with a Javascript
    object. The object acts like a dict where the keys of the dict are fields of
    the class.

    I wonder if this can be removed in favor of something more straightforward,
    but don't yet understand how this all gets used, so am wary of making such a
    change yet.
    """
    def __contains__(self, key):
        return key in self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def _check(self):
        """
        This will be overridden in subclasses! Up here, the check is to walk all
        fields and recursively check the other Blocks.
        """
        for name in dir(self):
            if name.startswith("_"):  # Something internal
                continue
            obj = getattr(self, name)
            if isinstance(obj, Block):
                obj._check()


def color_func(line):
    """
    The line provided might be a string containing code that evaluates to a
    list!?

    Returns a tuple of 4 floats, each between 0.0 and 1.0.

    TODO: what do the floats represent?
    TODO: come up with a safer approach than calling `eval`.
    """
    if line == "None":
        return (1.0, 1.0, 1.0, 1.0)
    line = eval(line)[:4]
    color = []
    for c in line:
        c = float(c)
        if c < 0.0:
            color.append(0.0)
        elif c > 1.0:
            color.append(1.0)
        else:
            color.append(c)
    n = len(color)
    if n < 4:
        color += [1.0] * (4-n)
    return color


# TODO: use a more standard caching decorator instead of _func_hash
_func_hash = {}  # Memoize the results
re_type = re.compile(r"<type (['\"])(\w+)\1>")
def high_func_num(func, min_value, max_value, can_be_none=False):
    """
    Returns a function that takes in a string and parses it to a value.

    The func converts a string to a value.
    The min_value and max_value clamp the value to a range.
    If can_be_none is set, the function we return will itself return None when
    given the string "None".
    """
    key = (id(func), min_value, max_value, can_be_none)
    if key in _func_hash:
        return _func_hash[key]

    def f(line):
        if can_be_none and line == "None":
            return None
        value = func(line)
        if value < min_value:
            return min_value
        elif value > max_value:
            return max_value
        else:
            return value

    s = str(func)
    match = re_type.match(s)
    if match:
        s = match.group(2)
    f.__name__ = "%s %s<=x<=%s"%(s, min_value, max_value)
    _func_hash[key] = f
    return f


def parse_string(line):
    """
    If the provided line is "None", we return None, and otherwise we return the
    line itself with whitespace stripped off the edges.
    """
    line = line.strip()
    if line == "None":
        return None
    return line.replace("\\n", "\n")


if __name__ == "__main__":
    class Test(Block):
        def __init__(self):
            self.a = 1
            self._a_func = int

    t = Test()
    t.b = 1
    print("a" in t)
    print("b" in t)
    print("_a_func" in t)
    print(t["a"])

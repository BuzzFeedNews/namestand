import namestand.patterns as p
import re

def combine(converters):
    def applicator(x):
        return reduce(lambda m, conv: conv(m), converters, x)
    def fn(x):
        if hasattr(x, "__iter__"):
            return map(fn, x)
        return applicator(x)
    return fn

def uppercase(x):
    return x.upper()

def lowercase(x):
    return x.lower()

def stripper(chars):
    def fn(x):
        return x.strip(chars)
    return fn

strip = stripper(None)

# Note: `pattern` can be a string or a compiled regular expression
def translator(pattern, replacement):
    def fn(x):
        if isinstance(pattern, re._pattern_type):
            return re.sub(pattern, replacement, x)
        return x.replace(pattern, replacement)
    return fn

# `test` can be a function or a list/tuple
def defaulter(test, default_value):
    def fn(x):
        if hasattr(test, '__call__'):
            return x if test(x) else default_value
        return x if x in test else default_value
    return fn

def falsey_replacer(default_value):
    return defaulter(lambda x: x, default_value)

def init_num_prefixer(prefix_char):
    return translator(p.starts_with_num, r"{0}\1".format(prefix_char))

underscore = translator(p.non_alphanumeric, "_")

remove_non_namey = translator(p.non_namey, "")

clean_comma_suffix = translator(p.comma_suffix, r" \1")

remove_name_cruft = translator(p.name_cruft, "")

remove_company_cruft = translator(p.company_cruft, "")

flip_last_first = translator(p.last_first, r"\2 \1")

compress_whitespace = translator(p.whitespace, r" ")


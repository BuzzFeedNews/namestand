# namestand

`namestand` is a Python library for easily transforming/standardizing lists of names (and other strings). No magic here, just a collection of useful tools.

`namestand` was developed with unwieldy database column–names in mind, but can by applied to any list of strings. Other uses might include: standardizing political donor names, normalizing survey responses, et cetera.

## Installation

```
pip install namestand
```

## Pre-Built Converters

`namestand` comes with a set* of broadly useful converters.

*Right now, just two of 'em. Contributions and suggestions welcome.

### namestand.downscore(string_or_list_of_strings)

Suggested usage: column names, form-response options, etc.

Steps:

1. Lowercases the string
2. Strips any leading and trailing whitespace
3. Converts any substring of non-ASCII alphanumeric characters to an underscore
4. Removes any leading and trailing underscores
5. Prefixes the string with "_" if it starts with a digit (which can otherwise cause trouble with `pandas` and other libraries). E.g., "2013 Happiness" becomes "_2013_happiness".

Example:

```python
namestand.downscore("Case Number") == "case_number"

namestand.downscore([
    "Case Number",
    "Case #",
    "Is Super-Duper?"
]) == [
    "case_number",
    "case",
    "is_super_duper"
]
```

### namestand.person_basic(string_or_list_of_strings) [very alpha]

Suggested usage: Donor names, etc.; note, though, that this converter does not have any special knowledge of the world, e.g., that "Riccchard" is likely a misspelling of "Richard".

Steps:

1. Uppercases the string
2. Strips any leading and trailing whitespace
3. Flips the "first" and "last" names if a comma is present
4. Removes the following characters that aren't either (unicode) letters, `'`, `-`, or spaces.

Along the way, it tries to gracefully handle name prefixes (Mr./Mrs./etc.) and suffixes (Jr./Sr./VII/Esq./etc.).

Example:

```python
namestand.person_basic("Antony, Mark") == "MARK ANTONY"
namestand.person_basic([
    u"Diego Velázquez-O'Connor",
    "Antony, Mark"
]) == [
    u"DIEGO VELÁZQUEZ-O'CONNOR",
    "MARK ANTONY"
]
```
### namestand.company_basic(string_or_list_of_strings) [very alpha]

Tries to remove common cruft from company names.

Steps:

1. Uppercases the string
2. Strips any leading and trailing whitespace
3. Removes the following characters that aren't either (unicode) letters, `'`, `-`, or spaces.
4. Removes "LLC", "LTD", and "INC"

Example:

```python
namestand.person_basic("American Banana Stand, Inc.") == "AMERICAN BANANA STAND"
```

## Custom Converters

You can easily build your own name-standardizing pipelines using the following tools.

### namestand.combine(list_of_transformers)

This function accepts a list of transformers (i.e., functions that accept a string and return a string) and returns a pipeline (i.e., a function that can be used in the same way as the pre-built converters). Converters themselves can be used as parts of pipelines, too. For example, if you wanted to change the `downscore` method to use hyphens, instead:

```python
downhyphen = namestand.combine([
    namestand.downscore,
    lambda x: x.replace("_", "-")
])
```

But `namestand` already comes with a few helpers for doing things like string replacements. So you could also do:

```python
downhyphen = namestand.combine([
    namestand.downscore,
    namestand.translator("_", "-")
])
```

Some helpful transformers:

- __`namestand.translator(pattern, replacement)`__: `pattern` can be a string or a compiled regex. Equivalent to an argument-aware combination of `lambda x: x.replace(string, replacement)` and `lambda x: re.sub(regex, replacement)`.

- __`namestand.swapper(pattern, replacement)`__: `pattern` can be a string or a compiled regex. If a given name matches the pattern (`re.match` for compiled regexes, `x in pattern` for string-`pattern`s), the entire name is replaced with the replacement. Otherwise, the given name is retained.

- __`namestand.stripper(chars_to_strip)`__: Equivalent to `lambda x: x.strip(chars_to_strip)`

- __`namestand.defaulter(test, default_value)`__: `test` can be either a list of "approved" values, or a function that returns True or False. If `x` doesn't pass the test (or isn't in the list), it is replaced with `default_value`.

## Tests

Additional usage examples can be found in [test/](test/). To test, run `nosetests` or `tox` from this repo's root directory. Currently tested, and passing, on the following Python versions:

```
2.7.14
3.5.4
3.6.4
3.7.5
3.8.0
```

## Feedback?

Pull requests, suggestions, etc. welcome.

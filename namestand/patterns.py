import re

non_alphanumeric = re.compile(r"[^0-9a-z]+", re.I)

non_namey = re.compile(r"[^\w\-' ]+", re.UNICODE)

last_first = re.compile(r"([^,]*), +([^,]*)")

starts_with_num = re.compile(r"^(\d)")

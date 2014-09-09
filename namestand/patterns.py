import re

non_alphanumeric = re.compile(r"[^0-9a-z]+", re.I)

non_namey = re.compile(r"[^\w\-' ]+", re.UNICODE)

comma_suffix = re.compile(r", *(JR|SR|I+|IV|VI*)\b")

last_first = re.compile(r"([^,]*), +([^,]*)")

starts_with_num = re.compile(r"^(\d)")

name_cruft = re.compile(r"\b(MR|MS|MRS|ESQ|SIR|HON)\b")

company_cruft = re.compile(r"\b(LLC|LTD|INC)\b")

whitespace = re.compile(r"\s+")

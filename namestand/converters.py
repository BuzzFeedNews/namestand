import namestand.utils as u

downscore = u.combine([
    u.lowercase,
    u.strip,
    u.underscore,
    u.stripper("_"),
    u.init_num_prefixer("_")
])

person_basic = u.combine([
    u.uppercase,
    u.strip,
    u.flip_last_first,
    u.clean_person,
    u.compress_whitespace
])

company_basic = u.combine([
    u.uppercase,
    u.clean_person,
    u.remove_company_cruft,
    u.strip,
    u.compress_whitespace
])

# -*- coding: utf-8 -*-
import namestand
import re
cols = """
Id
Id2
Geography
Estimate; EMPLOYMENT STATUS - Population 16 years and over
Margin of Error; EMPLOYMENT STATUS - Population 16 years and over
Percent; EMPLOYMENT STATUS - Population 16 years and over
Percent Margin of Error; EMPLOYMENT STATUS - Population 16 years and over
Estimate; EMPLOYMENT STATUS - In labor force
Margin of Error; EMPLOYMENT STATUS - In labor force
Percent; EMPLOYMENT STATUS - In labor force
Percent Margin of Error; EMPLOYMENT STATUS - In labor force
Estimate; EMPLOYMENT STATUS - In labor force - Civilian labor force
Margin of Error; EMPLOYMENT STATUS - In labor force - Civilian labor force
Percent; EMPLOYMENT STATUS - In labor force - Civilian labor force
Percent Margin of Error; EMPLOYMENT STATUS - In labor force - Civilian labor force
Estimate; EMPLOYMENT STATUS - In labor force - Civilian labor force - Employed
Margin of Error; EMPLOYMENT STATUS - In labor force - Civilian labor force - Employed
Percent; EMPLOYMENT STATUS - In labor force - Civilian labor force - Employed
Percent Margin of Error; EMPLOYMENT STATUS - In labor force - Civilian labor force - Employed
""".strip().split("\n")

def test_downscore():
   assert(namestand.downscore(cols[0]) == "id")
   c = namestand.downscore(cols) 
   assert(len(c) == len(cols))
   assert(c[0] == "id")
   assert(c[1] == "id2")
   assert(c[2] == "geography")
   assert(c[3] == "estimate_employment_status_population_16_years_and_over")

def test_num_prefixer():
    d = namestand.downscore
    assert(d("2013 Happiness") == "_2013_happiness")
    assert(d("The 2013 Happiness") == "the_2013_happiness")
    assert(namestand.init_num_prefixer("n")("2013") == "n2013")

def test_translator():
    converter = namestand.combine([
        namestand.downscore,
        namestand.translator("estimate_", "est_"),
        namestand.translator("percent_", "pct_"),
        namestand.translator("margin_of_error_", "moe_"),
        namestand.translator("employment_status", "status"),
        namestand.translator("population", "pop"),
        namestand.translator("_years_and_over", "y"),
        namestand.translator("_civilian", "_civ"),
        namestand.translator("_labor_force", "_lf"),
    ])
    c = converter(cols)
    assert(c[2] == "geography")
    assert(c[3] == "est_status_pop_16y")
    assert(c[6] == "pct_moe_status_pop_16y")
    assert(c[-1] == "pct_moe_status_in_lf_civ_lf_employed")

def test_last_first():
    lf = namestand.utils.flip_last_first
    assert(lf("Antony, Mark") == "Mark Antony")

def test_flip_proper():
    fp = namestand.person_basic
    assert(fp("Antony, Mark") == "MARK ANTONY")
    assert(fp("Antony, Mark M.") == "MARK M ANTONY")
    assert(fp("Mark M. Antony") == "MARK M ANTONY")
    assert(fp(u"Mark M. Antoñy") == u"MARK M ANTOÑY")
    assert(fp(u"Diego Velázquez-O'Connor") == u"DIEGO VELÁZQUEZ-O'CONNOR")

def test_complex_names():
    c = namestand.person_basic
    assert(c("Nolpmet, John Esq.") == "JOHN NOLPMET")
    assert(c("Nolpmet, John Mr.") == "JOHN NOLPMET")
    assert(c("Nolpmet, John M. Mr.") == "JOHN M NOLPMET")
    assert(c("John Nolpmet, Jr.") == "JOHN NOLPMET JR")
    assert(c("John Nolpmet, VIII") == "JOHN NOLPMET VIII")

def test_company():
    c = namestand.company_basic
    assert(c("American Banana Stand, Inc.") == "AMERICAN BANANA STAND")

def test_list_defaulter():
    choices = [ "foo", "bar" ]
    x = namestand.combine([
        namestand.defaulter(choices, "other")
    ])
    orig = [ "gah", "bar", "foo" ]
    assert(x(orig) == [ "other", "bar", "foo" ])

def test_fn_defaulter():
    x = namestand.combine([
        namestand.falsey_replacer("NOPE")
    ])
    orig = [ None, False, "hi", "there" ]
    assert(x(orig) == [ "NOPE", "NOPE", "hi", "there" ])

def test_swapper():
    x = namestand.swapper("BUZZFEED", "BuzzFeed")
    y = namestand.swapper(re.compile("BUZZFEED", re.I), "BuzzFeed")
    assert(x("BUZZFEED INC") == "BuzzFeed")
    assert(x("THE BUZZFEED") == "BuzzFeed")
    assert(x("BuzzFeed Inc.") == "BuzzFeed Inc.")
    assert(y("BUZZFEED INC") == "BuzzFeed")
    assert(y("BuzzFeed Inc.") == "BuzzFeed")
    assert(y("The BuzzFeed Inc.") == "BuzzFeed")

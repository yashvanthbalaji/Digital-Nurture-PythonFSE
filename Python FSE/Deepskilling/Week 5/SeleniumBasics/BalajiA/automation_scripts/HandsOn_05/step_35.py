# step35
# Ranking locator strategies from MOST to LEAST preferred for
# maintainable automation, with reasons (just notes, printed for the record)

ranking = [
    ("1. ID", "Unique per page by HTML rules, fastest to search, and "
               "very readable. Breaks only if the id itself is renamed."),
    ("2. CSS Selector (attribute/id based)", "Fast, readable, and can "
               "target most elements without needing text matching."),
    ("3. NAME", "Usually unique on forms, readable, but not guaranteed "
               "unique like id, and not every element has a name."),
    ("4. XPath (relative, attribute-based)", "Flexible and can do things "
               "CSS can't, like matching visible text - but slightly "
               "slower and easier to write incorrectly."),
    ("5. CLASS_NAME / TAG_NAME", "Often shared by MANY elements on a "
               "page (e.g. every button might share a class), so these "
               "are brittle and usually only safe combined with other "
               "filters."),
    ("6. XPath (absolute path)", "The LEAST preferred. It hard-codes the "
               "exact position of every parent element from  "
               "downward. Any layout change anywhere above the element "
               "breaks the locator instantly."),
]

for rank, reason in ranking:
    print(rank)
    print("  ->", reason)
    print()
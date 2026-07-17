notes = {
    "WebDriver": "Talks directly to ONE real browser. Sends commands like "
                 "'open this URL' or 'click this button' straight to it. "
                 "This is the only part we use in this course.",
    "Selenium Grid": "Solves 'I need to test on 20 browsers/machines at once'. "
                      "Runs the same test in parallel across many machines "
                      "instead of one after another.",
    "Selenium IDE": "A browser extension for beginners. You click around the "
                     "site and it records your actions, then can turn them "
                     "into code for you.",
}

for component, explanation in notes.items():
    print(component, "->", explanation)
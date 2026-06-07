"""Central glossary of beginner-friendly definitions for every key term used in
the curriculum.

Lessons list their ``key_terms`` as short strings; this module gives each term a
plain-English definition so the Lessons tab can show a real Vocabulary section
(term + meaning) instead of bare chips. Keeping definitions in one place keeps
them consistent across the many lessons that reuse the same words.

Keys are stored lowercase; look terms up with :func:`define` (case-insensitive).
"""
from __future__ import annotations

from typing import List, Tuple

GLOSSARY: dict[str, str] = {
    # Lesson 1 — Python mindset
    "program": "A set of step-by-step instructions a computer runs from top to bottom.",
    "print": 'A built-in function that shows text or values as output, e.g. print("hi").',
    "syntax": "The exact grammar and punctuation Python requires to understand your code.",
    "comment": "A note for humans that Python ignores, written after a # symbol.",
    "error message": "Python's feedback when something goes wrong; it names the line and the problem.",
    # Lesson 2 — Variables and types
    "variable": "A name that stores a value, e.g. age = 30.",
    "string": 'Text wrapped in quotes, e.g. "hello".',
    "integer": "A whole number with no decimal point, e.g. 42.",
    "float": "A number with a decimal point, e.g. 3.14.",
    "boolean": "A value that is either True or False.",
    "assignment": "Giving a variable a value using the = sign.",
    "comparison": "Checking how two values relate, e.g. == (equal) or > (greater than).",
    # Lesson 3 — Conditionals
    "if": "Runs a block of code only when a condition is True.",
    "elif": '"Else if" — checks another condition when the previous one was False.',
    "else": "Runs when none of the earlier if/elif conditions were True.",
    "condition": "An expression that is either True or False, used to make decisions.",
    "indentation": "The leading spaces that group lines into a block; Python uses it instead of braces.",
    "and": "Combines conditions; True only when both sides are True.",
    "or": "Combines conditions; True when at least one side is True.",
    # Lesson 4 — Loops
    "for loop": "Repeats a block once for each item in a sequence.",
    "range": "Produces a sequence of numbers, e.g. range(3) gives 0, 1, 2.",
    "sequence": "An ordered collection you can loop over, like a list or string.",
    "accumulator": "A variable that builds up a result across a loop, like a running total.",
    "iteration": "One pass through a loop; doing the repeated step once.",
    # Lesson 5 — Functions
    "function": "A reusable, named block of code that takes inputs and returns a result.",
    "parameter": "A named input listed in a function's definition.",
    "argument": "The actual value you pass into a function when you call it.",
    "return": "Sends a value back out of a function to whoever called it.",
    "scope": "Where a variable is visible; variables inside a function are local to it.",
    # Lesson 6 — Lists and dictionaries
    "list": "An ordered, changeable collection of items in square brackets, e.g. [1, 2, 3].",
    "dictionary": 'A collection of key→value pairs in curly braces, e.g. {"name": "Sam"}.',
    "index": "The position number of an item, starting at 0.",
    "key": "The label used to look up a value in a dictionary.",
    "value": "The data stored under a key, or held by a variable.",
    "collection": "Any structure that holds many items, like a list or dictionary.",
    # Lesson 7 — Debugging and tests
    "debugging": "Finding and fixing errors in your code.",
    "assert": "A statement that raises an error if a condition is False; used in tests.",
    "test": "Code that checks whether other code produces the expected result.",
    "exception": "An error raised while the program runs, like ValueError or KeyError.",
    "try": "Starts a block of risky code that might raise an exception.",
    "except": "Handles an exception raised in the matching try block.",
    # Lesson 8 — Files, JSON, APIs
    "file": "Saved data on disk that your program can read from or write to.",
    "json": "A common text format for structured data that maps to dicts and lists.",
    "api": "A service your program calls (often over the web) to get or send data.",
    "parse": "To read raw text and turn it into structured data your code can use.",
    "module": "A file of reusable Python code you import, e.g. import math.",
    "data processing": "Reading, cleaning, transforming, and summarizing data.",
    # Lesson 9 — OOP
    "class": "A blueprint for creating objects that bundle data and behavior.",
    "object": "A specific thing created from a class, with its own data.",
    "attribute": "A piece of data stored on an object, e.g. dog.name.",
    "method": "A function that belongs to an object, e.g. dog.bark().",
    "self": "The first parameter of a method; refers to the object it is called on.",
    "__init__": "The special method that sets up a new object's starting attributes.",
    # Lesson 10 — Prompt engineering
    "prompt": "The instructions you give an AI to get a useful answer.",
    "context": "Background information you give the AI so it understands your situation.",
    "constraints": "Rules that tell the AI what to do or avoid.",
    "output format": "How you want the AI's answer structured, e.g. a table or bullets.",
    "examples": "Sample inputs or outputs that show the AI exactly what you mean.",
    "verification": "A way to check that an answer or result is actually correct.",
    # Lesson 11 — Mini-project
    "project": "A small build that combines several skills into something that works.",
    "core logic": "The main rules or calculation at the heart of a program.",
    "input": "The data a program receives to work on.",
    "output": "The result a program produces.",
    "test case": "One specific input paired with the result you expect.",
    # Lesson 12 — Streamlit app
    "ui": "User interface: the parts of an app a person sees and interacts with.",
    "state": "Information an app remembers during a session, like progress or choices.",
    "secrets": "Sensitive values like API keys, kept out of your code.",
    "api key": "A private token that proves who you are when calling a service.",
    "ai feature": "A specific job done by AI inside an app, like generating a hint.",
    "learning loop": "The repeating cycle of read, practice, check, and reflect.",
    # Lesson 13 — Error handling
    "raise": "To trigger an exception yourself with the raise keyword.",
    "finally": "A block that always runs after try/except, used for clean-up.",
    "valueerror": 'An exception for a value of the right type but wrong content, e.g. int("abc").',
    # Lesson 14 — Comprehensions
    "list comprehension": "A one-line way to build a list, e.g. [x*2 for x in nums].",
    "filter": "Keeping only the items that pass a condition.",
    "expression": "A piece of code that produces a value, e.g. 2 + 3.",
    "dict comprehension": "A one-line way to build a dictionary from an iterable.",
    "iterable": "Anything you can loop over, like a list, string, or range.",
    # Lesson 15 — pandas
    "dataframe": "pandas' table of rows and columns, like a spreadsheet in code.",
    "series": "A single column of a pandas DataFrame.",
    "column": "One labeled field of data shared across all rows in a table.",
    "groupby": "A pandas operation that splits rows into groups to summarize each.",
    "aggregate": "To combine many values into one summary, like a sum or average.",
    "mean": "The average: the sum of values divided by how many there are.",
    # Lesson 16 — Dates and times
    "datetime": "Python's built-in module for working with dates and times.",
    "date": "A value holding a year, month, and day.",
    "timedelta": "A length of time, like the gap between two dates.",
    "fromisoformat": 'A method that parses a date from "YYYY-MM-DD" text.',
    "strftime": "A method that formats a date into readable text.",
    # Lesson 17 — Regex
    "regex": "Regular expression: a pattern language for finding text.",
    "pattern": "The template a regular expression matches against text.",
    "re": "Python's built-in regular-expression module.",
    "findall": "An re function that returns every match in the text as a list.",
    "raw string": 'A string written as r"..." so backslashes are taken literally.',
    "digit": "A single number character, 0-9; matched by \\d in regex.",
    # Lesson 18 — Clean code
    "type hint": "A note on a function showing expected input and output types.",
    "docstring": "A short text in triple quotes that documents what a function does.",
    "refactor": "Improving the structure of code without changing what it does.",
    "readability": "How easy code is for a human to read and understand.",
    "naming": "Choosing clear names that explain what code does.",
    # Lesson 19 — Testing
    "pytest": "A popular tool that finds and runs your test functions.",
    "edge case": "An unusual or boundary input where bugs often hide, like empty or zero.",
    "test-first": "Writing the test before the code, then making it pass (red→green).",
    # Lesson 20 — Web APIs
    "http": "The protocol browsers and programs use to talk to web servers.",
    "get": "An HTTP request that asks a server for data.",
    "status code": "A number from a server showing the result, e.g. 200 success, 404 not found.",
    "response": "What a server sends back after a request.",
    # Lesson 21 — Capstone
    "capstone": "A final project that pulls many skills together.",
    "split": 'A string method that breaks text into a list, e.g. "a b".split().',
    "frequency": "How many times something occurs.",
    "string methods": "Built-in actions on text, like .lower(), .split(), and .replace().",
}


def define(term: str) -> str:
    """Return the definition for ``term`` (case-insensitive), or a gentle fallback."""
    return GLOSSARY.get(term.strip().lower(), "A key term for this lesson — see the lesson text above for how it is used.")


def vocab_for_terms(terms: List[str]) -> List[Tuple[str, str]]:
    """Pair each term with its definition, ready to render as a vocab section."""
    return [(term, define(term)) for term in terms]

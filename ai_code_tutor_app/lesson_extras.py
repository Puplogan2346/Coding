"""Extra teaching content per lesson: a worked example and a common mistake.

Kept separate from ``curriculum.py`` (keyed by lesson id) so the lessons gain
depth without editing the large ``LESSONS`` data structure. The Lessons tab
looks these up by ``lesson.id`` and renders them under the explanation.
"""
from __future__ import annotations

WORKED_EXAMPLES: dict[str, str] = {
    "01-python-mindset": '''Run a tiny program and read the output line by line:

```python
print("Starting")
print(2 + 2)
print("Done")
```

Output:

```
Starting
4
Done
```

Python ran each line top to bottom: it printed the text, then the result of `2 + 2`, then the last line.''',
    "02-variables-types": '''Store different kinds of values, then use them together:

```python
name = "Sam"        # a string
age = 30             # an integer
is_member = True     # a boolean
print(name, "is", age)
```

Output: `Sam is 30`. Each variable holds a different type, and `print` can show several at once.''',
    "03-conditionals": '''Pick a grade based on a score:

```python
score = 75
if score >= 90:
    print("A")
elif score >= 70:
    print("B")
else:
    print("Keep practicing")
```

Output: `B`. Python checks each condition top to bottom and runs the first one that is True.''',
    "04-loops": '''Add up a list using an accumulator:

```python
total = 0
for number in [10, 20, 30]:
    total = total + number
print(total)
```

Output: `60`. The variable `total` grows by each number on every pass through the loop.''',
    "05-functions": '''Define a function, then call it with an argument:

```python
def greet(name):
    return "Hello, " + name

message = greet("Sam")
print(message)
```

Output: `Hello, Sam`. Here `name` is the parameter, `"Sam"` is the argument, and `return` hands the result back.''',
    "06-data-structures": '''Use a dictionary to look things up by name:

```python
scores = {"Sam": 90, "Lee": 85}
scores["Ada"] = 95        # add a new entry
print(scores["Sam"])      # look up by key
print(len(scores))        # how many entries
```

Output: `90` then `3`. You read a dictionary value by its key, not by a position number.''',
    "07-debugging-tests": '''Prove a function works with asserts:

```python
def double(n):
    return n * 2

assert double(3) == 6     # passes silently
assert double(0) == 0     # passes silently
print("Tests passed")
```

If `double` were wrong, the assert would raise an `AssertionError` pointing right at the failing line.''',
    "08-files-json-apis": '''Turn JSON text into a Python dictionary:

```python
import json

text = '{"name": "Sam", "age": 30}'
data = json.loads(text)   # text -> dict
print(data["name"])       # Sam
```

`json.loads` parses JSON text into a dictionary you can read with keys.''',
    "09-oop": '''Build an object from a class and call its method:

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return self.name + " says woof"

rex = Dog("Rex")
print(rex.bark())
```

Output: `Rex says woof`. `__init__` stores the name; `bark` is a method that uses `self`.''',
    "10-ai-prompting": '''Compare a weak prompt with a strong one.

Weak: `fix my code`

Strong:

```text
Role: Python tutor.
Task: explain why this loop prints nothing.
Code: for x in []: print(x)
Constraints: give a hint first, not the full answer.
```

The strong prompt supplies role, task, the actual code, and a constraint — so the reply is genuinely useful.''',
    "11-mini-projects": '''The heart of a quiz scorer compares answers to a key:

```python
def score(answers, key):
    return sum(1 for a, k in zip(answers, key) if a == k)

print(score(["A", "B", "C"], ["A", "X", "C"]))   # 2
```

`zip` pairs each answer with its correct answer, and we count how many match.''',
    "12-ai-apps-streamlit": '''A tiny interactive Streamlit app:

```python
import streamlit as st

name = st.text_input("Your name")
if st.button("Greet"):
    st.write("Hello, " + name)
```

The text input is the UI, the button triggers the logic, and `st.write` shows the output.''',
    "13-error-handling": '''Convert text to a number safely:

```python
def to_int(text):
    try:
        return int(text)
    except ValueError:
        return 0

print(to_int("42"))      # 42
print(to_int("hello"))   # 0
```

The bad input is caught by `except ValueError`, so the program keeps running instead of crashing.''',
    "14-comprehensions": '''Filter and keep only the even numbers:

```python
nums = [1, 2, 3, 4, 5]
evens = [n for n in nums if n % 2 == 0]
print(evens)   # [2, 4]
```

Read it as: "give me `n` for each `n` in `nums`, but only if `n` is even."''',
    "15-pandas-data": '''Average a value per group with pandas:

```python
import pandas as pd

df = pd.DataFrame({"team": ["A", "A", "B"], "points": [10, 20, 5]})
print(df.groupby("team")["points"].mean())
# A    15.0
# B     5.0
```

`groupby` splits the rows by team, then `.mean()` averages the points in each group.''',
    "16-dates-times": '''Measure the gap between two dates:

```python
from datetime import date

start = date(2024, 1, 1)
end = date(2024, 3, 1)
print((end - start).days)   # 60  (2024 is a leap year)
```

Subtracting two dates gives a timedelta; reading `.days` gives the number of days between them.''',
    "17-regex": '''Pull every number out of some text:

```python
import re

text = "Call 555 then 999"
print(re.findall(r"\\d+", text))   # ['555', '999']
```

`\\d+` matches one or more digits, and `findall` returns every match as a list of strings.''',
    "18-clean-code": '''The same function, before and after a clean-up:

```python
# Before
def c(p):
    return p * 0.9

# After
def apply_discount(price: float) -> float:
    """Return the price after a 10% discount."""
    return price * 0.9
```

The clean version explains itself with a good name, a type hint, and a one-line docstring.''',
    "19-pytest-testing": '''A small test file pytest can discover and run:

```python
# test_math.py
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5

def test_add_handles_zero():
    assert add(0, 0) == 0
```

Run `pytest` in your terminal and it finds every `test_` function and reports pass or fail.''',
    "20-web-apis": '''Call an API and read the response safely:

```python
import requests

response = requests.get("https://api.example.com/data")
if response.status_code == 200:
    data = response.json()
    print(data["temperature"])
else:
    print("Request failed:", response.status_code)
```

Always check the status code before reading the JSON body.''',
    "21-capstone-text-analyzer": '''Count words, then find the most common one:

```python
def word_frequencies(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts

freq = word_frequencies("the cat the dog the bird")
top = max(freq, key=freq.get)
print(top, freq[top])   # the 3
```

The counter builds a dictionary, then `max(..., key=freq.get)` finds the highest-count word.''',
}


COMMON_MISTAKES: dict[str, str] = {
    "01-python-mindset": '''Forgetting quotes around text. `print(Hello)` makes Python look for a variable named `Hello` and raises a NameError; `print("Hello")` prints the word.''',
    "02-variables-types": '''Adding a number to text without converting. `"Age: " + 30` raises a TypeError — convert the number first with `"Age: " + str(30)`.''',
    "03-conditionals": '''Using `=` (assignment) instead of `==` (comparison) in a condition. `if x = 5:` is an error; use `if x == 5:`.''',
    "04-loops": '''Off-by-one with range. `range(1, 5)` gives 1, 2, 3, 4 — the end number is not included.''',
    "05-functions": '''Confusing `print` and `return`. A function that only prints (and never returns) gives `None` when you try to use its result.''',
    "06-data-structures": '''Indexing a dictionary by position. Dictionaries are looked up by key (`scores["Sam"]`), not by number (`scores[0]`).''',
    "07-debugging-tests": '''Only testing the happy path. Always add an edge case — empty, zero, or negative — because that is where bugs hide.''',
    "08-files-json-apis": '''Mixing up `json.loads` (text → data) and `json.dumps` (data → text). Loads = load from text; dumps = dump to text.''',
    "09-oop": '''Forgetting `self`. Methods need `self` as the first parameter, and you access stored data with `self.name`, not just `name`.''',
    "10-ai-prompting": '''Asking vague questions with no context. The AI cannot help well without the task, the actual code, and what you already tried.''',
    "11-mini-projects": '''Assuming the answer list and key are the same length. `zip` stops at the shorter list, so decide how to handle a mismatch.''',
    "12-ai-apps-streamlit": '''Hard-coding an API key in the file. Keep secrets in environment variables or Streamlit secrets — never in committed code.''',
    "13-error-handling": '''Using a bare `except:` that swallows every error. Catch the specific exception you expect so real bugs still surface.''',
    "14-comprehensions": '''Cramming long, multi-step logic into one comprehension. If it is hard to read, a normal loop is the better choice.''',
    "15-pandas-data": '''Forgetting to select the column before aggregating, or expecting `groupby` to keep the original row order.''',
    "16-dates-times": '''Comparing a date to a string. Parse the text into a real date first with `date.fromisoformat("2024-01-01")`.''',
    "17-regex": '''Forgetting the raw-string prefix. Write patterns as `r"\\d+"` so Python does not misread the backslash.''',
    "18-clean-code": '''Relying on comments to explain confusing code. A clear name usually beats a comment — rename first.''',
    "19-pytest-testing": '''Naming test functions without the `test_` prefix. pytest only discovers and runs functions that start with `test_`.''',
    "20-web-apis": '''Reading `response.json()` without checking the status code first. A 404 or 500 has no useful data and may error.''',
    "21-capstone-text-analyzer": '''Forgetting to normalize case. Without `.lower()`, "The" and "the" are counted as two different words.''',
}


def worked_example(lesson_id: str) -> str:
    """Return the worked example markdown for a lesson, or empty string."""
    return WORKED_EXAMPLES.get(lesson_id, "")


def common_mistake(lesson_id: str) -> str:
    """Return the common-mistake note for a lesson, or empty string."""
    return COMMON_MISTAKES.get(lesson_id, "")

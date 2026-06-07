from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class QuizQuestion:
    prompt: str
    options: List[str]
    answer: str
    explanation: str


@dataclass(frozen=True)
class CodingChallenge:
    prompt: str
    starter_code: str
    tests: str
    hints: List[str]
    sample_solution: str


@dataclass(frozen=True)
class Lesson:
    id: str
    title: str
    level: str
    time_minutes: int
    objectives: List[str]
    explanation: str
    key_terms: List[str]
    quiz: List[QuizQuestion]
    challenge: CodingChallenge
    prompt_skill: str


LESSONS: List[Lesson] = [
    Lesson(
        id="01-python-mindset",
        title="Python mindset: commands, output, and mistakes",
        level="Beginner",
        time_minutes=25,
        objectives=[
            "Understand what a program is",
            "Use print to show output",
            "Read error messages without panic",
            "Write tiny experiments",
        ],
        explanation="""
Programming is giving a computer exact steps. Python reads your file from top to bottom and runs each instruction.

Start small. A useful beginner habit is to write one tiny idea, run it, observe what happened, and change one thing.

Example:

```python
print("Hello, learner")
print(2 + 3)
```

A mistake is feedback, not failure. If Python shows an error, look for three things:

1. The line number.
2. The error type, such as `NameError` or `SyntaxError`.
3. The message explaining what Python did not understand.

Comments are notes for humans:

```python
# This line explains the next line.
print("I am learning Python")
```
""".strip(),
        key_terms=["program", "print", "syntax", "comment", "error message"],
        quiz=[
            QuizQuestion(
                prompt="What does `print('Hi')` do?",
                options=["Stores the word Hi", "Shows Hi as output", "Creates a variable", "Deletes a file"],
                answer="Shows Hi as output",
                explanation="`print` sends text or values to the output area so you can see them.",
            ),
            QuizQuestion(
                prompt="What is the best first move when you see an error?",
                options=["Delete all code", "Read the line number and message", "Restart your computer", "Guess randomly"],
                answer="Read the line number and message",
                explanation="The line number and message usually tell you where to look and what went wrong.",
            ),
            QuizQuestion(
                prompt="Which line is a Python comment?",
                options=["// note", "<!-- note -->", "# note", "/* note */"],
                answer="# note",
                explanation="Python comments start with the `#` character.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create a function called `greet` that accepts a name and returns `Hello, NAME!`.",
            starter_code="""def greet(name):
    # Return a greeting string.
    pass
""",
            tests="""assert greet("Ava") == "Hello, Ava!"
assert greet("Jordan") == "Hello, Jordan!"
print("All tests passed for greet")
""",
            hints=[
                "A function can return a string with `return`.",
                "You can combine strings with `+` or use an f-string.",
                "The exclamation mark should be included at the end.",
            ],
            sample_solution="""def greet(name):
    return f"Hello, {name}!"
""",
        ),
        prompt_skill="When asking AI for help, include the exact error message and the code around the error.",
    ),
    Lesson(
        id="02-variables-types",
        title="Variables, strings, numbers, and booleans",
        level="Beginner",
        time_minutes=30,
        objectives=[
            "Store information in variables",
            "Use strings, integers, floats, and booleans",
            "Convert between basic types",
            "Explain the difference between `=` and `==`",
        ],
        explanation="""
A variable is a name that points to a value.

```python
name = "Maya"
age = 31
is_learning = True
```

Common types:

- `str`: text, like `"hello"`
- `int`: whole numbers, like `42`
- `float`: decimal numbers, like `3.14`
- `bool`: true or false values, `True` or `False`

`=` means assignment. It stores a value in a variable.

`==` means comparison. It asks whether two values are equal.

```python
score = 10       # assignment
score == 10      # comparison, evaluates to True
```
""".strip(),
        key_terms=["variable", "string", "integer", "float", "boolean", "assignment", "comparison"],
        quiz=[
            QuizQuestion(
                prompt="What does `name = 'Sam'` do?",
                options=["Compares name to Sam", "Stores 'Sam' in name", "Prints Sam", "Creates an error"],
                answer="Stores 'Sam' in name",
                explanation="A single equals sign assigns a value to a variable.",
            ),
            QuizQuestion(
                prompt="Which value is a boolean?",
                options=["'True'", "42", "True", "3.14"],
                answer="True",
                explanation="`True` without quotes is a boolean. `'True'` with quotes is a string.",
            ),
            QuizQuestion(
                prompt="What does `==` mean in Python?",
                options=["Assignment", "Addition", "Comparison", "A comment"],
                answer="Comparison",
                explanation="`==` compares whether two values are equal.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `total_with_tax(price, tax_rate)` that returns the total price rounded to two decimals.",
            starter_code="""def total_with_tax(price, tax_rate):
    # Example: total_with_tax(100, 0.08) should return 108.0
    pass
""",
            tests="""assert total_with_tax(100, 0.08) == 108.0
assert total_with_tax(19.99, 0.0725) == 21.44
assert total_with_tax(50, 0) == 50.0
print("All tests passed for total_with_tax")
""",
            hints=[
                "Tax is usually `price * tax_rate`.",
                "Total is price plus tax.",
                "Use `round(value, 2)`.",
            ],
            sample_solution="""def total_with_tax(price, tax_rate):
    total = price + (price * tax_rate)
    return round(total, 2)
""",
        ),
        prompt_skill="Ask AI to explain types by requesting examples and non-examples: `Give me 3 correct and 3 wrong examples of Python booleans.`",
    ),
    Lesson(
        id="03-conditionals",
        title="Decisions with if, elif, and else",
        level="Beginner",
        time_minutes=35,
        objectives=[
            "Use `if`, `elif`, and `else`",
            "Build comparison expressions",
            "Combine conditions with `and` and `or`",
            "Return different results based on data",
        ],
        explanation="""
Programs become useful when they make decisions.

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("Keep practicing")
```

Python uses indentation to know which lines belong inside a decision block.

Useful comparisons:

```python
age >= 18
name == "Alex"
score != 0
```

You can combine logic:

```python
if age >= 18 and has_ticket:
    print("Enter")
```
""".strip(),
        key_terms=["if", "elif", "else", "condition", "indentation", "and", "or"],
        quiz=[
            QuizQuestion(
                prompt="Which keyword handles the final fallback case?",
                options=["if", "elif", "else", "case"],
                answer="else",
                explanation="`else` runs when previous conditions were false.",
            ),
            QuizQuestion(
                prompt="What does indentation control in an `if` statement?",
                options=["Which lines belong to the block", "The font size", "The file name", "The data type"],
                answer="Which lines belong to the block",
                explanation="Python uses indentation to group code inside blocks.",
            ),
            QuizQuestion(
                prompt="Which expression means score is between 70 and 100 inclusive?",
                options=["score > 70 or score < 100", "score >= 70 and score <= 100", "score = 70 and 100", "score == 70 or 100"],
                answer="score >= 70 and score <= 100",
                explanation="Both conditions must be true, so `and` is the correct connector.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `grade_status(score)`. Return `invalid` when score is below 0 or above 100, `pass` when score is 70 or higher, otherwise `retry`.",
            starter_code="""def grade_status(score):
    # Return "invalid", "pass", or "retry".
    pass
""",
            tests="""assert grade_status(100) == "pass"
assert grade_status(70) == "pass"
assert grade_status(69) == "retry"
assert grade_status(-1) == "invalid"
assert grade_status(101) == "invalid"
print("All tests passed for grade_status")
""",
            hints=[
                "Check invalid scores first.",
                "Use `or` for below 0 or above 100.",
                "Then check pass, then fallback to retry.",
            ],
            sample_solution="""def grade_status(score):
    if score < 0 or score > 100:
        return "invalid"
    if score >= 70:
        return "pass"
    return "retry"
""",
        ),
        prompt_skill="For logic bugs, ask AI to trace your code with specific inputs: `Trace this function when score is 69, 70, and 101.`",
    ),
    Lesson(
        id="04-loops",
        title="Loops: repeat work without repeating yourself",
        level="Beginner",
        time_minutes=35,
        objectives=[
            "Use `for` loops to process sequences",
            "Use `range` for counting",
            "Understand accumulators",
            "Avoid common loop mistakes",
        ],
        explanation="""
Loops let you repeat a block of code.

```python
for number in range(3):
    print(number)
```

That prints 0, 1, and 2.

A common loop pattern is an accumulator: start with a value, update it during each loop, then return it.

```python
total = 0
for score in [80, 90, 100]:
    total = total + score
print(total)
```

You can loop through strings too:

```python
for letter in "python":
    print(letter)
```
""".strip(),
        key_terms=["for loop", "range", "sequence", "accumulator", "iteration"],
        quiz=[
            QuizQuestion(
                prompt="What values does `range(3)` produce in a loop?",
                options=["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3 only"],
                answer="0, 1, 2",
                explanation="`range(3)` starts at 0 and stops before 3.",
            ),
            QuizQuestion(
                prompt="What is an accumulator used for?",
                options=["Saving a running result", "Deleting a loop", "Changing Python versions", "Making text uppercase only"],
                answer="Saving a running result",
                explanation="An accumulator stores a result that changes during the loop.",
            ),
            QuizQuestion(
                prompt="Which line correctly loops through a list called `items`?",
                options=["for item in items:", "loop item of items:", "for items as item:", "repeat items:"],
                answer="for item in items:",
                explanation="Python `for` loops use `for item in sequence:`.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `count_vowels(text)` that returns how many vowels appear in the text. Count a, e, i, o, u in uppercase or lowercase.",
            starter_code="""def count_vowels(text):
    # Return the number of vowels in text.
    pass
""",
            tests="""assert count_vowels("python") == 1
assert count_vowels("Education") == 5
assert count_vowels("") == 0
assert count_vowels("AEIOU") == 5
print("All tests passed for count_vowels")
""",
            hints=[
                "Create a counter starting at 0.",
                "Convert each letter to lowercase before checking.",
                "Check whether a letter is in the string `aeiou`.",
            ],
            sample_solution="""def count_vowels(text):
    total = 0
    for letter in text:
        if letter.lower() in "aeiou":
            total += 1
    return total
""",
        ),
        prompt_skill="Ask AI for a loop trace table: `Make a table showing total after each loop for this code.`",
    ),
    Lesson(
        id="05-functions",
        title="Functions: reusable steps with inputs and outputs",
        level="Beginner",
        time_minutes=40,
        objectives=[
            "Define functions with `def`",
            "Use parameters and return values",
            "Separate printing from returning",
            "Write small functions that do one job",
        ],
        explanation="""
A function is a named block of reusable code.

```python
def double(number):
    return number * 2

result = double(5)
print(result)
```

Parameters are inputs. Return values are outputs.

Printing and returning are different:

- `print` shows a value to the user.
- `return` sends a value back to the code that called the function.

Good beginner function design: one function should do one clear job.
""".strip(),
        key_terms=["function", "parameter", "argument", "return", "scope"],
        quiz=[
            QuizQuestion(
                prompt="What keyword sends a value back from a function?",
                options=["print", "send", "return", "back"],
                answer="return",
                explanation="`return` is how a function gives a result back to the caller.",
            ),
            QuizQuestion(
                prompt="In `def double(number):`, what is `number`?",
                options=["A parameter", "A file", "A loop", "A comment"],
                answer="A parameter",
                explanation="A parameter is a named input in the function definition.",
            ),
            QuizQuestion(
                prompt="Why are small functions helpful?",
                options=["They are easier to test and understand", "They run only on phones", "They cannot have errors", "They remove all variables"],
                answer="They are easier to test and understand",
                explanation="Small focused functions are easier to reason about, reuse, and debug.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `format_name(first, last)` that returns a full name in title case, with extra spaces removed.",
            starter_code="""def format_name(first, last):
    # Example: format_name(" ada ", "LOVELACE") -> "Ada Lovelace"
    pass
""",
            tests="""assert format_name(" ada ", "LOVELACE") == "Ada Lovelace"
assert format_name("grace", "hopper") == "Grace Hopper"
assert format_name(" ALAN", " turing ") == "Alan Turing"
print("All tests passed for format_name")
""",
            hints=[
                "Use `.strip()` to remove outside spaces.",
                "Use `.title()` to title-case text.",
                "Combine first and last with one space between them.",
            ],
            sample_solution="""def format_name(first, last):
    clean_first = first.strip().title()
    clean_last = last.strip().title()
    return f"{clean_first} {clean_last}"
""",
        ),
        prompt_skill="Ask AI to review function design: `Does this function do one job? Suggest a cleaner version and explain why.`",
    ),
    Lesson(
        id="06-data-structures",
        title="Lists and dictionaries: storing many things",
        level="Beginner",
        time_minutes=45,
        objectives=[
            "Use lists for ordered collections",
            "Use dictionaries for labeled data",
            "Loop through collections",
            "Return structured results",
        ],
        explanation="""
Lists store ordered items.

```python
scores = [80, 95, 72]
print(scores[0])
```

Dictionaries store key-value pairs.

```python
student = {"name": "Nia", "score": 95}
print(student["name"])
```

Use a list when order matters or you have many similar items. Use a dictionary when each value needs a label.

You can combine them:

```python
students = [
    {"name": "Nia", "score": 95},
    {"name": "Omar", "score": 82},
]
```
""".strip(),
        key_terms=["list", "dictionary", "index", "key", "value", "collection"],
        quiz=[
            QuizQuestion(
                prompt="Which structure stores key-value pairs?",
                options=["list", "dictionary", "string", "range"],
                answer="dictionary",
                explanation="A dictionary maps keys to values.",
            ),
            QuizQuestion(
                prompt="What is the first index in a Python list?",
                options=["0", "1", "-1", "first"],
                answer="0",
                explanation="Python lists are zero-indexed, so the first item is at index 0.",
            ),
            QuizQuestion(
                prompt="Which code gets the score from `student = {'score': 90}`?",
                options=["student.score", "student['score']", "student(0)", "student->score"],
                answer="student['score']",
                explanation="Use square brackets with the key to get a dictionary value.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `summarize_scores(scores)` that returns a dictionary with `average`, `highest`, and `passed`. Passing means score >= 70. If the list is empty, return average 0, highest None, and passed 0.",
            starter_code="""def summarize_scores(scores):
    # Return a dictionary with average, highest, and passed.
    pass
""",
            tests="""assert summarize_scores([80, 90, 100]) == {"average": 90.0, "highest": 100, "passed": 3}
assert summarize_scores([60, 70, 69]) == {"average": 66.33, "highest": 70, "passed": 1}
assert summarize_scores([]) == {"average": 0, "highest": None, "passed": 0}
print("All tests passed for summarize_scores")
""",
            hints=[
                "Handle the empty list first.",
                "Use `sum(scores) / len(scores)` for average.",
                "Use `max(scores)` for highest.",
                "Use a loop or list comprehension to count passing scores.",
            ],
            sample_solution="""def summarize_scores(scores):
    if not scores:
        return {"average": 0, "highest": None, "passed": 0}

    average = round(sum(scores) / len(scores), 2)
    highest = max(scores)
    passed = 0
    for score in scores:
        if score >= 70:
            passed += 1

    return {"average": average, "highest": highest, "passed": passed}
""",
        ),
        prompt_skill="When asking AI about data structures, show a small example of the input and the exact output shape you want.",
    ),
    Lesson(
        id="07-debugging-tests",
        title="Debugging and tests: prove your code works",
        level="Beginner to Intermediate",
        time_minutes=45,
        objectives=[
            "Use print debugging intentionally",
            "Understand assertions",
            "Write simple tests",
            "Handle expected errors with try/except",
        ],
        explanation="""
Debugging means finding and fixing the difference between what you expected and what happened.

A simple test can use `assert`:

```python
def add(a, b):
    return a + b

assert add(2, 3) == 5
```

If the assertion is false, Python raises an error. That is useful because it shows your assumption failed.

Some errors are expected. You can handle them:

```python
try:
    number = int("abc")
except ValueError:
    number = 0
```

Good debugging questions:

- What did I expect?
- What actually happened?
- What is the smallest input that shows the problem?
""".strip(),
        key_terms=["debugging", "assert", "test", "exception", "try", "except"],
        quiz=[
            QuizQuestion(
                prompt="What does `assert x == 5` do?",
                options=["Always prints x", "Checks that x equals 5", "Changes x to 5", "Deletes x"],
                answer="Checks that x equals 5",
                explanation="An assertion checks a condition and raises an error if it is false.",
            ),
            QuizQuestion(
                prompt="Which block handles an expected error?",
                options=["try/except", "for/in", "def/return", "if/elif"],
                answer="try/except",
                explanation="`try/except` lets your program recover from expected exceptions.",
            ),
            QuizQuestion(
                prompt="What is a strong debugging habit?",
                options=["Change many things at once", "Use the smallest input that shows the issue", "Ignore error messages", "Never write tests"],
                answer="Use the smallest input that shows the issue",
                explanation="Small reproducible cases make bugs easier to isolate.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `safe_int(text, default=0)` that converts text to an int. If conversion fails, return the default value.",
            starter_code="""def safe_int(text, default=0):
    # Convert text to an int, or return default if it cannot be converted.
    pass
""",
            tests="""assert safe_int("42") == 42
assert safe_int("-7") == -7
assert safe_int("hello") == 0
assert safe_int("hello", default=99) == 99
print("All tests passed for safe_int")
""",
            hints=[
                "Use `int(text)` inside a try block.",
                "Catch `ValueError`.",
                "Return `default` inside the except block.",
            ],
            sample_solution="""def safe_int(text, default=0):
    try:
        return int(text)
    except ValueError:
        return default
""",
        ),
        prompt_skill="Ask AI for a failing test before asking it to fix code: `Write 3 tests that expose the bug in this function.`",
    ),
    Lesson(
        id="08-files-json-apis",
        title="Files, JSON, and APIs: talking to the outside world",
        level="Intermediate",
        time_minutes=50,
        objectives=[
            "Understand why JSON matters",
            "Parse JSON into Python data",
            "Explain APIs at a beginner level",
            "Design code that separates data fetching from data processing",
        ],
        explanation="""
Many apps exchange data as JSON. JSON looks similar to Python dictionaries and lists.

```json
{"name": "Riley", "skills": ["Python", "AI"]}
```

Python can parse JSON with the built-in `json` module:

```python
import json

text = '{"name": "Riley"}'
data = json.loads(text)
print(data["name"])
```

An API is a way for one program to ask another program for data or actions. A clean habit is to separate code that fetches data from code that processes data.

That makes your logic easier to test without needing the internet every time.
""".strip(),
        key_terms=["file", "JSON", "API", "parse", "module", "data processing"],
        quiz=[
            QuizQuestion(
                prompt="Which built-in module parses JSON in Python?",
                options=["math", "json", "random", "time"],
                answer="json",
                explanation="The built-in `json` module can parse and create JSON text.",
            ),
            QuizQuestion(
                prompt="Why separate fetching data from processing data?",
                options=["It makes logic easier to test", "It makes code impossible to read", "It stops Python from using variables", "It removes all errors"],
                answer="It makes logic easier to test",
                explanation="You can test processing with saved examples instead of calling the API every time.",
            ),
            QuizQuestion(
                prompt="What does `json.loads(text)` return for JSON object text?",
                options=["A Python dictionary", "A printed webpage", "A loop", "A syntax error every time"],
                answer="A Python dictionary",
                explanation="A JSON object maps naturally to a Python dictionary.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `parse_usernames(json_text)` that receives JSON text for a list of users and returns a list of usernames.",
            starter_code="""def parse_usernames(json_text):
    # json_text example: '[{"username": "ada"}, {"username": "grace"}]'
    pass
""",
            tests="""import json
sample = '[{"username": "ada"}, {"username": "grace"}]'
assert parse_usernames(sample) == ["ada", "grace"]
assert parse_usernames("[]") == []
assert parse_usernames(json.dumps([{"username": "linus"}])) == ["linus"]
print("All tests passed for parse_usernames")
""",
            hints=[
                "Import the built-in `json` module.",
                "Use `json.loads(json_text)` to parse the text.",
                "Loop through each user dictionary and collect `user['username']`.",
            ],
            sample_solution="""import json

def parse_usernames(json_text):
    users = json.loads(json_text)
    names = []
    for user in users:
        names.append(user["username"])
    return names
""",
        ),
        prompt_skill="When asking AI for API code, ask it to separate `fetch_data()` from `process_data(data)` so you can test the logic.",
    ),
    Lesson(
        id="09-oop",
        title="Object-oriented basics: classes and objects",
        level="Intermediate",
        time_minutes=55,
        objectives=[
            "Understand classes as blueprints",
            "Create objects with attributes",
            "Write methods",
            "Know when not to use a class",
        ],
        explanation="""
A class is a blueprint. An object is one thing made from that blueprint.

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} says woof"

pet = Dog("Luna")
print(pet.speak())
```

`__init__` runs when the object is created. `self` refers to the current object.

Use a class when you have data and behavior that belong together. Do not force classes into every problem. Simple functions are often enough.
""".strip(),
        key_terms=["class", "object", "attribute", "method", "self", "__init__"],
        quiz=[
            QuizQuestion(
                prompt="What is a class?",
                options=["A blueprint for objects", "Only a number", "A Python error", "A comment"],
                answer="A blueprint for objects",
                explanation="A class defines what its objects store and can do.",
            ),
            QuizQuestion(
                prompt="What does `self` refer to inside a method?",
                options=["The current object", "The operating system", "A string only", "The previous file"],
                answer="The current object",
                explanation="`self` lets a method access the current object's attributes and methods.",
            ),
            QuizQuestion(
                prompt="When is a simple function often better than a class?",
                options=["When the task is small and stateless", "When you need attributes", "When many methods share data", "Never"],
                answer="When the task is small and stateless",
                explanation="If there is no shared state, a simple function may be clearer.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create a `TodoList` class. It should start empty, have `add(item)`, `complete(item)`, and `remaining()` methods. Completing an item removes it if present.",
            starter_code="""class TodoList:
    def __init__(self):
        pass

    def add(self, item):
        pass

    def complete(self, item):
        pass

    def remaining(self):
        pass
""",
            tests="""todos = TodoList()
assert todos.remaining() == []
todos.add("learn functions")
todos.add("practice lists")
assert todos.remaining() == ["learn functions", "practice lists"]
todos.complete("learn functions")
assert todos.remaining() == ["practice lists"]
todos.complete("missing item")
assert todos.remaining() == ["practice lists"]
print("All tests passed for TodoList")
""",
            hints=[
                "Store items in `self.items`.",
                "Use `.append(item)` to add.",
                "Use `if item in self.items:` before removing.",
                "Return a copy with `list(self.items)` to protect internal state.",
            ],
            sample_solution="""class TodoList:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def complete(self, item):
        if item in self.items:
            self.items.remove(item)

    def remaining(self):
        return list(self.items)
""",
        ),
        prompt_skill="Ask AI whether a problem should use functions or classes, and require it to justify the tradeoff.",
    ),
    Lesson(
        id="10-ai-prompting",
        title="Prompt engineering for coding and learning",
        level="Beginner to Intermediate",
        time_minutes=45,
        objectives=[
            "Write prompts with goal, context, constraints, and output format",
            "Ask AI for explanations that match your level",
            "Use examples to reduce ambiguity",
            "Evaluate AI answers instead of blindly copying them",
        ],
        explanation="""
A strong prompt is a clear request plus useful context.

A practical prompt template:

```text
Role: Act as a patient Python tutor.
Goal: Help me understand why my loop is wrong.
Context: I am a beginner and I know variables and if statements.
Code: <paste code>
Constraints: Do not give the final answer immediately. Ask me one question first.
Output: Give a hint, then a small example, then a check-in question.
```

For coding, AI is most helpful when you ask for reasoning, tests, and small steps.

Good request:

```text
Explain this error in beginner language. Then show the smallest fix and one test that proves it works.
```

Weak request:

```text
Fix my code.
```

Your job is to verify AI output. Run tests, read the code, and ask follow-up questions.
""".strip(),
        key_terms=["prompt", "context", "constraints", "output format", "examples", "verification"],
        quiz=[
            QuizQuestion(
                prompt="Which prompt is stronger?",
                options=["Fix this", "Explain this ValueError to a beginner and give one small test", "Do code", "Make it better"],
                answer="Explain this ValueError to a beginner and give one small test",
                explanation="It gives the task, audience, and desired output.",
            ),
            QuizQuestion(
                prompt="Why include output format in a prompt?",
                options=["It tells AI how to structure the answer", "It makes Python faster", "It hides errors", "It removes the need to read"],
                answer="It tells AI how to structure the answer",
                explanation="Output format reduces ambiguity and makes answers easier to use.",
            ),
            QuizQuestion(
                prompt="What should you do before trusting AI-generated code?",
                options=["Run and test it", "Copy it without reading", "Delete your own code", "Assume it is perfect"],
                answer="Run and test it",
                explanation="AI output should be verified with tests and your own review.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `build_prompt(task, context, output_format)` that returns a clear prompt string containing the labels `Task:`, `Context:`, and `Output format:`.",
            starter_code="""def build_prompt(task, context, output_format):
    # Return a formatted prompt string.
    pass
""",
            tests="""prompt = build_prompt("Explain loops", "I know variables", "3 bullet points")
assert "Task: Explain loops" in prompt
assert "Context: I know variables" in prompt
assert "Output format: 3 bullet points" in prompt
assert prompt.index("Task:") < prompt.index("Context:") < prompt.index("Output format:")
print("All tests passed for build_prompt")
""",
            hints=[
                "Use an f-string with multiple lines.",
                "Include the exact labels from the prompt.",
                "The tests check both content and order.",
            ],
            sample_solution="""def build_prompt(task, context, output_format):
    return f"Task: {task}\\nContext: {context}\\nOutput format: {output_format}"
""",
        ),
        prompt_skill="Use the app's Prompt Lab to score your prompts before sending them to an AI model.",
    ),
    Lesson(
        id="11-mini-projects",
        title="Mini-project: build a quiz scorer",
        level="Intermediate",
        time_minutes=60,
        objectives=[
            "Break a project into functions",
            "Represent answers as lists",
            "Test a function with multiple cases",
            "Think like a builder instead of only a learner",
        ],
        explanation="""
Projects teach you how pieces fit together. Instead of starting with the full app, identify the smallest useful core.

For a quiz app, the core is scoring answers.

Inputs:

- a list of user answers
- a list of correct answers

Output:

- number correct

Once that works, you can add questions, progress tracking, and a user interface.

Builder habit: make the core logic work first, then add the UI.
""".strip(),
        key_terms=["project", "core logic", "input", "output", "test case", "iteration"],
        quiz=[
            QuizQuestion(
                prompt="What should you build first in a project?",
                options=["The smallest useful core", "The logo", "Every feature at once", "A long README only"],
                answer="The smallest useful core",
                explanation="A small core lets you test the idea before adding complexity.",
            ),
            QuizQuestion(
                prompt="Why separate logic from UI?",
                options=["Logic becomes easier to test", "UI stops working", "Variables disappear", "Python requires it always"],
                answer="Logic becomes easier to test",
                explanation="When logic is separate, you can test it without clicking through the interface.",
            ),
            QuizQuestion(
                prompt="What is a good next step after core logic works?",
                options=["Add one feature at a time", "Rewrite everything randomly", "Never test again", "Delete tests"],
                answer="Add one feature at a time",
                explanation="Small iterations reduce bugs and keep progress visible.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `score_quiz(answers, key)` that returns how many answers match in the same position. If the lists have different lengths, score only the pairs that exist.",
            starter_code="""def score_quiz(answers, key):
    # Compare answers to key and return count correct.
    pass
""",
            tests="""assert score_quiz(["A", "B", "C"], ["A", "B", "D"]) == 2
assert score_quiz(["A"], ["A", "B"]) == 1
assert score_quiz([], ["A"]) == 0
assert score_quiz(["x", "y"], ["a", "b"]) == 0
print("All tests passed for score_quiz")
""",
            hints=[
                "Use `zip(answers, key)` to pair items by position.",
                "Start `correct = 0`.",
                "Increment when the answer equals the key item.",
            ],
            sample_solution="""def score_quiz(answers, key):
    correct = 0
    for answer, correct_answer in zip(answers, key):
        if answer == correct_answer:
            correct += 1
    return correct
""",
        ),
        prompt_skill="For a project prompt, ask AI to build the smallest working version first and list later upgrades separately.",
    ),
    Lesson(
        id="12-ai-apps-streamlit",
        title="AI app basics with Streamlit",
        level="Intermediate",
        time_minutes=60,
        objectives=[
            "Understand simple web app structure",
            "Use state to remember interactions",
            "Keep secrets out of code",
            "Design AI features around a specific learning job",
        ],
        explanation="""
A simple interactive app needs three ideas:

1. UI: what the learner sees and clicks.
2. State: what the app remembers during a session.
3. Logic: what the app calculates or requests from AI.

For AI apps, never hard-code API keys in your source code. Use environment variables or your platform's secrets manager.

A good AI feature is specific. Instead of adding a generic chatbot, make it do a job:

- explain the current lesson
- generate a hint without giving the answer
- review a prompt with a rubric
- create a follow-up quiz from mistakes
""".strip(),
        key_terms=["UI", "state", "secrets", "API key", "AI feature", "learning loop"],
        quiz=[
            QuizQuestion(
                prompt="Where should API keys be stored?",
                options=["Hard-coded in public code", "In environment variables or secrets", "In a screenshot", "In a quiz answer"],
                answer="In environment variables or secrets",
                explanation="Secrets should be kept outside committed source code.",
            ),
            QuizQuestion(
                prompt="What is app state used for?",
                options=["Remembering information across interactions", "Changing Python syntax", "Deleting files", "Making all code public"],
                answer="Remembering information across interactions",
                explanation="State stores values like progress, chat history, or selected lesson.",
            ),
            QuizQuestion(
                prompt="Which AI feature is most specific for a learning app?",
                options=["A random chatbot", "A hint generator for the current lesson", "A blank page", "A button that says AI"],
                answer="A hint generator for the current lesson",
                explanation="Specific AI jobs are easier to design, test, and trust.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Create `make_lesson_card(title, progress)` that returns a dictionary with `title`, `progress`, and `status`. Status is `not started`, `in progress`, or `complete` based on progress 0, between 1 and 99, or 100+.",
            starter_code="""def make_lesson_card(title, progress):
    # Return a dictionary describing lesson progress.
    pass
""",
            tests="""assert make_lesson_card("Loops", 0) == {"title": "Loops", "progress": 0, "status": "not started"}
assert make_lesson_card("Loops", 50) == {"title": "Loops", "progress": 50, "status": "in progress"}
assert make_lesson_card("Loops", 100) == {"title": "Loops", "progress": 100, "status": "complete"}
assert make_lesson_card("Loops", 120)["status"] == "complete"
print("All tests passed for make_lesson_card")
""",
            hints=[
                "Use if/elif/else to choose the status.",
                "Return a dictionary with exactly the keys in the tests.",
                "Progress of 100 or more means complete.",
            ],
            sample_solution="""def make_lesson_card(title, progress):
    if progress <= 0:
        status = "not started"
    elif progress < 100:
        status = "in progress"
    else:
        status = "complete"

    return {"title": title, "progress": progress, "status": status}
""",
        ),
        prompt_skill="Before building an AI app, write a one-sentence job statement: `This AI helps the learner do X when Y happens.`",
    ),
    Lesson(
        id="13-error-handling",
        title="Error handling: try, except, and resilient code",
        level="Intermediate",
        time_minutes=35,
        objectives=[
            "Catch errors with try and except",
            "Handle specific error types instead of hiding all of them",
            "Use else and finally for clean-up",
            "Validate input so code fails politely instead of crashing",
        ],
        explanation="""
Real programs meet messy input: empty files, typos, missing keys, division by zero. **Error handling** lets your code respond instead of crashing.

The core tool is `try` / `except`:

```python
try:
    number = int(user_text)
except ValueError:
    number = 0  # a safe fallback
```

Python runs the `try` block. If a matching error happens, it jumps to `except` instead of stopping the whole program.

Catch *specific* errors, not everything:

```python
try:
    total = price / quantity
except ZeroDivisionError:
    total = 0
```

A bare `except:` that swallows every error hides real bugs. Name the error you expect.

Two helpers complete the pattern:

- `else` runs only when the `try` block had **no** error.
- `finally` runs **every time**, error or not — great for closing files.

```python
try:
    value = data["score"]
except KeyError:
    print("No score yet")
else:
    print("Score is", value)
finally:
    print("Done checking")
```

You can also *raise* your own error when something is wrong:

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age
```

Good rule of thumb: handle the errors you can reasonably expect, and let truly unexpected ones surface so you can fix the real bug.
""".strip(),
        key_terms=["exception", "try", "except", "raise", "finally", "ValueError"],
        quiz=[
            QuizQuestion(
                prompt="What does a try/except block do?",
                options=[
                    "Speeds up code",
                    "Catches and handles errors so the program can continue",
                    "Deletes variables",
                    "Hides all output",
                ],
                answer="Catches and handles errors so the program can continue",
                explanation="`try` runs risky code; `except` responds if a matching error happens.",
            ),
            QuizQuestion(
                prompt="Which error type does int('hello') raise?",
                options=["ValueError", "KeyError", "IndexError", "ZeroDivisionError"],
                answer="ValueError",
                explanation="The text is not a valid number, so Python raises a ValueError.",
            ),
            QuizQuestion(
                prompt="When does a `finally` block run?",
                options=[
                    "Only when there is an error",
                    "Only when there is no error",
                    "Always, whether or not an error happened",
                    "Never",
                ],
                answer="Always, whether or not an error happened",
                explanation="`finally` always runs, which makes it perfect for clean-up like closing files.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Write `safe_divide(a, b)` that returns `a / b`. If the division is impossible (dividing by zero or a non-number is passed in), return `None` instead of crashing.",
            starter_code="""def safe_divide(a, b):
    # Return a / b, or None if that is not possible.
    pass
""",
            tests="""assert safe_divide(10, 2) == 5
assert safe_divide(9, 3) == 3
assert safe_divide(5, 0) is None
assert safe_divide(7, "x") is None
print("All tests passed for safe_divide")
""",
            hints=[
                "Wrap the division in a try block.",
                "Catch ZeroDivisionError and TypeError in the except.",
                "Return None from the except block.",
            ],
            sample_solution="""def safe_divide(a, b):
    try:
        return a / b
    except (ZeroDivisionError, TypeError):
        return None
""",
        ),
        prompt_skill="Ask AI: 'What exceptions can this function raise, and how should I handle each one safely?'",
    ),
    Lesson(
        id="14-comprehensions",
        title="List comprehensions: transform data in one clean line",
        level="Intermediate",
        time_minutes=35,
        objectives=[
            "Write a list comprehension",
            "Add a condition to filter items",
            "Use a dictionary comprehension",
            "Know when a normal loop is clearer",
        ],
        explanation="""
A **list comprehension** builds a new list from an existing one in a single readable line. Compare the loop and the comprehension:

```python
# Loop version
doubled = []
for n in [1, 2, 3]:
    doubled.append(n * 2)

# Comprehension version
doubled = [n * 2 for n in [1, 2, 3]]   # [2, 4, 6]
```

Read it as: *"give me `n * 2` for each `n` in the list."*

Add an `if` at the end to **filter**:

```python
positives = [n for n in [-2, 5, -1, 8] if n > 0]   # [5, 8]
```

The same idea works for dictionaries:

```python
prices = {"apple": 1, "pear": 2}
doubled_prices = {name: cost * 2 for name, cost in prices.items()}
# {"apple": 2, "pear": 4}
```

Comprehensions are great for short transform-and-filter jobs. But reach for a regular loop when the logic is long, has several steps, or causes side effects (like printing or saving). Clear code beats clever code.
""".strip(),
        key_terms=["list comprehension", "filter", "expression", "dict comprehension", "iterable"],
        quiz=[
            QuizQuestion(
                prompt="What does [x * 2 for x in [1, 2, 3]] produce?",
                options=["[1, 2, 3]", "[2, 4, 6]", "[1, 4, 9]", "6"],
                answer="[2, 4, 6]",
                explanation="Each item is multiplied by 2, giving a new list [2, 4, 6].",
            ),
            QuizQuestion(
                prompt="How do you keep only items that pass a condition in a comprehension?",
                options=[
                    "Add an if at the end",
                    "Use a while loop",
                    "You cannot filter in a comprehension",
                    "Add a try block",
                ],
                answer="Add an if at the end",
                explanation="`[x for x in items if condition]` keeps only items where the condition is True.",
            ),
            QuizQuestion(
                prompt="When is a regular for loop clearer than a comprehension?",
                options=[
                    "When the logic is long or has side effects",
                    "Never",
                    "Only on Mondays",
                    "When the list is empty",
                ],
                answer="When the logic is long or has side effects",
                explanation="Comprehensions shine for short transforms; long or multi-step logic reads better as a loop.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Write `even_squares(numbers)` that returns a list of the squares of only the even numbers, using a list comprehension.",
            starter_code="""def even_squares(numbers):
    # Return squares of the even numbers, e.g. [1, 2, 3, 4] -> [4, 16].
    pass
""",
            tests="""assert even_squares([1, 2, 3, 4]) == [4, 16]
assert even_squares([5, 7, 9]) == []
assert even_squares([2, 4, 6]) == [4, 16, 36]
print("All tests passed for even_squares")
""",
            hints=[
                "An even number satisfies n % 2 == 0.",
                "The expression for each item is n * n.",
                "Put the if condition at the end of the comprehension.",
            ],
            sample_solution="""def even_squares(numbers):
    return [n * n for n in numbers if n % 2 == 0]
""",
        ),
        prompt_skill="Ask AI: 'Rewrite this loop as a list comprehension and tell me honestly whether it is more readable.'",
    ),
    Lesson(
        id="15-pandas-data",
        title="Data analysis with pandas: summarize real data",
        level="Project",
        time_minutes=50,
        objectives=[
            "Understand what a DataFrame is",
            "Select columns and filter rows",
            "Group rows and compute an average per group",
            "See how pandas turns many lines of code into one",
        ],
        explanation="""
**pandas** is the standard Python library for working with tables of data (spreadsheets, CSV files, query results). Its main object is the **DataFrame** — rows and columns, like a spreadsheet you control with code.

```python
import pandas as pd

data = {
    "category": ["fruit", "fruit", "veg"],
    "value": [10, 20, 6],
}
df = pd.DataFrame(data)
```

Select one column (a **Series**):

```python
df["value"]          # 10, 20, 6
df["value"].mean()   # 12.0
```

Filter rows with a condition:

```python
df[df["value"] > 8]  # only rows where value is above 8
```

The most powerful move is **group and aggregate** — answer "what is the average per category?" in one line:

```python
df.groupby("category")["value"].mean()
# fruit    15.0
# veg       6.0
```

That single line replaces a whole loop that keeps running totals and counts.

> Note: the in-app code checker runs in a locked-down mode that does not include pandas. So your hands-on challenge below builds the *same* grouped-average by hand with plain Python — this shows you exactly what `groupby().mean()` does for you. Run the pandas snippets above in the live app or your own machine, where pandas is installed.
""".strip(),
        key_terms=["DataFrame", "Series", "column", "groupby", "aggregate", "mean"],
        quiz=[
            QuizQuestion(
                prompt="What is a pandas DataFrame?",
                options=[
                    "A table of rows and columns",
                    "A single number",
                    "A Python error",
                    "A web server",
                ],
                answer="A table of rows and columns",
                explanation="A DataFrame is like a spreadsheet you control with code.",
            ),
            QuizQuestion(
                prompt="Which pandas operation groups rows and computes an average per group?",
                options=[
                    "df.groupby(col).mean()",
                    "df.delete()",
                    "df.print()",
                    "df.loop()",
                ],
                answer="df.groupby(col).mean()",
                explanation="groupby splits rows into groups, then .mean() averages each group.",
            ),
            QuizQuestion(
                prompt="Why summarize data instead of reading every row?",
                options=[
                    "Summaries reveal patterns quickly",
                    "Rows are illegal",
                    "It deletes the data",
                    "It makes the file bigger",
                ],
                answer="Summaries reveal patterns quickly",
                explanation="Averages, counts, and groups surface patterns you cannot see row by row.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Write `average_by_category(rows)` where `rows` is a list of dictionaries like `{\"category\": \"fruit\", \"value\": 10}`. Return a dictionary mapping each category to the average of its values. This is the plain-Python version of `df.groupby('category')['value'].mean()`.",
            starter_code="""def average_by_category(rows):
    # rows: list of {"category": str, "value": number}
    # Return {category: average_value}.
    pass
""",
            tests="""rows = [
    {"category": "fruit", "value": 10},
    {"category": "fruit", "value": 20},
    {"category": "veg", "value": 6},
]
assert average_by_category(rows) == {"fruit": 15.0, "veg": 6.0}
assert average_by_category([]) == {}
assert average_by_category([{"category": "x", "value": 4}]) == {"x": 4.0}
print("All tests passed for average_by_category")
""",
            hints=[
                "Keep a running total and a count for each category.",
                "Use dictionaries: totals[category] and counts[category].",
                "At the end, divide each total by its count (a dict comprehension works well).",
            ],
            sample_solution="""def average_by_category(rows):
    totals = {}
    counts = {}
    for row in rows:
        category = row["category"]
        totals[category] = totals.get(category, 0) + row["value"]
        counts[category] = counts.get(category, 0) + 1
    return {category: totals[category] / counts[category] for category in totals}
""",
        ),
        prompt_skill="Ask AI: 'Given columns [list them] and the question [your question], which pandas groupby and aggregation should I use?'",
    ),
    Lesson(
        id="16-dates-times",
        title="Working with dates and times",
        level="Intermediate",
        time_minutes=35,
        objectives=[
            "Create and read dates with the datetime module",
            "Parse a date from text",
            "Measure the difference between two dates",
            "Format a date for people to read",
        ],
        explanation="""
Apps constantly work with time: deadlines, streaks, "days since," schedules. Python's built-in **datetime** module handles all of it.

Make a date and read its parts:

```python
from datetime import date

today = date(2024, 5, 1)
print(today.year)   # 2024
print(today.month)  # 5
```

Parse a date that arrived as text (ISO format is `YYYY-MM-DD`):

```python
from datetime import date

deadline = date.fromisoformat("2024-12-25")
```

Subtract two dates to get a **timedelta**, then read `.days`:

```python
from datetime import date

start = date(2024, 1, 1)
end = date(2024, 1, 8)
gap = end - start
print(gap.days)   # 7
```

Format a date for humans with `strftime`:

```python
print(end.strftime("%B %d, %Y"))   # January 08, 2024
```

The same module has `datetime` (date + time) and `timedelta` (a length of time you can add or subtract). With these you can build countdowns, streak counters, and "due in N days" features.
""".strip(),
        key_terms=["datetime", "date", "timedelta", "fromisoformat", "strftime"],
        quiz=[
            QuizQuestion(
                prompt="Which module handles dates and times in Python?",
                options=["datetime", "random", "math", "json"],
                answer="datetime",
                explanation="The built-in datetime module provides date, time, datetime, and timedelta.",
            ),
            QuizQuestion(
                prompt="What do you get when you subtract two date objects?",
                options=[
                    "A timedelta showing the difference",
                    "A string",
                    "Nothing",
                    "An error every time",
                ],
                answer="A timedelta showing the difference",
                explanation="Subtracting dates gives a timedelta; read .days to get the number of days.",
            ),
            QuizQuestion(
                prompt="What text format does date.fromisoformat expect?",
                options=["YYYY-MM-DD", "MM/DD/YY", "a timestamp only", "day-month"],
                answer="YYYY-MM-DD",
                explanation="ISO format is year-month-day, e.g. 2024-12-25.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Write `days_between(start, end)` that takes two date strings in `YYYY-MM-DD` format and returns the number of days from `start` to `end` (a whole number).",
            starter_code="""def days_between(start, end):
    # start, end: date strings like "2024-01-01".
    # Return the number of days from start to end.
    pass
""",
            tests="""assert days_between("2024-01-01", "2024-01-08") == 7
assert days_between("2024-01-01", "2024-02-01") == 31
assert days_between("2024-01-10", "2024-01-10") == 0
print("All tests passed for days_between")
""",
            hints=[
                "Import date from datetime.",
                "Use date.fromisoformat to turn each string into a date.",
                "Subtract the two dates and return the result's .days.",
            ],
            sample_solution="""from datetime import date


def days_between(start, end):
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)
    return (end_date - start_date).days
""",
        ),
        prompt_skill="Ask AI: 'How do I parse this date format and calculate the difference in days between two dates?'",
    ),
    Lesson(
        id="17-regex",
        title="Pattern matching with regular expressions",
        level="Intermediate",
        time_minutes=40,
        objectives=[
            "Understand what a regular expression is",
            "Use the re module to search text",
            "Read common patterns like \\d and +",
            "Extract all matches from a string",
        ],
        explanation="""
A **regular expression** (regex) is a tiny pattern language for finding things in text: phone numbers, dates, words, digits. Python's built-in **re** module runs them.

The most useful function is `re.findall`, which returns **every** match as a list:

```python
import re

text = "Order 12 has 3 items"
re.findall(r"\\d+", text)   # ["12", "3"]
```

A few building blocks:

- `\\d` matches a single digit (0-9). `\\d+` matches one or more digits in a row.
- `\\w` matches a letter, digit, or underscore.
- `.` matches any character.
- `+` means "one or more"; `*` means "zero or more".

Write patterns as **raw strings** (`r"..."`) so backslashes are not misread by Python.

Other handy functions:

```python
re.search(r"\\d+", "abc 42")   # finds the first match (or None)
re.sub(r"\\d+", "#", "a1 b22")  # replace matches: "a# b#"
```

Regex feels cryptic at first, but for tasks like "pull all the numbers out" or "does this look like an email," it turns many lines of code into one pattern.
""".strip(),
        key_terms=["regex", "pattern", "re", "findall", "raw string", "digit"],
        quiz=[
            QuizQuestion(
                prompt="What is a regular expression used for?",
                options=[
                    "Finding and matching patterns in text",
                    "Doing math",
                    "Sorting numbers",
                    "Closing files",
                ],
                answer="Finding and matching patterns in text",
                explanation="Regex describes a text pattern so you can search, extract, or replace.",
            ),
            QuizQuestion(
                prompt="What does the pattern \\d+ match?",
                options=["One or more digits", "Only letters", "Spaces only", "Nothing"],
                answer="One or more digits",
                explanation="\\d is a digit and + means one or more, so \\d+ matches whole numbers.",
            ),
            QuizQuestion(
                prompt="Which re function returns all non-overlapping matches as a list?",
                options=["re.findall", "re.print", "re.delete", "re.loop"],
                answer="re.findall",
                explanation="re.findall returns every match in the text as a list of strings.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Write `find_numbers(text)` that returns a list of every whole number in the text, converted to integers. Example: `\"I have 2 cats and 10 fish\"` -> `[2, 10]`.",
            starter_code="""def find_numbers(text):
    # Return a list of all whole numbers in text, as ints.
    pass
""",
            tests="""assert find_numbers("I have 2 cats and 10 fish") == [2, 10]
assert find_numbers("no numbers here") == []
assert find_numbers("order 5, item 42, qty 100") == [5, 42, 100]
print("All tests passed for find_numbers")
""",
            hints=[
                "Import re and use re.findall with the pattern r\"\\d+\".",
                "findall returns strings; convert each to int.",
                "A list comprehension makes the conversion clean.",
            ],
            sample_solution="""import re


def find_numbers(text):
    return [int(match) for match in re.findall(r"\\d+", text)]
""",
        ),
        prompt_skill="Ask AI: 'Write a regular expression that matches [describe the pattern] and explain each part of it.'",
    ),
    Lesson(
        id="18-clean-code",
        title="Clean code: type hints, docstrings, and refactoring",
        level="Project",
        time_minutes=40,
        objectives=[
            "Write clear names that explain themselves",
            "Add type hints to function signatures",
            "Document functions with a short docstring",
            "Refactor a long function into smaller, named steps",
        ],
        explanation="""
Code is read far more often than it is written — usually by future you. **Clean code** is about being kind to that reader.

**Good names** remove the need for comments:

```python
# Unclear
def f(x):
    return x * 0.9

# Clear
def apply_discount(price):
    return price * 0.9
```

**Type hints** tell the reader (and tools) what goes in and what comes out:

```python
def apply_discount(price: float) -> float:
    return price * 0.9
```

**Docstrings** explain the job in one line:

```python
def apply_discount(price: float) -> float:
    \"\"\"Return the price after a 10% discount.\"\"\"
    return price * 0.9
```

**Refactoring** means improving the shape of code without changing what it does. If a function does three jobs, split it into three small, well-named functions. Small functions are easier to name, test, and reuse.

Clean code rules of thumb:

- One function, one job.
- Name things for what they mean, not how they work.
- Prefer a few clear lines over one clever line.
- If you need a comment to explain *what* code does, try a better name first.
""".strip(),
        key_terms=["type hint", "docstring", "refactor", "readability", "naming"],
        quiz=[
            QuizQuestion(
                prompt="What is the main benefit of clean code with good names and docstrings?",
                options=[
                    "It runs faster",
                    "It is easier for humans to read and maintain",
                    "It uses less memory",
                    "It hides bugs",
                ],
                answer="It is easier for humans to read and maintain",
                explanation="Clean code is mostly about the next human who reads it, including future you.",
            ),
            QuizQuestion(
                prompt="What does a type hint like def add(a: int, b: int) -> int communicate?",
                options=[
                    "The expected types of inputs and the return value",
                    "That the code is encrypted",
                    "That the function is private",
                    "Nothing at all",
                ],
                answer="The expected types of inputs and the return value",
                explanation="Type hints document expected input and output types for readers and tools.",
            ),
            QuizQuestion(
                prompt="When should you refactor a long function?",
                options=[
                    "When it does several jobs that could be smaller named functions",
                    "Never",
                    "Only if it crashes",
                    "Only on the last day",
                ],
                answer="When it does several jobs that could be smaller named functions",
                explanation="Splitting multi-job functions into small named ones improves readability and testing.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Write a clean function `summarize_scores(scores)` that returns a dictionary with the `min`, `max`, and `average` (rounded to 1 decimal) of a list of numbers. For an empty list, return all three as `None`. Use a clear name and a docstring.",
            starter_code="""def summarize_scores(scores: list) -> dict:
    \"\"\"Return min, max, and average (1 decimal) of scores; None for each if empty.\"\"\"
    pass
""",
            tests="""assert summarize_scores([10, 20, 30]) == {"min": 10, "max": 30, "average": 20.0}
assert summarize_scores([5]) == {"min": 5, "max": 5, "average": 5.0}
assert summarize_scores([2, 3]) == {"min": 2, "max": 3, "average": 2.5}
assert summarize_scores([]) == {"min": None, "max": None, "average": None}
print("All tests passed for summarize_scores")
""",
            hints=[
                "Handle the empty list first and return the None dictionary.",
                "Use the built-in min(), max(), sum(), and len() functions.",
                "Round the average with round(value, 1).",
            ],
            sample_solution="""def summarize_scores(scores: list) -> dict:
    \"\"\"Return min, max, and average (1 decimal) of scores; None for each if empty.\"\"\"
    if not scores:
        return {"min": None, "max": None, "average": None}
    return {
        "min": min(scores),
        "max": max(scores),
        "average": round(sum(scores) / len(scores), 1),
    }
""",
        ),
        prompt_skill="Ask AI: 'Review this function for naming, type hints, and a docstring, then suggest a cleaner version without changing its behavior.'",
    ),
    Lesson(
        id="19-pytest-testing",
        title="Automated testing with pytest",
        level="Intermediate",
        time_minutes=40,
        objectives=[
            "Understand why automated tests matter",
            "Write test functions with assert",
            "Cover normal cases and edge cases",
            "Practice the red-green test-first habit",
        ],
        explanation="""
A test is code that checks your other code. Automated tests catch bugs the moment something breaks — especially when you change code later.

The simplest test is an `assert`: it does nothing if the condition is True, and raises an error if it is False.

```python
def add(a, b):
    return a + b

assert add(2, 3) == 5      # passes silently
assert add(0, 0) == 0      # passes silently
```

**pytest** is the most popular test runner. You put tests in functions whose names start with `test_`, then run `pytest` in your terminal:

```python
# test_math.py
from mymath import add

def test_add_positive():
    assert add(2, 3) == 5

def test_add_with_zero():
    assert add(5, 0) == 5
```

```bash
pytest
```

pytest finds every `test_` function, runs it, and reports passes and failures.

Always test **edge cases** — the unusual inputs: empty strings, zero, negative numbers, very large values, missing data. Bugs love edges.

A powerful habit is **test-first** (red → green): write the test, watch it fail (red), then write just enough code to make it pass (green). The challenge below gives you the tests — your job is to write the function that turns them green.
""".strip(),
        key_terms=["test", "assert", "pytest", "edge case", "test-first"],
        quiz=[
            QuizQuestion(
                prompt="Why write automated tests?",
                options=[
                    "To catch bugs automatically when code changes",
                    "To make code slower",
                    "To delete code",
                    "To hide errors",
                ],
                answer="To catch bugs automatically when code changes",
                explanation="Tests re-check your code every time you run them, catching regressions early.",
            ),
            QuizQuestion(
                prompt="What does an assert statement do?",
                options=[
                    "Raises an error if a condition is False",
                    "Prints to the screen",
                    "Imports a module",
                    "Defines a class",
                ],
                answer="Raises an error if a condition is False",
                explanation="assert passes silently when True and raises AssertionError when False.",
            ),
            QuizQuestion(
                prompt="What is an edge case?",
                options=[
                    "An unusual or boundary input like empty or zero",
                    "The middle of a list",
                    "A type of comment",
                    "A faster algorithm",
                ],
                answer="An unusual or boundary input like empty or zero",
                explanation="Edge cases are boundary inputs where bugs commonly hide.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Make the tests pass: write `is_palindrome(text)` that returns True if the text reads the same forwards and backwards, ignoring spaces and capitalization.",
            starter_code="""def is_palindrome(text):
    # Ignore spaces and capitalization, then check if it reads the same backwards.
    pass
""",
            tests="""assert is_palindrome("racecar") == True
assert is_palindrome("Race car") == True
assert is_palindrome("hello") == False
assert is_palindrome("Was it a car or a cat I saw") == True
print("All tests passed for is_palindrome")
""",
            hints=[
                "Remove spaces with text.replace(' ', '') and lowercase with .lower().",
                "A string reversed is cleaned[::-1].",
                "Compare the cleaned string to its reverse.",
            ],
            sample_solution="""def is_palindrome(text):
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]
""",
        ),
        prompt_skill="Ask AI: 'Write 3 pytest tests for this function, including one edge case, and explain what each one checks.'",
    ),
    Lesson(
        id="20-web-apis",
        title="Calling web APIs: requests, status codes, and JSON",
        level="Intermediate",
        time_minutes=45,
        objectives=[
            "Understand the request and response cycle",
            "Read HTTP status codes",
            "Use the requests library to call an API",
            "Safely read values from a JSON response",
        ],
        explanation="""
An **API** lets your program ask another service for data over the web. You send a **request**; the service sends back a **response**.

The standard library for this is **requests** (install with `pip install requests`):

```python
import requests

response = requests.get("https://api.example.com/weather?city=Denver")
print(response.status_code)   # 200 means success
data = response.json()        # turn the JSON response into a Python dict
```

**Status codes** tell you what happened:

- `200` — success
- `404` — not found
- `500` — server error

Always check the status before trusting the data:

```python
if response.status_code == 200:
    data = response.json()
else:
    data = None
```

API responses are usually **JSON**, which becomes nested Python dictionaries and lists. Real responses are messy, so read values defensively (remember Lesson 13's try/except) in case a field is missing.

> Note: the in-app code checker has no internet and cannot install requests, so the challenge below works on a JSON response that has already been fetched for you. You practice the most important real-world skill: safely reading a value out of a messy response.
""".strip(),
        key_terms=["API", "HTTP", "GET", "status code", "JSON", "response"],
        quiz=[
            QuizQuestion(
                prompt="What does an HTTP status code of 200 mean?",
                options=["Success", "Not found", "Server error", "Redirect"],
                answer="Success",
                explanation="200 means the request succeeded; 404 is not found and 500 is a server error.",
            ),
            QuizQuestion(
                prompt="What format do most web APIs return data in?",
                options=["JSON", "A screenshot", "A Word document", "Raw electricity"],
                answer="JSON",
                explanation="JSON maps cleanly to Python dictionaries and lists.",
            ),
            QuizQuestion(
                prompt="Which Python library is commonly used to call web APIs?",
                options=["requests", "random", "turtle", "tkinter"],
                answer="requests",
                explanation="The requests library makes HTTP calls simple and readable.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Write `get_temperature(json_text)` that takes a JSON string from a weather API and returns the value at `main` -> `temp`. If that value is missing, return `None` instead of crashing.",
            starter_code="""def get_temperature(json_text):
    # Parse the JSON text and safely return data["main"]["temp"], or None.
    pass
""",
            tests="""assert get_temperature('{"main": {"temp": 72}}') == 72
assert get_temperature('{"main": {}}') is None
assert get_temperature('{"error": "not found"}') is None
print("All tests passed for get_temperature")
""",
            hints=[
                "Use json.loads(json_text) to turn the text into a dict.",
                "Wrap the lookup data['main']['temp'] in a try block.",
                "Catch KeyError and TypeError and return None.",
            ],
            sample_solution="""import json


def get_temperature(json_text):
    data = json.loads(json_text)
    try:
        return data["main"]["temp"]
    except (KeyError, TypeError):
        return None
""",
        ),
        prompt_skill="Ask AI: 'Show me how to call this API with requests, check the status code, and safely read a field from the JSON response.'",
    ),
    Lesson(
        id="21-capstone-text-analyzer",
        title="Capstone: build a word-frequency text analyzer",
        level="Project",
        time_minutes=55,
        objectives=[
            "Combine strings, loops, and dictionaries into one tool",
            "Count how often each word appears",
            "Handle the empty-input edge case",
            "See how small functions become a real feature",
        ],
        explanation="""
Time to combine skills into a real mini-tool: a **word-frequency analyzer** that counts how often each word appears in some text. This pattern powers search, tag clouds, and simple text analysis.

The plan uses things you already know:

1. **Normalize** the text: lowercase it so "The" and "the" count together.
2. **Split** it into words with `.split()`.
3. **Count** with a dictionary and the `.get(key, 0)` pattern.

```python
def word_frequencies(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts

word_frequencies("the cat the dog")
# {"the": 2, "cat": 1, "dog": 1}
```

Once you have the counts, you can build more on top using earlier lessons:

```python
# Top 3 words (Lesson 14 comprehension + sorting):
counts = word_frequencies(text)
top = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:3]
```

That is the whole idea of building software: small, well-named, tested functions that snap together into something useful. Your challenge is the core counter — the foundation everything else builds on.
""".strip(),
        key_terms=["capstone", "split", "dictionary", "frequency", "string methods"],
        quiz=[
            QuizQuestion(
                prompt="What does 'hello world'.split() return?",
                options=[
                    "['hello', 'world']",
                    "'hello world'",
                    "2",
                    "['h', 'e', 'l', ...]",
                ],
                answer="['hello', 'world']",
                explanation="split() with no argument breaks a string into a list of words on whitespace.",
            ),
            QuizQuestion(
                prompt="Which structure is best for counting how many times each word appears?",
                options=["A dictionary", "A single integer", "A boolean", "A file"],
                answer="A dictionary",
                explanation="A dictionary maps each word (key) to its count (value).",
            ),
            QuizQuestion(
                prompt="What does the dict method .get(key, 0) do?",
                options=[
                    "Returns the value or 0 if the key is missing",
                    "Deletes the key",
                    "Always returns 0",
                    "Sorts the dictionary",
                ],
                answer="Returns the value or 0 if the key is missing",
                explanation="get with a default avoids KeyError and is perfect for counting.",
            ),
        ],
        challenge=CodingChallenge(
            prompt="Write `word_frequencies(text)` that returns a dictionary mapping each lowercase word to how many times it appears. Words are separated by spaces. An empty string returns an empty dictionary.",
            starter_code="""def word_frequencies(text):
    # Return {word: count} using lowercase words split on whitespace.
    pass
""",
            tests="""assert word_frequencies("the cat the dog") == {"the": 2, "cat": 1, "dog": 1}
assert word_frequencies("") == {}
assert word_frequencies("Hi hi HI") == {"hi": 3}
print("All tests passed for word_frequencies")
""",
            hints=[
                "Lowercase the text first with .lower().",
                "Split into words with .split().",
                "Use counts[word] = counts.get(word, 0) + 1 inside a loop.",
            ],
            sample_solution="""def word_frequencies(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
""",
        ),
        prompt_skill="Ask AI: 'Help me extend my word-frequency analyzer to show the top 3 words, and suggest one edge case I should test.'",
    ),
]


def get_lesson_by_id(lesson_id: str) -> Lesson:
    for lesson in LESSONS:
        if lesson.id == lesson_id:
            return lesson
    raise KeyError(f"Unknown lesson id: {lesson_id}")


def lesson_titles() -> list[str]:
    return [lesson.title for lesson in LESSONS]

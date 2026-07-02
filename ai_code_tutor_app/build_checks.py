"""Static, no-execution checkpoint checks for guided project builds.

Parses learner code with ``ast`` and verifies structural requirements —
functions defined, constructs used, calls made — without ever executing the
code. This is what lets the Build Studio give real feedback on the public
deploy, where the subprocess code runner stays off.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class StepCheck:
    """One structural requirement for a build step.

    kind:
        "defines_function" — a function with name ``target`` exists.
        "uses" — the construct named by ``target`` appears (see _USES_NODES,
                 plus the special "main-guard" for ``if __name__ == "__main__"``).
        "calls" — a call to ``target`` appears; a dotted target like
                  "json.dumps" matches that attribute call, a bare target
                  matches either a plain name call or any attribute call with
                  that method name (e.g. "append").
    """

    kind: str
    target: str
    message: str


@dataclass(frozen=True)
class CheckResult:
    check: StepCheck
    passed: bool
    detail: str


_USES_NODES: dict[str, tuple[type, ...]] = {
    "if": (ast.If,),
    "for": (ast.For,),
    "while": (ast.While,),
    "function": (ast.FunctionDef, ast.AsyncFunctionDef),
    "loop": (ast.For, ast.While),
    "collection": (ast.Dict, ast.List, ast.ListComp, ast.DictComp),
    "try": (ast.Try,),
    "dict": (ast.Dict,),
    "list": (ast.List,),
    "return": (ast.Return,),
    "assert": (ast.Assert,),
    "f-string": (ast.JoinedStr,),
    "with": (ast.With,),
    "class": (ast.ClassDef,),
    "comprehension": (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp),
    "import": (ast.Import, ast.ImportFrom),
}


def _call_names(tree: ast.AST) -> set[str]:
    """Collect callable names: 'print', 'json.dumps', and bare method names."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            names.add(func.id)
        elif isinstance(func, ast.Attribute):
            names.add(func.attr)
            if isinstance(func.value, ast.Name):
                names.add(f"{func.value.id}.{func.attr}")
    return names


def _has_main_guard(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        test = node.test
        if not isinstance(test, ast.Compare):
            continue
        sides = [test.left, *test.comparators]
        if any(isinstance(side, ast.Name) and side.id == "__name__" for side in sides):
            return True
    return False


def _check_one(tree: ast.AST, check: StepCheck) -> CheckResult:
    if check.kind == "defines_function":
        defined = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        if check.target in defined:
            return CheckResult(check, True, f"Found def {check.target}(...)")
        return CheckResult(check, False, f"No function named {check.target} yet.")

    if check.kind == "uses":
        if check.target == "main-guard":
            if _has_main_guard(tree):
                return CheckResult(check, True, 'Found the if __name__ == "__main__": guard.')
            return CheckResult(check, False, 'Add an if __name__ == "__main__": block at the bottom.')
        node_types = _USES_NODES.get(check.target, ())
        if not node_types:
            return CheckResult(check, False, f"Unknown construct check: {check.target}")
        if any(isinstance(node, node_types) for node in ast.walk(tree)):
            return CheckResult(check, True, f"Found a {check.target} in your code.")
        return CheckResult(check, False, f"Your code does not use a {check.target} yet.")

    if check.kind == "calls":
        names = _call_names(tree)
        if check.target in names:
            return CheckResult(check, True, f"Found a call to {check.target}(...)")
        return CheckResult(check, False, f"Your code never calls {check.target}(...).")

    return CheckResult(check, False, f"Unknown check kind: {check.kind}")


def run_static_checks(code: str, checks: Sequence[StepCheck]) -> tuple[CheckResult, ...]:
    """Run every check against the code; a syntax error fails them all with the error."""
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        detail = f"Fix the syntax error first: line {exc.lineno}: {exc.msg}"
        return tuple(CheckResult(check, False, detail) for check in checks)
    return tuple(_check_one(tree, check) for check in checks)


def all_checks_pass(results: Sequence[CheckResult]) -> bool:
    return bool(results) and all(result.passed for result in results)

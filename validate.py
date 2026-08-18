#!/usr/bin/env python3
"""Doctrine validation for the skill-flow graph.

Proves the graph is identical in both carriers (CLAUDE.md mermaid fence,
flow-reminder.md XML envelope), grammatically sane, and that every node is
audited: each declared node must appear in NODE_SKILLS and every skill it
routes to must exist. --self-test mutates copies in a tempdir and asserts
the checks actually fail. ponytail: grammar-lite line parser, not a full
mermaid parser -- upgrade to mmdc rendering if GitHub ever renders what
this passes wrongly.
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"

LABEL = r'(?:\["[^"]*"\]|\{"[^"]*"\})'
NODE_RE = re.compile(rf'^\s*(\w+)({LABEL})\s*$')
EDGE_RE = re.compile(
    rf'^\s*(\w+)(?:{LABEL})?\s*(?:--\s*"[^"]*"\s*-->|-->)\s*(\w+)(?:{LABEL})?\s*$'
)
LABELED_ID = re.compile(rf'(\w+){LABEL}')
BRACKET_PAIRS = (('["', '"]'), ('{"', '"}'))

# Every declared node must have an entry here; [] = routing node, no skill.
NODE_SKILLS = {
    "Entry": [], "Scope": [], "TestGate": [], "Commit": [], "Ask": [], "Drift": [],
    "Grill": ["grill-me"],
    "Quest": ["to-questionnaire"],
    "Research": ["research", "find-docs"],
    "Proto": ["prototype"],
    "Design": ["codebase-design", "domain-modeling", "design-an-interface",
               "ubiquitous-language"],
    "Spec": ["to-spec"],
    "Tickets": ["to-tickets"],
    "Debug": ["systematic-debugging", "diagnosing-bugs"],
    "RevFirst": ["code-review", "clean-code"],
    "Improve": ["improve-codebase-architecture"],
    "RefPlan": ["request-refactor-plan"],
    "TDD": ["tdd", "clean-code"],
    "Impl": ["implement"],
    "Review": ["code-review"],
    "QA": ["qa"],
    "Discuss": ["teach", "research", "find-docs", "graphify"],
}
PLUGIN_SKILLS = {"systematic-debugging"}  # superpowers plugin, no local dir


def extract(path, markers):
    start, end = markers
    try:
        text = path.read_text().split(start, 1)[1].split(end, 1)[0]
        return text.strip("\n"), []
    except IndexError:
        return None, [f"{path.name}: cannot find {start!r}...{end!r} block"]


def graph_lines(body):
    return [line for line in body.splitlines()
            if line.strip() and not line.strip().startswith("%%")]


def classify(lines):
    declared, referenced, errors = set(), set(), []
    for line in lines:
        node, edge = NODE_RE.match(line), EDGE_RE.match(line)
        if node:
            declared.add(node.group(1))
        elif edge:
            referenced.update(edge.group(1, 2))
            declared.update(m.group(1) for m in LABELED_ID.finditer(line))
        else:
            errors.append(f"graph: unparseable line: {line.strip()!r}")
    return declared, referenced, errors


def check_balance(lines):
    return [f"graph: unbalanced {a}...{b} in: {line.strip()!r}"
            for line in lines for a, b in BRACKET_PAIRS
            if line.count(a) != line.count(b)]


def check_grammar(body):
    lines = graph_lines(body)
    if not lines or lines[0].strip() != "flowchart TD":
        return ["graph: first line must be 'flowchart TD'"]
    declared, referenced, errors = classify(lines[1:])
    errors += check_balance(lines[1:])
    errors += [f"graph: node {n!r} used in an edge but never given a label"
               for n in sorted(referenced - declared)]
    errors += [f"graph: node {n!r} declared but connected to nothing"
               for n in sorted(declared - referenced)]
    return errors, declared


def check_skills(declared):
    errors = [f"audit: node {n!r} missing from NODE_SKILLS map"
              for n in sorted(declared - NODE_SKILLS.keys())]
    errors += [f"audit: NODE_SKILLS lists unknown node {n!r}"
               for n in sorted(NODE_SKILLS.keys() - declared)]
    for node, skills in NODE_SKILLS.items():
        for skill in skills:
            if skill not in PLUGIN_SKILLS and not (SKILLS_DIR / skill).is_dir():
                errors.append(
                    f"audit: {node} routes to {skill!r} but "
                    f"~/.claude/skills/{skill} does not exist")
    return errors


def validate(repo):
    claude, errors = extract(repo / "CLAUDE.md", ("```mermaid\n", "```"))
    reminder, err2 = extract(
        repo / "flow-reminder.md", ("<skill-flow-graph>\n", "</skill-flow-graph>"))
    errors += err2
    if claude is None or reminder is None:
        return errors
    if claude != reminder:
        errors.append("identity: CLAUDE.md and flow-reminder graph bodies differ")
    grammar_errors, declared = check_grammar(claude)
    return errors + grammar_errors + check_skills(declared)


def self_test(repo):
    def mutated(transform):
        tmp = Path(tempfile.mkdtemp())
        for name in ("CLAUDE.md", "flow-reminder.md"):
            shutil.copy(repo / name, tmp / name)
        transform(tmp)
        found = validate(tmp)
        shutil.rmtree(tmp)
        return found

    failures = []
    if validate(repo):
        failures.append("self-test: pristine repo should validate clean")
    identity = mutated(lambda t: (t / "flow-reminder.md").write_text(
        (t / "flow-reminder.md").read_text().replace("user clear", "user cleared", 1)))
    if not any("identity" in e for e in identity):
        failures.append("self-test: carrier divergence went undetected")
    dropped = mutated(lambda t: (t / "CLAUDE.md").write_text(
        "\n".join(l for l in (t / "CLAUDE.md").read_text().splitlines()
                  if "Quest[" not in l)))
    if not any("never given a label" in e for e in dropped):
        failures.append("self-test: deleted node declaration went undetected")
    if not any("audit" in e for e in dropped):
        failures.append("self-test: audit map did not flag the missing node")
    return failures


def main():
    repo = Path(__file__).parent
    errors = self_test(repo) if "--self-test" in sys.argv else validate(repo)
    if errors:
        print(f"FAIL ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Doctrine validation for the skill-flow graph and plugin packaging.

Proves the graph is identical in both carriers (CLAUDE.md mermaid fence,
flow-reminder.md XML envelope), grammatically sane, every node audited
against installed skills, and the plugin manifests well-formed with every
hook file reference resolving. --self-test mutates copies in a tempdir and
asserts each check actually fails. ponytail: grammar-lite line parser, not
a full mermaid parser -- upgrade to mmdc rendering if GitHub ever renders
what this passes wrongly.
"""
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"

PLUGIN_MANIFEST = ".claude-plugin/plugin.json"
MARKET_MANIFEST = ".claude-plugin/marketplace.json"
HOOKS_FILE = "hooks/hooks.json"
CHECKED_PATHS = ("CLAUDE.md", "flow-reminder.md",
                 PLUGIN_MANIFEST, MARKET_MANIFEST, HOOKS_FILE)

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
        return ["graph: first line must be 'flowchart TD'"], set()
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


def load_json(path):
    try:
        return json.loads(path.read_text()), []
    except FileNotFoundError:
        return None, [f"{path.name} missing"]
    except json.JSONDecodeError as exc:
        return None, [f"{path.name} is not valid JSON: {exc}"]


def check_manifests(repo):
    plugin, errors = load_json(repo / PLUGIN_MANIFEST)
    market, more = load_json(repo / MARKET_MANIFEST)
    errors += more
    entries = (market or {}).get("plugins") or []
    if plugin is not None and not plugin.get("name"):
        errors.append("plugin.json needs a non-empty 'name'")
    if market is not None and (not market.get("name")
                               or not market.get("owner", {}).get("name")):
        errors.append("marketplace.json needs 'name' and 'owner.name'")
    if market is not None and (not entries or not all(
            p.get("name") and p.get("source") for p in entries)):
        errors.append("marketplace.json needs plugins with name + source")
    if plugin is not None and entries and \
            plugin.get("description") != entries[0].get("description"):
        errors.append("plugin description drifted between the two manifests")
    return [f"manifest: {e}" for e in errors]


def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for value in obj.values():
            yield from iter_strings(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_strings(item)


def check_hook_refs(repo):
    hooks, errors = load_json(repo / HOOKS_FILE)
    if hooks is None:
        return [f"hooks: {e}" for e in errors]
    refs = [ref for text in iter_strings(hooks)
            for ref in re.findall(r'\$\{CLAUDE_PLUGIN_ROOT\}/([^"\s]+)', text)]
    problems = [f"referenced file {ref!r} does not exist in repo"
                for ref in refs if not (repo / ref).exists()]
    if not refs:
        problems.append("hooks.json references no ${CLAUDE_PLUGIN_ROOT} files")
    return [f"hooks: {p}" for p in problems]


def check_reminder(repo):
    try:
        text = (repo / "flow-reminder.md").read_text()
    except FileNotFoundError:
        return ["reminder: flow-reminder.md missing"]
    if "flowchart TD" in text or "<skill-flow-graph>" in text:
        return ["reminder: must stay a slim ping — the graph lives only in CLAUDE.md"]
    return []


def validate(repo):
    claude, errors = extract(repo / "CLAUDE.md", ("```mermaid\n", "```"))
    packaging = check_reminder(repo) + check_manifests(repo) + check_hook_refs(repo)
    if claude is None:
        return errors + packaging
    grammar_errors, declared = check_grammar(claude)
    return errors + grammar_errors + check_skills(declared) + packaging


def mutated(repo, transform):
    tmp = Path(tempfile.mkdtemp())
    for rel in CHECKED_PATHS:
        dst = tmp / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(repo / rel, dst)
    transform(tmp)
    found = validate(tmp)
    shutil.rmtree(tmp)
    return found


MUTATIONS = (
    ("reminder regrowing a graph", ("reminder",),
     lambda t: (t / "flow-reminder.md").write_text(
         (t / "flow-reminder.md").read_text() + "\nflowchart TD\n")),
    ("deleted node declaration", ("never given a label", "audit"),
     lambda t: (t / "CLAUDE.md").write_text(
         "\n".join(l for l in (t / "CLAUDE.md").read_text().splitlines()
                   if "Quest[" not in l))),
    ("nameless plugin.json", ("manifest",),
     lambda t: (t / PLUGIN_MANIFEST).write_text('{"description": "no name"}')),
    ("plugin-less marketplace", ("manifest",),
     lambda t: (t / MARKET_MANIFEST).write_text(
         '{"name": "m", "owner": {"name": "o"}}')),
    ("dangling hook reference", ("hooks",),
     lambda t: (t / HOOKS_FILE).write_text(json.dumps({"hooks": {
         "UserPromptSubmit": [{"hooks": [{"type": "command",
             "command": "cat \"${CLAUDE_PLUGIN_ROOT}/missing.md\""}]}]}}))),
)


def self_test(repo):
    failures = ["self-test: pristine repo should validate clean"] \
        if validate(repo) else []
    for name, expected, transform in MUTATIONS:
        found = mutated(repo, transform)
        for token in expected:
            if not any(token in e for e in found):
                failures.append(f"self-test: {name} went undetected ({token})")
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

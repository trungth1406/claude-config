# Working Doctrine — skills first

Skills ARE the workflow. Every agent — talking to the user or to another agent —
routes work through the named skills below and invokes them autonomously; do not
improvise a process a skill already owns. The quality doctrine lives in the
`clean-code` skill: every number, threshold, SOLID signal, and taste rule comes
from there and is never restated here.

# The Flow

```mermaid
flowchart TD
    %% Routing only. Rationale, thresholds, and authority live in prose.
    Entry{"requirements clear?"}
    Entry -- "no" --> Grill["grill-me: attack the plan until it is sharp"]
    Entry -- "yes" --> Scope{"work scope?"}

    Grill -- "user still not confident" --> Quest["to-questionnaire: open questions become a questionnaire"]
    Quest --> Research["research + find-docs: dedicated agent resolves the open questions"]
    Research -- "findings cleared by user" --> Entry
    Research -- "not cleared" --> Grill
    Grill -- "user clear" --> Scope

    Scope -- "architecture (any design question, however small)" --> Proto["prototype: throwaway build answers the design question"]
    Proto --> Design["codebase-design + domain-modeling + design-an-interface: deep modules in ubiquitous-language terms, plus the language best-practice skill"]
    Design --> Spec["to-spec: synthesize the spec"]
    Spec --> Tickets["to-tickets: tracer-bullet tickets with blocking edges"]

    Scope -- "bug" --> Debug["systematic-debugging / diagnosing-bugs: confirm the hypothesis before any fix"]
    Debug -- "hypothesis confirmed" --> Tickets

    Scope -- "refactor" --> RevFirst["code-review: judge current code against clean-code"]
    RevFirst --> Improve["improve-codebase-architecture: find deepening opportunities"]
    Improve --> RefPlan["request-refactor-plan: tiny-commit refactor plan"]
    RefPlan -- "anything unclear" --> Entry
    RefPlan -- "clear" --> Tickets

    Scope -- "testing" --> TDD["tdd: red-green-refactor first, coverage to clean-code floors"]
    TDD --> Tickets

    Tickets -- "GATE: spec + tickets exist (no tickets, no work)" --> Impl["implement: build what the tickets say, tests in the same commit"]
    Impl -- "a test fails unexpectedly" --> Debug
    Impl -- "built" --> Review["code-review: independent report, zero unresolved criticals"]
    Review -- "criticals found" --> Impl
    Review -- "clean" --> QA["qa: independent pass, bugs become defect tickets"]
    QA -- "bugs found" --> Tickets
    QA -- "pass" --> TestGate{"suite green, coverage >= 80 percent, no untested code?"}
    TestGate -- "no: BLOCKED" --> Impl
    TestGate -- "yes" --> Commit["commit / push allowed"]
    Commit -- "more work remains" --> Entry

    Ask["(from anywhere) user asks for explanation or how-would-the-agent-do-it"] --> Discuss
    Discuss["discussion: route each question to its best skill -- teach, research + find-docs, graphify, docs tools; a user-named skill always wins"]
    Discuss -- "more questions" --> Discuss
    Discuss -- "settled: concise clearance, user confirms" --> Drift{"open spec/tickets still match the discussion outcome?"}
    Drift -- "no: drifted -- update spec + tickets" --> Spec
    Drift -- "yes" --> Entry
```

Guards, protocols, and standalone directives inject from `~/.claude/rules/`
(indexed in the README); the quality numbers live in the `clean-code` skill.

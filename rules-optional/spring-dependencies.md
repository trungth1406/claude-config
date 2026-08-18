# Spring — industrial-standard dependencies first

When the project is Spring-related (Spring Boot, Spring Cloud, Spring
Security, Spring Data, ...):

- Always look first for the industrial-standard library, starter, or
  dependency that already solves the problem — Spring's own starters and the
  battle-tested ecosystem around them — before writing anything by hand.
- Hand-rolled solutions ONLY when genuinely needed: no maintained standard
  covers the requirement, or the dependency's weight clearly outweighs a few
  lines. State the justification when hand-rolling.
- Resolve candidate libraries per the research-first rule (find-docs / ctx7 /
  context7) — pick current, maintained, majority-adopted options, never from
  memory.

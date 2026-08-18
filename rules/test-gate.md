# Test Gate — no untested code, no biased test fixes

- Code without tests is never committed or pushed. New or changed logic ships
  with its tests in the same commit — no test, no commit, no push.
- A failing test is never made to pass by editing the test. Always debug first
  (systematic-debugging / diagnosing-bugs) to prove the failure is not a logic
  bug. If it is a logic bug: file a defect ticket via /to-tickets and fix the
  code under that ticket — never bend the test's inputs or assertions. Only a
  test proven wrong by diagnosis may itself change, with the proof stated.
- Coverage hard floor: never below 80% — an absolute stop, no commit crosses
  it. The working floors remain the clean-code skill's (>=90% overall, >=95%
  critical paths); 80% is the never-cross line, not the target.

Full rationale: hard-guards.md in this directory. Quality authority: clean-code.

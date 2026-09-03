# Review pages — decisions and explanations land as a page, not a chat

- Any explanation or decision the owner must judge (a review, a design
  choice, a plan verdict) is delivered as a published artifact page, not
  console text. Console gets the link and a one-line summary.
- Every item on the page is drawn, not described: BEFORE (as planned or
  as is) and AFTER (the proposed change) side by side, same style, same
  example data, differences marked. Graphs, state machines, data flows;
  prose only as captions.
- Every item carries a ruling control (accept / change / reject) and a
  comment box that persists (artifact db). The agent reads them back
  before acting, answers each comment on the page under the item it
  belongs to, and never re-litigates in chat.
- One page per topic, updated in place (same URL); rulings survive the
  republish. Illustrative data is labeled as such.
- Every item shows its lifecycle as a pill, and the header tallies them:
  open (no agent response yet), reviewed (the agent responded, no ruling
  yet, or the owner says it is still unclear), decided (accept / change /
  reject recorded). A page is finished when nothing is open or reviewed.
- Later this becomes a schema-space node in neurons and possibly an app;
  until then it is this rule.

# AP News public CPU model verifier

**Powered by Kanana**

The candidate AP News verifier runs the public Kanana-1.5-15.7B-A3B-Instruct model on local server CPU. It does not expose a model API, redistribute weights, or use a paid AI inference service. News readers receive newsletter content, not access to the model. Deployment remains disabled until the unchanged actual semantic controls and recovered full-production rehearsal qualify.

The original model, conversion revision, exact file digest, copyright notice and responsible-use policy are recorded in [NOTICE](../third_party/kanana/NOTICE.txt). The unchanged upstream [Kanana License Agreement](../third_party/kanana/LICENSE.txt) accompanies this product documentation. These terms apply to Kanana materials and do not replace this repository's other applicable licenses.

The verifier uses the publisher's native dialogue format, including its initial empty system message. The pinned runtime adds exactly one BOS token; a real local tokenizer check verifies this before review. Only the observed final EOT token (128009) may terminate a verdict. EOM (128256), function calls, Python handoffs, unexpected channels, truncated contexts and exhausted output limits block acceptance.

Complete original source-free drafts, independent exhaustive factual word masks, exact agreement, a separate scope audit, the frozen independent ground-truth controls, and source entailment are all required. A successful protocol handshake does not establish semantic accuracy or deadline feasibility.

Each of the two source-blind target reviewers uses a completed native scope-analysis response before its final constrained decision. The planner validates exactly one original target and identifies its field, sentence ID and exact text before the complete reference context; it must not summarize or analyze the other context fields. Analysis has a finite 1,800-token budget and must end naturally at the verified EOT; a limit or partial response cannot be forced into a verdict. Only that reviewer's own completed analysis and the unchanged original input may appear in its final dialogue. Generated analysis remains fallible context, never evidence or approval. Private final receipts hash-link the exact raw analysis response.

The final global kind precedes the full word mask. A nonfactual decision must mark every original word nonfactual; a factual decision must contain factual words; uncertainty always blocks. Python validates these invariants independently of decoder constraints, and the two reviewers' kinds and complete masks must agree before the unchanged independent coverage audit. Planning analyses are never added to source-aware evidence requests. Extra deliberation does not relax the complete rehearsal's existing time limit.

The separate whole-inventory coverage audit uses ordinary Instruct completion with the complete semantic rules, including mandatory headline/report facts, quantifiers, attribution and negation. Its mode is recorded and checked separately during immutable evidence handoff; it receives no peer analyses and still rejects omissions or uncertainty.

The commitment contract distinguishes what the author affirms about the actual world from assumptions merely entertained in questions, hypothetical worlds or recommendations. It explicitly retains projected presuppositions, implicit headlines, future/capability/general claims, conditional causal relationships and attributed reporting acts. Wire labels are `actual_world_claim_present` / `no_actual_world_claim` / `uncertain`, with exhaustive `claim` / `not_claim` / `uncertain` word maps. Internal canonical factual ranges and all frozen expected controls are unchanged; renaming and clarification do not establish model competence.

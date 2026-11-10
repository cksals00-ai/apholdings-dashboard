# AP News public CPU model verifier

**Powered by Kanana**

The candidate AP News verifier runs the public Kanana-1.5-15.7B-A3B-Instruct model on local server CPU. It does not expose a model API, redistribute weights, or use a paid AI inference service. News readers receive newsletter content, not access to the model. Deployment remains disabled until the unchanged actual semantic controls and recovered full-production rehearsal qualify.

The original model, conversion revision, exact file digest, copyright notice and responsible-use policy are recorded in [NOTICE](../third_party/kanana/NOTICE.txt). The unchanged upstream [Kanana License Agreement](../third_party/kanana/LICENSE.txt) accompanies this product documentation. These terms apply to Kanana materials and do not replace this repository's other applicable licenses.

The verifier uses the publisher's native dialogue format, including its initial empty system message. The pinned runtime adds exactly one BOS token; a real local tokenizer check verifies this before review. Only the observed final EOT token (128009) may terminate a verdict. EOM (128256), function calls, Python handoffs, unexpected channels, truncated contexts and exhausted output limits block acceptance.

Complete original source-free drafts, independent exhaustive factual word masks, exact agreement, a separate scope audit, the frozen independent ground-truth controls, and source entailment are all required. A successful protocol handshake does not establish semantic accuracy or deadline feasibility.

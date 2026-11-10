# Candidate credential-free CPU verifier (not yet qualified)

Writer remains the pinned public Qwen3-8B GGUF. Art planning remains Qwen3-30B-A3B-Instruct-2507. Factual verification now uses the separate native-thinking Qwen3.5-9B candidate. Provider scores do not qualify publication: the actual11 scope controls,5 historical controls and full production/recovery/public/mail trial must pass before activation.

Verifier base publisher and Apache-2.0 license: https://huggingface.co/Qwen/Qwen3.5-9B
Quantized distribution: bartowski/Qwen_Qwen3.5-9B-GGUF
Immutable revision:182be2fd6c7bc44887d88a91cb03ff009cc9f549
File:Qwen_Qwen3.5-9B-Q6_K.gguf (7,958,818,848 bytes)
SHA256:073a9275e65d9c8cd2819cf5f77b99fbaa6e87ba591da6bbaa86ec073a64bfef

Art planning uses bartowski/Qwen_Qwen3-30B-A3B-Instruct-2507-GGUF at6c6e8692f43e4ca663f7ece8229a1361090d3a4c, file Qwen_Qwen3-30B-A3B-Instruct-2507-Q3_K_M.gguf, SHA256327c6e0826bee8f19172e96c94bb7bba385f7a39d08314803652df9942401c4f.

Each downloaded verifier/art file is digest-checked. Native verifier input ends with the publisher's assistant/thinking prefix. Reasoning runs without JSON grammar and must naturally close before an8192-token limit; a timeout, missing close or exhausted budget fails rather than forcing a verdict. Only then does the same original request plus its own completed reasoning produce schema-constrained JSON. Both raw stages are preserved. Context shifting is disabled and any engine-reported context truncation fails before a verdict, including the reasoning stage. Separate calls never receive each other's reasoning or answers; a third source-blind full-context audit still checks the inventory. Uncertainty or disagreement never grants approval. Sampling follows the thinking model's published1.0/0.95/20/0 settings. Reasoning alone uses the publisher-supported presence penalty1.5 to discourage observed repeated deliberation; the final schema-bound quotations have no presence penalty, preserving exact repeated source words.

Public weights download with token=False and inference is only on127.0.0.1/CPU. No hosted model endpoint, AI API credential or payment is used. Writer/verifier/art identities and caches are distinct. Review/cache revisions invalidate previous decisions. Production remains disabled until actual qualification.

The previous Q3 MoE candidate failed the actual independent scope and historical controls (42762262293); no production activation. The Q6 dense candidate changes weights, not labels, expected ranges or factual criteria. It requires llama.cpp b12244 (d5bbcd1f31dba754f716a26c3a4784502a6b9ede), downloaded archive SHA256 c1d7e7f31b5c43f3e5d44f667b4d57104217be3e5f2060320cd3735651238849. It remains unqualified until identical actual controls and full trial pass.

The first dense-candidate scope call (42791112952) exhausted8192 thinking tokens while repeatedly guessing absent response layout and recounting the rows. Native reasoning now receives the actual JSON contract used in the answer stage as escaped task data (format/cardinality/allowed values only, no expected verdicts). Reasoning still has no grammar constraint, must close naturally, and fails on exhaustion or truncation. Factual standards and synthetic/historical inputs are unchanged.

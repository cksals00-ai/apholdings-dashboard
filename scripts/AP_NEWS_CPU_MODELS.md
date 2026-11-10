# Credential-free CPU production candidate — not yet qualified

Source collection, copy, art and document checks run on server CPU. Public model files download with `token=False`; inference accepts requests only on127.0.0.1. No hosted AI endpoint, AI API credential or payment is used. Model-provider scores never qualify publication: actual11 synthetic scope controls,5 historical controls and the full production/recovery/public/mail rehearsal must pass before activation.

## Fixed models

- Writer: `Qwen/Qwen3-8B-GGUF`, revision `7c41481f57cb95916b40956ab2f0b139b296d974`, file `Qwen3-8B-Q4_K_M.gguf`.
- Native verifier: publisher/Apache-2.0 https://huggingface.co/Qwen/Qwen3.5-9B ; distribution `bartowski/Qwen_Qwen3.5-9B-GGUF`, revision `182be2fd6c7bc44887d88a91cb03ff009cc9f549`, file `Qwen_Qwen3.5-9B-Q6_K.gguf` (7,958,818,848 bytes), SHA256 `073a9275e65d9c8cd2819cf5f77b99fbaa6e87ba591da6bbaa86ec073a64bfef`.
- Art planner: `bartowski/Qwen_Qwen3-30B-A3B-Instruct-2507-GGUF`, revision `6c6e8692f43e4ca663f7ece8229a1361090d3a4c`, file `Qwen_Qwen3-30B-A3B-Instruct-2507-Q3_K_M.gguf`, SHA256 `327c6e0826bee8f19172e96c94bb7bba385f7a39d08314803652df9942401c4f`.
- Illustration: public SSD-1B and LCM adapter, with CLIP subject checks; exact revisions remain in `newsletter_cpu.py`. Their separate licenses apply; they are not all Apache-2.0.

Verifier/art weights are digest-checked. The llama.cpp archive is pinned to b12244 (`d5bbcd1f31dba754f716a26c3a4784502a6b9ede`), SHA256 `c1d7e7f31b5c43f3e5d44f667b4d57104217be3e5f2060320cd3735651238849`. Verifier decoding has two independent server slots with32768 context tokens each (65536 total), sharing weights only; writer/art use one slot. All profiles use CPU only.

## Verification protocol

Native reasoning receives the actual answer contract, without grammar constraints, and must naturally close before an8192-token limit. Only then is its own completed thought appended to the same original request for schema-constrained JSON. A timeout, exhausted budget, missing close or context truncation fails; no forced verdict is allowed. Both raw phases are archived. Context shifting is disabled. General reasoning uses the publisher's1.0/0.95/20/0 sampling and1.5 presence penalty; final schema-bound output has no presence penalty.

Each independent pair sees exactly one complete target plus the entire original draft as plain field strings. There is only one root request hash; no competing nested hashes, word-row lists or reviewer answers. The model selects first/last IDs from the explicitly supplied original word list, with schema enums restricted to that target's valid IDs. Code copies the original whole words, intervening whitespace, particles and punctuation. It never retypes, paraphrases, space-normalizes or guesses a missing quotation. Booleans, character offsets, reversed/out-of-bounds IDs, legacy quote replies, disagreement and uncertainty fail. A separate full-context audit checks the complete resulting inventory for omitted premises, negation, attribution and scope. Both analysts' per-target hashes and the global draft hash are preserved.

Factual ranges alone enter source entailment; certified pure proposals are excluded. All11 exact synthetic word ranges and all5 historical true/false cases remain unchanged. A successful control proof may be reused only with the exact tested model/runtime, full workflow definition, current fixture hashes and actual successful jobs. Synthetic proof dates bind to authenticated job start times; fresh news retains its own current-day guard and isolated run namespace. Raw evidence is preserved with the private checkpoint.

Earlier candidates failed actual semantic controls, repeated inventory planning or Korean quote spacing. These failures remain failures, not qualification. The word-anchor protocol addresses those formatting/planning failures; actual semantic and full deadline qualification are still required. Production remains disabled until they pass.

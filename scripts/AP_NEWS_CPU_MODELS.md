# Candidate credential-free CPU verifier (not yet qualified)

Writer remains the pinned public Qwen3-8B GGUF. Art planning remains Qwen3-30B-A3B-Instruct-2507. Factual verification now uses the separate native-thinking Qwen3-30B-A3B-Thinking-2507 candidate. Provider scores do not qualify publication: the actual11 scope controls,5 historical controls and full production/recovery/public/mail trial must pass before activation.

Verifier base publisher and Apache-2.0 license: https://huggingface.co/Qwen/Qwen3-30B-A3B-Thinking-2507
Quantized distribution: bartowski/Qwen_Qwen3-30B-A3B-Thinking-2507-GGUF
Immutable revision:6a509d3e0aef5b70ffdcaa478e23de77482e6165
File:Qwen_Qwen3-30B-A3B-Thinking-2507-Q3_K_M.gguf (14,076,803,072 bytes)
SHA256:7d5d7579c90596cd0e27bf94b002b52280c3031cdc699e4f64d8e94b1bbfdd6d

Art planning uses bartowski/Qwen_Qwen3-30B-A3B-Instruct-2507-GGUF at6c6e8692f43e4ca663f7ece8229a1361090d3a4c, file Qwen_Qwen3-30B-A3B-Instruct-2507-Q3_K_M.gguf, SHA256327c6e0826bee8f19172e96c94bb7bba385f7a39d08314803652df9942401c4f.

Each downloaded verifier/art file is digest-checked. Native verifier input ends with the publisher's assistant/thinking prefix. Reasoning runs without JSON grammar and must naturally close before a4096-token limit; a timeout, missing close or exhausted budget fails rather than forcing a verdict. Only then does the same original request plus its own completed reasoning produce schema-constrained JSON. Both raw stages are preserved. Separate calls never receive each other's reasoning or answers; a third source-blind full-context audit still checks the inventory. Uncertainty or disagreement never grants approval. Sampling follows the thinking model's published0.6/0.95/20/0 settings.

Public weights download with token=False and inference is only on127.0.0.1/CPU. No hosted model endpoint, AI API credential or payment is used. Writer/verifier/art identities and caches are distinct. Review/cache revisions invalidate previous decisions. Production remains disabled until actual qualification.

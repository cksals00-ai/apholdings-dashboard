# Candidate credential-free CPU verifier (not yet qualified)

Writer: the existing pinned Qwen3-8B public GGUF. Verifier and art planning candidate: Qwen3-30B-A3B-Instruct-2507, a non-thinking instruction model with30.5B total/3.3B active parameters. Model-provider scores are not publication qualification; the unchanged scope controls, historical factual controls and full rehearsal must pass.

Base publisher and Apache-2.0 license: https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507
Quantized distribution: bartowski/Qwen_Qwen3-30B-A3B-Instruct-2507-GGUF
Immutable revision:6c6e8692f43e4ca663f7ece8229a1361090d3a4c
File:Qwen_Qwen3-30B-A3B-Instruct-2507-Q3_K_M.gguf (14,076,803,072 bytes)
SHA256:327c6e0826bee8f19172e96c94bb7bba385f7a39d08314803652df9942401c4f

The process verifies the file digest, uses the native non-thinking chat prefix and a bounded quantized KV cache on CPU. Public weights download with token=False; inference is only on127.0.0.1. No hosted model endpoint, API credential, or paid AI API is used. Writer and verifier weights/receipts have separate immutable identities. The new prompt/cache and review revisions invalidate earlier decisions. Production remains disabled until actual qualification.

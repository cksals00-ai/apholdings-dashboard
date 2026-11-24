# Server-only public model runtime

No hosted AI inference API, API key, billing enrolment or paid fallback is used.
Public model files are downloaded without a Hugging Face token and executed on the
standard GitHub-hosted CPU runner. Prompts contain only official public source
material and AP editorial context. Subscriber records and mail credentials never
enter generation. Model child processes receive a minimal environment.

Pinned public weights validated by full server rehearsal41031927070:

- Qwen3-8B Q4_K_M, official public quantized weights
  https://huggingface.co/Qwen/Qwen3-8B-GGUF
  revision7c41481f57cb95916b40956ab2f0b139b296d974 (Apache2.0).
- Qwen3-14B Q4_K_M for English visual direction (CPU rehearsal passed)
  https://huggingface.co/Qwen/Qwen3-14B-GGUF
  revision530227a7d994db8eca5ab5ced2fb692b614357fd (Apache2.0).
  It runs after the copy model closes, with an8192-token CPU context, before diffusion.
  Its weights are downloaded anonymously into a separate uncached directory.
  Art uses the model card's non-thinking sampler (temperature0.7/top-p0.8/top-k20/
  min-p0/presence-penalty1.5); the factual copy profile is unchanged.
- Segmind SSD-1B https://huggingface.co/segmind/SSD-1B
  revision60987f37e94cd59c36b1cba832b9f97b57395a10 (Apache2.0 model card).
- LCM-LoRA SSD-1B https://huggingface.co/latent-consistency/lcm-lora-ssd-1b
  revision857c372dbe0edd8af6255638a68d0d7ccb7a3d76 (OpenRAIL++).
- CLIP local image/subject comparison https://huggingface.co/openai/clip-vit-base-patch32
  revision3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268. This downloads public
  weights; it never calls the OpenAI API or reads an OpenAI API key.
- llama.cpp CPU runtime b5401, https://github.com/ggml-org/llama.cpp/tree/b5401

The image/topic similarity check and second-pass text check are automated quality
filters, not guarantees of semantic correctness or human review. Original quote
receipts, source body hashes, model review output, image scores and all rendered
PDF/browser pages remain in an authenticated private company draft-release checkpoint for diagnosis. Publication
stops and sends a server alert if a gate fails.

Production remains fail-closed until an actual full server rehearsal has passed,
including new source collection, copy and art, all PDF pages, mobile and desktop,
isolated public preview bytes and owner-only test-mail acceptance. A scheduled
qualification check may be armed earlier; it cannot start generation until the
fixed main-branch rehearsal succeeds after an automatic bot recovery. The whole
producer workflow and its immutable runtime pin must match that tested version.
This allows unattended activation after qualification without a local-app step.

The full rehearsal passed on2026-10-30 after automatic bot recovery, including
public preview bytes and one owner-only test newsletter acceptance. Automatic
rollout verification41033418749 also passed. No hosted inference API was used.

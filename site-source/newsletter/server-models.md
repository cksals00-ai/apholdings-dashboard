# Server-only public model runtime

No hosted AI inference API, API key, billing enrolment or paid fallback is used.
Public model files are downloaded without a Hugging Face token and executed on the
standard GitHub-hosted CPU runner. Prompts contain only official public source
material and AP editorial context. Subscriber records and mail credentials never
enter generation. Model child processes receive a minimal environment.

Pinned public weights under evaluation:

- Qwen3-4B-Instruct-2507 Q4_K_M, quantized distribution
  https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF
  revision a06e946bb6b655725eafa393f4a9745d460374c9 (upstream Qwen Apache2.0).
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
PDF/browser pages remain in the checkpoint artifact for diagnosis. Publication
stops and sends a server alert if a gate fails.

Do not enable the production schedule until an actual full server rehearsal has
passed, including new source collection, copy and art, all PDF pages, mobile and
desktop, isolated public preview bytes and owner-only test-mail acceptance.

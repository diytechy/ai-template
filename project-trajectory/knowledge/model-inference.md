---
domains: [web]
researched: 2026-07-09
source: curated from a private research library
---
# Model inference

Curated research pack imported from the staged skill/knowledge library. Verify version-sensitive examples against the linked current documentation before shipping.

### Core references
- **In-browser:** **[Transformers.js](https://huggingface.co/docs/transformers.js)** (NLP/vision
  pipelines, WebGPU + WASM), **[WebLLM](https://github.com/mlc-ai/web-llm)** (OpenAI-style chat API,
  WebGPU), **[ONNX Runtime Web](https://onnxruntime.ai/docs/tutorials/web/)** (run any ONNX model).
  In 2026, Q4-quantized models under ~2 GB run interactively on an integrated GPU.
- **Local/server engines** ([2026 comparison](https://bizon-tech.com/blog/best-llm-inference-engines)):
  **[Ollama](https://ollama.com/)** (easiest single-user), **[llama.cpp](https://github.com/ggml-org/llama.cpp)**
  (max control/edge), **[vLLM](https://docs.vllm.ai/)** / **[SGLang](https://github.com/sgl-project/sglang)**
  (multi-user throughput via PagedAttention / RadixAttention), **[TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)** (peak NVIDIA throughput).
- **Mobile/native:** **[Core ML + coremltools](https://apple.github.io/coremltools/)** (Apple Neural
  Engine), **[ExecuTorch](https://pytorch.org/executorch/)** (PyTorch on-device, Meta's path for
  Llama 3.2 1B/3B), **[LiteRT/TFLite](https://ai.google.dev/edge/litert)**, **[ONNX Runtime Mobile](https://onnxruntime.ai/docs/tutorials/mobile/)** (12+ backends incl. Core ML, QNN). Production CV is now sub-20 ms on-device.
- **Structured output / reliability:** **[Anthropic tool use](https://docs.claude.com/en/docs/build-with-claude/tool-use)**,
  **[JSON Schema](https://json-schema.org/)**, and constrained decoding via
  **[Outlines](https://github.com/dottxt-ai/outlines)** / **[XGrammar](https://github.com/mlc-ai/xgrammar)** (now the default grammar backend in vLLM/SGLang/TensorRT-LLM/MLC).

### Actionable techniques
1. **Pick the runtime by *deployment target*, not benchmark hype:** browser tab → Transformers.js or
   WebLLM; one desktop user → Ollama/llama.cpp; many users on a GPU box → vLLM/SGLang; iOS/Android →
   Core ML / ExecuTorch / LiteRT. Same weights, different engine per surface.
2. **Budget memory before choosing a model.** Q4 quantization ≈ 0.5 GB per 1B params; keep model +
   KV cache under the device's usable VRAM. A 1B–3B Q4 model is the sweet spot for on-device.
3. **Make structure a guarantee, not a hope.** For anything a program parses, use constrained
   decoding against a JSON Schema (works ~100% vs 95–99% for plain tool-calling). Set
   `additionalProperties: false` on every object; express optional fields as nullable-and-required.

```python
# Guaranteed schema-valid output from an open model via Outlines (constrained decoding).
from outlines import models, generate
from pydantic import BaseModel

class RoomObject(BaseModel):
    label: str
    confidence: float
    bbox: list[float]          # [x, y, w, h]

model = models.transformers("Qwen/Qwen2.5-1.5B-Instruct")
detect = generate.json(model, RoomObject)         # FSM masks invalid tokens at generation time
obj = detect("Identify the main furniture item in this description: ...")   # -> RoomObject
```

```js
// In-browser, WebGPU, Q4 — no server, no API bill.
import { pipeline } from "@huggingface/transformers";
const gen = await pipeline("text-generation",
  "onnx-community/Qwen2.5-0.5B-Instruct", { device: "webgpu", dtype: "q4" });
console.log((await gen("One-line summary:", { max_new_tokens: 64 }))[0].generated_text);
```

### Gotchas
- WebGPU inference can't use the NPU yet (WebLLM/Transformers.js use the GPU); native runtimes can.
- Quantization below Q4 degrades sharply and *fabricates* (a documented failure —
  seen first-hand in a robotics pilot); don't drop precision to fit a too-big model, pick a smaller model.
- First browser load downloads hundreds of MB of weights — cache aggressively (Cache API / OPFS).

---

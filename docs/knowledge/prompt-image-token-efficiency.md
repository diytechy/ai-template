# Prompt text versus rasterized prompt images

**Research WI:** WI-155 · **retrieved:** 2026-07-15

## Questions and answers

### What is the per-provider image-versus-text token cost on representative prompts?

Native text cost follows the provider tokenizer and actual content. Image cost
follows canvas geometry, detail mode, resizing, and model family, so there is no
universal break-even. These transparent estimates use a rough English text
baseline; count the exact fixture with the target provider before a real decision.

| Shape | Readable rendering assumption | OpenAI `gpt-5-mini` high | Anthropic high-resolution model |
|---|---|---:|---:|
| Dense prose, 500 words (~667 text tokens) | 1000×1400, 16–18 px | ~2,281 (3.42×) | 1,800 (2.70×) |
| Code/table (~600 estimated text tokens) | 1400×900, 16 px mono | ~2,067 (3.45×) | 1,650 (2.75×) |
| Short instruction, 20 words (~27 text tokens) | 800×300, 24–28 px | 405 (15.0×) | 319 (11.81×) |

The OpenAI estimates apply its documented 32-pixel patch count and 1.62 model
multiplier. Anthropic uses `ceil(width/28) × ceil(height/28)` after any server
resize. Other OpenAI families use tile formulas, and standard-tier Claude may
downscale sooner, so these ratios must not be generalized across models.

### What fidelity is lost at readable resolutions?

Rasterization adds a lossy channel: font size, downscaling, tiling, blur, and
compression can change recognition. Provider guidance warns that small or
low-quality text causes mistakes. OCR benchmarks show material variation across
scene text, documents, handwriting, mathematics, and multilingual text; OCR
capability is not evidence of verbatim recovery or equivalent reasoning.

DeepSeek-OCR reports strong reconstruction below roughly 10× optical compression
for its specially trained system, but does not establish equal downstream
reasoning fidelity. Follow-up work found direct text-compression baselines could
match or beat visual reconstruction. LensVLM's more positive results rely on
post-training and selectively expanding compressed regions. Optical context
compression is specialized, lossy research—not a safe drop-in encoding for
hosted general-purpose prompt APIs.

### How does prompt caching change the result?

Both providers can cache repeated image-bearing prefixes under documented
conditions. OpenAI requires exact prefix matches; image bytes or links and detail
must remain identical. Anthropic caches through a breakpoint and warns that
adding or removing images changes cache validity. Thresholds and TTLs vary by
model.

Caching discounts a repeated identical image but does not remove the first-write
geometry cost, raster-generation complexity, or fidelity risk. Native text is
also cacheable and remains searchable, diffable, and deterministic. Encoding
text as pixels merely to cross a cache threshold is false economy.

## Decision guidance

Use native text for instructions, identifiers, citations, code, tables, and
exact wording. Add an image when layout, typography, spatial relationships, or
appearance is itself evidence. A raster-only prompt needs task-specific tests at
the exact model, dimensions, font, format, detail setting, and compression.

No downstream opt-in image renderer is justified for this kit on current
evidence. It would lose the cost/fidelity comparison and add rendering
machinery—likely including an imaging dependency for acceptable cross-platform
typography—outside the kit's stdlib-only script floor.

## Primary evidence (retrieved 2026-07-15)

- [Anthropic vision guide](https://platform.claude.com/docs/en/build-with-claude/vision)
- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [OpenAI vision and image token guide](https://developers.openai.com/api/docs/guides/images-vision)
- [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [OCRBench](https://arxiv.org/abs/2305.07895)
- [DeepSeek-OCR](https://arxiv.org/abs/2510.18234)
- [Optical Context Compression Is Just (Bad) Autoencoding](https://arxiv.org/abs/2512.03643)
- [LensVLM](https://arxiv.org/abs/2605.07019)

---
domains: [web]
researched: 2026-07-09
source: curated from a private research library
---
# Web rendering

Curated research pack imported from the staged skill/knowledge library. Verify version-sensitive examples against the linked current documentation before shipping.

### Core references
- **[WebGPU — W3C spec](https://www.w3.org/TR/webgpu/)** and **[MDN WebGPU API](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API)** — normative reference + practical API docs. WebGPU is 10–20× faster than WebGL for the compute (matmul/attention) that also powers in-browser ML, so it unifies A2 and A3.
- **[WebGPU Fundamentals](https://webgpufundamentals.org/)** and **[WebGPU Unleashed (free book)](https://shi-yan.github.io/webgpuunleashed/)** — the two best from-scratch teaching resources (pipelines, bind groups, compute shaders, 2D→3D).
- **[awesome-webgpu](https://github.com/mikbry/awesome-webgpu)** — curated ecosystem index (engines, tools, tutorials).
- **[three.js](https://threejs.org/docs/)** / **[Babylon.js](https://doc.babylonjs.com/)** — the two mature scene-graph engines if you don't want to write raw WebGPU. Both now render on WebGPU.
- **3D Gaussian Splatting** (for a spatial-capture project rendering real spaces): the
  **[original 3DGS paper (Kerbl et al., SIGGRAPH 2023)](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)**,
  **[GaussianSplats3D (three.js)](https://github.com/mkkellogg/GaussianSplats3D)**, and
  **[Babylon's Gaussian Splatting docs](https://doc.babylonjs.com/features/featuresDeepDive/mesh/gaussianSplatting/)**.
  The **KHR_gaussian_splatting glTF extension** is at release-candidate and expected to ratify in 2026 — meaning splats become first-class glTF alongside meshes; author toward glTF.

### Actionable techniques
1. **Choose the altitude deliberately.** Raw WebGPU for a bespoke renderer or heavy compute; a
   scene-graph engine (three.js/Babylon) for "load models, light them, orbit." Don't write a matrix
   stack by hand if a battle-tested engine already renders your glTF.
2. **Structure the renderer as explicit passes** (upload → depth pre-pass → shade → post). See
   *[The Structure of a WebGPU Renderer](https://whoisryosuke.com/blog/2025/structure-of-a-webgpu-renderer/)*.
   Named passes make it debuggable and let an agent reason about one stage at a time.
3. **Gaussian-splat performance:** prefer static textures over per-frame dynamic instance buffers
   (Babylon's V8 change took a 2.5M-splat scene from ~15 → 60 FPS this way); sort splats by depth on
   the GPU; budget by splat count and VRAM, not triangle count.

```js
// Minimal WebGPU frame loop — the skeleton every renderer shares.
const adapter = await navigator.gpu.requestAdapter();
const device  = await adapter.requestDevice();
const ctx = canvas.getContext("webgpu");
ctx.configure({ device, format: navigator.gpu.getPreferredCanvasFormat(), alphaMode: "premultiplied" });
function frame() {
  const enc  = device.createCommandEncoder();
  const pass = enc.beginRenderPass({ colorAttachments: [{
    view: ctx.getCurrentTexture().createView(),
    clearValue: { r: 0.02, g: 0.02, b: 0.03, a: 1 }, loadOp: "clear", storeOp: "store" }] });
  pass.setPipeline(pipeline); pass.setBindGroup(0, uniforms); pass.draw(3);
  pass.end();
  device.queue.submit([enc.finish()]);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

### Gotchas
- WebGPU is broadly shipped in 2026 but still feature-detect (`if (!navigator.gpu) fallbackToWebGL()`).
- Splat scenes are unlit point data — mixing them with lit PBR meshes needs careful depth/blend order.

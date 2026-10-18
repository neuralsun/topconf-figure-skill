# 内置图像设计

当前 Codex 模型理解论文并做对象重建，不需要额外调用 GPT API。生图使用本次会话内置工具，遵循 imagegen 技能，不引入网页端第三方路由或 Key。

```text
Use case: scientific-educational / infographic-diagram.
Asset type: conference-paper architecture design draft.
Scientific content: [facts from the figure contract].
Exact labels: [verbatim labels and required symbols].
Topology: [each branch, merge, residual, retrieval and output].
Visual grammar: [observed panel proportions, nesting, semantic palette,
strokes, token and tensor vocabulary, whitespace].
Composition: [paper-specific ratio and emphasis].
Style: white paper background, crisp flat geometry, restrained colors,
thin dark connectors, legible labels and meaningful internal structure.
Constraints: no invented results, values or layers; no marketing title,
watermark, decorative shadows or copying a reference composition.
Editable reconstruction target: separate text, modules, tensor faces,
matrix cells and arrows rather than inseparable textures.
```

用户明确只要原生矢量、不要生图时可跳过；用户指定 image2 时不要跳过后又称已用。

重建时先看布局，再对照语义合同修正拼写、缺失/多余连线与符号，按区域拆对象。复杂区域放大检查；原生重建可以改善对齐和走线。最终 PNG 与 SVG 同源；PPTX 也由同一场景生成，但 Office 字体/几何仍需核对。生图原稿与重建稿的微小差异不能称为像素级复刻。

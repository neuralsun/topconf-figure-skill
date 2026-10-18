---
name: topconf-figure
description: Create paper-specific ICLR/ICML/NeurIPS/CVPR-style neural-network architecture, framework and pipeline figures using reference-guided design, Codex built-in image generation and native vector reconstruction. Deliver editable PPTX, vector SVG and matching PNG. Use for 顶会架构图、网络结构图、模型框架图、Figure 1、参考顶会风格画图 or image2 制图 with editable outputs; not whole slide decks or statistical data plots.
---

# 顶会论文架构图工作室

提炼论文的计算关系与参考图的视觉语法，交付同源的 `figure.pptx`、`figure.svg`、`figure.png`。“蒸馏”是流程与视觉规则提炼，不是训练模型权重。

## 核心约束

- 科学内容来自用户的摘要、方法、代码或明确说明。参考图提供画法，不提供待画模型的技术事实；不虚构层、损失、数据和性能数字。
- 生图负责探索布局，Codex 负责语义核对和逐对象重建。位图插进 PPT 或包装成 SVG 不算可编辑矢量。
- 最终标题、标签、模块、张量平面、token、矩阵单元和箭头为原生对象。纯架构图默认没有栅格图片。
- 三个最终格式从同一场景 JSON 导出。原生渲染 PNG 是正式 PNG；生图原稿另存 `image-design.png`，不冒充同源 PNG。
- 设计先行：先完成并验收足以与参考图比较的设计图，再按逐对象清单转换。不得为迁就导出器而换掉布局、丢失插画或把精致图标简化成空框。默认不加外部总标题和图注；模块标签与图例保留，用户明确需要标题时再添加。
- 用户要求重新设计时，实际生成并检查新的设计稿；翻译、换标签或沿用既有构图时如实说明，不能称为重新生图。生图仍有技术错误时，在设计阶段记录并修正，重新检查并锁定修正后的预览，之后再导出终稿。
- 默认使用会话内置图像生成工具，按已安装的 imagegen 技能执行，不要求另购第三方 API 或提供 Key。用户明确选择 API/CLI 时才走该路径，不提取登录凭据或模拟内部 API。
- 工具没有模型选择参数时，说明使用应用当前提供的图像模型，不能宣称已强制指定 gpt-image-2。工具不可用时如实说明；可继续原生矢量创作，但披露未完成内置生图步骤。
- Codex 和内置生图仍由云端模型处理，不称为离线或“论文不离开电脑”。用户要求完全离线时不要调用云端模型。

## 工作流

### 0. 先优化用户提示词

用户给出一句话、草稿或完整提示词时，先保留原文，并整理为可执行的绘图说明，保存 `prompt-optimized.md`。用户要求只优化时，到此交付，不启动检索、生图或导出；要求画图时，简要展示优化结果后继续完整流程，默认不增加确认环节。

优化内容：澄清输入—模块—分支—融合—输出及箭头方向；保留用户指定的标签、技术名词、数值、语言和画布要求；明确主次层级、机制放大需求、配色含义、线型和可编辑输出要求。将“高级、顶会风”等模糊描述转成可以执行的视觉要求。用户已给出精确要求时只做必要整理，不扩大范围。

区分科学事实与设计选择：布局、字号、留白可合理补全；网络层、损失、训练方式、维度和实验结果不能补造。材料中出现技术矛盾时明确指出，只有影响科学含义的缺失才询问，其余采用合理的设计默认值。论文/代码与提示词冲突时保留冲突并核实，不静默改写事实。

优化说明包含“保留的科学内容、整理后的拓扑、视觉要求、输出要求、必要的待澄清项”。随后据此建立语义合同。检索参考并形成 style card 后，再将视觉规则融入实际生图提示词；不在检索前虚构已经看过的参考风格。

### 1. 建立语义合同

从已有材料提取：主结论、输入、核心模块、分支、融合、输出、可训练/冻结部分、线型含义、必须出现的标签。保存简短 `figure-contract.md`。用户材料足够就直接做；只有缺失信息会改变模型含义时才询问。有歧义的部分列出，不靠美观补造模块。按论文版面选比例，不强制 16:9；标签沿用用户语言，无指定时论文图可用英文。

### 2. 检索并实际看图

优先使用用户参考。否则读 [本地图库](references/local-gallery.md)，使用已有本地图库，不必启动网页：

```text
python <skill_dir>/scripts/retrieve_refs.py --gallery <gallery_dir> --query "multimodal memory fusion" --pattern architecture --limit 12 --output <work_dir>/references
```

脚本是元数据 BM25，不是 CLIP 语义检索。看联系表后打开匹配的原图，通常选 3–6 张拓扑相近且互补的图。不要因会议相同就假设风格一致。保留来源和论文链接。没有图库时使用用户参考；都没有时依据已提炼的视觉规则创作，并披露没有检索实图。

### 3. 提炼视觉语法

读 [视觉规则](references/visual-grammar.md)，写 `style-card.md`：叙事拓扑、面板比例、分组层级、阅读方向、语义配色、线型、字号、留白，以及 token、张量、Q/K/V、矩阵、金字塔、跳连等实际需要的元素。说明借鉴了哪些参考和哪些科学内容来自用户。

为当前论文重新构图，不复刻任一参考整图。每个容器都有明确含义，保留机制所需细节，避免简化成一排空的彩色方框。

### 4. 内置生图设计稿

用户要求 image2 时，实际完成一次内置生图设计步骤，不以手画模板冒充。提示词见 [图像设计](references/image-design.md)。把合同拓扑、精确标签和 style card 写入提示词。参考图输入方式服从当前工具能力，先查看本地图片；无法输入图片时描述观察所得视觉规则。

按实际返回位置保存设计原稿到工作目录，检查文字、箭头和无依据内容。没有尺寸控制参数时不要伪造参数。默认一份设计稿；发现具体问题再针对性修正，不无依据反复生成。

在转换前执行[质量门](references/quality-gates.md)的设计检查，实际并排对比参考图。科学内容或视觉质量不通过时先重新设计。锁定通过设计图的SHA256和对象清单后才进入下一步。

### 5. 重建可编辑场景并导出

读 [场景格式](references/scene-format.md)。先列出设计图中每个卡片、图标、插画和分组的component_map，再逐个映射到nodes和edges，保存 `figure.scene.json`。保持设计图的相对位置、密度、层级和对象细节，不重新发明一张简化图。科学事实以合同为准；语义修正应在设计质量门前完成。矩阵、张量、算子、文字、插画轮廓和连接线分别重建。

```text
python <skill_dir>/scripts/export_scene.py <work_dir>/figure.scene.json --output <output_dir>/figure --png-scale 2
```

依赖为 python-pptx、Pillow、Playwright 和 Chromium；优先用已有环境，桌面可调用 load_workspace_dependencies 定位内置运行时。脚本拒绝覆盖成品，修订用新版本名或明确使用 --force。

当前导出器支持矩形、圆角、椭圆、多边形、文字、折线、M/L/C/Q/Z曲线路径和简单线性渐变，可把复杂插画转换成原生PPT曲线并分组。超出范围时扩展原生表示，不静默栅格化或降低设计质量。照片确实必要时必须扩展独立可替换图片对象支持，并披露图片仍为位图；当前导出器没有图片节点支持。

### 6. 核对和交付

执行[最终质量门](references/quality-gates.md)，把设计图、最终PNG、Office渲染并排看：对象完整、插画图标保真、版式保留、语义正确、无穿字和遮挡。失败时返回设计或对象重建，再导出再检查；未通过不称为终稿。保留检查报告与具体修订记录，不保证任意位图像素级复刻。

脚本校验坐标、文字容量、PPTX XML、原生对象、零整页图片、PPTX/SVG 标签一致，输出 `figure.qa.json`；自动检查不能证明语义正确或没有任何重叠。能使用 PowerPoint/LibreOffice 时再实际打开或渲染 PPTX；无法做 Office 渲染时明确限制，不假称检查过。

交付三份成品链接和可供改图的场景 JSON。简述可编辑程度、独立位图和待核实内容，不默认增加封面或多页演示稿。

## 来源

借鉴 [Top-Conf Figure Gallery / FigureForge](https://github.com/qwdwqfwq/topconf-paper-figure-gallery) 的检索参考 → 视觉归纳 → 生成 → 对象重建 → 同场景导出流程。见 [来源与边界](references/provenance.md)。本技能脚本独立实现，不修改上游锁定流程。

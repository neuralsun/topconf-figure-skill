# 设计先行与转换质量门

先优化提示词并记录，再做设计，设计达到要求后才开始转换。设计图是视觉主文件；不能先写简单流程图，再把生成图当作无关装饰。用户未要求总标题和图注时，默认不加外部总标题、副标题、图号、长图注或底部口号；模块名称、状态说明、图例保留。明确要求无标题/图注时同步删除旧提示词中的这些内容。

## 设计质量门

实际打开设计图，与选中的参考图对照：科学含义、版式、插画、图标精细度、信息层级、文字和走线、留白。记录design-review中的具体问题和主观评分，不把评分称为自动审美指标。只有语义正确、没有标题图注违规且视觉质量达到8/10，才锁定设计图SHA256进入转换；不通过就带着具体缺陷重新设计。

```text
python scripts/quality_gate.py --stage design --design design.png --review review.json --output design-gate.json
```

## 逐对象转换

先建立component_map，覆盖每张卡片、每个图标、医学插画、核心分组、文字和连接关系。记录设计图中的位置、作用与对应scene_ids。复杂插画可以分层描摹成闭合曲线路径；文字必须保留为文字。仅在明确可接受独立位图时才使用局部图片，不以整页图片冒充可编辑图。

需要保真时扩展渲染器，不把复杂人物换成简笔人，不把精致图标换成方块/文字，也不重新换一套版式。导出器现支持M/L/C/Q/Z路径和原生PPT自定义几何、简单线性渐变。人物等有多个路径时可用group归为一组，仍能进入组中修改。

## 最终质量门

导出三种文件，实际渲染PPTX。把设计图、SVG渲染、Office渲染并排查看；检查对象漏失、视觉细节、版式比例、文字、颜色、图层、连接线和科学边界。结构校验通过不能替代视觉检查。

```text
python scripts/quality_gate.py --stage final --design design.png --review review.json --scene figure.scene.json --basename output/figure --output final-gate.json
```

程序检查SHA绑定、必需对象是否映射到真实对象ID、标签、原生对象/零整页图片、XML和跨格式文字一致、人工辅助视觉复核是否完成。视觉评价必须来自实际看图，不能提前把所有检查写成true。脚本不是自动审美或临床验证系统。

返回PASS才能称为终稿。设计质量失败返回REDESIGN_REQUIRED，修改设计；转换失败返回RECONSTRUCTION_REQUIRED，按对象重新转换并再检查。每轮保留具体缺陷和改动；工具不可用或连续修改不能改善时如实标注未达标，不能强行通过或继续无依据消耗生图。

review.json包含design_sha256、design_review、component_map、required_labels和conversion_review。各具体字段见quality_gate.py。质量报告随交付保留，原设计与失败版本保留供对照。

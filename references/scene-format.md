# 同源可编辑场景 v1

UTF-8 JSON，像素坐标，左上角原点。画布比例可变。导出器纯本地转换，不调用模型。

```json
{
  "version": 1,
  "title": "Example architecture",
  "canvas": {"width": 1600, "height": 700, "background": "#FFFFFF", "fontFamily": "Arial", "minFontSize": 16},
  "nodes": [
    {"id": "encoder", "type": "roundrect", "x": 100, "y": 220, "w": 300, "h": 120, "fill": "#E3EDFA", "stroke": "#638DB8", "radius": 12, "z": 10},
    {"id": "encoder-label", "type": "text", "x": 120, "y": 250, "w": 260, "h": 55, "text": "Encoder", "fontSize": 28, "bold": true, "align": "center", "color": "#172337", "z": 30},
    {"id": "decoder", "type": "rect", "x": 650, "y": 220, "w": 300, "h": 120, "fill": "#E8E2F5", "stroke": "#8D79B8", "z": 10}
  ],
  "edges": [
    {"id": "encoder-to-decoder", "from": "encoder", "to": "decoder", "stroke": "#44566C", "strokeWidth": 2, "arrow": true, "z": 20}
  ],
  "notes": "Scientific content and reference attribution."
}
```

## 节点

- rect / roundrect / ellipse：x,y,w,h。fill、stroke 用 #rrggbb 或 none；支持 strokeWidth、dash:true；圆角 radius。
- polygon：points:[[x,y],...] 为闭合轮廓，导出原生 PPT 多边形。张量的各个面分别建对象。
- path：commands为绝对坐标命令数组，例如[["M",10,10],["C",20,0,30,0,40,10],["L",40,40],["Z"]]；支持M/L/C/Q/Z，导出原生PPT自定义几何，保留贝塞尔曲线。可用group把人物或图标的多个路径合为一组。
- gradient：可选形如{"colors":["#FFFFFF","#E8F9FC"],"angle":90}的两色或多色线性填充；angle支持0/90。应来自设计稿，而非额外装饰。
- text：x,y,w,h,text,fontSize；支持 color,bold,italic，align=left/center/right，valign=middle/top，lineHeight（默认1.22）、padding（默认1）、wrap（默认true）。显式换行可固定分行。字体由 canvas.fontFamily 统一指定；中文用已安装中文字体，例如 Microsoft YaHei。
- z 为图层：外框0、模块10、箭头20、文字30，可按需求调整。稳定排序使 SVG 与 PPTX 图层一致。

## 连线

直接连线可用 from/to 引用非文字节点，fromSide/toSide 为 top/left/bottom/right，默认 right/left。已创建的目标对象可在 PPTX 附着原生端点，移动跟随效果需 Office 核对。

折线用 points:[[x,y],...]，各段为原生连接线，最后一段带箭头。arrow:false 为无箭头，dash:true 为虚线。折点不自动路由；没有 from/to 时不能宣称拖动模块会跟随。边的文字单独建 text 节点。

## 导出和校验

脚本以 Pillow 测量文字并为两种矢量格式保持相同分行，超框会报错。平台字体和 Office 字重排版仍有差异，应留余量并看图。

输出 .pptx / .svg / .png / .qa.json。PNG 用 Chromium 渲染 SVG，默认画布的2倍。PPTX 宽13.333英寸，高度保持比例，图形和文字为原生对象。

当前不支持照片、未经归一化的任意SVG语法、复杂公式排版、透明渐变和任意旋转。真曲线用path命令表示。需要其他特性时扩展渲染器，不静默忽略未知类型或把细腻插画换成简笔画。

硬检查：ID唯一、颜色、画布边界、文字容量、引用合法、XML可解析、零图片对象、PPTX/SVG文字一致。不覆盖全部遮挡、语义、箭头穿字、色觉和 Office 渲染。

## 可复现示例与 Office 复核

`assets/example.scene.json` 是虚构的多模态记忆架构示例，用于测试导出能力，不是要求所有论文套用的模板：

```text
python scripts/export_scene.py assets/example.scene.json --output output/example --png-scale 2
```

Windows 已安装 PowerPoint 时，可以只读打开并实际渲染首张幻灯片：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/render_powerpoint.ps1 -InputPptx output/example.pptx -OutputPng output/example-office.png
```

该辅助脚本关闭自己打开的演示文稿；不会关闭用户已有演示文稿。对比 Office 渲染和同源 PNG，检查主题效果、文字和自由曲线。如果 Office 没有安装，不假称已经做过这项复核。

设计图中已确认的人物插画和图标，可用vectorize_components.py按对象区域描摹成原生曲线路径。此工具需要vtracer、svgpathtools，可通过requirements-vector.txt安装，或用--python-deps指定已有依赖目录。只转换指定图形区域，文字重新建为文字；不能将整张图全部描摹后宣称每个文字标签可编辑。检查描摹轮廓、颜色和图层，并在PPT中用分组组织复杂对象。

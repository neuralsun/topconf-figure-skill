# 本地参考图检索

图库位置可通过 `--gallery` 指定；也可把技能目录 `config.example.json` 复制为 `config.local.json`，填写本机目录后供 Codex 读取。无需启动网页服务。`retrieve_refs.py`本身以`--gallery`参数为准，不自动加载该配置文件。图库根目录需含 data/figures.json 和 images/，不假设本机磁盘路径在其他电脑存在。

检索输出 references.json（标题、作者、原文、绝对图片路径、BM25 分数）和 reference-contact-sheet.png。看联系表后打开选中原图；完整论文 ID 以 JSON 为准。没有关键词命中时分数可能为零，应换词或人工选择，不把零分说成语义匹配。

```text
python scripts/retrieve_refs.py --gallery <gallery_dir> --query "encoder decoder segmentation multi scale" --pattern architecture --venue cvpr,iclr,neurips --limit 12 --output output/references
```

脚本只读本地元数据和图片，不下载、不调用模型、不上传。图片版权归原作者与出版方，保留出处；代码 MIT 不等于论文图可任意商用或打包分发。

# 原论文截图与溯源

需要从 PDF 截取架构图、公式或实验结果时读取本文件。截图应帮助解释内容，不承担原文没有的论证。

## 工具与环境

- 此 skill 的 `scripts/capture_pdf_region.py` 使用 Poppler 的 `pdftoppm` 和 Python 的 Pillow，支持整页预览及归一化区域裁剪。
- 优先复用已有 conda 环境，确认 `PIL` 可导入并检查 `pdftoppm` 是否在 PATH。非交互运行优先 `conda run -n 环境名 ...`；若 conda 启动受限，可直接调用该既有环境的解释器。
- 必须创建环境时，在 conda 配置的全局环境目录创建，例如 `conda create -n paper-report python=3.11`；只安装缺失依赖，如 `conda install -n paper-report -c conda-forge pillow poppler`。不在项目内创建 `.venv` 或 conda 前缀。
- Codex 提供 bundled runtime 时，可用依赖定位工具寻找 Poppler，必要时通过 `--pdftoppm` 传入可执行文件的绝对路径。
- 也可使用其他可靠的 PDF 渲染器或页面截图工具。只有完整图形才适合直接提取内嵌图片；论文图常由矢量、文字和多个对象组成，单独导出图片对象可能遗漏标签。

## 两阶段截图

将下面的环境名、论文路径、脚本路径和输出路径替换为实际值；默认不覆盖已有图片或元数据。脚本路径相对于本 skill 目录。

1. **先获取整页预览并查看。**

```text
conda run -n paper-report python scripts/capture_pdf_region.py --pdf work/paper.pdf --page 4 --out work/page-04.png --dpi 120
```

2. **根据预览裁剪。** 先定位主体及对应的完整原文图注/表注、小字解释和脚注，再选区域。`--box` 使用 `左,上,右,下`，均在 0–1 范围内；原点为渲染页面的左上角，右下角为 `(1,1)`。根据实际页面选坐标，不复制示例坐标到不同论文。

```text
conda run -n paper-report python scripts/capture_pdf_region.py --pdf work/paper.pdf --page 4 --box 0.08,0.12,0.94,0.47 --out outputs/paper-report/assets/fig-02-framework.png --dpi 240 --label "Fig. 2"
```

有意替换已检查的同名截图时加 `--overwrite`。路径有空格时按所用 shell 加引号。脚本以参数列表调用渲染器，不拼接 shell 命令。

## 清晰度与完整性

- `--page` 是从 1 开始的 PDF 物理页序号，不是论文页脚的印刷页码。
- 坐标依据渲染后的页面，避开 PDF 点坐标、旋转和屏幕缩放的换算。选区边界略大于内容区域，防止裁掉上下标、公式号和图例。
- 每次裁剪都须包含与内容对应的原文小字解释，包括完整 caption、图内小字、图下说明及脚注；公式截图也保留附近直接解释该公式的小字或变量定义。自行撰写的讲解不能代替原文说明截图。
- 通常使用 200–300 DPI。细密公式和表格可提高分辨率；提高 DPI 不能恢复低质量扫描件的细节。
- 宽表或多面板图显示过小时可拆成多个截图，保留行列标签、单位、图例、子图标识、比较条件及对应的完整原文注释，并说明截取范围。
- 主体与小字位置分散或跨页时，分别截取并紧邻展示，如 `fig-02-framework.png` 与 `fig-02-caption.png`。以“主体＋原文说明”作为一组核对，不裁掉小字来放大图形。
- 分页表格分别截取相关页，不把第二页结果当成缺少表头的独立表。公式号超出选区时扩大边界。
- 在报告实际显示尺寸下检查主体与小字都可读，再嵌入。额外箭头、强调框或重绘图标为“讲解标注”或“重绘”，并保留原文证据。

## 文件与出处

脚本生成 PNG 和同名 `.png.json` 元数据，记录来源 PDF、物理页码、归一化选区、像素边界、DPI 和人工提供的标签。`--label` 不是自动识别结果，须与原文核对。脚本只执行指定区域的裁剪，不会自动识别或补齐图表、公式和原文小字；区域选择与完整性检查由使用者完成。

建议用法，下面的主体截图应已包含完整小字图注；若使用单独的原文说明截图，在同一位置相邻嵌入：

```markdown
![方法整体流程：从输入到最终预测](./assets/fig-02-framework.png)

*Fig. 2，PDF 第 4 页。两个分支在输出前合并。*
```

正文中的补充说明只保留一两句观察重点或结论，避免重复原文 caption。图表编号和页码用于简短溯源，JSON 不能代替原文小字截图。论文链接与版本记录在内部阅读索引或资源元数据中，标题下只写作者与期刊/会议录取状态；图片链接以实际文件为准。

## 降级处理

- 在线 PDF 可先下载到授权工作目录，再裁剪；只能获取网页截图时，确认所见确实是原论文及正确版本。
- 缺少渲染器或无法获取原文时，继续完成能核实的讲解，说明未能截取的素材，不引用不存在的图片。
- OCR 不可靠的公式保留截图和文字解释；结果无法辨认时不猜数值。可从作者官方 HTML 版本核对，但注明版本差异。

工具参数依据 [Poppler pdftoppm 手册](https://manpages.debian.org/bookworm/poppler-utils/pdftoppm.1.en.html)；像素选区遵循 [Pillow Image.crop 文档](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.crop)。

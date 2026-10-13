# 论文阅读与汇报

`paper-reading-report` 是一个 Codex skill，用于精读论文并生成文字精简、以 Method 为重点的中文 Markdown 汇报稿。

## 汇报结构

- **Motivation**：研究问题、现有瓶颈和研究目标。
- **Method**：核心流程、关键机制、训练与推理，通常占讲解篇幅的 50%–65%。复杂公式配有直觉、符号、分项计算和设计作用的解释。
- **Experiment**：比较设定、主要结果、消融证据、成本及局限。

重要图表、复杂公式和实验结果可从原论文截取，截图须保留完整原文 caption、小字解释和脚注；位置分散时以主体与原文说明截图成组展示。默认交付 `report.md` 和配套截图资源。

## 报告格式

- 一级标题直接使用论文原始标题，保留原语言与措辞。
- 标题下只保留一行小字引用：**原文作者名单**与期刊/会议及录取状态。录取状态须核实，不能把预印本当作已录用论文。
- 正文适当精简，减少重复背景、重复图注和逐行抄表；保留核心机制、重要结果和复杂公式的必要讲解。
- 图表出处以简短编号和 PDF 页码标明，原文链接及版本保留在内部阅读索引或资源元数据。

## 调用示例

```text
请使用 $paper-reading-report 生成精简的中文 Markdown 汇报稿，以论文原始标题为标题，标题下仅列作者与期刊/会议录取状态，重点讲解 Method 和复杂公式，截图保留原文小字解释。
```

安装时将本仓库作为 `paper-reading-report` skill 目录放入你的 Codex skills 目录，或让 `$skill-installer` 从此仓库安装。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 完整阅读、讲解、证据核对和交付流程 |
| [agents/openai.yaml](agents/openai.yaml) | skill 名称和默认调用提示 |
| [assets/report-template.md](assets/report-template.md) | Motivation / Method / Experiment 汇报骨架 |
| [references/pdf-capture.md](references/pdf-capture.md) | 原文截图、页码记录和裁剪说明 |
| [scripts/capture_pdf_region.py](scripts/capture_pdf_region.py) | PDF 页面渲染、区域截图和出处元数据 |

截图脚本依赖 Poppler 的 `pdftoppm` 和 Python 的 Pillow。优先复用现有 conda 环境；其他可靠的 PDF 截图工具也可用于此工作流。

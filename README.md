# 论文阅读与汇报

`paper-reading-report` 是一个 Codex skill，用于精读论文并生成可直接讲述的中文 Markdown 汇报稿。

## 汇报结构

- **Motivation**：研究问题、现有瓶颈和研究目标。
- **Method**：核心流程、关键机制、训练与推理，通常占讲解篇幅的 50%–65%。复杂公式配有直觉、符号、分项计算和设计作用的解释。
- **Experiment**：比较设定、主要结果、消融证据、成本及局限。

重要图表、复杂公式和实验结果可从原论文截取，并记录图表编号及 PDF 页码。默认交付 `report.md` 和配套截图资源。

## 调用示例

```text
请使用 $paper-reading-report 阅读这篇论文，生成中文 Markdown 汇报稿，重点讲解 Method 和复杂公式，并截取关键图表。
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

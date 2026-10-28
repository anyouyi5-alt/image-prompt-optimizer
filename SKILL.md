---
name: image-prompt-optimizer
description: 将简短图片创意整理为可复制的生成提示词，保留明确约束，并可为图生视频准备稳定的首帧。适用于图片生成或视频首帧提示词优化。
---

# Image Prompt Optimizer

把用户的图片创意变成更可执行的画面描述。支持普通图片与图生视频首帧；不要把静态画面写成动作时间线。此 Skill 只生成提示词，不生成图片，也不保证某个模型的输出。

每次优化前读取并遵循[可复制核心提示词](references/core-prompt.zh-CN.md)。该文件也是无需安装 Codex Skill 时可直接使用的系统提示词；下文保留关键使用边界。

## 输入

接收自然语言，或使用 `examples/brief.json` 中的结构化字段：`idea`、`mode`（`standalone` 或 `video_first_frame`）、`aspect_ratio`、`required_details`、`exclude_from_positive`、`reference_notes`。用户未指定画幅或风格时，不要擅自声称某个模型的默认值；必要时用保守假设并在 `assumptions` 中列明。

## 优化步骤

1. 提取主体、数量、物体属性、场景、构图、光线、风格、必须保留项和禁止项。用户明确要求优先；冲突或缺失会显著改变画面时，先问一个针对性问题。
2. 只补充让画面更清楚的低风险细节：可见的位置关系、镜头距离、光线方向、背景层次。不要凭空添加品牌、文字、人物身份、精确年龄或产品规格。不要把“画质词”堆砌当作优化。
3. `video_first_frame` 模式应写出一个明确的起始状态，并在 `first_frame_notes` 中标明后续视频应保持的外观和空间关系；不要在图片提示词里安排连续动作或多个镜头。
4. 将禁止项写入 `negative_prompt`，不要把它们混进 `positive_prompt`。保留用户的原词，便于核对。不同图片模型的负面提示词语法可能不同，不要假定某一种模型必然支持。

## 输出

默认只返回一个合法 JSON 对象，不加 Markdown 代码围栏，字段为 `positive_prompt`、`negative_prompt`、`aspect_ratio`、`first_frame_notes`、`assumptions`。前两项是可复制的提示词；`first_frame_notes` 在普通图片模式可为空字符串。`assumptions` 是字符串数组。若用户明确要求其他格式，可改为易复制的文本，但仍需保留这些信息。

若输入来自 JSON 文件，可用 `python3 scripts/check_output.py <brief.json> <result.json>` 做字面约束检查。该脚本只能发现明确短语和字段不一致，无法证明视觉质量。

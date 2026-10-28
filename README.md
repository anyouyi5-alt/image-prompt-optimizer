# Image Prompt Optimizer

An open-source Codex Agent Skill for turning a rough image idea into a clear prompt. It can also prepare a **single still first frame** for an image-to-video workflow. The output keeps user constraints visible and separates positive and negative instructions.

This repository contains a working `SKILL.md`, a [copyable Chinese core prompt](references/core-prompt.zh-CN.md), example input and output, and a standard-library checker for explicit constraints. The Skill produces text; it does not generate images or call a model API.

## Install

From this repository directory, install the Skill and start a new Codex chat:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/image-prompt-optimizer"
cp -R SKILL.md README.md LICENSE examples references scripts tests "${CODEX_HOME:-$HOME/.codex}/skills/image-prompt-optimizer/"
```

Invoke `$image-prompt-optimizer`. For example:

```text
Use $image-prompt-optimizer. Make a 9:16 first-frame image prompt for a child in a yellow raincoat holding a red balloon on a wet street. Keep both colors; no text or watermark.
```

## Input and output

The Skill accepts a natural-language brief or the JSON shape in [`examples/brief.json`](examples/brief.json). It returns `positive_prompt`, `negative_prompt`, `aspect_ratio`, `first_frame_notes`, and `assumptions`. [`examples/result.json`](examples/result.json) shows one possible first-frame output; [`examples/standalone-brief.json`](examples/standalone-brief.json) and [`examples/standalone-result.json`](examples/standalone-result.json) show ordinary image mode. For a first frame, the positive prompt describes one visible moment; motion belongs in a later video prompt.

The checker verifies literal required and excluded phrases, field types, aspect ratio, and first-frame notes:

```bash
python3 scripts/check_output.py examples/brief.json examples/result.json
python3 scripts/check_output.py examples/standalone-brief.json examples/standalone-result.json
python3 -B -m unittest discover -s tests -v
```

These checks do not measure image quality or how a particular generator interprets the prompt. Inspect generated images before claiming an improvement.

## Using the first frame

Once you generate an image from the prompt, you can use it as a first-frame reference in a compatible image-to-video tool. [GatsbyAI](https://gatsbyai.app/) offers an image-to-video workflow. Check the site's current controls before choosing a model or settings. This Skill is useful without that service and has no required account or network dependency.

## License

MIT. See [`LICENSE`](LICENSE).

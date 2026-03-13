<div align="center">

# PRD-Creat

Public repo for the `prd-creater` skill, with a synced Notion PRD template catalog, scenario-based shortlist guides, and one-command installers for Codex and other AI tools.

<p>
  <img alt="Visibility" src="https://img.shields.io/badge/repo-public-brightgreen">
  <img alt="Templates" src="https://img.shields.io/badge/templates-98-blue">
  <img alt="Categories" src="https://img.shields.io/badge/categories-10-orange">
  <img alt="Official Notion Templates" src="https://img.shields.io/badge/official%20notion-6-black">
</p>

<p>
  <a href="#quick-start">Quick Start</a> ·
  <a href="#scenario-guide">Scenario Guide</a> ·
  <a href="#test-sample">Test Sample</a> ·
  <a href="#repo-map">Repo Map</a> ·
  <a href="#maintenance">Maintenance</a>
</p>

</div>

> If you want to turn rough feature ideas, design briefs, roadmap items, or research notes into a Notion-ready PRD, this repo gives you both the reusable skill and the template selection layer.

## What You Get

| Module | What it gives you |
| --- | --- |
| [`skills/prd-creater/`](./skills/prd-creater/) | The skill itself, including the PRD scaffold, synced references, and refresh scripts |
| [`Readme/模板清单-PRD-Creater.md`](./Readme/%E6%A8%A1%E6%9D%BF%E6%B8%85%E5%8D%95-PRD-Creater.md) | The full raw list of `98` Notion Marketplace PRD templates |
| [`Readme/模板分类与场景-PRD-Creater.md`](./Readme/%E6%A8%A1%E6%9D%BF%E5%88%86%E7%B1%BB%E4%B8%8E%E5%9C%BA%E6%99%AF-PRD-Creater.md) | A scenario-based guide that groups all `98` templates into `10` practical categories |
| [`Readme/测试模板-设计PRD.md`](./Readme/%E6%B5%8B%E8%AF%95%E6%A8%A1%E6%9D%BF-%E8%AE%BE%E8%AE%A1PRD.md) | A complete design-focused PRD sample generated with the skill workflow |
| [`scripts/install-prd-creater.ps1`](./scripts/install-prd-creater.ps1) | Windows one-command installer for Codex or any local skills/prompts directory |
| [`scripts/install-prd-creater.sh`](./scripts/install-prd-creater.sh) | macOS/Linux installer for other AI toolchains |

## Quick Start

Use this if your AI tool supports a local `skills`, `prompts`, or similar directory.

<details>
<summary><strong>Windows PowerShell</strong></summary>

Install to the default Codex skills directory:

```powershell
$target = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills" } else { Join-Path $HOME ".codex\\skills" }
$script = Join-Path $env:TEMP "install-prd-creater.ps1"
Invoke-WebRequest "https://raw.githubusercontent.com/aEboli/PRD-Creat/main/scripts/install-prd-creater.ps1" -OutFile $script
& $script -TargetDir $target -Force
```

Install to another AI tool's local directory:

```powershell
$script = Join-Path $env:TEMP "install-prd-creater.ps1"
Invoke-WebRequest "https://raw.githubusercontent.com/aEboli/PRD-Creat/main/scripts/install-prd-creater.ps1" -OutFile $script
& $script -TargetDir "C:\\path\\to\\your\\ai-tool\\skills" -Force
```

</details>

<details>
<summary><strong>macOS / Linux</strong></summary>

Install to the default Codex skills directory:

```bash
curl -fsSL https://raw.githubusercontent.com/aEboli/PRD-Creat/main/scripts/install-prd-creater.sh -o /tmp/install-prd-creater.sh
bash /tmp/install-prd-creater.sh "${CODEX_HOME:-$HOME/.codex}/skills" --force
```

Install to another AI tool's local directory:

```bash
curl -fsSL https://raw.githubusercontent.com/aEboli/PRD-Creat/main/scripts/install-prd-creater.sh -o /tmp/install-prd-creater.sh
bash /tmp/install-prd-creater.sh "/path/to/your/ai-tool/skills" --force
```

</details>

After installation, try:

```text
Use $prd-creater to turn this feature brief into a PRD.
```

## Scenario Guide

The current snapshot is based on `2026-03-13` and includes:

- `98` templates total
- `68` free templates
- `30` paid templates
- `6` official Notion templates

### Scenario Summary

| Category | Count | Best for |
| --- | ---: | --- |
| Official Notion Baseline | 6 | Starting from the safest Notion-owned PRD spine |
| General Product PRD | 27 | Standard feature specs, iteration docs, single-project PRDs |
| AI / Intelligent Product PRD | 4 | AI capability, model constraints, evaluation, guardrails |
| Startup / MVP / Early Product | 8 | Lean MVP planning and fast-moving small teams |
| Discovery / Strategy / Problem Framing | 14 | Problem definition, evidence capture, option comparison |
| Design / UX / Website Requirements | 8 | Design-heavy specs, website redesigns, UX review |
| Roadmap / Prioritization / Planning | 13 | Prioritization, quarterly planning, roadmap-linked delivery |
| Engineering / Internal Tool / Technical Spec | 7 | Internal tooling, technical constraints, tracking plans |
| PM Workspace / Collaboration Hub / Knowledge Base | 5 | Managing many PRDs, briefs, meetings, and knowledge assets |
| BRD / Approval / Compliance / Business Ops | 6 | Approvals, BRDs, RFPs, compliance, formal cross-team workflows |

Go deeper here:

- [Scenario-based shortlist guide](./Readme/%E6%A8%A1%E6%9D%BF%E5%88%86%E7%B1%BB%E4%B8%8E%E5%9C%BA%E6%99%AF-PRD-Creater.md)
- [Full raw catalog](./Readme/%E6%A8%A1%E6%9D%BF%E6%B8%85%E5%8D%95-PRD-Creater.md)
- [Usage guide](./Readme/%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E-PRD-Creater.md)

## Test Sample

Want to see what the skill actually outputs?

- [Design-focused PRD sample: 帮助中心 2.0 改版](./Readme/%E6%B5%8B%E8%AF%95%E6%A8%A1%E6%9D%BF-%E8%AE%BE%E8%AE%A1PRD.md)

This sample uses the `Design / UX / Website Requirements` family and demonstrates how the skill handles:

- information architecture
- search experience
- article readability
- support deflection metrics

## Repo Map

```text
PRD-Creat/
  skills/
    prd-creater/
      SKILL.md
      agents/openai.yaml
      assets/
      references/
      scripts/
  Readme/
  scripts/
  doc/
```

### Key Paths

| Path | Purpose |
| --- | --- |
| [`skills/prd-creater/SKILL.md`](./skills/prd-creater/SKILL.md) | Trigger rules, workflow, and output guidance for the skill |
| [`skills/prd-creater/assets/notion-prd-template.md`](./skills/prd-creater/assets/notion-prd-template.md) | Paste-ready PRD scaffold |
| [`skills/prd-creater/references/notion-prd-marketplace-catalog.json`](./skills/prd-creater/references/notion-prd-marketplace-catalog.json) | Structured Notion template catalog |
| [`skills/prd-creater/references/notion-prd-marketplace-scenario-guide.md`](./skills/prd-creater/references/notion-prd-marketplace-scenario-guide.md) | Scenario-oriented shortlist guide for the skill itself |
| [`scripts/generate_prd_template_guides.py`](./scripts/generate_prd_template_guides.py) | Regenerates the categorized template guides |
| [`doc/进展记录.md`](./doc/%E8%BF%9B%E5%B1%95%E8%AE%B0%E5%BD%95.md) | Ongoing project progress log |

## Maintenance

Refresh the Notion Marketplace `PRD` catalog:

```bash
python skills/prd-creater/scripts/sync_notion_marketplace_catalog.py --query PRD
```

Regenerate the categorized guides:

```bash
python scripts/generate_prd_template_guides.py
```

Validate the skill:

```bash
python C:/Users/AEboli/.codex/skills/.system/skill-creator/scripts/quick_validate.py C:/Users/AEboli/Documents/PRD-Creat/skills/prd-creater
```

## Related Docs

- [Usage guide](./Readme/%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E-PRD-Creater.md)
- [Project PRD](./Readme/PRD-PRD-Creater.md)
- [Progress log](./doc/%E8%BF%9B%E5%B1%95%E8%AE%B0%E5%BD%95.md)

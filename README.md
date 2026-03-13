# PRD-Creat

`PRD-Creat` 是一个公开仓库，用来维护 `prd-creater` skill 以及基于 Notion Marketplace `PRD` 搜索结果整理出的模板目录、分类清单和安装脚本。

仓库地址：[aEboli/PRD-Creat](https://github.com/aEboli/PRD-Creat)

## 仓库内容

- `skills/prd-creater/`：skill 本体、模板骨架、参考资料和同步脚本
- `Readme/模板清单-PRD-Creater.md`：98 个模板的原始完整清单
- `Readme/模板分类与场景-PRD-Creater.md`：98 个模板的分类表和推荐使用场景
- `Readme/测试模板-设计PRD.md`：使用 `prd-creater` 生成的设计类 PRD 测试样例
- `Readme/使用说明-PRD-Creater.md`：协作者使用说明
- `Readme/PRD-PRD-Creater.md`：本项目 PRD
- `scripts/`：模板分类生成脚本和跨平台安装脚本
- `doc/进展记录.md`：持续进展记录

## 快速安装

如果你的 AI 工具支持“本地 prompts/skills 目录”，可以直接把 `prd-creater` 安装进去。

### Windows PowerShell

安装到默认 Codex skills 目录：

```powershell
$target = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills" } else { Join-Path $HOME ".codex\\skills" }
$script = Join-Path $env:TEMP "install-prd-creater.ps1"
Invoke-WebRequest "https://raw.githubusercontent.com/aEboli/PRD-Creat/main/scripts/install-prd-creater.ps1" -OutFile $script
& $script -TargetDir $target -Force
```

安装到其他 AI 工具的本地目录：

```powershell
$script = Join-Path $env:TEMP "install-prd-creater.ps1"
Invoke-WebRequest "https://raw.githubusercontent.com/aEboli/PRD-Creat/main/scripts/install-prd-creater.ps1" -OutFile $script
& $script -TargetDir "C:\\path\\to\\your\\ai-tool\\skills" -Force
```

### macOS / Linux

安装到默认 Codex skills 目录：

```bash
curl -fsSL https://raw.githubusercontent.com/aEboli/PRD-Creat/main/scripts/install-prd-creater.sh -o /tmp/install-prd-creater.sh
bash /tmp/install-prd-creater.sh "${CODEX_HOME:-$HOME/.codex}/skills" --force
```

安装到其他 AI 工具的本地目录：

```bash
curl -fsSL https://raw.githubusercontent.com/aEboli/PRD-Creat/main/scripts/install-prd-creater.sh -o /tmp/install-prd-creater.sh
bash /tmp/install-prd-creater.sh "/path/to/your/ai-tool/skills" --force
```

安装完成后，可直接使用提示词：

```text
Use $prd-creater to turn this feature brief into a PRD.
```

## 当前模板快照

- 总模板数：`98`
- 免费模板：`68`
- 付费模板：`30`
- Notion 官方模板：`6`

## 模板分类总览

| 分类 | 数量 | 适用场景 |
| --- | ---: | --- |
| 官方 Notion 基线模板 | 6 | 先按官方标准骨架起草，再补团队字段 |
| 通用产品 PRD | 27 | 常规功能需求、版本迭代、单项目说明 |
| AI / 智能产品 PRD | 4 | AI 功能、模型约束、评测与护栏指标 |
| 创业 / MVP / 早期产品 | 8 | 小团队、快试错、MVP 验证 |
| 产品发现 / 策略 / 需求澄清 | 14 | 先定义问题、机会、方案和证据 |
| 设计 / UX / 网站需求 | 8 | 设计协作、网站改版、体验规格 |
| 路线图 / 优先级 / 计划排期 | 13 | 优先级排序、季度规划、发布联动 |
| 工程 / 内部工具 / 技术规格 | 7 | 内部系统、技术约束、埋点和规格说明 |
| PM 工作台 / 协作中枢 / 文档库 | 5 | 管理多份 PRD、brief、任务和会议 |
| BRD / 审批 / 合规 / 专项业务 | 6 | BRD、审批、RFP、合规和正式流程 |

完整文档：

- [模板清单-PRD-Creater.md](C:/Users/AEboli/Documents/PRD-Creat/Readme/模板清单-PRD-Creater.md)
- [模板分类与场景-PRD-Creater.md](C:/Users/AEboli/Documents/PRD-Creat/Readme/模板分类与场景-PRD-Creater.md)
- [使用说明-PRD-Creater.md](C:/Users/AEboli/Documents/PRD-Creat/Readme/使用说明-PRD-Creater.md)

## 维护命令

刷新 Notion Marketplace `PRD` 目录：

```bash
python skills/prd-creater/scripts/sync_notion_marketplace_catalog.py --query PRD
```

重新生成分类表和场景指南：

```bash
python scripts/generate_prd_template_guides.py
```

校验 skill：

```bash
python C:/Users/AEboli/.codex/skills/.system/skill-creator/scripts/quick_validate.py C:/Users/AEboli/Documents/PRD-Creat/skills/prd-creater
```

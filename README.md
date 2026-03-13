# PRD-Creat

`PRD-Creat` 是一个独立项目仓库，用来版本化维护 `prd-creater` skill。这个 skill 以 Notion 官方 PRD 写作骨架为底座，并接入了 Notion Marketplace 中 `PRD` 搜索结果的完整模板目录快照。

当前仓库包含：

- `skills/prd-creater/`：可直接版本管理的 skill 正文、脚本、模板和参考资料
- `Readme/模板清单-PRD-Creater.md`：98 个 Notion PRD 模板清单
- `Readme/使用说明-PRD-Creater.md`：使用说明
- `Readme/PRD-PRD-Creater.md`：该 skill 的项目 PRD
- `doc/进展记录.md`：本仓库自己的进展记录

## 目录结构

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
  doc/
```

## 当前模板快照

- 总模板数：`98`
- 免费模板：`68`
- 付费模板：`30`
- Notion 官方模板：`6`

完整清单见 [模板清单-PRD-Creater.md](C:/Users/AEboli/Documents/PRD-Creat/Readme/模板清单-PRD-Creater.md)。

## 更新模板目录

在仓库根目录执行：

```bash
python skills/prd-creater/scripts/sync_notion_marketplace_catalog.py --query PRD
```

脚本会刷新：

- `skills/prd-creater/references/notion-prd-marketplace-catalog.json`
- `skills/prd-creater/references/notion-prd-marketplace-catalog.md`

如果你也希望同步仓库级模板清单，可以把更新后的 Markdown 再复制到 `Readme/模板清单-PRD-Creater.md`。

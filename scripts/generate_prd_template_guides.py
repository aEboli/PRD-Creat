#!/usr/bin/env python3
"""
Generate curated PRD template guides from the synced Notion Marketplace catalog.

Outputs:
- Readme/模板分类与场景-PRD-Creater.md
- skills/prd-creater/references/notion-prd-marketplace-scenario-guide.md
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "skills" / "prd-creater" / "references" / "notion-prd-marketplace-catalog.json"
CN_GUIDE_PATH = REPO_ROOT / "Readme" / "模板分类与场景-PRD-Creater.md"
EN_GUIDE_PATH = REPO_ROOT / "skills" / "prd-creater" / "references" / "notion-prd-marketplace-scenario-guide.md"

BUCKETS = [
    {
        "id": "official",
        "title_cn": "官方 Notion 基线模板",
        "title_en": "Official Notion Baseline",
        "use_case_cn": "想先用最稳妥的 Notion 官方结构起草，再按团队习惯扩展字段。",
        "use_case_en": "Start from the safest Notion-owned structure, then adapt it to your team.",
        "signals_cn": "用户强调“官方模板”“不要太花哨”“先要标准骨架”。",
        "signals_en": "The user asks for an official template, a standard spine, or the safest default.",
    },
    {
        "id": "general",
        "title_cn": "通用产品 PRD",
        "title_en": "General Product PRD",
        "use_case_cn": "新功能、需求迭代、单一项目说明，暂时不需要复杂配套系统。",
        "use_case_en": "Draft a straightforward PRD for a feature, improvement, or single project.",
        "signals_cn": "用户只给了功能想法、范围、目标和 KPI，希望尽快成文。",
        "signals_en": "The user has a feature idea plus scope, goals, and KPIs, and wants a quick first draft.",
    },
    {
        "id": "ai",
        "title_cn": "AI / 智能产品 PRD",
        "title_en": "AI / Intelligent Product PRD",
        "use_case_cn": "涉及模型能力、数据要求、评测方式、护栏指标或 AI 风险说明。",
        "use_case_en": "Document AI capabilities, data needs, evaluation plans, guardrails, and risk controls.",
        "signals_cn": "需求里出现 AI、模型、训练数据、评测、自动化代理等字眼。",
        "signals_en": "The request mentions AI, models, evaluation, training data, or agentic workflows.",
    },
    {
        "id": "startup",
        "title_cn": "创业 / MVP / 早期产品",
        "title_en": "Startup / MVP / Early Product",
        "use_case_cn": "资源有限、需要先验证问题和价值，强调 MVP、试错速度与对齐效率。",
        "use_case_en": "Move quickly with a lean spec for an MVP, early-stage launch, or startup team.",
        "signals_cn": "团队小、上线快、资料少，希望先产出最小可行 PRD。",
        "signals_en": "The team is early-stage, moving fast, and wants a minimum viable PRD.",
    },
    {
        "id": "discovery",
        "title_cn": "产品发现 / 策略 / 需求澄清",
        "title_en": "Discovery / Strategy / Problem Framing",
        "use_case_cn": "还在定义问题、澄清机会、比较方案、沉淀洞察，PRD 更像决策文档。",
        "use_case_en": "Frame the problem, compare options, capture evidence, and align on direction.",
        "signals_cn": "输入更像研究结论、策略文档、机会树、brief 或一页纸。",
        "signals_en": "Inputs look more like research notes, strategy docs, briefs, or one-pagers.",
    },
    {
        "id": "design",
        "title_cn": "设计 / UX / 网站需求",
        "title_en": "Design / UX / Website Requirements",
        "use_case_cn": "面向设计协作、体验评审、网站改版、设计规范或交互说明。",
        "use_case_en": "Support design collaboration, UX review, site redesigns, and experience specs.",
        "signals_cn": "需求强调设计稿、交互流程、信息架构、网站页面或设计评审。",
        "signals_en": "The work centers on design artifacts, UX flows, site structure, or review checklists.",
    },
    {
        "id": "roadmap",
        "title_cn": "路线图 / 优先级 / 计划排期",
        "title_en": "Roadmap / Prioritization / Planning",
        "use_case_cn": "需要做排序、季度排期、发布计划、跟踪推进或项目管理联动。",
        "use_case_en": "Prioritize work, sequence releases, manage roadmaps, and keep execution aligned.",
        "signals_cn": "用户关注 roadmap、优先级、RICE、季度计划、发布节奏或追踪面板。",
        "signals_en": "The request focuses on roadmaps, prioritization, quarterly planning, or release tracking.",
    },
    {
        "id": "engineering",
        "title_cn": "工程 / 内部工具 / 技术规格",
        "title_en": "Engineering / Internal Tool / Technical Spec",
        "use_case_cn": "偏内部系统、软件规格、工程协作、技术约束、数据埋点或合规实现。",
        "use_case_en": "Document internal tools, software specs, technical constraints, tracking plans, or compliance detail.",
        "signals_cn": "需求里提到 internal tool、software spec、工程实现、埋点、架构等。",
        "signals_en": "The scope includes internal tools, software specifications, engineering detail, or tracking plans.",
    },
    {
        "id": "workspace",
        "title_cn": "PM 工作台 / 协作中枢 / 文档库",
        "title_en": "PM Workspace / Collaboration Hub / Knowledge Base",
        "use_case_cn": "不是单份 PRD，而是要管理一组 PRD、brief、任务、会议和知识资产。",
        "use_case_en": "Manage multiple PRDs, briefs, meetings, and knowledge assets in one operating system.",
        "signals_cn": "用户要的是 hub、workspace、OS、manager、library 或协作文档中心。",
        "signals_en": "The user wants a hub, workspace, operating system, manager, library, or collaboration center.",
    },
    {
        "id": "business",
        "title_cn": "BRD / 审批 / 合规 / 专项业务",
        "title_en": "BRD / Approval / Compliance / Business Ops",
        "use_case_cn": "偏商务需求、立项、审批、RFP、合规或跨部门正式流程文档。",
        "use_case_en": "Handle BRDs, approvals, RFPs, compliance, and other formal cross-functional workflows.",
        "signals_cn": "文档面向业务方、审批链路、供应商选择、合规检查或正式立项。",
        "signals_en": "The document targets business stakeholders, approval chains, vendors, or compliance reviews.",
    },
]

SCENARIO_HINTS = [
    ("internal tool", "适合后台、运营平台或内部流程系统。", "Best for back-office tools, admin systems, or internal workflows."),
    ("website", "适合官网、营销站或页面改版类需求。", "Best for websites, landing pages, or site redesigns."),
    ("roadmap", "适合把需求和路线图、发布时间点一起管理。", "Best when the PRD must stay tied to a roadmap or release plan."),
    ("release", "适合需要明确版本节奏、上线门槛和里程碑的项目。", "Best when you need release timing, launch criteria, and milestones."),
    ("brief", "适合先把问题定义清楚，再逐步扩成正式 PRD。", "Best for clarifying the problem before expanding into a full PRD."),
    ("1-pager", "适合领导快速浏览的一页式需求概览。", "Best for a leadership-friendly one-pager."),
    ("discovery", "适合前期探索、机会判断和方案筛选。", "Best for early discovery, opportunity sizing, and option comparison."),
    ("growth", "适合增长实验、漏斗优化和效果验证。", "Best for growth experiments and funnel optimization."),
    ("analytics", "适合埋点规划、数据指标定义和分析协作。", "Best for tracking plans, analytics requirements, and measurement design."),
    ("software", "适合软件规格说明、技术约束和交付边界。", "Best for software specifications, technical constraints, and delivery boundaries."),
    ("security", "适合安全、合规、审计或治理类要求。", "Best for security, compliance, audit, and governance workflows."),
    ("approval", "适合立项审批、请求受理和跨部门流转。", "Best for approval flows, intake, and cross-functional requests."),
    ("collab", "适合多人持续协作、文档跟踪和会议联动。", "Best for ongoing collaboration, document tracking, and meeting coordination."),
    ("document manager", "适合 PM 或项目负责人长期管理多份需求文档。", "Best for PMs or owners managing a portfolio of requests over time."),
    ("project manager/product owner", "适合 PM 或项目负责人长期管理多份需求文档。", "Best for PMs or owners managing a portfolio of requests over time."),
    ("product manager os", "适合 PM 或项目负责人长期管理多份需求文档。", "Best for PMs or owners managing a portfolio of requests over time."),
    ("design", "适合和设计评审、交互说明或体验规范一起使用。", "Best when the PRD lives next to design review and UX guidance."),
    ("startup", "适合小团队快速验证 MVP 和商业价值。", "Best for small teams validating an MVP quickly."),
    ("mvp", "适合资源有限但需要快速推进的 MVP 阶段。", "Best for a fast-moving MVP phase with limited resources."),
    ("ai", "适合 AI 功能定义、模型约束、评测与风险说明。", "Best for AI features, model constraints, evaluation plans, and risk controls."),
    ("brief library", "适合沉淀一组可复用 brief，而不是只写单篇 PRD。", "Best for maintaining a reusable brief library, not just one PRD."),
]

DEFAULT_SCENARIO_CN = {
    "official": "适合先沿用官方结构起草，再补充团队自己的字段和细节。",
    "general": "适合大多数常规功能需求、版本迭代和单项目说明。",
    "ai": "适合需要写清 AI 能力、数据来源、评测方法和护栏指标的需求。",
    "startup": "适合创业团队、MVP 验证和快速试错的轻量 PRD。",
    "discovery": "适合在立项前整理问题、证据、方向与方案取舍。",
    "design": "适合设计驱动型需求、网站改版和体验规格说明。",
    "roadmap": "适合把需求和优先级、季度计划、发布时间点放在一起管理。",
    "engineering": "适合工程细节较重、需要技术约束或内部系统说明的场景。",
    "workspace": "适合管理一组相关文档、任务、会议和知识资产，而不是单篇 PRD。",
    "business": "适合正式审批、业务需求澄清、BRD 或跨部门协作文档。",
}

DEFAULT_SCENARIO_EN = {
    "official": "Use the official structure as a safe starting point, then add team-specific fields as needed.",
    "general": "Use for most standard feature specs, requirement updates, and single-project PRDs.",
    "ai": "Use when you must document AI capability, data sources, evaluation plans, and guardrail metrics.",
    "startup": "Use for startup teams, MVP validation, and fast-moving product bets.",
    "discovery": "Use before commitment to frame the problem, evidence, tradeoffs, and options.",
    "design": "Use for design-heavy work, site redesigns, UX review, and interaction-focused specs.",
    "roadmap": "Use when the PRD must stay connected to prioritization, timelines, and release planning.",
    "engineering": "Use for internal tooling, technical constraints, engineering-heavy scope, or tracking plans.",
    "workspace": "Use for a workspace that manages many related docs, tasks, meetings, and knowledge assets.",
    "business": "Use for formal approvals, BRDs, business workflows, compliance, and vendor-facing processes.",
}


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def classify_template(template: dict) -> str:
    name = (template.get("name") or "").lower()
    categories = {c.lower() for c in (template.get("categories") or [])}

    if template.get("official"):
        return "official"
    if "ai" in categories or "ai-powered tools" in categories or any(
        key in name for key in ("ai prd", "structured ai", "ai-powered")
    ):
        return "ai"
    if any(key in name for key in ("brd", "business requirement", "business requirements", "approval", "rfp", "charter")):
        return "business"
    if any(key in name for key in ("website", "design", "ux", "ui ", "heuristics", "faq")):
        return "design"
    if any(
        key in name
        for key in (
            "discovery",
            "strategy",
            "opportunity solution tree",
            "1-pager",
            "product brief",
            "evidence box",
            "growth experiment",
            "requirements gathering",
            "challenge a feature request",
        )
    ):
        return "discovery"
    if any(
        key in name
        for key in (
            "roadmap",
            "priorit",
            "rice",
            "weighted scoring",
            "quarterly",
            "release",
            "definition of ready",
            "project management",
            "tracker",
        )
    ):
        return "roadmap"
    if any(
        key in name
        for key in ("internal tool", "software", "developer portal", "architecture", "analytics", "security", "spec document")
    ):
        return "engineering"
    if any(
        key in name
        for key in ("workspace", "team hub", "product manager os", "designer hub", "library", "document manager", "collaboration", "collab")
    ):
        return "workspace"
    if any(key in name for key in ("startup", "mvp", "early-stage")) or "startup" in categories:
        return "startup"
    if {"compliance", "pr & comms", "agency", "company planning"} & categories:
        return "business"
    if {"design", "design request", "design critique meeting", "design brief", "design system"} & categories:
        return "design"
    if {"product strategy doc", "user research"} & categories:
        return "discovery"
    if {"project management", "roadmaps & calendars", "product roadmap", "project roadmap", "project plans", "scrum board"} & categories:
        return "roadmap"
    if {"engineering", "engineering tech spec", "eng knowledge base"} & categories:
        return "engineering"
    if {"team hub", "product knowledge base"} & categories:
        return "workspace"
    return "general"


def infer_template_scenario(template: dict, bucket_id: str, language: str) -> str:
    name = (template.get("name") or "").lower()
    for needle, cn, en in SCENARIO_HINTS:
        if needle in name:
            return cn if language == "cn" else en
    if language == "cn":
        return DEFAULT_SCENARIO_CN[bucket_id]
    return DEFAULT_SCENARIO_EN[bucket_id]


def sort_templates(templates: list[dict]) -> list[dict]:
    return sorted(templates, key=lambda item: (0 if item.get("official") else 1, 0 if item.get("is_free") else 1, item.get("price") or 0, item.get("index") or 0))


def build_bucketed_templates(payload: dict) -> dict[str, list[dict]]:
    bucketed: dict[str, list[dict]] = defaultdict(list)
    for template in payload["templates"]:
        bucketed[classify_template(template)].append(template)
    return {bucket_id: sort_templates(bucketed.get(bucket_id, [])) for bucket_id in [bucket["id"] for bucket in BUCKETS]}


def render_cn(payload: dict, bucketed: dict[str, list[dict]]) -> str:
    summary = payload["summary"]
    lines = [
        "# 模板分类与场景-PRD-Creater",
        "",
        "对应对象：`PRD-Creater` skill  ",
        f"技能目录：`{REPO_ROOT / 'skills' / 'prd-creater'}`",
        "",
        "下方内容基于仓库内同步的 `98` 个 Notion Marketplace `PRD` 模板快照，按使用场景重新归类，方便在生成 PRD 前先选模板家族，再决定输出骨架。",
        "",
        "## 快照概览",
        "",
        f"- 同步时间：`{payload['synced_at']}`",
        f"- 模板总数：`{payload['total_templates']}`",
        f"- 免费模板：`{summary['free_count']}`",
        f"- 付费模板：`{summary['paid_count']}`",
        f"- Notion 官方模板：`{summary['official_count']}`",
        "",
        "## 分类总览",
        "",
        "| 分类 | 数量 | 适用场景 | 选型信号 |",
        "| --- | ---: | --- | --- |",
    ]

    for bucket in BUCKETS:
        count = len(bucketed[bucket["id"]])
        lines.append(
            f"| {bucket['title_cn']} | {count} | {bucket['use_case_cn']} | {bucket['signals_cn']} |"
        )

    lines.extend(
        [
            "",
            "## 分类明细",
            "",
            "说明：每个模板只放入一个主分类，`推荐使用场景` 列给出优先适用的典型场景，便于快速筛选。",
        ]
    )

    for bucket in BUCKETS:
        templates = bucketed[bucket["id"]]
        lines.extend(
            [
                "",
                f"### {bucket['title_cn']}（{len(templates)}）",
                "",
                f"- 适用场景：{bucket['use_case_cn']}",
                f"- 选型信号：{bucket['signals_cn']}",
                "",
                "| # | 模板 | Creator | 价格 | 来源 | 推荐使用场景 | 链接 |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )

        for template in templates:
            name = (template.get("name") or "").replace("|", "\\|")
            creator = (template.get("creator_name") or "").replace("|", "\\|")
            price = template.get("price_display") or "Free"
            source = "Official" if template.get("official") else "Community"
            scenario = infer_template_scenario(template, bucket["id"], "cn").replace("|", "\\|")
            url = template.get("url") or template.get("purchase_url") or ""
            lines.append(
                f"| {template['index']} | {name} | {creator} | {price} | {source} | {scenario} | {url} |"
            )

    return "\n".join(lines) + "\n"


def render_en(payload: dict, bucketed: dict[str, list[dict]]) -> str:
    summary = payload["summary"]
    lines = [
        "# Notion PRD Marketplace Scenario Guide",
        "",
        f"- Synced at: `{payload['synced_at']}`",
        f"- Total templates: `{payload['total_templates']}`",
        f"- Free templates: `{summary['free_count']}`",
        f"- Paid templates: `{summary['paid_count']}`",
        f"- Official Notion templates: `{summary['official_count']}`",
        "",
        "Use this guide to shortlist a template family before drafting a PRD.",
        "",
        "## Category summary",
        "",
        "| Category | Count | Best when... | Selection signals |",
        "| --- | ---: | --- | --- |",
    ]

    for bucket in BUCKETS:
        count = len(bucketed[bucket["id"]])
        lines.append(
            f"| {bucket['title_en']} | {count} | {bucket['use_case_en']} | {bucket['signals_en']} |"
        )

    lines.extend(
        [
            "",
            "## Templates by category",
            "",
            "Each template appears in one primary category so the guide stays decision-oriented.",
        ]
    )

    for bucket in BUCKETS:
        templates = bucketed[bucket["id"]]
        lines.extend(
            [
                "",
                f"### {bucket['title_en']} ({len(templates)})",
                "",
                f"- Best when: {bucket['use_case_en']}",
                f"- Selection signals: {bucket['signals_en']}",
                "",
                "| # | Template | Creator | Price | Source | Best fit | Link |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )

        for template in templates:
            name = (template.get("name") or "").replace("|", "\\|")
            creator = (template.get("creator_name") or "").replace("|", "\\|")
            price = template.get("price_display") or "Free"
            source = "Official" if template.get("official") else "Community"
            scenario = infer_template_scenario(template, bucket["id"], "en").replace("|", "\\|")
            url = template.get("url") or template.get("purchase_url") or ""
            lines.append(
                f"| {template['index']} | {name} | {creator} | {price} | {source} | {scenario} | {url} |"
            )

    return "\n".join(lines) + "\n"


def main() -> int:
    payload = load_catalog()
    bucketed = build_bucketed_templates(payload)

    CN_GUIDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EN_GUIDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CN_GUIDE_PATH.write_text(render_cn(payload, bucketed), encoding="utf-8")
    EN_GUIDE_PATH.write_text(render_en(payload, bucketed), encoding="utf-8")

    counts = Counter()
    for bucket_id, templates in bucketed.items():
        counts[bucket_id] = len(templates)

    print("[OK] Generated categorized PRD guides")
    for bucket in BUCKETS:
        print(f"  - {bucket['title_en']}: {counts[bucket['id']]}")
    print(f"[OK] Chinese guide: {CN_GUIDE_PATH}")
    print(f"[OK] English guide: {EN_GUIDE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

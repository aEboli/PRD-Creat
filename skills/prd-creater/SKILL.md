---
name: prd-creater
description: Create product requirement documents using the synced Notion Marketplace PRD template catalog plus Notion's official PRD guidance. Use when Codex needs to turn a feature idea, roadmap item, stakeholder request, discovery notes, meeting notes, or a rough product brief into a structured PRD, or when the user asks to match, compare, shortlist, or reuse Notion PRD templates from the marketplace.
---

# PRD Creater

## When to use
- Turn raw product inputs into a clean PRD.
- Rewrite messy notes into a structured Notion-style document.
- Draft a first-pass PRD when the user only has a feature idea or meeting summary.
- Standardize PRDs across a team so each document follows the same section order and decision logic.

## Workflow
1. Identify the source material and audience.
   - Accept feature ideas, product briefs, stakeholder asks, workshop notes, user research summaries, roadmap items, or launch requests.
   - Mirror the user's language unless they ask for a different output language.
2. Choose the right marketplace pattern before drafting.
   - Use `references/notion-prd-marketplace-catalog.md` for a quick scan of the synced marketplace results.
   - Use `references/notion-prd-marketplace-catalog.json` when you need richer details such as full descriptions, extracted body text, creator metadata, or category tags.
   - Use `references/notion-prd-marketplace-scenario-guide.md` when the user asks for a shortlist by use case, team maturity, product type, or operating model.
   - If the user names a specific template, match by `name` or `slug` first.
   - If the user wants the safest default, prefer official Notion templates.
   - If the user wants a niche use case, use `references/notion-prd-marketplace-selection-guide.md` to map the request to the closest template family.
3. Extract the minimum facts needed to write the PRD.
   - Capture the product or feature name, target users, problem, value, goals, scope, core requirements, constraints, dependencies, risks, launch criteria, and owners if available.
   - If information is missing, make the smallest reasonable assumption and mark it as `Needs confirmation`.
4. Start from Notion's official PRD spine.
   - Use the five stable sections from Notion's guidance: `Context`, `Goals and KPIs`, `Constraints and assumptions`, `Dependencies`, and `Tasks`.
   - Expand with the official writing steps when the request needs more depth: `Scope`, `Features or requirements`, `Release criteria`, and `Metrics for success`.
5. Add richer context only when it helps decisions.
   - For cross-functional, experimental, or high-risk work, pull optional sections from `references/notion-official-prd-template.md`, such as `Hypothesis`, `Related work`, `Design and interaction`, `Qualitative feedback`, `Guardrail metrics`, or `Open questions`.
6. Produce a paste-ready PRD.
   - Use `assets/notion-prd-template.md` as the default scaffold.
   - Adapt the section emphasis to the selected marketplace pattern instead of forcing every output into the same shape.
   - Keep the doc concise, specific, and decision-oriented.
   - Prefer bullets for requirements, tasks, and risks.
7. Review before delivery.
   - Remove fluff and duplicated ideas.
   - Make sure every requirement is testable, every metric is measurable, and every unknown is visible.
8. Refresh the catalog when needed.
   - Run `python scripts/sync_notion_marketplace_catalog.py --query PRD` whenever the user wants the latest marketplace snapshot.
   - Treat the catalog as time-sensitive data.

## Output rules
- Prefer a short metadata block at the top when operational tracking matters: owner, status, target release, last updated, reviewers.
- When writing for non-English teams, use bilingual headings with a local-language heading plus the English Notion heading.
- Always separate `In scope` and `Out of scope`.
- Pair each goal with one or more KPIs.
- Write requirements as observable outcomes, not vague implementation wishes.
- Put unresolved items under `Risks and open questions` or `Open questions`.
- If the request is thin, add `Assumptions` and `Needs confirmation` instead of pretending certainty.
- When a user asks for template comparison or shortlisting, answer from the synced marketplace catalog before drafting.
- Do not load the full catalog into the answer unless the user explicitly wants the whole list; filter first by use case, source, price, or template family.

## Fast mapping from raw input
- Feature idea: convert it into `Context`, `Target users`, `Problem`, `Goals`, and `Hypothesis`.
- Meeting notes: extract `Decisions`, `Open questions`, `Dependencies`, and `Tasks`.
- User research: turn findings into `Context`, `Evidence`, `Requirements`, and `Guardrail metrics`.
- Launch or rollout brief: emphasize `Release criteria`, `Risks`, `Dependencies`, and `Owner or timeline`.

## Quality bar
- Keep the opening summary short enough for leadership to scan quickly.
- Keep each section actionable for design, engineering, and stakeholders.
- Surface assumptions and tradeoffs early.
- Avoid generic goals like "improve experience" unless they are paired with a measurable KPI.
- If priorities conflict, make the tradeoff explicit in scope, risks, or open questions.

## Resources
- `references/notion-official-prd-template.md`: Summary of the Notion official PRD structure, writing steps, and optional context layers derived from Notion's official help center, blog, and marketplace pages.
- `references/notion-prd-marketplace-catalog.md`: Human-readable index of the synced PRD marketplace results.
- `references/notion-prd-marketplace-catalog.json`: Full structured catalog with metadata, categories, links, and extracted body text for each synced template.
- `references/notion-prd-marketplace-scenario-guide.md`: Scenario-based shortlist guide that groups the synced templates into practical families such as official baseline, AI PRD, startup MVP, roadmap planning, engineering spec, and business ops.
- `references/notion-prd-marketplace-selection-guide.md`: Quick heuristics for mapping a user request to the closest marketplace template family.
- `assets/notion-prd-template.md`: Paste-ready Markdown scaffold for drafting PRDs in a Notion-friendly format.
- `scripts/sync_notion_marketplace_catalog.py`: Refresh the marketplace catalog from Notion's public search page.

## Example prompts
- `Use $prd-creater to turn this feature idea into a formal PRD.`
- `Use $prd-creater to turn this roadmap item into an English PRD with KPIs and release criteria.`
- `Use $prd-creater to convert this interview summary into a Notion-ready PRD.`
- `Use $prd-creater to shortlist the best 5 Notion PRD templates for an internal tool launch.`
- `Use $prd-creater to match this request to the closest template in the synced Notion marketplace catalog, then draft the PRD.`

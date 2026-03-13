#!/usr/bin/env python3
"""
Sync a Notion Marketplace search result into JSON and Markdown catalogs.

Default target:
    query = PRD
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

SEARCH_URL = "https://www.notion.com/templates/search?query={query}"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/134.0.0.0 Safari/537.36"
)
BLOCK_NODES = {
    "paragraph",
    "heading-1",
    "heading-2",
    "heading-3",
    "heading-4",
    "heading-5",
    "heading-6",
    "list-item",
    "ordered-list",
    "unordered-list",
    "blockquote",
}


def fetch_next_data(query: str) -> dict:
    url = SEARCH_URL.format(query=urllib.parse.quote(query))
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    if not match:
        raise RuntimeError("Could not find __NEXT_DATA__ in the search page")

    return json.loads(match.group(1))


def collect_text(node: object, chunks: list[str]) -> None:
    if isinstance(node, dict):
        node_type = node.get("nodeType")
        if node_type == "text":
            value = node.get("value")
            if isinstance(value, str) and value:
                chunks.append(value)

        for child in node.get("content", []) or []:
            collect_text(child, chunks)

        if node_type in BLOCK_NODES:
            chunks.append("\n")
    elif isinstance(node, list):
        for item in node:
            collect_text(item, chunks)


def extract_body_text(serialized_body: object) -> str:
    chunks: list[str] = []
    collect_text(serialized_body, chunks)
    text = "".join(chunks)
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def format_price(price: object) -> str:
    if price in (None, 0, 0.0, "0", "0.0", ""):
        return "Free"
    if isinstance(price, int):
        return f"${price}"
    if isinstance(price, float):
        if price.is_integer():
            return f"${int(price)}"
        return f"${price:.2f}".rstrip("0").rstrip(".")
    return str(price)


def to_iso(timestamp_ms: object) -> str | None:
    if not isinstance(timestamp_ms, (int, float)):
        return None
    return dt.datetime.fromtimestamp(timestamp_ms / 1000, tz=dt.timezone.utc).isoformat()


def normalize_template(index: int, item: dict) -> dict:
    creator_name = item.get("creatorName") or ""
    creator_username = item.get("creatorUsername") or ""
    categories = [c.get("name") for c in item.get("categories", []) if c.get("name")]
    body_text = extract_body_text(item.get("serializedBody"))
    slug = item.get("slug") or ""
    price = item.get("price")
    official = creator_name.lower() == "notion" or creator_username.lower() == "notion"

    return {
        "index": index,
        "name": item.get("name"),
        "slug": slug,
        "url": f"https://www.notion.com/templates/{slug}" if slug else None,
        "creator_name": creator_name,
        "creator_username": creator_username,
        "creator_template_count": item.get("creatorTemplateCount"),
        "official": official,
        "price": price,
        "price_display": format_price(price),
        "is_free": price in (None, 0, 0.0, "0", "0.0", ""),
        "description": item.get("description") or "",
        "body_text": body_text,
        "categories": categories,
        "template_id": item.get("templateId") or item.get("id"),
        "purchase_url": item.get("purchaseUrl"),
        "duplication_url": item.get("duplicationHref"),
        "public_site_url": item.get("publicSiteUrl"),
        "last_updated": to_iso(item.get("lastUpdated")),
        "screenshots_count": len(item.get("screenshots", []) or []),
        "mobile_screenshots_count": len(item.get("mobileScreenshots", []) or []),
        "videos_count": len(item.get("videos", []) or []),
    }


def build_summary(templates: list[dict]) -> dict:
    official_count = sum(1 for t in templates if t["official"])
    free_count = sum(1 for t in templates if t["is_free"])
    paid_count = len(templates) - free_count

    category_counter: Counter[str] = Counter()
    for template in templates:
        category_counter.update(template["categories"])

    return {
        "official_count": official_count,
        "community_count": len(templates) - official_count,
        "free_count": free_count,
        "paid_count": paid_count,
        "top_categories": [
            {"name": name, "count": count}
            for name, count in category_counter.most_common(12)
        ],
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown(path: Path, payload: dict) -> None:
    templates = payload["templates"]
    summary = payload["summary"]

    lines = [
        "# Notion Marketplace PRD Template Catalog",
        "",
        f"- Search query: `{payload['query']}`",
        f"- Source URL: `{payload['source_url']}`",
        f"- Synced at: `{payload['synced_at']}`",
        f"- Total templates: `{payload['total_templates']}`",
        f"- Free: `{summary['free_count']}`",
        f"- Paid: `{summary['paid_count']}`",
        f"- Official Notion templates: `{summary['official_count']}`",
        f"- Community templates: `{summary['community_count']}`",
        "",
        "## Top categories",
        "",
    ]

    for category in summary["top_categories"]:
        lines.append(f"- {category['name']}: {category['count']}")

    lines.extend(
        [
            "",
            "## Template list",
            "",
            "| # | Template | Creator | Price | Source | Categories | Link |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    for template in templates:
        name = (template["name"] or "").replace("|", "\\|")
        creator = (template["creator_name"] or "").replace("|", "\\|")
        price = template["price_display"]
        source = "Official" if template["official"] else "Community"
        categories = ", ".join(template["categories"][:3]).replace("|", "\\|")
        link = template["url"] or ""
        lines.append(
            f"| {template['index']} | {name} | {creator} | {price} | {source} | {categories} | {link} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Full descriptions and extracted body text live in the JSON catalog.",
            "- Re-run the sync script to refresh counts, prices, and template metadata.",
        ]
    )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Notion Marketplace template search results.")
    parser.add_argument("--query", default="PRD", help="Marketplace search query.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory. Defaults to the skill references directory.",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    output_dir = Path(args.output_dir).resolve() if args.output_dir else script_dir.parent / "references"
    output_dir.mkdir(parents=True, exist_ok=True)

    data = fetch_next_data(args.query)
    page_props = data["props"]["pageProps"]
    templates_raw = page_props.get("templates") or page_props.get("searchTemplates") or []
    templates = [
        normalize_template(index, item)
        for index, item in enumerate(templates_raw, start=1)
    ]

    payload = {
        "query": args.query,
        "source_url": SEARCH_URL.format(query=urllib.parse.quote(args.query)),
        "synced_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "total_templates": page_props.get("totalTemplates", len(templates)),
        "summary": build_summary(templates),
        "templates": templates,
    }

    slug = re.sub(r"[^a-z0-9]+", "-", args.query.lower()).strip("-") or "templates"
    json_path = output_dir / f"notion-{slug}-marketplace-catalog.json"
    md_path = output_dir / f"notion-{slug}-marketplace-catalog.md"

    write_json(json_path, payload)
    write_markdown(md_path, payload)

    print(f"[OK] Synced {len(templates)} templates")
    print(f"[OK] JSON: {json_path}")
    print(f"[OK] Markdown: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate real Markdown links, navigation targets, and the topic SVG assets."""

from functools import cache
from html.parser import HTMLParser
from pathlib import Path
import sys
import tomllib
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class LinksAndIds(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "img" and "src" in attrs:
            self.links.append(attrs["src"])


@cache
def parse(path):
    # Rendering excludes links inside code fences and handles reference-style links.
    rendered = markdown.markdown(path.read_text(encoding="utf-8"), extensions=[
        "extra", "toc", "pymdownx.superfences", "pymdownx.tabbed",
    ])
    result = LinksAndIds()
    result.feed(rendered)
    return result


def navigation_paths(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from navigation_paths(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from navigation_paths(item)


def main():
    errors = []
    pages = sorted(DOCS.rglob("*.md"))
    required = ["index.md", "mission.md", "lessons/index.md", "cheatsheet/index.md",
                "debugging/index.md", "interview/index.md", "references/index.md",
                "references/resources.md", "references/glossary.md"]
    for relative in required:
        if not (DOCS / relative).is_file():
            errors.append(f"Missing portal page: {relative}")
    link_count = 0
    for page in pages:
        for link in parse(page).links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            link_count += 1
            path = unquote(parts.path)
            target = ((DOCS / path.lstrip("/")) if path.startswith("/") else (page.parent / path)).resolve() if path else page
            if not target.is_relative_to(DOCS):
                errors.append(f"{page.relative_to(ROOT)}: link escapes published docs: {link}")
                continue
            if target.is_dir():
                target = target / "index.md"
            if not target.is_file():
                errors.append(f"{page.relative_to(ROOT)}: missing target: {link}")
            elif parts.fragment and target.suffix == ".md" and unquote(parts.fragment) not in parse(target).ids:
                errors.append(f"{page.relative_to(ROOT)}: missing heading: {link}")
    config = tomllib.loads((ROOT / "zensical.toml").read_text())
    for path in navigation_paths(config["project"]["nav"]):
        if not (DOCS / path).is_file():
            errors.append(f"Navigation target is missing: {path}")
    for relative in ["overrides/.icons/custom/github-actions.svg",
                     "overrides/.icons/svgl/github-actions.svg", "docs/assets/github-actions-logo.svg"]:
        try:
            if ElementTree.parse(ROOT / relative).getroot().tag != "{http://www.w3.org/2000/svg}svg":
                errors.append(f"Invalid SVG root: {relative}")
        except (OSError, ElementTree.ParseError) as error:
            errors.append(f"{relative}: {error}")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {len(pages)} Markdown pages and {link_count} local links; {len(errors)} errors.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())

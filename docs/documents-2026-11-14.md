# Privacy and support visual refresh — 2026-11-14

All six English, Simplified Chinese and Japanese privacy/support pages now use the homepage's deep navy, ice-blue and cyan identity. The refresh adds a shared brand header and footer, route-preserving language links, breadcrumbs, numbered sections, desktop section navigation, a native expandable mobile contents list and clear email contact links.

## Content integrity

Every original paragraph was extracted from the previous committed pages into `scripts/document_content.json`. Comparison against Git confirmed that paragraph text and order were preserved verbatim in all six rendered pages. Effective policy dates, service descriptions, fees, retention terms and the support email were not changed. Introductory navigation copy is separate from the original policy/help sections.

The Japanese pages now also include the consistent footer. There are no new forms, trackers, external fonts or JavaScript dependencies. Canonical, locale-alternate and sharing metadata were added.

## Checks

- `scripts/build_documents.py --check` checks all six generated pages against the content source/template; included in the existing deployment validation script.
- `scripts/check_site.py`: nine public pages, document/home metadata, section targets, local assets, cross-language links and static asset allowlist passed.
- Chrome DevTools tested all six documents at 375, 390, 768 and 1440 px (24 layouts): no horizontal overflow or clipped text containers; images loaded; all contents links resolved. Mobile index/desktop sidebar visibility matched the breakpoints.
- Mobile contents expansion and section navigation verified: `#section-02` appeared in view; reduced-motion scrolling was `auto`.
- Support contact points to the existing `mailto:otsgame@yahoo.com`; language links preserve `/support/` or `/privacy/`.
- [Privacy desktop screenshot](screenshots/privacy-zh-desktop.png) and [Support mobile screenshot](screenshots/support-zh-mobile.png) visually reviewed.
- `git diff --check` passed. The three homepages and their assets are unchanged.

## Cache compatibility

An initial browser navigation reused older HTML alongside the freshly edited stylesheet. The new layout therefore ships as `documents.css`; the original `style.css` remains intact for cached legacy pages. New document HTML explicitly loads the new stylesheet. The fresh document render was rechecked after this separation.

## Publishing

Publication uses the existing GitHub Pages workflow and the repository-scoped Kepsley SSH identity. Only `site/` is deployed. Final HTTPS source comparisons and deployment evidence are retained locally under `.preview/`.

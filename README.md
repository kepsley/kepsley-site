# Kepsley website

Independent public website for Kepsley (formerly Linsora).

- Repository: git@github.com:kepsley/kepsley-site.git
- Website: https://www.kepsley.com/
- English: /, /privacy/, /support/
- Simplified Chinese: /zh/, /zh/privacy/, /zh/support/
- Japanese: /ja/, /ja/privacy/, /ja/support/

Only `site/` is published. Never add App source, models, private recordings, API keys or review credentials.

## Preview and checks

```sh
python3 scripts/build_home.py  # after editing localized homepage copy
python3 scripts/build_documents.py  # after editing document copy or layout
python3 scripts/check_site.py
python3 -m http.server 8771 --bind 127.0.0.1 --directory site
```

## GitHub Pages

The independent workflow deploys `site/` on pushes to main or manual dispatch. Enable Settings → Pages → GitHub Actions in **kepsley/kepsley-site**. Configure the custom domain there; Actions deployments do not use a CNAME file as their configuration source.

Before switching App links, verify domain ownership, DNS, the HTTPS certificate and all nine public pages. Set the Pages custom domain to `www.kepsley.com`. In Name.com DNS, set host `www`, type `CNAME`, target `kepsley.github.io`. Apex forwarding is optional and requires its own configuration. Do not change MX or unrelated records. privacy/support subdomains are deferred.

Source upload is not evidence of a live custom domain. DNS and Pages configuration require separate verification.

## Production isolation

The source baseline was read from Linso-site. That repository, its workflow, Pages settings and linsora.icqnft.com remain unchanged. Old App versions continue using the old site. Existing support contact and operator identity are retained.

## Brand homepage

The three homepages are generated at authoring time by `scripts/build_home.py`. Edit the localized content there and regenerate; the public site remains static HTML/CSS/SVG with no JavaScript, external fonts, analytics or forms. Each homepage keeps its introduction button and offers a secondary iOS download link to `https://apps.apple.com/app/id6817633126`, without a fixed storefront or language parameter. `home.css` is isolated from the privacy/support stylesheet.

The 2026-11-14 design positions Kepsley as a personal memory butler. The final palette follows user feedback: deep navy, ice-blue text and cyan accents. All scenes and illustrations are original, explicitly illustrative rather than customer records. `share.svg` is the source for the 1200×630 raster social preview.

See `docs/homepage-2026-11-14.md` for validation and screenshots. Publishing still uses the existing GitHub Pages workflow.

## Privacy and support pages

The six localized documents use the same navy/cyan brand shell with a desktop table of contents and a collapsible mobile index. Their content source is `scripts/document_content.json`; `scripts/build_documents.py` renders the static pages. Update that content source deliberately when changing policy or help text. The visual refresh preserved every original paragraph in order.

`documents.css` styles the new document layout. The original `style.css` remains available so cached copies of older HTML do not receive incompatible new layout rules. Homepage styles remain isolated in `home.css`. Verification: `docs/documents-2026-11-14.md`.

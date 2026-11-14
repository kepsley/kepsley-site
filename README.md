# Kepsley website

Independent public website for Kepsley (formerly Linsora).

- Repository: git@github.com:kepsley/kepsley-site.git
- Intended custom domain: https://kepsley.com/
- English: /, /privacy/, /support/
- Simplified Chinese: /zh/, /zh/privacy/, /zh/support/
- Japanese: /ja/, /ja/privacy/, /ja/support/

Only `site/` is published. Never add App source, models, private recordings, API keys or review credentials.

## Preview and checks

```sh
python3 scripts/check_site.py
python3 -m http.server 8771 --bind 127.0.0.1 --directory site
```

## GitHub Pages

The independent workflow deploys `site/` on pushes to main or manual dispatch. Enable Settings → Pages → GitHub Actions in **kepsley/kepsley-site**. Configure the custom domain there; Actions deployments do not use a CNAME file as their configuration source.

Before switching App links, verify domain ownership, DNS, the HTTPS certificate and all nine public pages. Configure the apex A records using GitHub Pages documentation; optionally point www to kepsley.github.io. Do not change MX or unrelated records. privacy/support subdomains are deferred.

Source upload is not evidence of a live custom domain. DNS and Pages configuration require separate verification.

## Production isolation

The source baseline was read from Linso-site. That repository, its workflow, Pages settings and linsora.icqnft.com remain unchanged. Old App versions continue using the old site. Existing support contact and operator identity are retained.

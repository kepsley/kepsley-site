# iOS download link — 2026-11-17

The English, Simplified Chinese and Japanese homepages retain the primary introduction action and add a secondary outlined download link. All use `https://apps.apple.com/app/id6817633126`, without a fixed storefront or language. Navigation uses plain HTTPS anchors, with no client JavaScript or tracking.

The homepage generator is the source of truth. Static validation now requires exactly one download destination with this app ID on each homepage, while retaining the `#how` introduction link and the prohibition on TestFlight links/forms/iframes. Policy and support pages are unchanged.

Verification:

- `python3 scripts/check_site.py` and `git diff --check` pass; all nine pages remain valid and generated output matches source.
- With the user's approval, an isolated headless Chromium replaced the unavailable Chrome DevTools/browser connection. It did not use a personal browser profile.
- All three languages pass at 320, 375, 390, 768 and 1440 CSS pixels: no horizontal overflow, download targets at least 44 pixels high, language menu clearance, visible keyboard focus and preserved introduction navigation.
- Actual clicks and keyboard Enter request the exact App Store destination. These outgoing requests were intercepted for deterministic navigation tests; they are not evidence of a native App Store installation.
- The initial 320-pixel check found grid minimum sizing forcing the buttons past the right edge. A zero-minimum mobile grid track and shrinkable hero copy fixed it; all 15 combinations passed afterward.
- Apple public lookup returned app ID 6817633126, name Kepsley, version 1.0.3 in Hong Kong and the US; China returned no entry. From this network, both the generic and original Hong Kong web links redirect to the China storefront Today page. Availability and storefront handling remain Apple's behavior; the site does not force a different region or promise availability everywhere.

Local layout evidence and screenshots are retained under ignored `.preview/download-check.json` and `.preview/download-screenshots/`. Publication uses the existing GitHub Pages workflow on main; post-push online verification is recorded separately in `.preview/download-deployment.json`.

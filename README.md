# 배틀 군단 · 원정대 — Web v0.6.8

This folder is a new, independent GitHub Pages deployment handoff for the compiled game.
Authorized public repository: `hikim-0606/battle-legion-expedition-web`.
Generating this folder performs no repository writes or deployment.

The `.part` files contain only the tested compiled Web export. They are each at most
8 MiB to keep each upload small. `artifact-manifest.json` records every part,
archive and output SHA-256. `unpack.py` verifies them and creates `public/`.
This bundle contains no editable Godot source project, user saves, signing keys,
credentials, Android APK, or contents/settings from any existing deployed website.
The compiled PCK contains the game's shipped resources and compiled scripts.

## Authorized deployment handoff

Upload this folder's files to the new repository root on `main`, preserving
`.github/workflows/pages.yml`. Upload only the handoff files; do not upload `public/`
or the original source workspace. Enable Pages with the GitHub Actions source.
The workflow validates and unpacks the parts, then publishes only `public/` using
official GitHub actions. No account credentials belong in this repository.

For local verification, run `python unpack.py` in a separate copy of this folder.
To preview, serve the generated `public/` with a local HTTP server; iPhone use needs
HTTPS. Full iPhone/Safari device testing has not been performed. Browser local saves
belong to that browser and origin; clearing site data removes them. Keep the final
Pages origin and URL stable across version updates. Offline installation requires
the initial complete download and successful service-worker registration.

This is a browser/PWA build, not an iOS App Store app. All original asset notices
remain inside the compiled game pack.

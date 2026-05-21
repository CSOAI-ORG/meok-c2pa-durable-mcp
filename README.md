# MEOK C2PA Durable Content Credentials MCP

> ## 🧱 Part of the MEOK Governance Substrate (£499/mo)
> See [meok.ai/article-50-kit](https://meok.ai/article-50-kit).

# C2PA 2.2 durable Content Credentials — soft + hard binding

<!-- mcp-name: io.github.CSOAI-ORG/meok-c2pa-durable-mcp -->

[![PyPI](https://img.shields.io/pypi/v/meok-c2pa-durable-mcp)](https://pypi.org/project/meok-c2pa-durable-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What this does

C2PA 2.2 (released May 2025) introduced **Durable Content Credentials**: manifests that survive lossy transforms, cropping, screenshotting, AND adversarial removal. The mechanism is a **soft + hard binding** pair:

- **Hard binding** — cryptographic hash inside the manifest (breaks on edit)
- **Soft binding** — perceptual fingerprint + watermark that survives edits

Together they let a verifier conclude *"this image WAS originally credentialed by X, even though the manifest has since been stripped or the image edited"*.

**Nobody else has shipped a C2PA 2.2 MCP yet.** Adobe's tooling lands late 2026. First-mover.

## Tools

| Tool | Purpose |
|---|---|
| `build_durable_manifest(content_hash, mime, claim_generator?, model_id?, ...)` | C2PA 2.2 manifest skeleton |
| `build_soft_binding(image_meta, perceptual_method?)` | Perceptual fingerprint assertion |
| `merge_hard_and_soft(manifest, soft_binding)` | Combine into durable manifest |
| `verify_durable_manifest(asset_meta, manifest, soft_binding?)` | Cryptographic + perceptual verification |
| `list_soft_binding_methods()` | Digimarc, robust pHash, video pdf-hash |
| `sign_cose1_envelope(claim, signer_key_id)` | COSE_Sign1 envelope for embedding |

## Sister MCPs

Part of the MEOK **Governance** + **content provenance** stack:

- `agent-content-watermark-mcp` — EU AI Act Article 50(2) watermark
- `meok-eu-aigc-icon-mcp` — EU Code-of-Practice icon
- `watermarking-authenticity-mcp` — broader C2PA + dispatch
- `agent-incident-relay-mcp` — broadcasts missing-credential incidents

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Pricing

| Option | Price |
|---|---|
| Self-host MIT | £0 |
| Universal PAYG | £29/mo + £0.0002/call |
| Governance Substrate | £499/mo |
| A2A Substrate | £999/mo |
| Defence | £4,990/mo |

Buy: https://meok.ai/governance

## Sources

- [C2PA 2.2 specification (May 2025)](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html)
- [Digimarc Content Credentials integration](https://www.digimarc.com/products/digital-watermarks/content-credentials)

## Wire it up — full stack

This MCP composes with the broader MEOK chain. See [meok.ai/mcp-stack](https://meok.ai/mcp-stack).

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677).

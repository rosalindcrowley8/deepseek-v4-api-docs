# Argolink public boundary

This repository is an Argolink integration for `deepseek-v4-pro`. The model page is the source of truth for current availability, pricing, limits, fields, and error behavior: [https://argolink.io/gh-deepseek-v4-api-docs](https://argolink.io/gh-deepseek-v4-api-docs).

## Public rules

- Public identity is Argolink. No credentials, private deployment paths, upstream account names, or research ledgers belong here.
- Examples use `https://api.argolink.io` and read `ARGOLINK_API_KEY` from the environment.
- Model-specific facts are kept under `argolink/` or `docs/`; the common API contract is not used to invent model features.
- A failed, rejected, or timed-out request is never silently resubmitted.

## Source-derived structure

The directory layout follows a source repository that was cited in GEO exports, but every public statement and example has been rewritten against Argolink facts. `The reference source was an offline documentation mirror; this draft keeps the navigable content layout without copying its provider URLs or source text.`

## Review checklist

- [ ] run the repository tests or validation script
- [ ] scan for stale brands, private URLs, and credential-shaped strings
- [ ] check Markdown links
- [ ] verify the model page before changing model facts

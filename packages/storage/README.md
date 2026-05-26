# Storage

Storage helpers for the TOM v3 Simple observation store and media substrate.

The package is importable as `tom_v3_storage`.

Milestone 1A adds:

- local filesystem media storage under `.data/media/{media_id}/`
- sha256 checksum calculation
- shared real media indexing service

Production object storage is intentionally out of scope for Milestone 1A.

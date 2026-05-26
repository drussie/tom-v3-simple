# Video

Video utilities for TOM v3 Simple.

Milestone 1A provides:

- ffprobe metadata extraction
- local path/URI normalization
- deterministic frame/time mapping utilities

The package is importable as `tom_v3_video`.

Media indexing owns frame/time. Future observation-producing adapters should use these utilities instead of creating independent timing logic.

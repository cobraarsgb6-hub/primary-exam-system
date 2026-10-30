# Plan: 004-content-media-fixes

## Architectural Plan
1. **Grammar Normalizer**: Add `formatSubjectAfterFronted_` helper in `Code.gs` to preserve capitalized proper names after fronted adverbials.
2. **Dynamic Bank Quality**: Ensure historical accuracy in sample dynamic generation (Sputnik 1957).
3. **Frontend Video Linking**: Embed relevant, verified educational video IDs in `CURRICULUM` within `Index.html` with graceful fallback when videos are absent.
4. **Bundle Synchronization**: Run `python bundle.py` to regenerate single-file distribution.
5. **Quality Gate**: Run full regression test suite (48 tests).

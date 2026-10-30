# Tasks: 003-security-privacy

## P2 Gate: Security & Privacy Invariants Tasks

- [x] **T031**: Audit all 37 public RPC endpoints in `Code.gs` and verify strict server-side authorization checks (`isAdminTokenValid_`, `isStudentTokenValid_`).
- [x] **T032**: Confirm entrance model: Gateway PIN backed by salted SHA-256 hashes (`ADMIN_PIN_HASH`, `ALI_PIN_HASH`, `MOSTAFA_PIN_HASH`) with brute-force rate-limiting.
- [x] **T033**: Verify that client-facing question delivery (`publicQuestions_`) strictly strips `correctAnswer` and explanations.
- [x] **T034**: Build dedicated automated security regression test suite (`tests/security.test.js`) covering token forgery, expiration, student isolation, admin protection, and rate limiting.
- [x] **T035**: Integrate security test suite into `package.json` (`npm test`) and achieve 100% PASS (48/48 tests green).
- [x] **T036**: Update Truth Ledger (`CURRENT_STATUS_AR.md`) and roadmap to mark P2 closed.

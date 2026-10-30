# Tasks: 002-live-integration

## P1 Gate: Live Integration & Autonomous Sync Tasks

- [x] **T023**: Verify live Coligo LMS credentials against `https://prod-api.coligolms.com/api/v3/authenticate` (Verified: `ahmed.ibrahim144` with `dbbfd0` links to both Ali and Mostafa).
- [x] **T024**: Update `cloud_coligo_sync.py` to support resilient multi-password candidate authentication (`COLIGO_PASSWORD`, `COLIGO_MOSTAFA_PASSWORD`, `COLIGO_ALI_PASSWORD`).
- [x] **T025**: Update `.github/workflows/coligo-cloud-sync.yml` to pass candidate secrets into the runner environment.
- [x] **T026**: Generate deterministic, secure SHA-256 hashes for all three system PINs (`1990`, `2016`, `2014`) and provide the unified `SYNC_SECRET`.
- [ ] **T027**: Deploy latest `Code.gs` to Google Apps Script as a **New Version** to activate `doPost(e)` and eliminate `Script function not found: doPost`.
- [ ] **T028**: Configure Script Properties in Google Apps Script Editor (`SYNC_SECRET`, `ADMIN_PIN_HASH`, `ALI_PIN_HASH`, `MOSTAFA_PIN_HASH`).
- [ ] **T029**: Configure GitHub Repository Secrets (`COLIGO_USERNAME`, `COLIGO_PASSWORD`, `GAS_WEBHOOK_URL`, `SYNC_SECRET`).
- [ ] **T030**: Execute E2E verification test of webhook ingestion and record in the Truth Ledger.

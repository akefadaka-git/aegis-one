# AEGIS ONE — A2 External Dependency and Android Capability Reconciliation

**Record:** AEGIS-A2-RECON-001  
**Version:** 0.1.0  
**Date:** 2026-11-12  
**Status:** PARTIAL — read-only reconciliation; A2 closure not proposed  
**AEGIS repository:** `akefadaka-git/aegis-one`  
**IROKA repository baseline:** `main` at `1a6f30cc3e64b8551f8e725c4cad8fcc3fa2c472`

## 1. Scope and evidence standard

This record reconciles the AEGIS A2 baseline against the current IROKA dependency candidates and the Android/Samsung platform constraints. It is documentation and evidence reconciliation only. It does not modify IROKA, implement AEGIS application code, provision keys, enroll or configure a handset, activate VPN/lockdown, or authorize merge, release, deployment, or A5.

A branch or passing CI run is evidence only for the exact source revision and tests actually executed. A test-adapter pass is not production-provider assurance. A feature branch is not a canonical dependency merely because it exists or is ahead of `main`.

## 2. AEGIS PR #1 — CI interpretation

PR: https://github.com/akefadaka-git/aegis-one/pull/1

Original PR workflow run [43126436817](https://github.com/akefadaka-git/aegis-one/actions/runs/43126436817) completed successfully. Its job checked out GitHub's synthetic PR merge ref and ran at merge commit `9370104168e13b82d8a4187ce39f26f73f7eb232`, which merged source head `773972aafca38670bcb9e353e2f7f097db5fa9c8` into base `94d95d4c9a6a47a444ced56708b66fb9f2cba215`. The validator passed, but this was a PR merge-ref check, not a strict source-head-only check.

The workflow was corrected to check out `github.event.pull_request.head.sha` for pull-request events and `github.sha` for push/manual events. The corrected workflow passed on exact source head `528bf95dcda950850f0d64f927a80550874f6c39` in both [push run 43126909777](https://github.com/akefadaka-git/aegis-one/actions/runs/43126909777) and [pull-request run 43126917577](https://github.com/akefadaka-git/aegis-one/actions/runs/43126917577). Both runs completed successfully. The PR run log explicitly checked out `528bf95` and printed `DOCUMENTATION VALIDATION: PASS`.

The validator expansion at `04f69e27859228eb2234287db2e786d26e75b914` first failed because the reconciliation document did not explicitly enumerate all binding ODR exclusions. The report was corrected to include all four exclusions and all four deferrals, and the validator now checks three documents, including this reconciliation record.

**Final exact-head CI at `b65159f50d8bd7a817af47f95fbcfbb70427f1da`: PASS.** Push run [43127082664](https://github.com/akefadaka-git/aegis-one/actions/runs/43127082664) and PR run [43127092137](https://github.com/akefadaka-git/aegis-one/actions/runs/43127092137) both completed successfully, checked out exactly `b65159f`, and printed `DOCUMENTATION VALIDATION: PASS` / `Validated 3 documents and all required governance markers.` This is structural documentation validation, not implementation, Android behavior, or security assurance. The PR had no submitted reviews or inline review threads at the time of inspection. It remains draft and unmerged.

## 3. IROKA dependency reconciliation

Reviewed IROKA `main` at `1a6f30cc3e64b8551f8e725c4cad8fcc3fa2c472`, plus the named feature branches below. None of these feature branches is merged into IROKA `main` by this record.

### 3.1 G01 — identity, tenant context and reviewer proof

**Evidence**
- Branch `feat/a3-8-g01-tenant-reconciliation`, current HEAD `c57e4298005222ce476f685972062983c78d626f`.
- Implementation commit `334a7113eb189b04ff3b1bdcf11909adc301da5d`; subsequent two commits on that branch are documentation-only.
- GitHub Actions run [42951439361](https://github.com/akefadaka-git/iroka/actions/runs/42951439361) checked out the implementation commit and passed formatting, compilation, the no-default-features safeguard, 139 tests, and Clippy.
- `crates/iroka-kernel/src/reviewer_proof.rs` defines domain-separated JCS Ed25519 proofs, exact scope binding, a maximum 300-second proof lifetime, a 30-second key-binding freshness limit, current credential/key revocation checks, and one-time proof consumption.
- `crates/iroka-kernel/src/tenant.rs` resolves an opaque `TenantContext` from a verified principal and Owner-provisioned membership, with an explicit freshness bound.

**Disposition: PARTIAL.** The cryptographic code and deterministic tests are verified at the cited implementation commit. The authoritative issuer-side `ReviewerKeyBindingResolver` still requires a real provider and independent review. Tenant membership uses a SQLite single-node adapter; no multi-node consistency guarantee is established. A verified login or tenant membership does not by itself prove reviewer designation or approval of a particular record.

### 3.2 G02 — Owner and organization authority

**Evidence**
- Branch `feat/a3-8-g02-owner-organization-authority`, HEAD `31dd1cff9ab48c7ecedb941e920281f5e1924051`; comparison with current `main`: 49 commits ahead, 0 behind.
- Owner-selected model A is documented in `docs/architecture/G02-OWNER-GOVERNED-ORGANIZATION-AUTHORITY-CONTRACT-v0.1.0.md`: G02 must be the sole canonical source for organization creation, appointment, scoped delegation, suspension/reactivation, and revocation using Owner-signed versioned commands.
- The inspected `OwnerSecurityAction` currently contains credential revocation, signing-key revocation, and approval revocation. It does not contain organization creation or organization-delegation designation/revocation actions.
- G05's `G02AuthorizationAuthority::authorize_organization_scope` has a default DENY implementation. The inspected `KernelG02AuthorizationAdapter` implements global G05 capability authorization but does not override that organization-scope method.
- The G02 branch contains the authority contract and readiness decision, but no verified organization-authority provider implementation or exact-head CI evidence was established.

**Disposition: MISSING / FAIL-CLOSED.** The authority model is decided; the provider is not implemented or verified. Global capability authorization, tenant membership, Owner approval, and reviewer designation must not be conflated. Until the canonical G02 provider exists, organization-scoped reviewer designation and revocation must remain denied. Family/guardian authority is also a separate domain: enterprise organization roles must not be reused as guardian/child authority. AEGIS still needs an explicit guardian relationship, delegated caregiver scope, child-appropriate consent, revocation, emergency-contact and age/ownership transfer contract.

### 3.3 G05 — memory approval integration and the local designation conflict

**Evidence**
- Branch `feat/a3-8-g05-verified-reviewer-integration`, current HEAD `10aca6e4fc5ed3a85d7218d6473f72f0c155d154`; comparison with `main`: 214 commits ahead, 0 behind.
- The tested implementation commit is `5dd6ca77afab958b01b0d9009dbb71ff32f05342`; the branch is one documentation-only commit ahead of that implementation.
- GitHub Actions run [42957553177](https://github.com/akefadaka-git/iroka/actions/runs/42957553177) checked out exactly `5dd6ca77afab958b01b0d9009dbb71ff32f05342` and passed formatting, workspace/all-target compilation, the no-default-features safeguard, 141 tests, and Clippy.
- The integrated G01 reviewer-proof type carries private fields for reviewer/key/designation, memory/record/digest, purpose/classification and approval scope. G05 compares those fields against its canonical memory and pending approval envelope.
- However, `crates/iroka-g05-memory/src/registry.rs` creates and writes a `g05_reviewer_designations` table. Its `designate_reviewer` and `revoke_reviewer_designation` methods call G02 authorization and G01 key-binding validation, then persist local designation records. The activation path later resolves the active designation from that G05-local table.
- G02's binding Owner decision says G02 is the sole canonical organization-authority provider and G05 must not maintain a competing organization-role registry. No signed G02 designation receipt, canonical G02 lookup, or projection-freshness/consistency contract was established in the inspected implementation.
- G01 proof consumption and G05 approval consumption occur in separate SQLite transactions. A failure between them is fail-closed but may require a new proof; there is no cross-database atomicity.

**Disposition: PARTIAL / UNRESOLVED INTEGRATION CONFLICT.** The cryptographic reviewer-proof and G05 approval-consumption path pass deterministic tests, but the local designation table is not proven to be a read-only projection of G02 authority. It must not be treated as canonical. Reconcile it to a G02-issued, versioned, revocable authority result and define how G05 detects stale/revoked designations before A3.8 can close. Do not accept the passing 141-test run as proof that the G02 provider exists.

### 3.4 G11 — memory lifecycle audit

**Evidence**
- The G05 integration candidate adds a separate `iroka.g11.memory-lifecycle-event` schema, append-only SQLite table, independent SHA-256 chain, event-ID idempotency, and a G05 transactional outbox adapter.
- The G05 run [42957553177](https://github.com/akefadaka-git/iroka/actions/runs/42957553177) includes the G11 code and its deterministic tests.
- The G11 memory lifecycle stream is separate from the existing G11 decision audit stream. The payload omits memory content and content digest.
- Outbox delivery is retryable and idempotent, but G05-to-G11 delivery is not a distributed transaction. SQLite is single-node only.
- Earlier G11 candidate commit `3311627c162156898cb6bf76ac6a072edc93b653` had no associated workflow run in the inspected evidence; do not use that historical commit as the current G11 verification head.

**Disposition: PARTIAL.** The separate event schema/outbox adapter has deterministic CI evidence as part of the G05 integration candidate. Cross-database atomicity, multi-node durability, external witness anchoring, and independent A4 assurance remain unverified.

### 3.5 G08 — durable orchestration

**Evidence**
- Branch `architecture/g08-orchestration-a2-contract`, HEAD `04c3bab0ba4de2e634ce28612c90ed7451ef9ceb`.
- Compared with current `main`: **diverged**, 3 commits ahead and 299 behind; merge base `143311a655be68acea2700650b7f88c9fb085526`.
- The branch contains an A2 contract draft only. It explicitly excludes execution grants, G09 side effects, distributed queue, multi-region operation, and production deployment. It still records Owner disposition and interface reconciliation as pending.
- The contract's referenced repository baseline is stale relative to current `main`.

**Disposition: UNRESOLVED / NOT ADOPTABLE.** Do not stack AEGIS work on this divergent branch or claim it is a current canonical orchestration dependency. A separate lineage reconciliation is required before any future integration.

### 3.6 G09 — constrained execution

**Evidence**
- Branch `feat/coding-intelligence-c1-5-sandbox`, HEAD `394226c48cc21339906816d123837b8ab3622400`; 111 commits ahead of current `main`, 0 behind.
- GitHub Actions run [42690239677](https://github.com/akefadaka-git/iroka/actions/runs/42690239677) checked out that exact commit and passed formatting, compilation, the no-default-features safeguard, 133 tests, and Clippy.
- The code is a repository/workspace coding sandbox with scoped execution grants and bounded Linux command execution. It is not an Android device-management or mobile command protocol.
- No exact target-device execution adapter, Android command authorization schema, or verified on-device execution evidence was found.

**Disposition: PARTIAL / NOT AN AEGIS DEVICE CONTROL PROVIDER.** Reuse only the general constrained-execution concepts where appropriate. AEGIS requires its own separately authorized, device-bound command protocol, capability allowlist, expiry/replay controls, user/Owner consent semantics, local policy enforcement, and auditable response handling.

## 4. Android and Samsung capability reconciliation

### 4.1 Separate the three deployment profiles

1. **Personal app profile:** ordinary Android application permissions and user-consented APIs. It can protect its own app data and vault, provide app-level lock and local threat signals, and use a user-approved `VpnService`. It cannot globally inspect every other app's private storage or intercept all Android file operations.
2. **Profile Owner / Work Profile:** enterprise control is scoped to the managed work profile. ODR-016 defers this integration; do not include it as an assumed v1 capability.
3. **Device Owner / fully managed device:** supported Android Enterprise policies can control a company-owned fully managed device. Enrollment is a privileged provisioning step and remains separately unauthorized.

### 4.2 Samsung Knox gate

Samsung's Knox SDK documentation states that on Android 15 or later, full Knox SDK feature access requires the app to be the AE Device Owner of a fully managed device or the Profile Owner of a work profile. The target handset is reported as Android 16, so full Knox SDK access cannot be assumed in the ordinary personal-app profile. Some ISV APIs have narrower exemptions; each API must be checked individually.

Knox access is permission- and license-dependent. Development and commercial license types, app association, license activation, product entitlements and device compatibility are distinct checks. An account or generic license reference does not establish access to every Knox API. The exact Knox product, license type, app association and API entitlement remain unverified.

### 4.3 VPN and traffic visibility

Android Enterprise supports always-on VPN and lockdown for managed devices or profiles under the applicable Device Owner/Profile Owner management mode. A work-profile VPN does not route traffic from personal-profile apps. A personal-profile VPN is subject to Android user consent and routing constraints. Do not promise universal inspection of encrypted third-party traffic; ODR-032 explicitly excludes that capability.

### 4.4 Device evidence still outstanding

The Samsung Galaxy A16 (SM-A165F) evidence remains screenshot-observed, not independently interrogated. The following are still **UNKNOWN** or **NOT TESTED**: bootloader lock state, Verified Boot state, Keystore security level, StrongBox availability, attestation-chain validity, Device Owner eligibility, Knox product/license entitlement, VPN lockdown behavior, and emergency background execution.

No diagnostic app installation, factory reset, Device Owner/Profile Owner enrollment, setting change, bootloader/firmware change, VPN configuration, or lockdown activation is authorized by this record.

## 4.5 Binding Owner Decision Register constraints

The authoritative source remains `AEGIS-A2-ODR-001 v1.1` and Architecture Amendment v1.3. The repository's Owner Decision Register file is a reference summary, not a replacement for the complete 47-decision source. Preserve every condition and rationale in the authoritative version.

**Excluded**
- **ODR-017:** absolute prevention of AEGIS ONE app removal.
- **ODR-023:** global interception of all Android file operations.
- **ODR-032:** universal inspection of encrypted third-party traffic.
- **ODR-045:** AI-authorized irreversible actions.

**Deferred**
- **ODR-012:** automatic software-backed security fallback.
- **ODR-016:** Profile Owner / Work Profile integration.
- **ODR-036:** camera capture on suspicious activity.
- **ODR-038:** remote data wipe.

These dispositions are binding constraints on the capability matrix and any future implementation plan. A platform API that technically offers a related capability does not override an Owner exclusion or deferred decision.

## 5. Consolidated A2 finding register

| ID | Domain | Status | Closure evidence required |
|---|---|---|---|
| A2-R01 | AEGIS PR exact-head CI | **PASS** at `b65159f50d8bd7a817af47f95fbcfbb70427f1da` | [Push run 43127082664](https://github.com/akefadaka-git/aegis-one/actions/runs/43127082664) and [PR run 43127092137](https://github.com/akefadaka-git/aegis-one/actions/runs/43127092137); both checked out exact head and validated all 3 documents. |
| A2-R02 | G01 issuer reviewer-key binding | **PARTIAL** | Real authoritative resolver, revocation freshness evidence, independent review |
| A2-R03 | G02 organization authority | **MISSING / FAIL-CLOSED** | Owner-signed canonical organization/delegation provider and adversarial tests |
| A2-R04 | G05 local designation table | **UNRESOLVED CONFLICT** | G02 canonical source integration; no G05-owned competing authority; stale/revoked projection tests |
| A2-R05 | G11 memory lifecycle audit | **PARTIAL** | Outbox recovery tests, independent A4 review, explicit single-node limits or qualified shared store |
| A2-R06 | G08 orchestration lineage | **UNRESOLVED** | Reconcile 3-ahead/299-behind divergent branch and stale baseline |
| A2-R07 | G09 device execution boundary | **MISSING for AEGIS device control** | AEGIS-specific device command contract and device-bound tests |
| A2-R08 | Android/Knox capabilities | **PARTIAL / UNKNOWN** | Per-API model/API/license matrix and separately authorized device evidence |
| A2-R09 | Offline/emergency execution | **NOT TESTED** | Background/force-stop/reboot/offline test plan and authorized device test |
| A2-R10 | Cross-domain assurance | **NOT RUN** | Independent A4 review and adversarial end-to-end provider-failure matrix |
| A2-R11 | Family/guardian authority | **MISSING** | Owner-approved guardian/child relationship, scoped caregiver delegation, consent, revocation and emergency authority contract |

## 6. A2 closure decision

**A2 is NOT READY FOR CLOSURE.** The documentation baseline and some IROKA candidate code have passing deterministic CI, but the G02 canonical organization-authority provider is missing, the G05 local designation store conflicts with the Owner-selected authority boundary, G08 is divergent, and AEGIS-specific Android/Knox/device-command capabilities remain unverified.

A2 closure must wait for:
1. Corrected AEGIS PR workflow evidence proving checkout of the exact source head.
2. A reconciled G01/G02/G05/G11 authority and audit dependency contract, including a resolution of the G05 local designation table.
3. A G08 adoption decision based on a reconciled current branch lineage, or an explicit decision not to depend on G08.
4. AEGIS-specific G09/device command boundary specification.
5. A per-device Android/Knox capability matrix that preserves all exclusions and deferred decisions.
6. An explicit finding for every remaining unknown, with evidence, a bounded limitation, or a formally recorded deferral.

No A3 implementation, IROKA merge, AEGIS merge, device enrollment, privileged configuration, signing, release, deployment, or A5 activation is authorized by this reconciliation.

## 7. Authoritative platform references

- [Samsung Knox SDK — Android 15+ Device Owner/Profile Owner requirement](https://docs.samsungknox.com/dev/knox-sdk/)
- [Samsung Knox SDK — license types and activation](https://docs.samsungknox.com/dev/knox-sdk/introduction/about-licenses/)
- [Samsung Knox SDK — license FAQ and API permissions](https://docs.samsungknox.com/dev/knox-sdk/faq/licensing/)
- [Android Enterprise — DPC networking and always-on VPN](https://developer.android.com/work/dpc/network-telephony)
- [Android Enterprise — managed device and Work Profile data/policy scope](https://support.google.com/work/android/answer/7502354)

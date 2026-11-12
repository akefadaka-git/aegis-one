# AEGIS ONE — A2 Architecture Baseline

**Status:** Draft baseline for Owner review; not an implementation authorization  
**Version:** 0.1.0  
**Repository:** `akefadaka-git/aegis-one`  
**Governance:** Owner-governed; stage-gated

## 1. Purpose and scope

AEGIS ONE is an Android security and protection platform powered by IROKA. This document establishes a traceable architecture starting point for assessment and reconciliation. It is documentation only: it does not authorize device enrollment, privileged configuration, code implementation, signing, release, merge, deployment, or production activation.

The platform is intended to support personal devices, family protection, enterprise-managed fleets, multiple devices, and offline emergency protection. The design must remain honest about Android API, OEM, model, license, and user-consent boundaries.

## 2. Architecture principles

1. **Owner authority is explicit.** Owner-governed changes and consequential operations require a verifiable authorization path.
2. **Least privilege.** Use ordinary application permissions where sufficient; use Device Owner or Knox capabilities only on eligible, deliberately provisioned devices.
3. **Fail closed for trust.** Invalid, expired, revoked, replayed, or incorrectly scoped authorization must not grant access.
4. **Offline resilience.** Essential local protections and emergency workflows must remain bounded and useful without network access.
5. **Deterministic enforcement.** AI may classify, explain, and recommend. Deterministic policy and explicit authorization govern consequential actions.
6. **Evidence before claims.** Device capabilities, security properties, and test coverage are reported only when supported by reproducible evidence.
7. **Privacy by design.** Minimize collection, protect sensitive data cryptographically, and make monitoring scope visible.
8. **Amharic-first localization.** Amharic is a first-class language; English is also supported. Localization must cover security messages, recovery, accessibility, dates, and help content.

## 3. Deployment profiles

### 3.1 Personal device profile

A consent-based Android application. Candidate capabilities include local threat detection, app-level lock, encrypted local vault, privacy controls, and an Android `VpnService` where the user explicitly grants VPN consent. This profile does not imply global visibility into other applications or the Android filesystem.

### 3.2 Dedicated managed-device profile

A separately provisioned enterprise profile using Android Enterprise Device Owner controls and supported Samsung Knox capabilities where the exact device, OS/API level, Knox SDK, license, and policy permit them. Provisioning and activation require separate Owner authorization and a tested rollback/recovery plan.

### 3.3 Shared platform services

Shared services include cryptographic identity and trust, policy distribution, device inventory, family/enterprise tenancy, encrypted storage metadata, threat intelligence, incident coordination, audit evidence, and IROKA integration. Online services must not be prerequisites for local emergency behavior.

## 4. Logical component boundaries

- **Identity and trust:** Owner identity, device identity, credential lifecycle, key binding, attestation evidence, revocation, and recovery.
- **Authority and tenancy:** Separate personal, family, enterprise, operator, and Owner authority domains. No implicit elevation between them.
- **Device management:** Enrollment state, device posture, supported policy capabilities, inventory, and lifecycle.
- **Personal security:** App-level protections, local threat signals, privacy controls, and user-consented permissions.
- **Family protection:** Guardian/child relationships, age-appropriate policy, transparent controls, emergency contacts, and auditable delegation.
- **Enterprise management:** Organization-scoped administration, fleet policy, compliance posture, and administrator delegation.
- **Secure vault:** Authenticated encryption, key separation, protected file/folder metadata, backup/recovery design, and access audit.
- **Threat defense:** Malware and potentially unwanted application signals, phishing protection, risk scoring, and explainable alerts.
- **Network defense:** User-consented VPN, DNS filtering, network anomaly signals, and explicit limitations for encrypted traffic inspection.
- **Offline emergency:** Local emergency contacts, bounded response workflow, durable local event queue, and safe recovery.
- **Execution control:** Explicitly authorized, constrained operations; no AI-only authority for irreversible actions.
- **Audit and assurance:** Tamper-evident event records, privacy-preserving evidence, synchronization status, and verification.
- **IROKA integration:** Policy, intelligence, orchestration, and reporting interfaces with authenticated, scoped, revocable requests.
- **Android/Knox adapter:** Capability detection and versioned adapters; unsupported capabilities must report unavailable rather than simulate success.

## 5. Android capability boundaries

An ordinary Android application cannot globally intercept every file operation, inspect another app's private storage, or replace the system lock screen. Device Owner APIs provide supported enterprise controls, not unrestricted operating-system control. Deeper global visibility requires supported OS/OEM integration and must be proven for each target device.

A VPN-based network layer is constrained by Android's VPN consent model and routing behavior. Universal inspection of encrypted third-party traffic is not a platform assumption. VPN lockdown can disrupt connectivity and must not be activated without explicit authorization, compatibility testing, and a recovery path.

Preventing removal of the AEGIS ONE application absolutely is not a design guarantee. Camera capture on suspicious activity, remote wipe, Profile Owner/Work Profile integration, and automatic software-backed security fallback remain deferred as recorded in the Owner Decision Register.

## 6. Security architecture requirements

- Use platform-backed cryptographic APIs and hardware-backed keys when demonstrably available; record the actual security level.
- Separate identity keys, vault keys, transport credentials, and audit-integrity keys.
- Define key rotation, revocation, recovery, backup, and compromise response before production use.
- Bind authorization to principal, device, scope, action, expiry, and unique request identifier; reject replay.
- Require authenticated and integrity-protected policy updates; preserve last-known-good policy with bounded expiry.
- Store the minimum necessary telemetry; do not place vault contents, secrets, or unnecessary personal data in audit events.
- Define secure update provenance, rollback protections, vulnerability response, and independent security review.
- Treat attestation as evidence with freshness and verifier requirements, not as a boolean assertion.

## 7. Owner Decision Register constraints

The binding decision source is **AEGIS-A2-ODR-001 v1.1** (47 decisions) and its **Architecture Amendment v1.3**. This baseline does not replace, reinterpret, or expand that register.

The following exclusions remain binding:

- **ODR-017:** Absolute prevention of AEGIS ONE app removal — excluded.
- **ODR-023:** Global interception of all Android file operations — excluded.
- **ODR-032:** Universal inspection of encrypted third-party traffic — excluded.
- **ODR-045:** AI-authorized irreversible actions — excluded.

The following items remain deferred and are not silently included in implementation scope:

- **ODR-012:** Automatic software-backed security fallback.
- **ODR-016:** Profile Owner / Work Profile integration.
- **ODR-036:** Camera capture on suspicious activity.
- **ODR-038:** Remote data wipe.

All other conditional approvals retain their original conditions. If the authoritative register is amended, this baseline must be reconciled against that version before implementation.

## 8. Device evidence baseline

The initial target handset is Samsung Galaxy A16, model SM-A165F. Previously supplied screenshots indicate Android 16, One UI 8.5, and Knox 3.13 / Knox API 40. These are screenshot-observed values, not independent runtime verification.

The following remain **UNKNOWN** or **NOT TESTED** until supported diagnostic evidence is collected under a separately authorized procedure: bootloader lock state, Verified Boot state, Keystore security level, StrongBox availability, attestation-chain validity, Device Owner eligibility, VPN lockdown behavior, and emergency background execution. Knox product/license entitlement also remains unverified. No diagnostic application installation, enrollment, reset, or device-setting change is authorized by this document.

## 9. Stage gates and non-authorizations

- **A1 — Assessment/specification/freeze:** establish requirements, threat model, scope, and authoritative decisions.
- **A2 — Read-only reconciliation:** compare the architecture and contracts with authoritative sources; record gaps and conflicts.
- **A3 — Implementation:** requires explicit Owner authorization after A2 closure.
- **A4 — Verification:** exact-head tests, security review, and evidence reconciliation.
- **A5 — Deployment:** separate explicit authorization; never implied by A4.

This repository baseline and its documentation validation do not close A1/A2, authorize A3, or authorize merge/deployment. Preserve existing work and all recorded exclusions and deferrals.

## 10. Open reconciliation items

1. Establish a canonical device identity and attestation contract distinct from user/Owner identity.
2. Define separate personal, family, enterprise, and Owner authority models.
3. Specify offline authorization, revocation freshness, and emergency behavior.
4. Reconcile IROKA G01/G02/G05/G08/G09/G11 contracts before depending on them.
5. Define the AEGIS-specific device-command protocol; do not reuse a general coding sandbox as a mobile command interface.
6. Define offline audit queue integrity, deduplication, synchronization, and loss reporting.
7. Verify Samsung Knox SDK product/license/API entitlements for the target model.
8. Produce a capability matrix by Android API level, device model, and management profile.

## 11. Acceptance evidence required

A future A2 closure record must identify the exact source references and commit heads reviewed, all findings and dispositions, unresolved risks, authoritative Owner decisions, and the exact document commit. A future A4 record must identify exact-head CI results, test coverage, device/API matrix, independent security review, and reproducible evidence. No status is PASS or VERIFIED-CLOSED merely because this document exists.


## 12. Current dependency reconciliation

The current read-only evidence record is [IROKA and Android A2 Reconciliation](../reconciliation/IROKA-ANDROID-A2-RECONCILIATION.md). It supersedes the generic status of the open items in Section 10 with a versioned finding register and exact IROKA source references.

The reconciliation remains **PARTIAL** and A2 is **NOT READY FOR CLOSURE**. In particular, the G02 canonical organization-authority provider is missing, G05's local reviewer-designation table is not reconciled with the Owner-selected G02 authority model, G08's candidate branch is divergent, and AEGIS-specific Android/Knox/device-command capabilities remain unverified.

No A3 implementation or privileged device operation is authorized by this baseline.

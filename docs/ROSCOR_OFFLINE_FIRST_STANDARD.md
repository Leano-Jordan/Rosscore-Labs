# Rosscore Labs — Offline-First and Disconnected-Operation Standard

**Status:** Canonical company-wide standard  
**Authority:** Founder → Ross (Company Director) → Project Director → assigned specialist  
**Applies to:** Every Rosscore Labs product, technical specification, implementation, test plan, release assessment, demo and customer-facing claim.

## 1. Purpose

“Offline” is a user-visible operating capability, not a synonym for caching files, installing a shortcut, having a local-network connection, or hiding an error page.

Rosscore products have different requirements. The project Director must declare each product's intended operating modes and supported offline workflows. This standard makes the terms, evidence, and claim boundaries consistent across the company; it does not silently impose identical product scope on every repository.

## 2. Canonical definition

A feature is offline-capable only within a clearly declared scope where the required interface, data and operation remain usable without the network or host dependencies named in that scope.

For an **offline-first product**, internet or cloud service must enhance everyday operation rather than gate its core, declared local workflows. Losing connectivity must not silently discard saved work, corrupt data, or present an online-only operation as successful.

Unless the product contract explicitly says otherwise, “works offline” means:
- the installed application can launch after a full close/reopen;
- the supported interface and navigation are available locally;
- supported local reads and writes do not depend on a reachable remote server;
- saved changes survive reload/restart and have clear local/pending state;
- reconnecting safely reconciles queued work without silent loss or duplicate consequential actions.

A product may label a capability **cached/read-only offline**, **device-local offline**, **local-network-only**, or **online-only**. These are different capabilities and must not be sold as equivalent.

## 3. The five operating modes

1. **Online/cloud:** remote service is reachable; local cache may improve speed but does not imply offline support.
2. **Cached/read-only offline:** a previously downloaded shell, assets or pages can render locally. Unsupported writes and missing pages remain unavailable. This is not full offline operation.
3. **Device-local offline:** the app, supported data and workflows run on the user's device without a separate PC/server or internet.
4. **Local-host/network:** a PC or local host serves other devices over a local network or hotspot. This may work without internet, but it is **not device-independent**; clients still depend on that host being available.
5. **Connected synchronization:** local changes are reconciled with a trusted host/cloud when connectivity returns. Sync is a separate capability, not proof that all features work offline.

Project contracts must identify which modes are implemented and which are targets. Never use a vague “offline” label where a more precise label is required.

## 4. Delivery architecture must match the claim

- A browser-installed PWA requires a supported secure origin for service-worker installation—normally HTTPS; local loopback is a development exception. Plain HTTP on a normal LAN IP (for example, `http://192.168.x.x:port`) is not a valid secure PWA install origin.
- A PWA installed from HTTPS can still depend on its server for server-rendered pages, business data, form submissions, assets or authentication. A service worker does not turn those dependencies into a self-contained app automatically.
- A local Laravel/PHP development server is a host dependency. A phone opened to that server cannot reach it when the server is stopped or the route/network is unavailable.
- If the product promise requires independence from both internet and the user's PC, choose and implement a delivery/data architecture that can satisfy it: for example a complete device-local web app/PWA data layer, a packaged application, or another explicitly justified design.
- Static assets, a cached landing/dashboard page, or a generic fallback screen do not count as full UI and workflow parity.

## 5. Required project-level offline contract

Every project that requires offline operation must document, in its own repository:

- target devices and supported delivery/install route;
- whether the product is offline-first or online-first;
- the exact screens, records, attachments and mutations supported offline;
- which features are read-only, device-local, local-host-dependent or online-only;
- local persistence, pending queue, retry/idempotency and conflict behaviour;
- expected behavior on close/reopen, storage failure, host failure, app update and reconnect;
- data ownership, business isolation, backup/export and recovery expectations;
- known gaps and the evidence required to close them.

Company-level policy belongs in the Rosscore Labs repository. Product-specific implementation state, tests, decisions and acceptance evidence belong in that product's repository. Do not duplicate this policy into competing contracts; link to it and add only product-specific requirements.

## 6. Acceptance test — required for offline-first claims

For each supported device/delivery path, execute the following after a successful connected installation and initial data preparation:

1. Close the app fully; disable Wi-Fi and mobile data; make any required PC/server unavailable.
2. Launch from the installed app icon, not a remembered URL that depends on a dev server.
3. Traverse every declared core offline screen and navigation path.
4. Read locally available business records and perform each declared offline mutation.
5. Reload, force-close and reopen; verify the saved changes remain and pending work is visible.
6. Verify that file/attachment claims match what is actually stored locally.
7. Restore connectivity and verify safe reconciliation, retries, idempotency, rejected changes and conflict handling.
8. Repeat after an app restart/update scenario where the release changes the service worker or local schema.

Record device/browser/OS, installation origin, exact build/commit, connectivity/host state, steps, observed outcomes and failures. Automated tests are required, but code assertions and green CI alone do not prove physical-device offline operation.

## 7. Evidence vocabulary

Use these labels consistently:

- **OBSERVED:** directly seen in source, tool, runtime or test output.
- **IMPLEMENTED:** the change exists in the identified commit.
- **TESTED:** the relevant check actually ran and passed.
- **VERIFIED:** evidence supports the intended behavior at the named layer.
- **PROVEN:** repeated realistic or recovery-grade evidence supports the operational claim.
- **INFERRED:** reasoned conclusion that is not directly observed.
- **UNKNOWN:** evidence is insufficient.
- **BLOCKED:** an external dependency or owner decision prevents safe progress.

A narrower passing check cannot close a broader requirement. A documentation update cannot upgrade implementation maturity. Never convert a hypothesis or failed launch screenshot into a proven root cause without the matching evidence.

## 8. Failure and loop prevention

Project Directors must:
- inspect current repository state and existing failure records before repeating a diagnosis;
- assign one owner/specialist per bounded workstream;
- keep one source of truth and one acceptance authority;
- classify failures by application, test/contract, data/fixture, environment/runtime, CI, tooling, contract drift or nondeterminism;
- preserve failed hypotheses and stop repeating the same cache-only or assertion-only patch without new evidence;
- record the changed commit and the exact verification result before reporting progress;
- leave unsupported features marked unavailable rather than silently pretending success.

When the same boundary repeatedly fails, escalate to architecture/forensics instead of creating another parallel backlog or repeating the same correction.

## 9. Customer-facing truth

A product page, proposal or demo must state offline capabilities at the evidence level actually achieved. Never equate installability with offline usability, cached assets with offline workflows, local-network mode with host independence, or automated tests with device proof.

Distinguish current capability from roadmap intent. A limitation must be disclosed before it can materially affect a purchasing decision. Project Directors inherit both this rule and the Rosscore Labs client-facing identity standard.

## 10. Authority and precedence

This is the single canonical company definition of offline terminology and proof requirements. Every Project Director must consult it. Product-specific architecture documents may define stricter acceptance gates, but may not contradict these definitions or claim unsupported capability.

Founder instructions remain highest authority. The Company Director coordinates portfolio-level consistency; the owning Project Director remains responsible for implementation and acceptance inside its repository.

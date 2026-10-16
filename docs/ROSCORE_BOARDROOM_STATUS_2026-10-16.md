# Rosscore Labs — Boardroom Status
**Review date:** 2026-10-16  
**Scope:** Company portfolio, repositories, current GitHub Actions evidence, release risks and monetisation readiness.  
**Evidence boundary:** GitHub evidence can establish code/repository activity and recorded verification. It does not establish bank balances, revenue collected, customer contracts or active sales conversations unless those are recorded in the company systems.

## Executive assessment

Rosscore Labs has a real software and website portfolio, but the inspected company records do not yet give a dependable view of revenue, sales pipeline, customer commitments or delivery capacity. Those commercial figures are **UNKNOWN**, not assumed to be zero.

The company is still carrying a meaningful gap between building products and proving they are ready to sell and operate. The immediate strategy should combine a narrow, paid website implementation offer with release-hardening of the two declared core products. Avoid spreading solo-developer time equally across every product.

## Portfolio status

| Asset | Observed state | Commercial decision / next gate |
|---|---|---|
| **Zazu EMP** | Active event/catering operations platform with substantial connected workflows. The 2026-10-16 Director audit explicitly says **release not certified**. Latest main push and associated quality/security runs include successful checks, but they do not prove full offline use or recovery. Open issues #34 and #35 focus on standalone phone-local offline launch and verified sync acceptance. | Keep as a core product. Prove the installed phone works with the PC/server and internet unavailable; then test restart persistence, queued changes, reconciliation and backup/restore. Do not launch a lifetime deal before those gates and legal/brand clearance are resolved. |
| **Swift Order** | POS, stock, suppliers, purchase orders, receiving, invoicing, users and reporting code exists. The main-branch ESLint workflow failed on 2026-10-13 because it references a missing `.eslintrc.js`; the repository contains `.eslintrc.cjs`. A current release certification was not found. | Fix the CI configuration and establish a clean main-branch baseline. Keep release gates around authorisation, stock/financial invariants, licensing, database upgrade, backup/restore and invoice/report consistency. Sell only a tightly scoped pilot that can be supported. |
| **GnuGuard** | Kotlin/Jetpack Compose Android Wi-Fi/network diagnostics app. The latest observed workflow failure was a Dependabot dependency-snapshot error (reported dependencies missing from its snapshot); that is **not proof that the app itself fails to compile**. A fresh app build, automated test result and physical-device acceptance were not established in this review. | Treat as a product candidate, not a released product. First obtain a clean Gradle build/test and real-device permission/scanning checks. Validate one paying IT-support use case before building subscriptions or white-label licensing. |
| **Zahzu Inventory Assistant (ZIA)** | Shopify inventory/purchasing app with implemented route surfaces for inventory health, reorder rules, supplier mapping, purchase orders, receiving and sync status. However, the last observed CI on 2026-10-12 fails TypeScript checking across inventory logic and routes. The project audit states current Shopify scopes are read-only and receipt records queue locally; Shopify inventory write-back is not active. The app URL/redirects are deployment placeholders; no dedicated end-to-end business-workflow test suite is recorded. | Promising focused B2B micro-SaaS candidate, but not commercially ready. Plug must clear typecheck, add workflow tests, verify tenant isolation and Shopify lifecycle behaviour, and implement/test an approved inventory-write path before representing receiving as a completed stock update. |
| **Maggie's Hair & Beauty** | Reusable five-page static website foundation with service data, gallery, contact and WhatsApp booking flow. Latest observed build/deployment workflows on 2026-10-12 succeeded. Physical-device acceptance and final customer/content approval are not proven by CI. | Best reusable website asset for a productized setup/customisation service. Confirm the intended customer facts, image rights, contact details and handover before resale or deployment. |
| **Leano ITC Website** | Company/service website with latest observed CI and Pages deployment successful on 2026-10-12. | Use as Rosscore's sales surface: clear service offer, portfolio demos, direct enquiry path and support terms. Green CI is not evidence of leads or sales. |
| **Catering Website Template** | Next.js/TypeScript V1 template foundation. Its own README excludes backend services, CMS, payments, authentication and database until required. Telemetry marked repository access as blocked, so current CI/readiness was not verified here. | Sell as a source/template or customised website package only after checking the actual latest files and quality gate. Do not describe it as a full catering SaaS. |
| **Thabz Driving School** | Mobile-first static lead-generation website with WhatsApp/phone enquiry path; current README says prices stay private and business/offer details require confirmation. | Potential client-site delivery/reference asset, not automatically a generic marketplace template. Confirm client ownership/approval and final runtime behaviour. |
| **Plumbing website repositories** | `plumbing_website` and `Plumbers_in_pretoria` both identify themselves in their README as “Plumbers in Pretoria — Rosscore Plumbing Pack”. The `plumbing_website` GitHub description instead says “Mandla 411” pest-control/cleaning/handyman services. The portfolio telemetry also associates the stale Mandla 411 name with `plumbing_website`. | **Identity conflict / duplication risk.** Determine the canonical repository and intended business before deploying, selling or publishing either site. Do not copy or delete repositories merely to remove the mismatch. |
| **Rosscore portfolio tracking** | The refreshed telemetry snapshot generated at 2026-10-16 21:32 UTC flags Swift Order and GnuGuard CI signals and ZIA CI failure. The company control records previously omitted ZIA from the human-readable registry and used the old repository slug. | Company-level ZIA registration and canonical mapping have now been updated. The telemetry matcher was corrected to recognise the actual “Rosscore Director Health Report” workflow name. The control-plane workflow and telemetry workflow completed successfully on company commit `169a5e0`; however, Director health artifacts remain `artifact_access_unavailable` across tracked projects because the cross-repository token cannot authenticate or retrieve those artifacts. The public metadata snapshot is fresh, but per-project Director readiness is still not established. |

## Commercial position

1. **Fastest plausible route to cash:** fixed-scope website setup/customisation for local businesses, supported by a working live demo and clear quote/deposit/handover terms. This can generate revenue sooner than waiting for digital-template marketplace discovery.
2. **Template marketplaces are a second channel, not the entire plan.** The current website repositories are static HTML or Next.js source projects, not automatically Framer-native projects. Prepare native Framer versions if pursuing Framer Marketplace; otherwise sell the code-based template or implementation service through a suitable channel after checking its current rules.
3. **Zazu and Swift Order remain the declared core products.** Zazu needs real offline/recovery acceptance; Swift Order needs reliable CI and its critical operational release gates. Do not substitute source-code volume for release proof.
4. **ZIA is an additional product track.** Its merchant workflow is clearer than a generic inventory assistant, but typecheck and the absent Shopify inventory write-back currently block a credible paid production promise.
5. **GnuGuard stays in validation.** Do not build subscription infrastructure or spend time on white-label packaging before build/device proof and direct buyer interest.
6. **Do not forecast the proposed AppSumo $40k–$80k target or $1,500–$5,000 GnuGuard licences as expected revenue.** Those are unvalidated targets until pricing, demand, conversion, implementation cost and support burden are measured.

## Portfolio-control fixes completed in this review

- Added **Zahzu Inventory Assistant (ZIA)** to the Rosscore project registry and corporate supporting portfolio.
- Corrected the company registry and machine-readable control plane to use `Leano-Jordan/ZIA-Inventory_Assist_Plugin`.
- Added company-level routing to Plug and made the control-plane linter enforce ZIA's project/repository/alias mapping.
- Corrected portfolio telemetry's report-name matching so “Rosscore Director Health Report” runs are recognised.
- Changes were committed directly to the existing `main` branch; no branch was created.

These are company-control/documentation changes. The ZIA repository's own manifest and agent contract still contain the old slug and should be reconciled by Plug inside the ZIA repository boundary.

- **VERIFIED:** Rosscore Control Plane passed on company commit `169a5e0` ([run](https://github.com/Leano-Jordan/Rosscore-Labs/actions/runs/38970043800)). Portfolio telemetry completed successfully on the same commit ([run](https://github.com/Leano-Jordan/Rosscore-Labs/actions/runs/38970043948)), but cross-repository Director health artifacts remain unavailable. A valid `ROSCORE_TELEMETRY_TOKEN` with read access to Actions runs/artifacts across tracked repositories is still needed; the collector currently falls back to public metadata when token authentication fails.

## Next operating priorities

1. **Revenue:** use the Leano ITC site as a business-facing sales surface and package one clear, fixed-scope website offer; keep a simple lead → quote → deposit → delivery → balance ledger.
2. **Zazu:** close the standalone-phone offline requirement with device evidence and reconcile current-head state/test results. Preserve the distinction between cached navigation and complete offline business operation.
3. **ZIA:** resolve TypeScript errors on main, then establish repeatable build and workflow tests. Keep inventory writes disabled until a supported, tested mutation path and scope are approved.
4. **Swift Order:** repair the invalid ESLint config path, rerun CI and then work down release blockers.
5. **GnuGuard:** obtain a fresh Gradle build/test baseline and test on a physical Android device.
6. **Asset hygiene:** resolve the duplicate/conflicting plumbing site identity and capture an authoritative inventory of demos, clients, licences, live URLs and owner approvals.
7. **Restore trustworthy portfolio health reports:** refresh the cross-repository telemetry token/permissions and verify that health artifacts can be downloaded, rather than treating metadata-only telemetry as Director certification.

## Unknowns requiring a real company ledger

No current, auditable figures for cash collected, monthly recurring revenue, operating costs, customer count, qualified leads, outstanding quotes, deposits, customer support commitments or production deployments were surfaced in the inspected company records. Keep these fields marked **UNKNOWN** until recorded; do not infer them from GitHub activity, CI status or website source code.

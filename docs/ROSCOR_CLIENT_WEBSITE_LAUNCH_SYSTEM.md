# Rosscore Labs — Client Website Launch System

**Status:** ACTIVE  
**Version:** 1.0  
**Owner:** Ross / Rosscore Labs

## Purpose
Repeatable, beginner-safe delivery process for commercial business websites.

## 1. Standard architecture
- Source: GitHub repository
- Hosting/deployment: Cloudflare Pages
- DNS/security: Cloudflare DNS
- Domain: client-owned registrar account
- Email: client-owned email provider, only when required
- Applications: separate infrastructure lane; do not force app workloads into this website stack.

Cloudflare Pages supports Git-based deployments and custom domains. Apex domains require the domain to be a Cloudflare zone and use Cloudflare nameservers. The Free Pages plan currently allows 500 builds/month and up to 100 custom domains per project. Verify current limits before production launch.

## 2. Ownership rule
The client owns the domain registration, domain registrar account, business email account, analytics/search accounts, business data and content.

Rosscore manages the website source code, deployment configuration, hosting configuration, and DNS configuration when authorised.

Never register a client's domain in Rosscore's personal account unless there is a documented commercial reason and an agreed transfer/ownership process.

## 3. Client intake
- Legal/business name
- Trading name
- Primary contact
- Phone/email
- Preferred domain name
- Existing domain, if any
- Logo/brand assets
- Business description
- Services/products
- Prices, where applicable
- Address/service area
- Opening hours
- Social links
- Contact/booking destination
- Required legal/privacy information
- Required business email addresses

## 4. Pre-launch gate
- Client has approved the final website
- Commercial terms/deposit are settled
- Domain ownership is confirmed
- Required content/assets are supplied
- Contact and booking links are tested
- Mobile and desktop layouts are tested
- No broken internal links remain
- Images have usable dimensions/compression
- Page titles/meta basics exist
- HTTPS works
- Domain resolves correctly
- Production deployment succeeds

## 5. Domain procedure
1. Search the preferred domain.
2. Prefer a relevant local domain for South African businesses, commonly .co.za.
3. Register it in the client's name/business account.
4. Enable auto-renewal where appropriate.
5. Record registrar, expiry date and ownership details in Rosscore's client record.
6. Add the domain to Cloudflare.
7. Copy the exact Cloudflare nameservers supplied for that zone.
8. Update nameservers at the registrar.
9. Wait for delegation to complete.
10. Confirm DNS before changing additional records.

Never guess nameservers. Copy the exact values Cloudflare gives for that domain.

## 6. Website deployment procedure
1. Confirm repository/default branch.
2. Connect repository to Cloudflare Pages.
3. Set build command/output directory only when the project requires it.
4. Deploy.
5. Test the generated Pages URL.
6. Add the client's custom domain.
7. Confirm HTTPS.
8. Test apex domain and www behaviour.
9. Test all critical navigation paths.
10. Test forms/booking/contact actions.
11. Test on Android Chrome and desktop Edge.
12. Record launch status.

## 7. Client handover
- Live website address
- Domain registrar/account ownership confirmation
- Email details, if provisioned
- Basic maintenance instructions
- What Rosscore manages
- What the client owns
- Support/maintenance terms
- Renewal responsibilities and dates

## 8. Commercial boundary
Separate the website price and infrastructure costs in the proposal:
- Website build
- Launch/setup
- Domain cost
- Email cost, if required
- Optional ongoing maintenance/care plan

Do not silently absorb recurring third-party costs into Rosscore's margin.

## 9. Support model
Every client site should have an operational record containing:
- Client
- Repository
- Domain
- Registrar
- Cloudflare zone
- Hosting/deployment project
- Email provider
- Launch date
- Renewal dates
- Current deployment status
- Last health check
- Known issues
- Maintenance plan

Do not store passwords or secret keys in GitHub documentation.

## 10. Beginner rule
Rosscore does not require the developer to understand networking theory before launching a website.

For each launch, the developer follows the checklist and records the exact values provided by the platforms.

Plain language:
- Domain: the client's internet address.
- Hosting: where the website is delivered from.
- DNS: the system that tells the internet where that address should go.
- Nameservers: the DNS service responsible for answering those directions.
- HTTPS: the encrypted connection between the visitor and website.

## 11. Failure handling
If a site is unreachable:
1. Check deployment status.
2. Check custom-domain status.
3. Check Cloudflare zone status.
4. Check nameservers.
5. Check DNS records.
6. Check HTTPS/certificate status.
7. Check the repository/build.
8. Check recent changes.
9. Roll back the website deployment if the application itself is responsible.

Never randomly change DNS records.

## 12. Standard stack decision
Default: GitHub + Cloudflare Pages + Cloudflare DNS + client-owned registrar.

Use another architecture when the website requires a backend, database, authentication, payments, server-side processing, persistent jobs, or other application infrastructure.

That becomes the application infrastructure standard rather than the basic website standard.
# Rosscore Labs — Project Registry

**Purpose:** authoritative company-level map of projects and their repository boundaries.

## Company Director

- Name: **Jarvis**
- Role: Rosscore Labs company-level Director
- Authority: company-level coordination, governance, routing, strategy, challenge and execution within granted authority
- Code boundary: `Leano-Jordan/Rosscore-Labs` for company documentation and governance
- Product implementation authority: none unless explicitly routed and authorized through the project's own repository contract

## Projects

### Zazu EMP

- Product: Zazu Event Management Platform
- Repository: `Leano-Jordan/ZazuEMP`
- Local workspace: `C:\Projects\ZazuEMP`
- Project Director: Zazu Director
- Project authority: Zazu repository only
- Company role: Initial Rosscore Labs product
- State source: current Zazu repository, living state/release documentation and verified CI/runtime evidence

### Swift Order

- Product: Swift Order
- Repository: `Leano-Jordan/store-ordering-system`
- Project Director: Swift Order Project Director
- Project authority: Swift Order repository only
- Company role: Initial Rosscore Labs product
- State source: current Swift Order repository, living state/release documentation and verified CI/runtime evidence

## Future projects

New projects must be registered here before becoming part of the company's managed portfolio.

Required fields:

- project name
- product/service
- repository
- local workspace when applicable
- project director
- lifecycle/status
- strategic role
- current-state source
- allowed write boundary

## Boundary rule

The registry gives Jarvis awareness of every project. It does **not** merge project knowledge or project authority.

A project repository remains an isolated execution domain.

## Registry integrity rules

- One product maps to one authoritative project repository unless explicitly documented otherwise.
- A project Director may not claim authority over another project's repository.
- A company-level decision does not automatically authorize product-repository writes.
- Repository changes that alter project identity, authority or boundaries must update this registry as part of the same controlled change.

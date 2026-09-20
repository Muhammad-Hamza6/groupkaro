# GroupKaro

Group-buy for home services in Pakistan. Neighbours in a society pool their demand for the same service (starting with **AC servicing**) so a vetted vendor does the whole building at a group rate. GroupKaro coordinates the pool and takes a commission — it never performs the service.

## Start here

| Doc | What it's for |
|---|---|
| [docs/VISION.md](docs/VISION.md) | The North Star — the full product + technical vision, corrected and de-risked. The *what & why*. |
| [docs/SCRUM-MVP.md](docs/SCRUM-MVP.md) | The buildable pilot plan — epics, stories, acceptance criteria, estimates, sprints. The *how & when*. **Start with Phase 0 (§8).** |

## Locked decisions

1. **Name:** GroupKaro.
2. **Model:** group-buy pooling now; vendor bidding is V2.
3. **Money:** manual escrow for the pilot (no gateway in code); aggregator-backed escrow is V2. *Platform-held escrow is SBP-regulated — get legal sign-off before the first payment.*
4. **Docs:** VISION = long-term vision; SCRUM-MVP = the strict pilot subset.
5. **Commission:** 10% of pool value, deducted from vendor payout.

## MVP at a glance

- **Service:** AC servicing only · **Scope:** one society you operate · **Roles:** Admin/Operator, Resident, Vendor.
- **Stack:** Next.js 14 + Tailwind/shadcn (PWA) · Django + Django REST Framework + PostgreSQL · phone-OTP auth · in-app + `wa.me` notifications.
- **No** payment gateway, WebSockets, or WhatsApp automation in the pilot — all deferred (see SCRUM-MVP §9).

## Current phase

Planning complete → **Phase 0: manual validation** (close one AC deal by hand) → Sprint 0 build.

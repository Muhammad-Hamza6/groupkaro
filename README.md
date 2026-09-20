# GroupKaro

Group-buy for home services in Pakistan. Neighbours in a society pool their demand for the same service (starting with **AC servicing**) so a vetted vendor does the whole building at a group rate. GroupKaro coordinates the pool and takes a commission — it never performs the service.

## Start here

| Doc | What it's for |
|---|---|
| [docs/VISION.md](docs/VISION.md) | North Star — full product + technical vision. |
| [docs/SCRUM-MVP.md](docs/SCRUM-MVP.md) | Buildable pilot plan — epics, stories, AC, sprints. |
| [backend/README.md](backend/README.md) | How to run the Django API. |
| [frontend/README.md](frontend/README.md) | How to run the Next.js app. |

## Locked decisions

1. **Name:** GroupKaro.
2. **Model:** group-buy pooling now; vendor bidding is V2.
3. **Money:** manual escrow for the pilot (no gateway in code).
4. **Commission:** 10% of pool value, deducted from vendor payout.

## Repo layout

- `backend/` — Django + Django REST Framework API
- `frontend/` — Next.js 14 (App Router) + TypeScript PWA
- `docs/` — vision + scrum plans

## Status

F0-1 in progress: backend + frontend scaffold, then CI, then Docker.

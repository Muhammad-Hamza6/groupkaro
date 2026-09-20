# GroupKaro — MVP Scrum Plan (AC-Servicing Pilot)

**Team:** 3 developers · **Cadence:** 2-week sprints · **Method:** Scrum (lean)
**Scope:** the pilot subset of [VISION.md](VISION.md) — one service (AC servicing), one society you operate, group-buy pooling, **manual** money, 3 roles (Admin/Operator, Resident, Vendor).
**Status:** Ready to build after Phase 0 (see §8).

> Everything here is a strict subset of the vision. If a request isn't in this doc, it's in the **V2+ parking lot (§9)** — not this build.

---

## 1. Why this differs from your first scrum (the fixes)

| Your v1 scrum | Problem | Fix here |
|---|---|---|
| 1-week sprints, 5 ceremonies/week | Ceremony overhead eats a 3-dev team (you flagged this yourself) | **2-week sprints**, lighter ceremonies |
| Backend-first, horizontal slices | No end-to-end value until ~Sprint 8 | **Vertical slices** — full pledge→confirm loop working by end of Sprint 3 |
| "Pooling" model, but spec said "bidding" | Two products | **Pooling only** for MVP; bidding is V2 (matches locked decision) |
| Payments absent, undefined | Silent contradiction with the spec's escrow | **Manual money, explicitly designed** (Epic MN) |
| Stories were one-liners | Not buildable | Every story has **AC + points + priority + tasks** |
| 3 roles, but spec had 4 | Mismatch | **3 roles** by design; Society-Admin hierarchy is V2 |

---

## 2. Team & roles

| Role | Who | Notes |
|---|---|---|
| Product Owner | Muhammad (or one dev part-time) | Owns backlog priority + pilot vendor/society relationships |
| Scrum Master | **Rotates each sprint** | Runs ceremonies, clears blockers; still does normal dev work |
| Dev 1 | Backend + data model owner | Django/DRF, auth, money, jobs |
| Dev 2 | Resident-facing frontend owner | `/app` |
| Dev 3 | Vendor-facing frontend + notifications owner | `/vendor`, notifications |

Admin/Operator panel (`/admin`) is **shared** — it's small and shared context helps. All three review each other's PRs.

---

## 3. Cadence & ceremonies (2-week sprint)

| Ceremony | When | Length | Purpose |
|---|---|---|---|
| Sprint Planning | Mon, week 1 | 60–90 min | Pick stories, break into tasks, estimate |
| Daily Standup | Daily | 10–15 min | Did / doing / blockers (async thread ok) |
| Backlog Refinement | Wed, week 1 | 30–45 min | Groom next sprint's stories, clarify AC |
| Sprint Review / Demo | Fri, week 2 | 30 min | Demo working software on staging |
| Retro | Fri, week 2 | 30 min | Keep / drop / try |

**Board columns:** Backlog → Ready → In Progress → In Review → Staging/QA → Done.

### Definition of Ready (a story can enter a sprint only if…)
- Has acceptance criteria, a point estimate, a priority, and an owner.
- Dependencies identified and unblocked.
- UI stories have a wireframe or a reference component.
- No open question that blocks starting.

### Definition of Done (a story is done only if…)
- Meets its acceptance criteria.
- Reviewed by ≥1 other dev and merged to `main`.
- Works on **mobile web** (primary target); no console errors, no broken flows.
- **Non-trivial logic has ≥1 test** (the ponytail rule — money/auth/state transitions especially).
- Deployed to **staging**.
- Money & auth paths: input validated at the trust boundary.

---

## 4. Estimation

Fibonacci points (1, 2, 3, 5, 8, 13). **Velocity is unproven until Sprint 2** — the per-sprint point sums below are a *plan hypothesis*, not a promise. After Sprint 2, recalculate velocity from actuals and **rebalance; cut `Should`/`Could` stories before `Must`.** Priorities use MoSCoW.

---

## 5. Product backlog (Epics → Stories)

Story ID format: `EPIC-n`. Each: **statement · acceptance criteria · points · priority · deps · tasks**.

### Epic F0 — Foundations

**F0-1 · Repo & tooling** — *As a team, we need a Next.js frontend and a Django API side by side so work has a home and types don't drift.*
- **AC:** `apps/web` (Next+TS, via Turborepo) and `apps/api` (Django + DRF, Python venv/poetry) both boot with one documented command each (or a root `docker-compose up` for local dev); `apps/api` exposes an OpenAPI schema (`drf-spectacular`) that generates a TS client/types consumed by `apps/web`; lint + typecheck (web) + lint/format (`ruff`/`black`, api) + build run in CI on every PR.
- **5 · Must · deps: —**
- Tasks: init Turborepo + scaffold web · scaffold Django project (`apps/api`, DRF installed) · `drf-spectacular` schema + generated TS types · base eslint/prettier (web) + ruff/black (api) · GitHub Actions.

**F0-2 · Environments & CI/CD** — *deploy targets exist so we demo on staging every sprint.*
- **AC:** api→Railway/Render (Django via Gunicorn), web→Vercel, db→Neon (dev + staging); `.env.example` complete; push to `main` auto-deploys to staging; smoke check passes.
- **5 · Must · deps: F0-1**
- Tasks: provision Neon/Railway/Vercel · secrets · deploy pipeline · staging smoke test.

**F0-3 · Schema & migrations** — *the corrected schema (VISION §9) as Django models + seed so features have a foundation.*
- **AC:** all MVP tables modeled as Django models across their apps; `makemigrations`/`migrate` applied cleanly; nullable-FK insert order honored; GIN indexes present (`django.contrib.postgres.indexes.GinIndex`); a `seed` management command creates 1 society + 1 admin + sample residents + 1 vendor; migrate + seed documented in README.
- **8 · Must · deps: F0-2**
- Tasks: model all tables (Django models) · migrations · GIN indexes · `manage.py seed` command · doc.

**F0-4 · Phone-OTP auth + JWT** — *residents/vendors sign in by phone, no passwords.*
- **AC:** send OTP (hashed, expiring, attempt-capped) → verify → JWT + refresh (`djangorestframework-simplejwt`); resend throttled (DRF throttle classes); expired/invalid handled; SMS adapter is pluggable (console-logs in dev).
- **8 · Must · deps: F0-3**
- Tasks: otp send/verify views · SMS gateway adapter · SimpleJWT issue/refresh wiring · DRF throttle config · tests (pytest-django).

**F0-5 · RBAC + society scoping middleware** — *the wrong role/society can't touch the wrong data.*
- **AC:** role guard (admin/resident/vendor) as a DRF permission class; residents see only their own society (queryset scoping); 403 on violation; allow/deny matrix unit-tested.
- **5 · Must · deps: F0-4**
- Tasks: custom DRF permission classes · role guard · society-scope queryset filtering · tests.

**F0-6 · App shells & mobile PWA base** — *three role surfaces exist to build into.*
- **AC:** `/admin`, `/app`, `/vendor` route groups; mobile-first layout; shadcn configured; auth-gated routing; loading/error boundaries.
- **5 · Must · deps: F0-1**
- Tasks: layouts + per-role nav · shadcn init · client auth guard · base components.

### Epic RS — Resident

**RS-1 · Join society via invite** — *As a resident I join my society with an invite code so I only see its pools.*
- **AC:** enter code → `society_id` set; invalid code handled; resident thereafter scoped to that society.
- **3 · Must · deps: F0-5**
- Tasks: `POST /join` · onboarding UI · tests.

**RS-2 · Browse pools** — *As a resident I see open pools in my society so I can find one to join.*
- **AC:** feed of `open` pools; card shows service, date, fill counter, price hint, deadline; sorted by soonest deadline.
- **3 · Must · deps: RS-1, AD-2**
- Tasks: `GET /pools` · feed UI · tests.

**RS-3 · Pool detail + join/pledge** — *As a resident I pledge with my unit count so I'm counted and priced right.*
- **AC:** detail shows description, participants (first name + flat), **polled** live counter, current tier; Join collects flat_no + `unit_count` + confirm; **no payment at pledge**; can't double-join (unique enforced); counter increments; leave allowed while `open`.
- **8 · Must · deps: RS-2**
- Tasks: `GET /pools/:id` · `POST /pools/:id/join` · `DELETE /leave` · polled counter (TanStack refetchInterval) · unit_count input · tests (unique, counter, leave).

**RS-4 · My pools** — *As a resident I track pools I'm in and their payment status.*
- **AC:** tabs Joined / Completed; per-pool status + payment badge (pledged / paid); links to detail.
- **3 · Must · deps: RS-3**
- Tasks: `GET /pools/mine` · UI · tests.

### Epic VN — Vendor

**VN-1 · Register + profile (pending approval)** — *As a vendor I sign up and declare categories/areas so I can be vetted and matched.*
- **AC:** OTP register; profile (business_name, cnic, cnic image upload to R2, categories, areas); `is_approved=false` initially; cannot see or confirm pools until approved.
- **5 · Must · deps: F0-4**
- Tasks: `POST /vendor/register` · profile UI · R2 upload · `PATCH /vendor/services` · tests.

**VN-2 · Available pools** — *As an approved vendor I see pools I can serve.*
- **AC:** approved-only; shows `threshold_met`/`sourcing` pools matching my area + category (GIN match); card shows society, area, headcount, date, tier.
- **3 · Must · deps: VN-1, AD-1**
- Tasks: `GET /vendor/pools/available` · UI · tests.

**VN-3 · Confirm assignment** — *As a vendor I confirm a pool assigned to me so the booking locks.*
- **AC:** confirm a `sourcing` pool assigned to me → status `confirmed`; residents + admin notified; resident contact details unlocked to me.
- **5 · Must · deps: AD-4**
- Tasks: `POST /vendor/pools/:id/confirm` · guard (assigned to me) · notify · tests.

**VN-4 · My jobs + mark complete** — *As a vendor I work my confirmed jobs and report completion.*
- **AC:** list confirmed/scheduled jobs with resident contacts + address; mark complete (+ optional proof photo) → awaits admin confirmation.
- **5 · Must · deps: VN-3**
- Tasks: `GET /vendor/jobs` · `PATCH /jobs/:id/complete` + proof upload · tests.

**VN-5 · Payouts view** — *As a vendor I see what I've been paid.*
- **AC:** table (gross, commission, net, status, date) + month total.
- **3 · Should · deps: MN-3**
- Tasks: `GET /vendor/payouts` · UI · tests.

### Epic AD — Admin / Operator

**AD-1 · Vendor vetting queue** — *As an admin I approve/suspend vendors so only vetted ones take work.*
- **AC:** list vendors + status; view cnic/phone/business; approve → `is_approved`; suspend; only approved vendors are matchable.
- **5 · Must · deps: F0-5, VN-1**
- Tasks: `GET /admin/vendors` · `PATCH approve|suspend` · admin list+detail UI · tests.

**AD-2 · Create pool with tiers** — *As an admin I create an AC pool with price tiers so residents can join.*
- **AC:** form (title, desc, category=`ac_servicing`, price_tiers, target_headcount, pledge_deadline, scheduled_date); validated; starts `open`; shows in resident feed.
- **5 · Must · deps: F0-6**
- Tasks: `POST /admin/pools` · tier editor · validation · tests.

**AD-3 · Pool monitoring** — *As an admin I watch every pool so I can run the pilot.*
- **AC:** list pools with status + fill + deadline; detail shows participants (name, flat, units, paid?); manual close/cancel available.
- **5 · Must · deps: AD-2, RS-3**
- Tasks: `GET /admin/pools` (+detail) · monitoring UI · tests.

**AD-4 · Assign vendor** — *As an admin I assign a vetted vendor to a filled pool.*
- **AC:** only `threshold_met` pools; only approved vendors matching area/category; assign → status `sourcing`, `assigned_vendor_id` set, vendor notified.
- **5 · Must · deps: AD-3, VN-2**
- Tasks: `POST /admin/pools/:id/assign` · vendor picker · notify · tests.

**AD-5 · Complete pool** — *As an admin I confirm delivery so payout + reviews trigger.*
- **AC:** after vendor marks done, admin confirms → status `completed`; creates payout record (MN-3) and prompts reviews (TR-1).
- **3 · Must · deps: VN-4, MN-3**
- Tasks: `PATCH /admin/pools/:id/complete` · guards · tests.

### Epic MN — Money (manual) & lifecycle

**MN-1 · Record manual payment** — *As an admin I log that a resident paid so escrow is tracked in-app (no gateway).*
- **AC:** on a `confirmed` pool, record payment (amount, method, external_ref) → writes a `payments` row **and** sets `participant.payment_status=paid` **in one transaction**; idempotent per participant.
- **5 · Must · deps: VN-3**
- Tasks: `POST /admin/pools/:id/payments` · transactional write + projection · UI · tests (tx, idempotency).

**MN-2 · 80% rule → scheduled** — *As a system, once enough have paid the job is greenlit.*
- **AC:** when ≥80% of participants (configurable per pool) are `paid` → status `scheduled`, date confirmed; participants + vendor notified.
- **3 · Must · deps: MN-1**
- Tasks: threshold calc · transition · notify · boundary test (79/80/81%).

**MN-3 · Payout net commission** — *As an admin I capture revenue on completion.*
- **AC:** on `completed` → `vendor_payouts` row (gross, commission = 10%, net); mark `paid` when transferred; commission recorded for analytics; PKR rounding correct.
- **5 · Must · deps: AD-5**
- Tasks: `POST /admin/pools/:id/payout` · commission calc · UI · tests (rounding).

**MN-4 · Cancel + refund** — *As an admin I can cancel and flag refunds.*
- **AC:** cancel → status `cancelled`; paid participants → `refunded` (payments + projection); reason recorded; participants notified.
- **3 · Must · deps: MN-1**
- Tasks: `POST /admin/pools/:id/cancel` · refund projection · notify · tests.

**MN-5 · Auto-expire pools** — *As a system, dead pools clear themselves.*
- **AC:** scheduled job flips `open`→`expired` when `pledge_deadline` passed and headcount < target; participants notified; no charges (payment is post-threshold).
- **3 · Must · deps: RS-3**
- Tasks: cron job · transition · notify · test.

### Epic NT — Notifications (lite)

**NT-1 · In-app notifications** — *As any user I'm told when something happens to my pool.*
- **AC:** notifications surfaced per role; created on `threshold_met`, `confirmed`, `scheduled`, `completed`, `cancelled`; mark-read works.
- **5 · Must · deps: F0-6**
- Tasks: notification writer util · `GET` + `PATCH read` · bell UI · wire events · tests.

**NT-2 · WhatsApp share deep links** — *As a resident/admin I share a pool to WhatsApp in one tap.*
- **AC:** share button → `wa.me` link with pre-filled text + pool URL; works on mobile; society invite link shareable the same way.
- **2 · Must · deps: RS-3**
- Tasks: build `wa.me` URLs · share buttons · device test.

**NT-3 · Deadline reminder** — *As a resident I'm nudged before a pool I could join closes.*
- **AC:** scheduled job sends in-app (+ optional SMS) reminder X hours before `pledge_deadline` to residents who haven't joined a still-open pool.
- **3 · Should · deps: NT-1, MN-5**
- Tasks: cron · targeting · message · test.

### Epic TR — Trust

**TR-1 · Ratings & reviews** — *As a resident I rate the vendor after completion so others can trust them.*
- **AC:** after a `completed` pool, participants prompted to rate 1–5 + comment; **one review per resident per pool** (unique enforced); vendor `rating`/`total_jobs`/`completion_rate` recalculated; rating shown on vendor cards.
- **5 · Must · deps: AD-5**
- Tasks: `POST review` · vendor stat recalc · show on vendor card · tests (unique, recalc).

### Epic HD — Hardening

**HD-1 · Pilot analytics** — *As an admin I can judge the pilot.*
- **AC:** fill rate, avg time-to-fill, pledge→paid conversion, pools by status, commission earned.
- **5 · Should · deps: MN-3**
- Tasks: `GET /admin/analytics` · queries · cards · test.

**HD-2 · Logging & error tracking** — *As a team we can debug the live pilot.*
- **AC:** structured request logging on api; client + server errors captured (Sentry free tier); money actions audit-logged.
- **3 · Must · deps: F0-2**
- Tasks: logger middleware · Sentry · audit log on money paths.

**HD-3 · Integration pass + UAT** — *the whole loop works before real users.*
- **AC:** end-to-end happy path verified on staging with a seeded society (create → join → threshold → assign → confirm → pay → 80% → complete → payout → review); issues triaged; go/no-go checklist done.
- **8 · Must · deps: all MVP Musts**
- Tasks: e2e runbook · UAT session · bug triage · pilot go/no-go checklist.

---

## 6. Sprint plan (vertical slices)

| Sprint | Theme | Stories | Sprint goal / demo | ~pts |
|---|---|---|---|---|
| **0** (setup, ~1 wk) | Skeleton | F0-1, F0-2, F0-3 + wireframes + kick off SMS/WhatsApp paperwork | Repo deploys to staging; schema + seed exist | 18* |
| **1** | Auth + spine | F0-4, F0-5, F0-6, RS-1, AD-2 | Log in by OTP; admin creates a pool; resident joins the society | 26 |
| **2** | Core loop: pledge→threshold | RS-2, RS-3, AD-3, MN-5 | Residents fill a pool, watch the counter cross the threshold; dead pools expire | 19 |
| **3** | Vendor + assignment (loop closes) | VN-1, AD-1, VN-2, AD-4, VN-3 | A vetted vendor is assigned and **confirms** a filled pool — full loop end to end | 23 |
| **4** | Money + completion | MN-1, MN-2, VN-4, AD-5, MN-3, MN-4 | A pool completes: payments recorded, 80%→scheduled, vendor paid net 10%, refunds work | 24 |
| **5** | Trust + notifications + polish | TR-1, NT-1, NT-2, NT-3, RS-4, VN-5 | Reviews live; users notified in-app + WhatsApp share; mobile polish | 21 |
| **6** | Hardening + pilot prep | HD-1, HD-2, HD-3 + buffer | Green end-to-end on staging; UAT passed; go/no-go for the live pilot | 16 |

*Sprint 0 is setup, not velocity. **End-to-end value lands at Sprint 3**, not Sprint 8.

**Rebalance rule:** after Sprint 2, set velocity from actuals. If over capacity, drop `Should` stories (VN-5, NT-3, HD-1) before any `Must`.

---

## 7. Track ownership per sprint (parallelism)

| Sprint | Dev 1 (backend/data) | Dev 2 (resident FE) | Dev 3 (vendor FE + notif) |
|---|---|---|---|
| 1 | F0-4, F0-5 | RS-1 | F0-6 (shared) |
| 2 | MN-5, pools API | RS-2, RS-3 | AD-3 (shared admin) |
| 3 | AD-4, matching | VN-2 wiring | VN-1, VN-3 |
| 4 | MN-1, MN-2, MN-3 | AD-5 (shared) | VN-4, MN-4 |
| 5 | TR-1 recalc | RS-4, review UI | NT-1, NT-2, NT-3 |
| 6 | HD-2, analytics API | HD-3 driving | HD-1 UI |

Rough guide, not a cage — swarm on blockers.

---

## 8. Phase 0 — Manual validation (do this before/alongside Sprint 0)

**Do not build past Sprint 0 until one AC deal closes end-to-end by hand.**
- Pick 1 real society in your city (ideally where you know the secretary).
- Run one pool manually: Google Form + the society WhatsApp group + a spreadsheet.
- Collect payment the manual-escrow way: residents transfer to your business account; you track it; you pay the vendor minus 10%.
- **Validate:** does a secretary/organizer actually rally people? Do pledges convert to payment? Does a vendor honor group pricing and show up? Is 10% acceptable to the vendor?
- This *is* the real product with humans instead of code — it de-risks everything and matches the manual-escrow decision.

---

## 9. V2+ parking lot (explicitly NOT in this build)

Everything below is deferred — it lives here so it stops leaking into MVP sprints:
- **Bidding / reverse auction** (vendors compete on a filled pool).
- **Aggregator-backed escrow** + JazzCash/EasyPaisa integration (needs legal entity + licensed partner — VISION §6).
- **Multi-society**: Main Admin onboarding societies, Society-Admin self-serve dashboard, admin incentive model.
- **Resident-created custom pools** (min 2).
- **WhatsApp automation** (template messages, needs Meta Business verification).
- **Realtime WebSockets** (replace polled counter).
- **Multi-category** beyond AC servicing.
- Vendor **trust score**, structured **disputes**, **referrals**, recurring **AMC** plans, **Urdu** i18n.

---

## 10. Risks & mitigations (project-level)

| Risk | Mitigation |
|---|---|
| **Velocity unproven** | Points above are a hypothesis; recalc after Sprint 2, cut `Should` before `Must`. |
| **SMS-OTP / WhatsApp lead time** | Start provider signup + any verification in **week 0** as a parallel track (F0/Sprint 0). |
| **No vendor supply in the pilot society** | PO recruits + vets 1–2 AC vendors by hand **before Sprint 3**. |
| **Scope creep** (bidding/escrow/categories sneaking in) | §9 is a parking lot, not a to-do; ponytail discipline on every PR. |
| **Legal sign-off for manual escrow** | Get a lawyer's OK **before the first real payment** — blocks the *live pilot*, not dev. |
| **Ceremony overhead** | 2-week cadence + async standups; time-box hard. |

---

*What to build is defined by the stories above. Why it's shaped this way is in [VISION.md](VISION.md). Start with Phase 0.*

# GroupKaro — Product & Technical Vision (North Star)

**Document type:** Product + Technical Specification
**Version:** 2.0 (corrected, de-risked)
**Status:** Vision / long-term reference. For what we actually build first, see [SCRUM-MVP.md](SCRUM-MVP.md).

> This is the **destination**, not the first build. Every section is tagged:
> `[MVP]` = in the first pilot · `[V2]` = after the pilot proves the loop · `[V3]` = scale/expansion.
> The MVP is a strict subset of this document. Nothing here should be built ahead of its tag.

## Locked decisions (do not re-litigate without a written reason)

| # | Decision | Rationale |
|---|---|---|
| 1 | **Name: GroupKaro** | Bilingual, brandable, consumer-facing. |
| 2 | **Model: pooling now, bidding later (hybrid)** | Pooling with vetted vendors protects quality and is a simpler MVP. Bidding is a V2 layer once vendor supply + ratings exist. |
| 3 | **Money: manual escrow for the pilot** | Platform-held automated escrow is a regulated activity in Pakistan (see §6). We do NOT custody money in code until a licensed path exists. |
| 4 | **Vision (this doc) vs MVP (scrum)** | This is the North Star; the pilot ships a thin subset. |
| 5 | **Commission: 10% of pool value**, deducted from vendor payout | Single revenue line for V1. |

---

## 1. What GroupKaro is

Home services in Pakistan are priced per household. In one apartment society, dozens of neighbours need the *same* service in the *same* window — summer AC servicing, pre-Eid deep cleaning — yet each pays retail and negotiates alone. Nobody aggregates this synchronised, latent demand.

**GroupKaro aggregates a society's demand into a single "pool," then places that pool with a vetted vendor at a group rate.** More neighbours in the pool → lower per-head price. The platform coordinates and (at scale) safeguards payment; it takes a commission on completed pools.

**What we do NOT do:** we never perform a service. We are a coordination + trust layer between residents and vendors. We are not a repair company.

---

## 2. The insight (why this works)

- **Synchronised demand is free money left on the table.** The neighbours already exist, already want the service, already talk in a WhatsApp group. We don't create demand — we *collect* it.
- **The live fill counter is the emotional engine.** "14/20 joined — 6 more unlocks the group rate" creates urgency and social proof. This is the single most important piece of UX; protect it.
- **The society WhatsApp group is the distribution channel.** Shareable invite links dropped into that group are the entire top-of-funnel for V1 — no paid acquisition needed to validate.

---

## 3. Product model — pooling now, bidding later

### 3.1 The pool lifecycle (one state machine serves both models)

```
DRAFT
  → OPEN                 collecting pledges; live counter ticking
  → THRESHOLD_MET        target headcount reached before deadline
  → SOURCING             a vendor is being locked in (see 3.2)
  → CONFIRMED            vendor + price locked, participants notified
  → COLLECTING_PAYMENT   residents pay (manual in V1)
  → SCHEDULED            enough paid; service date set
  → IN_PROGRESS          service day
  → COMPLETED            admin confirms delivery
  → CLOSED               payout done, commission taken

Side exits:
  OPEN → EXPIRED         deadline passed, threshold not met (no charge)
  any  → CANCELLED       with refunds per §6 rules
```

### 3.2 How a vendor gets locked in

- **`[MVP]` Pooling (assign a vetted vendor at a tiered price).** Pricing tiers are set on the pool (e.g. 10 flats = ₨2,500/AC, 20 = ₨2,200, 30 = ₨1,900). When the threshold is met, the admin assigns one **pre-vetted** vendor who **confirms** they'll honour the tier. No open competition — quality and safety come first while the vendor base is small.
- **`[V2]` Bidding (reverse auction on top of the pool).** Once a pool fills, it can instead be opened to *approved* vendors who submit bids; lowest is auto-flagged, admin can accept or override. This is added **only after** we have (a) enough approved vendors per area to make competition real and (b) a rating system to stop the race-to-the-bottom from sacrificing quality.

> **Why not bidding first?** "Lowest bid wins" for services performed inside people's homes (AC gas work, electrical) rewards the cheapest, not the safest. With a thin vendor base it also just produces one-bid "auctions." Pooling with vetting is the correct V1; bidding is a scaling feature, not a starting point.

---

## 4. Roles & permissions

**At scale (this doc)** there are four roles. **`[MVP]` collapses these to three** — see the note below.

| Action | Main Admin | Society Admin | Resident | Vendor |
|---|---|---|---|---|
| Register a society | ✅ | — | — | — |
| Appoint a Society Admin | ✅ | — | — | — |
| Create a society pool | ✅ | ✅ `[V2]` | — | — |
| Join a pool | — | ✅ | ✅ | — |
| See all societies | ✅ | — | — | — |
| See own society only | — | ✅ | ✅ | — |
| Assign / confirm a vendor | ✅ | ✅ `[V2]` | — | — |
| Submit a bid | — | — | — | ✅ `[V2]` |
| Approve / vet / ban a vendor | ✅ | — | — | — |
| Record payment / release payout | ✅ | — | — | — |
| Mark pool complete | ✅ | ✅ `[V2]` | — | — |

> **`[MVP]` role collapse.** The pilot runs in **one** society that **you operate**. So Main Admin and Society Admin are the *same person* — one **Admin/Operator** role — and the multi-society hierarchy (Main Admin appointing per-society admins) is a **`[V2]` scaling feature**. MVP roles = **Admin/Operator, Resident, Vendor.** This removes an entire dashboard from the first build.

**Role definitions (target state):**
- **Main Admin (platform owner)** — onboards societies, appoints Society Admins, approves/vets vendors, controls money, sees everything, owns analytics.
- **Society Admin `[V2]`** — one per society, runs that society's pools, cannot see other societies. *Needs an incentive to do unpaid coordination work — see §11.2.*
- **Resident** — joins their society by invite link, joins pools, `[V2]` creates limited custom pools (min 2 people).
- **Vendor** — signs up, **must pass vetting before taking work** (see §7), serves approved areas/categories, gets paid after completion.

---

## 5. Dashboards

Four surfaces at scale; **three in the MVP**. All are mobile-first PWA — residents live on their phones.

| Surface | Route | Purpose | MVP? |
|---|---|---|---|
| Admin / Operator | `/admin` | Create + run pools, vet vendors, record money, view the pilot | ✅ `[MVP]` (merged Main + Society admin) |
| Society Admin | `/society/:id/admin` | Per-society self-service management | `[V2]` |
| Resident | `/app` | Discover, join, track pools | ✅ `[MVP]` |
| Vendor | `/vendor` | See pools, confirm/bid, mark done, see payouts | ✅ `[MVP]` |

Screen-level detail for each surface lives in [SCRUM-MVP.md](SCRUM-MVP.md) as user stories with acceptance criteria — that is the buildable source of truth. This doc stays at the "what and why" level.

---

## 6. Money & the legal reality (read this before writing any payment code)

### 6.1 The hard constraint

Holding residents' money and paying it out to vendors is **not** something a normal JazzCash/EasyPaisa *merchant* account permits. A merchant account lets you collect money **for your own** goods/services. The moment you **custody third-party funds and remit them to someone else**, you are acting as a payment aggregator / money transmitter, which in Pakistan falls under **State Bank of Pakistan** regulation (PSO/PSP licensing, or operating **through** an already-licensed aggregator/EMI). Getting this wrong is an existential legal risk, not a technical detail.

### 6.2 What we do at each phase

| Phase | How money moves | Regulatory exposure |
|---|---|---|
| **`[MVP]` Manual escrow** | Resident transfers directly to **your registered business bank account**. Admin records "paid" in-app. On completion, admin manually transfers vendor's share (minus 10%) and marks "released." | Low — you're collecting for a service you're coordinating, at pilot scale, by hand. **Confirm with a Pakistani corporate lawyer before the first rupee.** |
| **`[V2]` Aggregator-backed escrow** | Integrate a **licensed** payment aggregator/PSP that supports **marketplace split settlement** (holds funds, pays out to vendors). We never touch the float. | Medium — carried by the licensed partner. Requires a registered company + contracts. |
| **`[V3]` Own escrow rails** | Only if volume justifies pursuing SBP licensing directly. | High — full licensing project. |

### 6.3 Rules (apply at every phase)

- **Refunds:** pool expires (threshold not met) → nobody is charged (payment happens *after* threshold, so this is a non-event in V1). Vendor no-show → full refund + vendor trust penalty. Dispute → admin decides manually `[MVP]`, structured flow `[V2]`.
- **Partial participation:** default rule — **80% of pledged participants must pay** for the pool to run; the rest are dropped or pay cash on the day. Configurable per pool.
- **Payout timing `[V2]`:** T+2 after admin release, giving a dispute window.
- **Currency:** all amounts PKR, stored as `DECIMAL(12,2)`.
- **Per-unit pricing:** a "flat" is not one AC. Price is **per serviceable unit** (per AC), captured when a resident joins (how many ACs), not per household. This fixes the biggest hidden pricing bug — see §9.

---

## 7. Trust & safety (a stranger enters someone's home)

This is a service marketplace sending vendors into homes; trust is the product, not a feature.

- **`[MVP]` Vendor vetting gate.** A vendor cannot take a pool until the admin **manually approves** them after checking **CNIC + phone + a reference/sample of past work**. No automated KYC needed at pilot scale — just an approval flag the admin flips.
- **`[MVP]` Ratings.** After completion, participants rate the vendor 1–5 with an optional comment. One review per resident per pool.
- **`[V2]` Vendor trust score** — derived from ratings, completion rate, no-shows; gates access to higher-value pools and bidding.
- **`[V2]` Structured disputes** — evidence upload, defined resolution SLA.
- **`[V3]` Formal KYC** — CNIC verification via a KYC provider, background checks.

---

## 8. System architecture

### 8.1 Target (this doc)

```
Clients (PWA): Admin · Society Admin · Resident · Vendor
        │  HTTPS / REST
API Gateway (Django + DRF): JWT auth (SimpleJWT) · permission classes (RBAC) · throttling
        │
Apps: Auth · Pool · Sourcing(assign/bid) · Payment · Notification
        │
PostgreSQL  ·  Redis (cache, OTP, rate limits)  ·  WebSockets (live counter, via Django Channels)
        │
External: licensed payment aggregator · WhatsApp Cloud API · S3/R2 (proof images) · SMS OTP gateway
```

### 8.2 `[MVP]` Simplified architecture (what actually ships first)

Cut everything that isn't load-bearing for one society:

- **No WebSockets.** The live counter updates via polling / refetch-on-focus (TanStack Query, ~15–30s). WebSockets are a `[V2]` upgrade once concurrency justifies them.
- **No payment gateway.** Manual money (§6) → no Payment app, no escrow state machine in code.
- **No automated WhatsApp.** Use **click-to-WhatsApp deep links** (`wa.me` with pre-filled text) for sharing + in-app notifications. Automated WhatsApp *template* messages need Meta Business verification (weeks) → `[V2]`.
- **Redis** only if OTP/rate-limiting needs it; otherwise a Postgres `otp_codes` table is enough at pilot scale.
- **DRF over Django's default templating.** The API is pure JSON (DRF `ViewSet`s/`APIView`s); Django's own template engine and admin-site rendering aren't used for end-user surfaces — the built-in Django Admin is optionally handy for internal debugging only, not the `/admin` product surface (that's still a Next.js route).

Result: **Next.js PWA + Django/DRF + Postgres.** That's the whole MVP stack.

**Design principles (all phases):** RBAC enforced in middleware; money moves only through defined state transitions; bids are append-only (never edited, only accepted/rejected) `[V2]`.

---

## 9. Data model (corrected)

Full corrected schema below. **Fixes applied vs the original v1 are listed at the end of this section** — those were real bugs.

```sql
-- USERS
users (
  id            UUID PK,
  phone         VARCHAR(20) UNIQUE NOT NULL,
  full_name     VARCHAR(255) NOT NULL,
  email         VARCHAR(255),
  role          VARCHAR(30) NOT NULL CHECK (role IN ('main_admin','society_admin','resident','vendor')),
  society_id    UUID NULL REFERENCES societies(id),   -- nullable: breaks the society<->user cycle
  flat_no       VARCHAR(20),
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
)

-- OTP (was missing entirely; phone-OTP auth needs it)
otp_codes (
  id          UUID PK,
  phone       VARCHAR(20) NOT NULL,
  code_hash   VARCHAR(255) NOT NULL,     -- store a hash, never the raw code
  expires_at  TIMESTAMPTZ NOT NULL,
  attempts    INT NOT NULL DEFAULT 0,
  consumed_at TIMESTAMPTZ NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
)  -- INDEX (phone, expires_at)

-- SOCIETIES
societies (
  id            UUID PK,
  name          VARCHAR(255) NOT NULL,
  city          VARCHAR(100) NOT NULL,
  address       TEXT,
  admin_user_id UUID NULL REFERENCES users(id),  -- nullable: set AFTER the admin user exists
  invite_code   VARCHAR(20) UNIQUE NOT NULL,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
)
-- Insert order to satisfy the FKs: create society (admin_user_id NULL)
-- → create admin user with society_id → UPDATE society.admin_user_id.

-- VENDORS
vendors (
  id                 UUID PK,
  user_id            UUID UNIQUE NOT NULL REFERENCES users(id),
  business_name      VARCHAR(255) NOT NULL,
  cnic               VARCHAR(20),               -- vetting (new)
  cnic_image_url     TEXT,                      -- vetting (new)
  service_categories TEXT[] NOT NULL DEFAULT '{}',
  service_areas      TEXT[] NOT NULL DEFAULT '{}',  -- GIN-indexed; normalise to a join table at [V3]
  rating             DECIMAL(3,2) NOT NULL DEFAULT 0,
  total_jobs         INT NOT NULL DEFAULT 0,
  completion_rate    DECIMAL(5,2) NOT NULL DEFAULT 0,
  is_approved        BOOLEAN NOT NULL DEFAULT FALSE,  -- the [MVP] vetting gate
  is_suspended       BOOLEAN NOT NULL DEFAULT FALSE,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
)  -- GIN INDEX on service_areas, service_categories

-- POOLS (was "tasks"; renamed to match the product language)
pools (
  id                UUID PK,
  title             VARCHAR(255) NOT NULL,
  description       TEXT,
  service_category  VARCHAR(100) NOT NULL,     -- seeded with 'ac_servicing' for MVP
  pool_type         VARCHAR(20) NOT NULL DEFAULT 'society_wide' CHECK (pool_type IN ('society_wide','custom')),
  created_by        UUID NOT NULL REFERENCES users(id),
  society_id        UUID NOT NULL REFERENCES societies(id),
  price_tiers       JSONB,                     -- [{min_units:10, price_per_unit:2500}, ...]
  target_headcount  INT NOT NULL CHECK (target_headcount >= 1),
  current_headcount INT NOT NULL DEFAULT 0,    -- denormalised counter; source of truth = pool_participants
  status            VARCHAR(30) NOT NULL DEFAULT 'open'
                    CHECK (status IN ('draft','open','threshold_met','sourcing','confirmed',
                                      'collecting_payment','scheduled','in_progress','completed',
                                      'cancelled','expired')),
  assigned_vendor_id UUID NULL REFERENCES vendors(id),
  accepted_bid_id    UUID NULL REFERENCES bids(id),  -- FK added; nullable; set on accept [V2]
  pledge_deadline    TIMESTAMPTZ,
  sourcing_deadline  TIMESTAMPTZ,              -- bidding window close [V2]
  scheduled_date     DATE,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
)  -- INDEX (society_id), (status), (service_category)

-- POOL PARTICIPANTS (pledge + per-unit + payment projection)
pool_participants (
  id             UUID PK,
  pool_id        UUID NOT NULL REFERENCES pools(id) ON DELETE CASCADE,
  user_id        UUID NOT NULL REFERENCES users(id),
  unit_count     INT NOT NULL DEFAULT 1 CHECK (unit_count >= 1),  -- e.g. #ACs — fixes flat!=unit
  joined_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  payment_status VARCHAR(30) NOT NULL DEFAULT 'pledged'
                 CHECK (payment_status IN ('pledged','paid','refunded')),  -- projection of payments ledger
  UNIQUE (pool_id, user_id)
)  -- INDEX (pool_id)

-- BIDS  [V2]
bids (
  id         UUID PK,
  pool_id    UUID NOT NULL REFERENCES pools(id) ON DELETE CASCADE,
  vendor_id  UUID NOT NULL REFERENCES vendors(id),
  amount     DECIMAL(12,2) NOT NULL,
  notes      TEXT,
  eta_days   INT,
  status     VARCHAR(20) NOT NULL DEFAULT 'pending'
             CHECK (status IN ('pending','accepted','rejected','withdrawn')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (pool_id, vendor_id)
)  -- INDEX (pool_id), (vendor_id)

-- PAYMENTS (money ledger — SINGLE source of truth for money state)
payments (
  id             UUID PK,
  pool_id        UUID NOT NULL REFERENCES pools(id),
  user_id        UUID NOT NULL REFERENCES users(id),
  amount         DECIMAL(12,2) NOT NULL,
  method         VARCHAR(30) NOT NULL DEFAULT 'manual_transfer',  -- 'jazzcash'|'easypaisa'|'bank' [V2]
  external_ref   VARCHAR(255),                 -- bank ref / gateway txn id
  status         VARCHAR(30) NOT NULL DEFAULT 'recorded'
                 CHECK (status IN ('recorded','refunded')),   -- gateway states ('held','released'...) [V2]
  recorded_by    UUID REFERENCES users(id),    -- which admin logged it (manual escrow)
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
)  -- INDEX (pool_id), (status)
-- Rule: pool_participants.payment_status is updated in the SAME transaction that
-- writes a payments row. Ledger is truth; participant status is a cached projection.

-- VENDOR PAYOUTS
vendor_payouts (
  id                UUID PK,
  pool_id           UUID NOT NULL REFERENCES pools(id),
  vendor_id         UUID NOT NULL REFERENCES vendors(id),
  gross_amount      DECIMAL(12,2) NOT NULL,
  commission_amount DECIMAL(12,2) NOT NULL,
  net_amount        DECIMAL(12,2) NOT NULL,
  status            VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','paid','failed')),
  paid_at           TIMESTAMPTZ,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
)

-- NOTIFICATIONS
notifications (
  id         UUID PK,
  user_id    UUID NOT NULL REFERENCES users(id),
  type       VARCHAR(50) NOT NULL,
  title      VARCHAR(255) NOT NULL,
  body       TEXT,
  link       TEXT,
  is_read    BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)  -- INDEX (user_id, is_read)

-- REVIEWS
reviews (
  id         UUID PK,
  pool_id    UUID NOT NULL REFERENCES pools(id),
  user_id    UUID NOT NULL REFERENCES users(id),
  vendor_id  UUID NOT NULL REFERENCES vendors(id),
  rating     INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  comment    TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (pool_id, user_id)                    -- one review per resident per pool (was missing)
)
```

**Schema fixes applied vs your v1 (these were genuine bugs):**
1. **Circular FK** `societies.admin_user_id ↔ users.society_id` — both made **nullable** with a documented insert order; otherwise neither row can be inserted first.
2. **Two sources of truth for payment state** (`task_participants.payment_status` *and* `payments.status`) — collapsed: **`payments` ledger is truth**, participant status is a projection updated in the same transaction.
3. **Missing OTP table** — added `otp_codes` (hashed, with expiry + attempts); phone-OTP auth is impossible without it.
4. **Reviews had no uniqueness** — added `UNIQUE(pool_id, user_id)`; otherwise one resident can spam a vendor's rating.
5. **`accepted_bid_id` had no FK** — added (nullable), and the pool↔bid two-way reference is documented.
6. **`flat_no` ≠ serviceable unit** — added `unit_count` on participants so a 4-AC flat is priced correctly. This was a silent, revenue-affecting pricing bug.
7. **Array columns unindexed** — added GIN indexes on `service_areas`/`service_categories`; normalise to a join table only at `[V3]`.
8. **Money precision/currency** — `DECIMAL(12,2)`, PKR, documented.
9. **`tasks` renamed `pools`** — matches the product's own language and removes the spec/scrum vocabulary split.

---

## 10. API surface (corrected, aligned to the model)

All under `/api/v1`, JWT in `Authorization: Bearer`. **`[MVP]`** endpoints marked; the rest are `[V2]`.

```
AUTH
  POST /auth/otp/send            send OTP to phone                         [MVP]
  POST /auth/otp/verify          verify OTP → JWT (+ refresh)              [MVP]
  POST /auth/refresh             refresh token                            [MVP]

ADMIN / OPERATOR
  POST   /admin/societies              register society + its admin        [V2] (MVP seeds one by hand)
  GET    /admin/societies              list all societies                  [V2]
  GET    /admin/vendors                list vendors                        [MVP]
  PATCH  /admin/vendors/:id/approve    approve (vetting gate)              [MVP]
  PATCH  /admin/vendors/:id/suspend    suspend                            [MVP]
  POST   /admin/pools                  create a pool (tiers, deadline)     [MVP]
  GET    /admin/pools                  list/monitor pools                  [MVP]
  POST   /admin/pools/:id/assign       assign a vetted vendor              [MVP]
  PATCH  /admin/pools/:id/complete     mark completed                      [MVP]
  POST   /admin/pools/:id/payments     record a manual payment            [MVP]
  POST   /admin/pools/:id/payout       record vendor payout (net of 10%)  [MVP]
  POST   /admin/pools/:id/cancel       cancel + refund                    [MVP]
  GET    /admin/analytics              pilot metrics                       [MVP-lite]

RESIDENT
  POST   /join                    join society via invite code             [MVP]
  GET    /pools                   open pools in my society                 [MVP]
  GET    /pools/:id               pool detail + live counter               [MVP]
  POST   /pools/:id/join          pledge (name, flat, unit_count)          [MVP]
  DELETE /pools/:id/leave         leave before threshold                   [MVP]
  GET    /pools/mine              my pools (joined/paid/completed)         [MVP]
  POST   /pools                   create a custom pool (min 2)             [V2]

VENDOR
  POST  /vendor/register          create vendor profile (pending approval) [MVP]
  GET   /vendor/pools/available   pools I can serve                        [MVP]
  POST  /vendor/pools/:id/confirm confirm a tiered assignment              [MVP]
  POST  /vendor/pools/:id/bid     submit a bid                             [V2]
  GET   /vendor/jobs              my confirmed jobs + resident contacts    [MVP]
  PATCH /vendor/jobs/:id/complete mark service done (+ proof photo)        [MVP]
  GET   /vendor/payouts           payout history                           [MVP]
  PATCH /vendor/services          update categories/areas                  [MVP]

WEBSOCKET EVENTS  [V2] — MVP uses polling instead
  pool:counter_updated · pool:threshold_met · pool:confirmed · notification:new
```

---

## 11. Risks & mitigations (the real project risk is here, not in the code)

### 11.1 Three-sided cold-start
You need residents **and** a vendor **and** (at scale) a society admin, in the same area, at the same time. **Mitigation:** the pilot deliberately shrinks this to **one society you operate** + **1–2 vendors you recruit by hand**. Don't build multi-society onboarding until one society's loop repeats.

### 11.2 The Society Admin has no incentive `[V2]`
Unpaid coordination work doesn't sustain itself. Before enabling self-serve societies, define the admin's reward: free/discounted service, a cut of commission, or visible status. **Until that's designed, you (Main Admin) are every society's admin.**

### 11.3 Quality & safety of vendors
A bad AC job (gas leak, damaged unit) inside a home can end the business early. **Mitigation:** the `[MVP]` vetting gate + ratings; bidding withheld until ratings exist (§3.2).

### 11.4 Pledge → payment drop-off
Free pledges are cheap; the gap to actually paying is where pools die. **Mitigations:** the 80%-paid rule (§6.3); consider a small **refundable pledge deposit** `[V2]` to filter tyre-kickers; keep the payment step dead simple.

### 11.5 Pricing heterogeneity
Flats differ (1 AC vs 4). A single group price is wrong. **Fixed** by per-unit pricing (`unit_count`, §9).

### 11.6 Payments & legality
Covered in §6 — the dominant existential risk. Manual escrow + a lawyer's sign-off before the pilot; no custody-in-code until licensed.

### 11.7 Notifications & verification lead time
WhatsApp Cloud API automation + SMS-OTP aggregator both need setup/verification that surprises teams late. **Mitigation:** MVP uses `wa.me` deep links + in-app; start any SMS-gateway/WhatsApp-verification paperwork in week 0 as a parallel track.

---

## 12. Open questions

**Resolved (folded into this doc):**
- Model → pooling now, bidding `[V2]`.
- Escrow → manual for pilot; aggregator-backed `[V2]`; §6.
- Partial participation → 80% paid = run.
- Bidding window → 48h default, configurable `[V2]`.
- Payout timing → T+2 after release `[V2]`.
- Vendor KYC → manual vetting gate `[MVP]`, formal KYC `[V3]`.
- Blind vs open bidding → open, `[V2]`.

**Still open (founder decisions — flag before the phase that needs them):**
1. **Legal entity** for even manual escrow — sole proprietor vs registered company? (Blocks the first payment; get legal advice.)
2. **Refundable pledge deposit** — worth the friction to cut no-shows? (Revisit after pilot drop-off data.)
3. **Society Admin incentive model** — required before `[V2]` multi-society.
4. **SMS-OTP provider** — Twilio (pricey for PK) vs a local aggregator; pick in week 0.

---

## 13. Tech stack

| Layer | Target `[V2+]` | `[MVP]` (leaner) |
|---|---|---|
| Frontend | Next.js 14 (App Router) + TS | same |
| UI | Tailwind + shadcn/ui | same |
| Server state | TanStack Query | same (also powers the polled counter) |
| Client state | Zustand | same, minimal |
| Realtime | Django Channels + Redis | **skip** — poll instead |
| Backend | Python + Django + Django REST Framework | same |
| ORM / DB | Django ORM + PostgreSQL | same |
| Cache | Redis | **only if** OTP/rate-limit needs it; else Postgres |
| Auth | JWT (`djangorestframework-simplejwt`) + phone OTP | same (local SMS gateway) |
| Payments | licensed aggregator (split settlement) | **none** — manual (§6) |
| Notifications | WhatsApp Cloud API + in-app | **`wa.me` deep links** + in-app |
| File storage | S3 / Cloudflare R2 (via `django-storages`) | R2 (proof photos only) |
| Hosting | Vercel (web) + Railway/Render (api, via Gunicorn) + Neon (db) | same |
| Repo layout | Turborepo for `apps/web` (Next.js) + a separate Django project (`apps/api`), API contract shared via an OpenAPI schema (`drf-spectacular`) generating TS types for the frontend | same, but don't over-engineer the schema-sync tooling early |

---

*End of vision. The buildable plan — epics, stories, acceptance criteria, estimates, sprints — is in [SCRUM-MVP.md](SCRUM-MVP.md).*

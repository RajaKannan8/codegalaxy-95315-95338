# DevArena Backend

DevArena Backend is the core service for DevArena, a centralized, gamified code review platform. It provides REST APIs for user management, project and repository catalog, rule enforcement, PR/bug logging, dispute mediation, rewards, gamification, and rich integrations.

## Getting Started

### Prerequisites

- Python 3.10+
- (Optional) Virtualenv

### Setup & Installation

1. **Clone this repository**  
   ```bash
   git clone <repo-url>
   cd devarena_backend
   ```

2. **Create & activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**
   ```bash
   uvicorn src.api.main:app --reload
   ```
   Visit the interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs)

### Environment Variables

All configuration in this demo is hardcoded or mocked. For production, use `.env` for DB credentials, secret keys, etc.

---

## Architecture Overview

```mermaid
graph TD
    A[Client<br/>(Frontend SPA)] -- HTTP REST --> B(FastAPI App)
    subgraph DevArena Backend
    B -- /api/v1/auth/* <br/>JWT Issues, Users --> C[Auth Router]
    B -- /api/v1/projects/* <br/>Project CRUD --> D[Projects Router]
    B -- /api/v1/bugs/* <br/>Bug Log/API --> E[Bugs Router]
    B -- /api/v1/gamification/* <br/>XP, Awards, Stats --> F[Gamification Router]
    B -- /api/v1/rules/* <br/>Rule CRUD --> G[Rules Router]
    B -- /api/v1/disputes/* <br/>Dispute Engine --> H[Disputes Router]
    B -- /api/v1/redeem/* <br/>Reward Center --> I[Redeem Router]
    B -- /api/v1/leaderboards/* --> J[Leaderboard Router]
    B -- /api/v1/notifications/* --> K[Notifications Router]
    C --> L[JWT Middleware/Access Control]
    end
    B -.->|3rd-party<br/>future| M[(VCS, Slack, Discord,<br/>ESLint)]
```

- All endpoints are secured with JWT (except `/auth`).
- Routers are modular, each handles business logic for a domain.
- CORS enabled for local cross-origin requests.
- Stubs/helpers for VCS, notification, gamification, and rule integrations.

---

## Main Modules

- **Authentication & Access Control:**  
  Register/login, role-based JWT tokens, `/api/v1/auth`.  
  _Roles_: admin, reviewer, developer.

- **Project Management:**  
  CRUD for projects/repos, role-gated, with VCS scaffold.

- **Rule Engine:**  
  CRUD for validation/enforcement rules, future integration: SonarQube/ESLint.

- **Bug Logging:**  
  Log, list, and delete bugs per project; API designed for bug tracker integrations.

- **Dispute Resolution:**  
  Raise, resolve, or delete disputes (admin only). Notification/mediation stubs.

- **Gamification:**  
  XP/awards stats, leaderboard (in-memory), event tracking.

- **Redeem Center:**  
  Rewards and redemption history; extendable for real prize fulfillment.

- **Dashboards & Leaderboards:**  
  XP and badge leaderboards available for authenticated users.

- **Notifications:**  
  Stubs for Slack, Discord, Email; extendable for async background delivery.

---

## REST API Endpoints

- `/api/v1/auth/login` – Login, get JWT token
- `/api/v1/auth/register` – Register user
- `/api/v1/auth/me` – Get current user info
- `/api/v1/projects/` – List/create/delete projects (role-based)
- `/api/v1/bugs/` – List/add/remove bugs
- `/api/v1/disputes/` – List/add/resolve/delete disputes
- `/api/v1/gamification/stats` – Get XP/level stats
- `/api/v1/gamification/awards` – Get badges
- `/api/v1/leaderboards/` – Leaderboard by XP
- `/api/v1/rules/` – PR/bug rule CRUD (admin/reviewer)
- `/api/v1/redeem/rewards` – List rewards
- `/api/v1/redeem/redeem` – Redeem reward
- `/api/v1/redeem/my-redemptions` – Redemption history
- `/api/v1/notifications/` – Admin/reviewer can push notifications

API is self-documented. Visit `/docs`.

---

## Usage Notes

- Minimal/no persistent storage: data resets on restart. See comments in source to swap in a real DB or external service.
- Extend API authentication by updating `middleware.py`.
- Integrate with real bug/PR/VCS systems by implementing stubs.
- Adjust/test role-gating in routers to match your org needs.

---

## Testing

### Recommended Test Coverage

- **Unit tests** for all routers: authentication, CRUD, and edge cases
- **Integration tests** for end-to-end flows (auth, JWT, protected endpoints)
- **Mock tests** for VCS, notification, and external integrations

Use `pytest` for tests. Place under `tests/` and run:

```bash
pytest
```

<!-- TODO: Add more detailed example tests for each router, including JWT auth and negative scenarios -->

---

## License

MIT or see repository.


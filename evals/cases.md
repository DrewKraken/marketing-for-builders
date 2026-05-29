# Evaluation cases

The raw product descriptions used to evaluate the `positioning` skill — realistic, founder-style "feature dumps." Each is fed to the skill exactly as written. All are fictional except InvoiceParser Pro (a real product, used with permission of its maker — the author).

Round 1 set (5 cases, chosen to span different product shapes):

| # | Name | Shape |
|---|------|-------|
| 1 | InvoiceParser Pro | B2B SaaS (real) |
| 2 | DeployKit | developer tool / CLI |
| 3 | Streaktastic | consumer mobile app |
| 4 | DentalFlow | vertical SaaS |
| 5 | PayBridge | payments API |

---

**1. InvoiceParser Pro** — AI-powered accounts payable automation. Extract, validate, review, and export invoice data for bookkeepers, accounting firms, and small businesses. Capabilities: AI invoice extraction (Azure Document Intelligence + GPT-4o fallback); header fields, line items, multi-rate VAT, bank/payment routing; 13-layer currency resolver incl. a SWIFT-BIC layer; ~99% accuracy, under ~5s per single-page invoice; review queue with bulk approve and per-vendor automation rules; pushes to QuickBooks Online, Xero, and Zoho Books with vendor enrichment, attach PDF, GL sync; per-vendor learning (each correction trains the next extraction); inbound email + client portal; public REST API + HMAC webhooks; multi-workspace for firms; plans from solo bookkeeper to firm.

**2. DeployKit** — a command-line tool for deploying web apps. Go, single binary, no dependencies. YAML config. Docker, rolling/blue-green/canary deploys, pre/post hooks, AWS/GCP/Azure, built-in rollback, parallel deploys over SSH, plugin system. Open source (MIT). CLI-first with an optional web dashboard. Secrets via env files or Vault.

**3. Streaktastic** — a habit-tracking app for iOS and Android (React Native). Create habits, set daily/weekly goals, track streaks. Reminders, calendar heatmap, stats, streak freezes, device sync, widget, dark mode. Freemium (free up to 3 habits; premium unlocks unlimited habits, themes, analytics). Social: friends, streaks, leaderboards.

**4. DentalFlow** — practice-management software for dental offices. Cloud web app. Drag-and-drop scheduling, SMS/email reminders, patient records and charting, treatment plans, insurance claim submission/tracking, billing, intake forms, patient portal, dashboards. Imaging-system integrations. HIPAA compliant. Role-based access. Multi-location. Per-provider pricing.

**5. PayBridge** — a payments API for developers. REST + SDKs (Python, Node, Ruby, Go, PHP). Cards, ACH, wallets. One-time charges, subscriptions, invoicing, hosted checkout, webhooks, refunds, disputes, dashboard. PCI compliant, tokenization, 135 currencies, marketplace payouts, test mode, usage-based pricing, built-in fraud detection.

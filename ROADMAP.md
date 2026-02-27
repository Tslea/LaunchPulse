# LaunchPulse — Roadmap

## Fase 1: Foundation (Settimane 1-2) ✅

Pipeline funzionante end-to-end per una singola idea.

- [x] Setup FastAPI backend con endpoint base
- [x] Integrazione Claude API per generazione PRD (structured output)
- [x] Template landing page HTML ottimizzato (single-file, <50KB, mobile-first)
- [x] Template engine con rendering placeholder e protezione XSS
- [x] Auto-deploy su Vercel via REST API
- [x] Form email con salvataggio lead su Supabase
- [x] Pipeline orchestrator (idea → PRD → landing → render → deploy)
- [x] Schema database Supabase (ideas, prds, landing_pages, deployments, leads)
- [x] Scaffold dashboard Next.js
- [x] Test suite (16 test)

---

## Fase 2: Creative + Ads (Settimane 3-4)

Automazione completa della parte advertising.

### Seedream 4 — Generazione Creative
- [ ] Client Seedream 4 via Replicate API (`backend/app/clients/seedream_client.py`)
- [ ] Prompt engineering: Claude genera prompt ottimizzati per Seedream 4 dal PRD
- [ ] Generazione 3-5 varianti per idea, formato 9:16 (1080x1920px per TikTok)
- [ ] 1 variante 16:9 (1200x630px) per OG image della landing page
- [ ] Storage immagini su Supabase Storage o S3
- [ ] Nuovo schema: tabella `creatives` (idea_id, image_url, prompt, format, variant)
- [ ] Prompt file: `backend/app/prompts/creative_generation.py`

### TikTok Ads Automation
- [ ] Setup TikTok Business account + app developer (manuale, una tantum)
- [ ] Client TikTok Marketing API (`backend/app/clients/tiktok_client.py`)
- [ ] Servizio creazione campagna (`backend/app/services/ads_service.py`):
  - Crea Campaign (obiettivo: TRAFFIC o CONVERSIONS)
  - Crea Ad Group (targeting, budget, schedule, placement)
  - Upload creative (immagini da Seedream 4)
  - Crea Ad (collega creative + copy + landing URL)
  - Attiva campagna
- [ ] Generazione ad copy con Claude: 3 varianti headline + description
- [ ] Prompt file: `backend/app/prompts/ad_copy.py`
- [ ] Endpoint: `POST /api/v1/ideas/{id}/create-campaign`
- [ ] Schema: tabella `campaigns` (idea_id, tiktok_campaign_id, status, budget, config)

### Celery + Redis
- [ ] Configurazione Celery worker (`backend/app/worker.py`)
- [ ] Attivare Redis in `docker-compose.yml`
- [ ] Migrare pipeline da sincrono ad asincrono (Celery task)
- [ ] Endpoint restituisce `202 Accepted` + task_id per polling status
- [ ] Endpoint: `GET /api/v1/pipeline/{task_id}/status`

### Aggiornamento Pipeline
- [ ] Aggiungere step 5 (creative generation) e step 6 (campaign setup) al pipeline
- [ ] Iniettare OG image generata da Seedream 4 nel template landing
- [ ] Test integrazione ads (mock TikTok API)

---

## Fase 3: Dashboard + Intelligence (Settimane 5-6)

Monitoring e decisione assistita.

### Dashboard React
- [ ] Setup completo Next.js con routing, layout, e componenti base
- [ ] Pagina **Overview**: lista idee con Pulse Score, status, budget speso
- [ ] Pagina **Idea Detail**: drill-down con grafici temporali, funnel completo
  - Funnel: Impressions → Clicks → Landing Visits → Email Signups
  - Performance per creative (quale immagine/copy performa meglio)
  - Grafici: line chart metriche nel tempo, bar chart comparativa varianti
- [ ] Pagina **Comparativa**: confronto side-by-side tra 2-4 idee
- [ ] Pagina **Decisione**: suggerimenti AI (kill / continue / scale)
- [ ] Componenti UI: card metrica, badge status, chart wrapper, tabella leads

### Pull Metriche TikTok
- [ ] Job schedulato (Celery beat) per pull metriche ogni ora
- [ ] Servizio: `backend/app/services/metrics_service.py`
- [ ] Endpoint: `GET /api/v1/ideas/{id}/metrics`
- [ ] Schema: tabella `metrics_snapshots` (idea_id, timestamp, impressions, clicks, ctr, cpc, spend)

### Pulse Score
- [ ] Implementazione formula composita:
  - CTR (25%) — rispetto a benchmark TikTok per categoria
  - Conversion Rate (30%) — email signups / landing visits
  - CPC relativo (20%) — rispetto al benchmark di settore
  - Volume signups (25%) — numero assoluto normalizzato
- [ ] Score 0-100, calcolato in tempo reale alla lettura
- [ ] Soglie: <30 = kill, 30-60 = incerto, 60-80 = promettente, >80 = forte PMF signal
- [ ] Servizio: `backend/app/services/pulse_score.py`

### Notifiche
- [ ] Alert automatici su: budget esaurito, CPC anomalo, milestone signups
- [ ] Webhook opzionale (Slack, email) per notifiche
- [ ] Kill switch automatico: ferma campagna se CPC > 3x benchmark

---

## Fase 4: Scale + Polish (Settimane 7-8)

Ottimizzazione, A/B testing, e multi-utente.

### A/B Testing Automatico
- [ ] Generazione variante B (headline + CTA alternativi) via Claude
- [ ] Split traffico 50/50 tramite parametro `?v=B` nell'URL ads
- [ ] Tracking conversioni separato per variante A vs B
- [ ] Calcolo significatività statistica (chi-squared test)
- [ ] Dashboard: visualizzazione risultati A/B con confidence interval
- [ ] Auto-winner: dopo 100+ visite per variante, disattiva la peggiore

### Iterazione Assistita
- [ ] Analisi AI delle performance: Claude analizza metriche e suggerisce miglioramenti
- [ ] Suggerimenti specifici: nuova headline, diverso angolo creativo, target diverso
- [ ] Endpoint: `POST /api/v1/ideas/{id}/iterate` — lancia nuova iterazione con varianti
- [ ] Storico iterazioni con confronto performance tra versioni

### Multi-Canale (oltre TikTok)
- [ ] Client Meta Ads API (`backend/app/clients/meta_client.py`)
- [ ] Client Google Ads API (`backend/app/clients/google_client.py`)
- [ ] Adattamento formato creative per ogni piattaforma:
  - TikTok: 9:16 (1080x1920)
  - Meta/Instagram: 1:1 (1080x1080) + 9:16 per Stories
  - Google: 1.91:1 (1200x628) per Display
- [ ] Dashboard comparativa cross-canale

### Autenticazione + Multi-Tenancy
- [ ] Integrazione Supabase Auth (magic link o OAuth)
- [ ] Middleware autenticazione FastAPI
- [ ] Row Level Security su tutte le tabelle (user_id)
- [ ] Isolamento dati tra utenti
- [ ] Pagina login/signup nel dashboard

### Onboarding
- [ ] Flow guidato per nuovi utenti:
  1. Connetti account TikTok Ads
  2. Configura budget default e target geo
  3. Inserisci prima idea
  4. Tutorial interattivo del pipeline
- [ ] Wizard step-by-step nel dashboard

---

## Costi di Riferimento

| Voce | Per Idea | 10 Idee/Mese |
|------|----------|--------------|
| Claude API (PRD + Landing + Copy) | ~€0.09 | ~€0.90 |
| Seedream 4 (5 immagini) | ~€0.20 | ~€2.00 |
| Vercel hosting | Gratis | Gratis |
| Supabase | Gratis | Gratis |
| **Infrastruttura totale** | **~€0.30** | **~€3.00** |
| TikTok Ads (5 giorni × €7/giorno) | ~€35 | ~€350 |
| **TOTALE** | **~€35.30** | **~€353** |

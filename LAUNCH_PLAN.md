# IncuBrix 30-Day Multi-Channel Growth Launch Kit
## Production Execution Plan for Day-One Deployment

**Organization**: IncuBrix Private Limited  
**Target Function**: Growth Engineering & Outbound GTM  
**Document Status**: Ready for Immediate Execution Next Monday  

---

### 1. Executive Summary & Strategy

This Launch Kit provides a turnkey, 30-day outbound execution plan designed for IncuBrix to begin contacting verified creators immediately.

The strategy combines **high-precision creator segmentation** (podcasters with backlogs and expert educators) with **multi-channel touchpoints** (Email, LinkedIn, Instagram/X) and a **Done-For-You preview asset hook**, maximizing response rates while preserving 100% domain and account health.

---

### 2. Multi-Channel Safe Volume & Deliverability Limits

To safeguard domain reputation, prevent platform rate limits, and maintain high inbox placement, daily outreach volumes are strictly throttled per channel:

| Channel | Safe Daily Volume / Account | Multi-Account Scaling Target | Sending Window & Cadence | Deliverability Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **Cold Email** | 25-30 emails / mailbox / day | 4 mailboxes = **100-120 emails / day** | Mon - Fri, 08:30 - 17:30 recipient local time | DKIM, SPF, DMARC enforced; 14-day mailbox warm-up; plain text + 1 preview link. |
| **LinkedIn** | 15-20 connection requests / day | 2 accounts = **30-40 touchpoints / day** | Mon - Sat, staggered 4-8 min delays | Personal profile with creator badge; 1-on-1 personalized note referencing recent episode. |
| **Instagram DM** | 12-15 DMs / handle / day | 2 handles = **25-30 DMs / day** | Mon - Sun, evening peak (18:00 - 21:00) | Only DM active creator accounts with bio business inquiries; reference latest Reel. |
| **X (Twitter) DM** | 15-20 DMs / handle / day | 1 handle = **15-20 DMs / day** | Mon - Fri, business hours | Verified organization badge; no link in initial DM (ask permission first). |
| **Aggregate Daily** | — | **170 - 210 touches / day** | **~850 - 1,050 creators / week** | **3-channel sequence with 2 follow-ups on Priority A.** |

---

### 3. Step-by-Step 30-Day Execution Roadmap

```
+---------------------------------------------------------------------------------------------------+
| WEEK 1: INFRASTRUCTURE HARDENING & PILOT OUTREACH                                                 |
+---------------------------------------------------------------------------------------------------+
| • Owner: Growth Engineer & Head of Outbound                                                       |
| • Operational Steps:                                                                              |
|   1. Domain & DNS Provisioning: Connect 3 secondary sending domains (e.g., tryincubrix.com,       |
|      incubrixapp.com) to Google Workspace. Configure SPF, DKIM, and DMARC policies.              |
|   2. Mailbox Warmup: Initiate warmup sequencing via Instantly / Smartlead at 15 warmups/day.      |
|   3. Lead Ingestion: Run `python -m src.cli run --target 1000` to refresh the latest 1,000       |
|      verified leads and verify 25 Priority A sequences.                                           |
|   4. Preview Asset Generation: Pre-render 25 60-second vertical preview clips for Priority A      |
|      creators at `https://incubrix.com/preview/{creator_id}`.                                     |
|   5. Pilot Deployment: Dispatch Day 1 touchpoints to the top 25 Priority A creators.              |
| • Volume: 25 Priority A leads (Email + LinkedIn).                                                 |
| • Milestone: 100% inbox placement verified, 0 spam complaints, first 4 replies logged.            |
+---------------------------------------------------------------------------------------------------+
```

```
+---------------------------------------------------------------------------------------------------+
| WEEK 2: FULL MULTI-CHANNEL RAMP & FIRST FOLLOW-UPS                                                |
+---------------------------------------------------------------------------------------------------+
| • Owner: Growth Engineer & SDR                                                                    |
| • Operational Steps:                                                                              |
|   1. Scale Email Volume: Increase daily sending volume to 50 emails/day across warmed mailboxes.  |
|   2. Launch LinkedIn InMail & Connection Flow: Trigger 20 personalized connection requests/day     |
|      for expert-led creators.                                                                     |
|   3. Trigger Priority A Step 2: Dispatch Follow-up 1 (Day 4 preview clip demo link) to all      |
|      unresponsive Priority A leads.                                                               |
|   4. Instagram DM Pilot: Initiate 15 daily DMs to video-first YouTubers and podcasters.           |
|   5. CRM Sync: Sync lead status and replies into HubSpot/Close CRM.                              |
| • Volume: 250 leads contacted; 25 Step 2 follow-ups sent.                                         |
| • Milestone: First 8 discovery demo calls scheduled.                                              |
+---------------------------------------------------------------------------------------------------+
```

```
+---------------------------------------------------------------------------------------------------+
| WEEK 3: OPTIMIZATION, BACKLOG ANGLE & STEP 3 PIVOTS                                               |
+---------------------------------------------------------------------------------------------------+
| • Owner: Growth Engineer & Account Executive                                                      |
| • Operational Steps:                                                                              |
|   1. Full Outbound Throughput: Scale email to 100/day and social DMs to 35/day.                    |
|   2. Trigger Priority A Step 3: Dispatch Follow-up 2 on backup channel (Day 8 graceful close)     |
|      to finalize Priority A sequences.                                                            |
|   3. Deploy "Backlog Clearance" Angle: Run specialized campaign targeting creators with >50       |
|      episodes offering instant archive repurposing.                                              |
|   4. A/B Copy Testing: Measure plain text pitch vs. Done-For-You preview asset link across       |
|      100 randomized leads.                                                                        |
| • Volume: 500 cumulative leads contacted; 150 follow-ups dispatched.                              |
| • Milestone: 22 discovery calls completed; 8 paying pilot trials started.                         |
+---------------------------------------------------------------------------------------------------+
```

```
+---------------------------------------------------------------------------------------------------+
| WEEK 4: CONVERSION, RERUN REFRESH & EXPANSION                                                     |
+---------------------------------------------------------------------------------------------------+
| • Owner: Full Growth Team                                                                         |
| • Operational Steps:                                                                              |
|   1. Pipeline Refresh: Execute `python -m src.cli refresh` to ingest 1,000 fresh creators and     |
|      update existing lead interaction dates with 0 duplicates.                                    |
|   2. Convert Trial Pilots: Transition Week 2 & 3 trial activations into annual studio subscriptions |
|      ($199/mo or $1,999/yr).                                                                      |
|   3. Expansion to 5,000 Leads: Deploy exceptional target pipeline across additional categories     |
|      (AI, Finance, Coding, Design).                                                               |
|   4. Executive GTM Review: Present CAC, reply rate, and ARR metrics to IncuBrix leadership.       |
| • Volume: 1,000+ total leads contacted; full sequence completion.                                 |
| • Milestone: 160 replies, 45 demos booked, 18 paid subscription commitments ($35k+ ARR pipeline).|
+---------------------------------------------------------------------------------------------------+
```

---

### 4. Channel Responsiveness & Mix Recommendation

Based on response data across creator archetypes:

```
+--------------------+-----------------------+---------------------+-------------------+
| Creator Segment    | Primary Channel (Best)| Backup Channel      | Expected Reply %  |
+--------------------+-----------------------+---------------------+-------------------+
| Podcasters         | Business Email (65%)  | LinkedIn / X (35%)  | 14.5% - 18.2%     |
| Video-First (YT)   | Instagram DM (50%)    | Business Email (50%)| 12.0% - 15.8%     |
| Expert-Led         | LinkedIn InMail (60%) | Email (40%)         | 18.0% - 24.5%     |
+--------------------+-----------------------+---------------------+-------------------+
```

**Recommendation**: Allocate outreach budget and daily time:
- **Email (50%)**: Broadest reach, lowest friction, automated tracking.
- **LinkedIn (30%)**: Highest ticket value ($999/yr expert creators).
- **Instagram/X (20%)**: High engagement for fast-growing video podcasters.

---

### 5. Tooling Stack & Monthly Budget

| Tool / Service | Purpose | Monthly Cost | Owner |
| :--- | :--- | :--- | :--- |
| **IncuBrix Growth Engine** | Discovery, verification, deduplication, scoring, outreach drafting | **$0.00** (Open Source Python/SQLite) | Growth Engineer |
| **Secondary Domains (x3)** | Dedicated cold outreach domains | **$3.00/mo** ($36/yr on Cloudflare) | Growth Engineer |
| **Google Workspace (x3)** | Professional mailboxes for cold sending | **$18.00/mo** ($6/user/mo) | Operations |
| **Instantly / Smartlead** | Mailbox warmup and sending automation | **$37.00/mo** | Growth Engineer |
| **HubSpot CRM (Starter)** | Pipeline tracking and deal management | **$20.00/mo** | Sales / AE |
| **Total Monthly Investment** | Full-scale multi-channel infrastructure | **$78.00 / month** | — |

*Direct cost per qualified lead: **<$0.08**.*

---

### 6. Targets After 30 Days (Quantified Model)

| Metric | Conservative | Target (Expected) | Stretch (Exceptional) |
| :--- | :--- | :--- | :--- |
| **Unique Qualified Creators Contacted** | 800 | **1,000** | 2,500 |
| **Cumulative Multi-Channel Touches** | 2,000 | **2,800** | 7,000 |
| **Open Rate (Email)** | 38.0% | **46.5%** | 52.0% |
| **Positive Reply Rate** | 11.0% | **16.0%** (160 replies) | 19.5% |
| **Discovery Demos Booked** | 30 | **45 meetings** | 110 meetings |
| **Demo-to-Trial Conversion** | 35.0% | **40.0%** (18 trials) | 48.0% |
| **Closed ARR Pipeline** | $18,000 | **$35,800 ARR** | $85,000+ ARR |

---

### 7. Risk Matrix & Mitigation Protocol

1. **Risk: Mailbox Domain Blacklisting / Spam Placement**
   - *Mitigation*: Hard cap of 30 cold emails per domain per day; secondary domains used exclusively (never email from `incubrix.com` root domain); automated warmup running continuously; mandatory opt-out in every message.
2. **Risk: Creator Burnout / Negative Social Backlash**
   - *Mitigation*: 100% individualized personalization hooks (referencing specific content titles); zero bulk automated messaging on platforms where prohibited; respectful graceful opt-out after 3 touches.
3. **Risk: API Rate-Limiting or Source Deprecation**
   - *Mitigation*: The engine is decoupled from any single API. If Apple Podcasts rate-limits, the engine falls back seamlessly to RSS feed parsing, local JSON/CSV seed registries, and web scraping with exponential backoff.

---

### 8. IncuBrix Company Deliverables Required Next Monday

To initiate outreach on Monday morning, IncuBrix leadership must provide:
1. **Access to 3 Google Workspace seats** on secondary sending domains.
2. **Internal API endpoint or token** for generating shareable 60-second video clip preview links (`https://incubrix.com/preview/{creator_id}`).
3. **Designated Account Executive / Founder calendar link** (Cal.com / Calendly) for demo booking integrations.

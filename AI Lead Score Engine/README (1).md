# 🧠 AI Lead Scoring Engine

A production-ready machine learning system to score and rank leads based on user behavior, engagement, and demographics. Integrates with CRM/WhatsApp for real-time lead intelligence.

---

## 📊 Project Overview

This project builds an **AI-powered Lead Scoring System** using:
- Gradient Boosted Trees for prediction
- LLM (optional) for post-ranking
- Real-time API inference with FastAPI
- Monitoring via `evidently`
- PII masking and compliance readiness

---

## 🛠️ Features

- ⏱ Real-time scoring API (`< 300ms` latency)
- 🔐 Data privacy with PII masking (email, phone)
- ✅ Model monitoring with drift detection
- 📥 Batch inference + CRM Push (WhatsApp/Hubspot etc.)
- 📈 Lead ranking dashboard

---

## 🚀 Demo (Synthetic Dataset)

| Lead ID | Intent Score | Sentiment | CTA Clicks |
|---------|--------------|-----------|------------|
| LEAD1001 | 0.91        | 0.88      | 4          |
| LEAD1042 | 0.87        | 0.52      | 5          |

---

## 🧬 Dataset Columns

- `avg_session_duration`, `clicks_on_cta`, `recent_activity_gap_hours`
- `user_age_group`, `location_tier`, `occupation_type`
- `ad_click_origin`, `products_viewed_count`, `last_message_sentiment`
- `days_since_first_contact`, `intent_score`

---

## 🏗️ Architecture

```
Client → FastAPI → Model (GBDT) → Post-Processing (LLM optional) → CRM/Webhook
                                   ↓
                            Monitoring (Evidently)
```

---

## 📦 Installation

```bash
git clone https://github.com/yourname/lead-scoring-engine.git
cd lead-scoring-engine
pip install -r requirements.txt
```

---

## ⚙️ Run the API

```bash
uvicorn main:app --reload --port 8000
```

Send POST request to `/predict` with features like:
```json
{
  "clicks_on_cta": 3,
  "products_viewed_count": 5,
  "last_message_sentiment": 0.6,
  ...
}
```

---

## 📉 Monitoring Drift

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
report.run(reference_data=ref_df, current_data=latest_batch)
report.save_html("drift_report.html")
```

---

## 📈 Business KPIs

- Conversion Lift (vs baseline)
- High-intent Leads Identified (Top 10%)
- Time to Response (post-score)
- Sales Team Feedback

---

## 📃 License

[MIT License](LICENSE)
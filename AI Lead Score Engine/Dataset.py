import pandas as pd
import numpy as np
import random

# Seed for reproducibility
np.random.seed(42)

# Constants
n_samples = 500

# Helper data
age_groups = ['18-25', '26-35', '36-50']
location_tiers = ['Tier 1', 'Tier 2', 'Tier 3']
occupation_types = ['student', 'salaried', 'self-employed']
ad_sources = ['Google Ads', 'Meta Ads', 'Organic', 'WhatsApp']

# Generate synthetic data
data = {
    'lead_id': [f'LEAD{1000+i}' for i in range(n_samples)],
    'avg_session_duration': np.round(np.random.normal(120, 30, n_samples), 2),
    'clicks_on_cta': np.random.poisson(2, n_samples),
    'recent_activity_gap_hours': np.round(np.random.exponential(24, n_samples), 1),
    'user_age_group': np.random.choice(age_groups, n_samples),
    'location_tier': np.random.choice(location_tiers, n_samples),
    'occupation_type': np.random.choice(occupation_types, n_samples),
    'ad_click_origin': np.random.choice(ad_sources, n_samples),
    'products_viewed_count': np.random.randint(1, 15, n_samples),
    'last_message_sentiment': np.round(np.random.uniform(-1, 1, n_samples), 2),
    'days_since_first_contact': np.random.randint(1, 30, n_samples),
}

# Simulate intent_score
intent_score = (
    0.3 * (data['clicks_on_cta']) +
    0.2 * (15 - data['recent_activity_gap_hours']) +
    0.2 * (data['products_viewed_count']) +
    0.1 * (np.array(data['last_message_sentiment']) * 10) +
    0.2 * (30 - np.array(data['days_since_first_contact']))
)
intent_score = (intent_score - np.min(intent_score)) / (np.max(intent_score) - np.min(intent_score))
data['intent_score'] = np.round(intent_score, 3)

# Create DataFrame
df = pd.DataFrame(data)

# Add 'consent_given' (90% True, 10% False)
df['consent_given'] = np.random.choice([True, False], size=n_samples, p=[0.9, 0.1])

# Add 'email'
df['email'] = df['lead_id'].apply(lambda x: f"{x.lower()}@example.com")

# Add 'phone_number'
def generate_phone():
    return str(random.choice([9, 8, 7])) + ''.join([str(random.randint(0, 9)) for _ in range(9)])
df['phone_number'] = [generate_phone() for _ in range(n_samples)]

# Save to CSV
df.to_csv("synthetic_lead_data.csv", index=False)

print("✅ Synthetic dataset generated: synthetic_lead_data.csv")

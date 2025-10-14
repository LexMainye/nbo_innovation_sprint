### WER & CER Results by Etiology 

| Etiology | WER Mean | Count | CER Mean | Count |
| :--- | :--- | :--- | :--- | :--- |
| Cerebral Palsy | 0.22 | 62 | 0.12 | 62 |
| Multiple Sclerosis (MS) | 0.11 | 94 | 0.06 | 94 |
| Neurological disorder | 0.19 | 32 | 0.13 | 32 |
| Parkinson’s Disease | 0.22 | 60 | 0.15 | 60 |

### Summary of Findings (Development Set)

This table summarizes the model's performance on the development set, grouped by the speaker's underlying condition (etiology).

- **Highest Error Rates**: Speakers with **Cerebral Palsy** and **Parkinson's Disease** presented the most significant challenge for the model, both showing the highest Word Error Rate (WER) of **0.22**. Parkinson's Disease also had the highest Character Error Rate (CER) at **0.15**.
- **Best Performance**: The model performed best on speech from the speaker with **Multiple Sclerosis (MS)**, achieving a significantly lower WER of **0.11** and CER of **0.06**.
- **Sample Size**: It's important to note the variation in sample sizes. The `Neurological disorder` category has the smallest sample count (32), which may affect the reliability of its aggregated metrics compared to `Multiple Sclerosis (MS)` with 94 samples.
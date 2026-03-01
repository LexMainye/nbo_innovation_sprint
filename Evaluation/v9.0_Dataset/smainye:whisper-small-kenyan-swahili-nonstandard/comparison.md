# Comparison: Dev vs. Test Set Performance

This report compares the performance of the `smainye/whisper-small-kenyan-swahili-nonstandard` model on the **Development Set** versus the **Test Set**.

## 1. Overall Performance Comparison

| Metric | Development Set | Test Set | Difference (Dev -> Test) |
| :--- | :--- | :--- | :--- |
| **Examples** | 272 | 554 | +282 examples |
| **Overall WER** | 0.356 (35.6%) | 0.300 (30.0%) | **-5.6% (Improvement)** |
| **Overall CER** | 0.151 (15.1%) | 0.119 (11.9%) | **-3.2% (Improvement)** |

### Key Insight
The model performs **significantly better on the Test set** (30% WER) compared to the Development set (35.6% WER). This is a positive indicator that the model generalizes well to unseen data, or that the Test set might be slightly less challenging (e.g., better audio quality or less severe speech impairments on average).

---

## 2. Severity Trend Analysis

| Severity | Dev WER | Test WER | Trend Consistency |
| :--- | :--- | :--- | :--- |
| **Mild** | 0.33 | 0.25 | **Improved** |
| **Moderate** | 0.45 | 0.32 | **Improved** |
| **Severe** | 0.28 | 0.35 | **Degraded** |

### Key Insight
*   **Correction of Trend:** In the **Development Set**, we observed an anomaly where "Severe" speech had better recognition (0.28) than "Mild" (0.33) and "Moderate" (0.45).
*   **Test Set Normalization:** The **Test Set** results follow a more expected pattern: **Mild (0.25) < Moderate (0.32) < Severe (0.35)**. This confirms that the Dev set anomaly was likely due to specific speaker outliers (e.g., `KES006`).
*   **Severe Drop:** While Mild and Moderate performance improved significantly in the Test set, performance on **Severe** cases actually dropped (0.28 -> 0.35), suggesting the Test set contains more challenging "severe" examples.

---

## 3. Etiology Comparison (WER)

| Etiology | Dev WER | Test WER |
| :--- | :--- | :--- |
| **Cerebral Palsy** | 0.40 | 0.34 |
| **Multiple Sclerosis (MS)** | 0.09 | 0.36 |
| **Neurodevelopmental disorder** | 0.42 | 0.30 |
| **Parkinson’s Disease** | 0.39 | 0.18 |

### Key Insight
*   **Parkinson's Improvement:** There is a drastic improvement for **Parkinson’s Disease** (39% -> 18% WER), likely due to speaker differences (Dev: KES020 vs Test: KES021).
*   **MS Degradation:** **Multiple Sclerosis** shows a significant degradation (9% -> 36% WER). In the Dev set, the MS speaker (`KES018`) was the top performer, whereas the Test set MS speaker (`KES035`) presented more difficulty.
*   **Consistency:** **Cerebral Palsy** and **Neurodevelopmental disorders** show consistent improvements (6-12% drop in WER), aligning with the overall positive trend.

---

## Summary
The **Test Set evaluation validates the model's capability**, showing a stronger overall performance (30% WER). The "severity anomaly" seen in the Dev set has been resolved, providing a more reliable baseline for how the model handles different levels of speech impairment. However, the high variability between speakers within the same etiology (e.g., MS and Parkinson's) highlights that **individual speaker characteristics** remain the biggest driver of performance variance.

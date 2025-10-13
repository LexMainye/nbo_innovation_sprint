# Comparing My Dev and Test Set Results for the Whisper Small Model

## 1. My Introduction

In this document, I'm comparing the results from my evaluation of the `openai/whisper-small` model across both the **development (dev) set** and the **test set**. My goal is to see how well the baseline model's performance holds up on unseen data and to solidify my understanding of its limitations before I move on to fine-tuning.

From my initial analyses, I've concluded that the main challenge is a **domain mismatch**: the standard Whisper model simply isn't trained for the unique acoustic patterns of non-standard Swahili speech. This comparison is the final step in confirming that finding.

---

## 2. My Overall Performance Comparison

When I put the overall numbers side-by-side, I saw a notable improvement from the dev set to the test set. The average Word Error Rate (WER) dropped by about 10 percentage points, and the Character Error Rate (CER) saw an even bigger improvement. While this is a positive sign, an 83.7% WER is still extremely high and confirms the model isn't usable for this task in its current state. The improvement does suggest, however, that the test set might have been slightly less challenging than the dev set.

| Metric                      | My Dev Set Results | My Test Set Results |
| :-------------------------- | :----------------: | :-----------------: |
| **Avg. Word Error Rate (WER)** |       93.6%        |      **83.7%** |
| **Avg. Character Error Rate (CER)**|       50.0%        |      **32.8%** |

---

## 3. Performance Comparison by Etiology

This is where I found the most interesting variations. In my dev set, the model performed best on speakers with Multiple Sclerosis (MS). However, in the test set, the best performance was on speakers with Parkinson's Disease. This shift tells me that the model's performance is highly sensitive to the specific speakers and acoustic patterns present in each data split, rather than being generally better at one condition over another.

| Etiology                    | Dev Set CER | Test Set CER | Dev Set WER | Test Set WER |
| :-------------------------- | :---------: | :----------: | :---------: | :----------: |
| Cerebral Palsy              |    40.0%    |    39.0%     |    93.0%    |    88.0%     |
| Multiple Sclerosis (MS)     |  **26.0%** |    38.0%     |  **84.0%** |    90.0%     |
| Parkinson’s Disease         |    48.0%    |  **21.0%** |    94.0%    |  **78.0%** |
| Neurological / Neurodev.    |    60.0%    |    34.0%     |    91.0%    |    82.0%     |

---

## 4. Performance Comparison by Severity

The trend I saw here was consistent across both sets. As the severity of the speech impairment increased, so did the error rates. This was entirely expected and confirms that the standard model is not robust to more significant deviations from typical speech. The performance on "mild" cases was significantly better than on "severe" cases in both evaluations, which gives me a good starting point for my fine-tuning experiments.

| Severity | Dev Set CER | Test Set CER | Dev Set WER | Test Set WER |
| :------- | :---------: | :----------: | :---------: | :----------: |
| Mild     |    35.0%    |  **28.0%** |    88.0%    |  **78.0%** |
| Moderate |    46.0%    |    36.0%     |    90.0%    |    89.0%     |
| Severe   |    55.0%    |    40.0%     |    95.0%    |    89.0%     |

---

## 5. My Final Conclusion and Next Steps

After comparing both sets, my main conclusion is solidified: the `openai/whisper-small` model needs to be fine-tuned. The fact that its performance was inconsistent on specific etiologies but consistent on severity trends gives me valuable information. The model is clearly struggling with the *domain* of non-standard speech itself.

The improvement I saw in the test set is encouraging, as it suggests that with proper training, the model can learn these difficult patterns. My analysis of these baseline results is now complete, and my path forward is clear. I will now proceed with my plan to fine-tune the model directly on my Swahili non-standard speech dataset.
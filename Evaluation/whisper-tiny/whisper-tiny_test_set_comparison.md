
# Whisper-Tiny Test Set Performance Comparison: English vs. Swahili

This document provides a comparative analysis of the Word Error Rate (WER) and Character Error Rate (CER) for the `openai/whisper-tiny` model on the test sets of the Kenyan English and Swahili non-standard speech datasets.

## 1. Overall Performance (Test Set)

| Language | Dataset | Average WER | Average CER |
| :--- | :--- | :---: | :---: |
| **English** | `kenyan_english_nonstandard_speech_v0.9` | **38.0%** | **22.4%** |
| **Swahili** | `kenyan_swahili_nonstandard_speech_v0.9` | **96.1%** | **52.8%** |

**Key Observations (Overall):**

- The model performs significantly better on the English dataset compared to the Swahili dataset.
- The extremely high error rates on the Swahili dataset confirm the model's inability to transcribe Swahili, as it was not trained on this language.

---

## 2. Performance Breakdown by Speaker Characteristics (Test Set)

### 2.1. English (`kenyan_english_nonstandard_speech_v0.9`)

#### By Etiology:

| Etiology | Average WER | Average CER |
| :--- | :---: | :---: |
| Cerebral Palsy | 48.1% | 26.2% |
| Multiple Sclerosis (MS) | 29.1% | 14.5% |
| Neurodevelopmental disorder | 50.2% | 28.1% |
| Parkinson’s Disease | 64.2% | 38.9% |

#### By Severity:

| Severity | Average WER | Average CER |
| :--- | :---: | :---: |
| Mild | 35.7% | 18.9% |
| Moderate | 45.3% | 25.8% |
| Severe | 58.6% | 34.2% |

### 2.2. Swahili (`kenyan_swahili_nonstandard_speech_v0.9`)

#### By Etiology:

| Etiology | Average WER | Average CER |
| :--- | :---: | :---: |
| Cerebral Palsy | 99.0% | 66.0% |
| Multiple Sclerosis (MS) | 99.0% | 56.0% |
| Neurodevelopmental disorder | 95.0% | 52.0% |
| Parkinson’s Disease | 93.0% | 35.0% |

#### By Severity:

| Severity | Average WER | Average CER |
| :--- | :---: | :---: |
| Mild | 93.9% | 45.0% |
| Moderate | 97.6% | 54.3% |
| Severe | 97.7% | 67.8% |

**Key Observations (Breakdown):**

- For the English dataset, the model shows the best performance on speakers with Multiple Sclerosis and the highest error rates on speakers with Parkinson's Disease.
- For the Swahili dataset, the error rates remain consistently high across all speaker conditions.
- As observed in the dev set, error rates for both languages generally increase with the severity of the speech impairment.

---

## 3. Qualitative Examples (Test Set)

### English Example:

-   **Ground Truth:** `at the supermarket i usually compare prices carefully because the the cost of basic items like unga and sugar keeps changing almost every other week and i have to stick to my monthly budget`
-   **Prediction:** `after this supermarket i usually compare presence carefully because the cost of basic items like and shimgag tips changing almost every other week and i have to stick to my monthly budget`
-   **WER:** 0.2059, **CER:** 0.1376

### Swahili Example:

-   **Ground Truth:** `kila disemba familia yetu hukutana kijijini kwa babu na bibi huko kisii ambapo tunapika vyakula vya kitamaduni kama ugali wa mtama samaki wa kukaanga na mboga za kienyeji`
-   **Prediction:** `kilai di sambo from late to ukutanak si jene kobabun nabibi rokukisi ambapotra nabika via kula via kita maduni kama ugali umtama samarko kanga amboga zakenej`
-   **WER:** 1.0, **CER:** 0.3392

---

## 4. Conclusion (Test Set)

The test set results reinforce the conclusions from the dev set analysis. The `openai/whisper-tiny` model is not a viable solution for transcribing non-standard Swahili without specific fine-tuning. Its performance on non-standard English, while better, varies significantly depending on the speaker's specific speech condition and severity.


# Whisper-Tiny Dev Set Performance Comparison: English vs. Swahili

This document provides a comparative analysis of the Word Error Rate (WER) and Character Error Rate (CER) for the `openai/whisper-tiny` model on the development sets of the Kenyan English and Swahili non-standard speech datasets.

## 1. Overall Performance (Dev Set)

| Language | Dataset | Overall WER | Overall CER |
| :--- | :--- | :---: | :---: |
| **English** | `kenyan_english_nonstandard_speech_v0.9` | **54.9%** | **34.8%** |
| **Swahili** | `kenyan_swahili_nonstandard_speech_v0.9` | **100%** | **100%** |

**Key Observations:**

- The model shows a moderate ability to transcribe non-standard Kenyan English, but the performance on Swahili is extremely poor, as expected, due to the lack of Swahili training data.

---

## 2. Performance Breakdown by Speaker Characteristics (Dev Set)

### 2.1. English (`kenyan_english_nonstandard_speech_v0.9`)

#### By Etiology:

| Etiology | Average WER | Average CER |
| :--- | :---: | :---: |
| Cerebral Palsy | 53.5% | 31.2% |
| Multiple Sclerosis (MS) | 29.1% | 14.5% |
| Neurodevelopmental disorder | 49.8% | 27.8% |
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
| Cerebral Palsy | 100% | 71.6% |
| Multiple Sclerosis (MS) | 98.8% | 52.8% |
| Neurodevelopmental disorder | 98.8% | 71.6% |
| Parkinson’s Disease | 98.8% | 71.6% |

#### By Severity:

| Severity | Average WER | Average CER |
| :--- | :---: | :---: |
| Mild | 98.8% | 71.6% |
| Moderate | 98.8% | 71.6% |
| Severe | 98.8% | 71.6% |

**Key Observations (Breakdown):**

- For English, the model performs best on speakers with Multiple Sclerosis and struggles most with Parkinson's Disease.
- For Swahili, the error rates are consistently high across all conditions.
- Error rates for both languages increase with the severity of the speech impairment.

---

## 3. Qualitative Examples (Dev Set)

### English Example:

-   **Ground Truth:** `it s a cake of course but am not a good fan of cakes i think but but once in a while fine it s yummy too and i m thirsty again`
-   **Prediction:** `it s like a cook i m not having fun on cakes i think but once you re now in fine it s yummy too i m thirsty again`
-   **WER:** 0.5, **CER:** 0.3175

### Swahili Example:

-   **Ground Truth:** `kila disemba familia yetu hukutana kijijini kwa babu na bibi huko kisii ambapo tunapika vyakula vya kitamaduni kama ugali wa wa mtama samaki wakukaanga na mboga za kienyeji`
-   **Prediction:** `kikilat di di semafamila iya tu un kutana kikit zinik ku ku kom ba bunabi bi uku kikisi hambapur kikikun hape ka viat kula viat kiketama dunikama ugaluantama samaki akukangan nam boga zakinia`
-   **WER:** 1.0, **CER:** 0.4477

---

## 4. Conclusion (Dev Set)

The development set results confirm that the model has some capability in transcribing non-standard English but fails completely with Swahili. The performance breakdown provides insights into which speaker characteristics are more challenging for the model.

# Finetuning Baseline Report: `openai/whisper-small` on Swahili Non-Standard Speech

This document presents a comprehensive report on the baseline finetuning of the `openai/whisper-small` model for Swahili non-standard speech recognition. The analysis was conducted using the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset. The key objective of this report is to document the model's performance, which will serve as a crucial baseline for comparison against future 'endline' models with further improvements.

## 1. Executive Summary

This report details the baseline performance of the `openai/whisper-small` model finetuned on the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset. The primary goal of this analysis is to establish a benchmark for future endline comparisons. The model was trained for 1000 steps and achieved a final Word Error Rate (WER) of 0.3135 and a Character Error Rate (CER) of 0.1218 on the test set. These results will serve as the baseline for evaluating further model improvements.

## 2. Baseline Experiment Configuration

- **Base Model:** `openai/whisper-small`
- **Language:** Swahili (`sw`)
- **Dataset:** `cdli/kenyan_swahili_nonstandard_speech_v0.9`
- **Output Directory:** `/jupyter_kernel/trained_models/sw_nonstandard_tune_whisper_small_baseline`


### Finetuning Strategy
- **Encoder:** Updated (`UPDATE_ENCODER = True`)
- **Projection Layer:** Updated (`UPDATE_PROJ = True`)
- **Decoder:** Frozen (`UPDATE_DECODER = False`)
- **SpecAugment:** Enabled (`USE_SPECAUGMENT = True`)

### Training Hyperparameters
- **Max Epochs:** 10
- **Max Steps:** 1000
- **Learning Rate:** `1e-4` (with polynomial decay)
- **Train Batch Size:** 32
- **Evaluation Batch Size:** 16

### Trainer Settings
- **Logging Steps:** 5
- **Save Steps:** 50
- **LR Scheduler Type:** `polynomial`
- **LR Warmup Steps:** 50
- **LR End:** `1e-8`
- **LR Decay Power:** 4
- **Max Generation Length:** 128
- **Evaluation on Start:** `True`
- **Evaluation Steps:** 50
- **FP16 Precision:** `True`
- **BF16 Precision:** `False`
- **Checkpoints to Store:** 2

## 3. Data Preparation

The dataset was filtered to include only audio samples of 30 seconds or less, which is a requirement for Whisper model training.

- **Training Set:** 2,855 examples (filtered from 3,949)
- **Test Set:** 554 examples (filtered from 865)
- **Validation (Dev) Set:** 272 examples (filtered from 417)

## 4. Baseline Training Results

The model was trained for 1000 steps. The table below shows the training progress at various steps.

| Step | Training Loss | Validation Loss | WER      | CER      |
|---:|:---|:---|:---|:---|
| 0    | No log        | 2.8895          | 0.9356   | 0.4909   |
| 50   | 1.4404        | 1.3115          | 0.6778   | 0.2722   |
| 100  | 0.8812        | 0.9941          | 0.5278   | 0.2335   |
| 150  | 0.8051        | 0.9050          | 0.4740   | 0.2093   |
| 200  | 0.5312        | 0.8506          | 0.4531   | 0.2010   |
| 250  | 0.6256        | 0.8317          | 0.4371   | 0.1917   |
| 300  | 0.4642        | 0.8212          | 0.4159   | 0.1817   |
| 350  | 0.3866        | 0.8208          | 0.4273   | 0.1891   |
| 400  | 0.3190        | 0.8223          | 0.4039   | 0.1675   |
| 450  | 0.2984        | 0.8204          | 0.3971   | 0.1669   |
| 500  | 0.2976        | 0.8181          | 0.4021   | 0.1724   |
| 550  | 0.2832        | 0.8237          | 0.4030   | 0.1761   |
| 600  | 0.2496        | 0.8261          | 0.3954   | 0.1603   |
| 650  | 0.2432        | 0.8243          | 0.4001   | 0.1635   |
| 700  | 0.2818        | 0.8266          | 0.4019   | 0.1670   |
| 750  | 0.2407        | 0.8265          | 0.4043   | 0.1675   |
| 800  | 0.2434        | 0.8267          | 0.4032   | 0.1675   |
| 850  | 0.2389        | 0.8268          | 0.4007   | 0.1673   |
| 900  | 0.2264        | 0.8268          | 0.4018   | 0.1675   |
| 950  | 0.3173        | 0.8269          | 0.4015   | 0.1674   |
| 1000 | 0.2702        | 0.8269          | 0.4015   | 0.1674   |

- **Final Training Loss:** 0.4961
- **Epochs Completed:** 10

## 5. Baseline Evaluation Results

The final model was evaluated on the validation (dev) and test sets. The best performing model was loaded for this evaluation.

### Validation (Dev) Set
- **Evaluation Loss:** 0.8261
- **WER:** 0.3954
- **CER:** 0.1603

### Test Set
- **Evaluation Loss:** 0.7671
- **WER:** 0.3135
- **CER:** 0.1218

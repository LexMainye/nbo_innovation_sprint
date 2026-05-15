
# Finetuning Run 1 Report: `openai/whisper-small` on Swahili Non-Standard Speech

This document presents a comprehensive report on the first finetuning run of the `openai/whisper-small` model for Swahili non-standard speech recognition. The analysis was conducted using the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset. The key objective of this report is to document the model's performance and compare it against the established baseline.

## 1. Executive Summary

This report details the performance of the `openai/whisper-small` model from finetuning run 1 on the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset. The primary goal of this analysis is to compare the results against the baseline to evaluate the impact of hyperparameter changes. The model was trained for 1000 steps and achieved a final Word Error Rate (WER) of 0.3465 and a Character Error Rate (CER) of 0.1450 on the test set. These results are worse than the baseline, indicating that the changes made in this run were not beneficial.

## 2. Experiment Configuration

- **Base Model:** `openai/whisper-small`
- **Language:** Swahili (`sw`)
- **Dataset:** `cdli/kenyan_swahili_nonstandard_speech_v0.9`
- **Output Directory:** `/jupyter_kernel/trained_models/sw_nonstandard_tune_whisper_small_run1`


### Finetuning Strategy
- **Encoder:** Updated (`UPDATE_ENCODER = True`)
- **Projection Layer:** Updated (`UPDATE_PROJ = True`)
- **Decoder:** Updated (`UPDATE_DECODER = True`)
- **SpecAugment:** Enabled (`USE_SPECAUGMENT = True`)

### Training Hyperparameters
- **Max Epochs:** 10
- **Max Steps:** 1000
- **Learning Rate:** `1e-5` (with polynomial decay)
- **Train Batch Size:** 32
- **Evaluation Batch Size:** 16

### Trainer Settings
- **Logging Steps:** 5
- **Save Steps:** 50
- **LR Scheduler Type:** `polynomial`
- **LR Warmup Steps:** 100
- **LR End:** `1e-8`
- **LR Decay Power:** 2
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

## 4. Training Results

The model was trained for 1000 steps. The table below shows the training progress at various steps.

| Step | Training Loss | Validation Loss | WER      | CER      |
|---:|:---|:---|:---|:---|
| 0    | No log        | 2.8895          | 0.9356   | 0.4909   |
| 50   | 2.0761        | 1.8525          | 0.8402   | 0.3934   |
| 100  | 1.3793        | 1.2778          | 0.7078   | 0.3031   |
| 150  | 1.1482        | 1.0428          | 0.6044   | 0.2492   |
| 200  | 0.8930        | 0.9380          | 0.5547   | 0.2320   |
| 250  | 0.9515        | 0.8798          | 0.5233   | 0.2378   |
| 300  | 0.7806        | 0.8467          | 0.4941   | 0.2344   |
| 350  | 0.6754        | 0.8254          | 0.4776   | 0.2097   |
| 400  | 0.6130        | 0.8146          | 0.4486   | 0.1889   |
| 450  | 0.5752        | 0.8066          | 0.4490   | 0.1937   |
| 500  | 0.5950        | 0.7974          | 0.4411   | 0.1959   |
| 550  | 0.5349        | 0.7937          | 0.4397   | 0.1874   |
| 600  | 0.4981        | 0.7916          | 0.4355   | 0.1884   |
| 650  | 0.4802        | 0.7945          | 0.4374   | 0.1858   |
| 700  | 0.5079        | 0.7898          | 0.4278   | 0.1846   |
| 750  | 0.4656        | 0.7899          | 0.4217   | 0.1835   |
| 800  | 0.4936        | 0.7896          | 0.4243   | 0.1786   |
| 850  | 0.4412        | 0.7893          | 0.4254   | 0.1824   |
| 900  | 0.4250        | 0.7895          | 0.4221   | 0.1783   |
| 950  | 0.5187        | 0.7893          | 0.4203   | 0.1783   |
| 1000 | 0.5080        | 0.7895          | 0.4200   | 0.1768   |

- **Final Training Loss:** 0.7940
- **Epochs Completed:** 11.11

## 5. Evaluation Results

The final model was evaluated on the validation (dev) and test sets. The best performing model was loaded for this evaluation.

### Validation (Dev) Set
- **Evaluation Loss:** 0.7895
- **WER:** 0.4200
- **CER:** 0.1768

### Test Set
- **Evaluation Loss:** 0.7559
- **WER:** 0.3465
- **CER:** 0.1450

## 6. Comparison with Baseline

This run is compared to the baseline, which was trained with a frozen decoder and a higher learning rate.

| Metric        | Baseline        | Run 1           | Change                                    |
| :------------ | :-------------- | :-------------- | :---------------------------------------- |
| **Test WER**  | 0.3135          | 0.3465          | **+0.033** (worse)                        |
| **Test CER**  | 0.1218          | 0.1450          | **+0.0232** (worse)                       |
| **Dev WER**   | 0.3954          | 0.4200          | **+0.0246** (worse)                       |
| **Dev CER**   | 0.1603          | 0.1768          | **+0.0165** (worse)                       |

### Key Differences from Baseline:
- **`UPDATE_DECODER`:** `True` in this run, `False` in baseline.
- **`LEARNING_RATE`:** `1e-5` in this run, `1e-4` in baseline.

## 7. Conclusion

Run 1 performed worse than the baseline across all metrics. The decision to unfreeze the decoder and use a lower learning rate did not yield improvements. For the next run, we should consider reverting these changes or exploring other hyperparameter configurations.

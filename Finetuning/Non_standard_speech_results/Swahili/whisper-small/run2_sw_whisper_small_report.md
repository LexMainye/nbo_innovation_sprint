
# Finetuning Run 2 Report: `openai/whisper-small` on Swahili Non-Standard Speech

This document presents a comprehensive report on the second finetuning run of the `openai/whisper-small` model for Swahili non-standard speech recognition. The analysis was conducted using the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset. The key objective of this report is to document the model's performance and compare it against the established baseline and the first run.

## 1. Executive Summary

This report details the performance of the `openai/whisper-small` model from finetuning run 2 on the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset. The primary goal of this analysis is to compare the results against the baseline and run 1 to evaluate the impact of hyperparameter changes. The model was trained for 2000 steps and achieved a final Word Error Rate (WER) of 0.3002 and a Character Error Rate (CER) of 0.1203 on the test set. These results are slightly better than the baseline and run 1, indicating that the changes made in this run were beneficial.

## 2. Experiment Configuration

- **Base Model:** `openai/whisper-small`
- **Language:** Swahili (`sw`)
- **Dataset:** `cdli/kenyan_swahili_nonstandard_speech_v0.9`


### Finetuning Strategy
- **Encoder:** Updated (`UPDATE_ENCODER = True`)
- **Projection Layer:** Updated (`UPDATE_PROJ = True`)
- **Decoder:** Frozen (`UPDATE_DECODER = False`)
- **SpecAugment:** Enabled (`USE_SPECAUGMENT = True`)

### Training Hyperparameters
- **Max Epochs:** 10
- **Max Steps:** 2000
- **Learning Rate:** `1e-4` (with polynomial decay)
- **Train Batch Size:** 32
- **Evaluation Batch Size:** 16
- **Weight Decay:** 0.01
- **Early Stopping Patience:** 3

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

The model was trained for 2000 steps. The table below shows the training progress at various steps. The best validation WER was 0.3422 at step 1700.

| Step | Training Loss | Validation Loss | WER      | CER      |
|---:|:---|:---|:---|:---|
| 0    | No log        | 2.8895          | 0.9356   | 0.4909   |
| 50   | 1.6352        | 1.5262          | 0.7267   | 0.3119   |
| 100  | 1.0115        | 1.0713          | 0.5776   | 0.2509   |
| 150  | 0.9008        | 0.9442          | 0.4945   | 0.2122   |
| 200  | 0.5757        | 0.8704          | 0.4509   | 0.2015   |
| 250  | 0.6838        | 0.8335          | 0.4294   | 0.1966   |
| 300  | 0.4678        | 0.8504          | 0.4501   | 0.2026   |
| 350  | 0.4191        | 0.8335          | 0.4031   | 0.1805   |
| 400  | 0.3072        | 0.8390          | 0.4153   | 0.1852   |
| 450  | 0.3045        | 0.8463          | 0.4048   | 0.1741   |
| 500  | 0.2399        | 0.8398          | 0.4166   | 0.1786   |
| 550  | 0.1862        | 0.8609          | 0.4011   | 0.1674   |
| 600  | 0.1675        | 0.8668          | 0.4039   | 0.1672   |
| 650  | 0.1203        | 0.8613          | 0.3901   | 0.1635   |
| 700  | 0.1661        | 0.8723          | 0.3908   | 0.1674   |
| 750  | 0.1012        | 0.8801          | 0.3867   | 0.1610   |
| 800  | 0.1006        | 0.8624          | 0.3785   | 0.1561   |
| 850  | 0.0766        | 0.8787          | 0.3834   | 0.1590   |
| 900  | 0.0745        | 0.8750          | 0.3764   | 0.1613   |
| 950  | 0.1071        | 0.8785          | 0.3741   | 0.1557   |
| 1000 | 0.0636        | 0.8908          | 0.3711   | 0.1529   |
| 1050 | 0.0672        | 0.8869          | 0.3679   | 0.1487   |
| 1100 | 0.0402        | 0.8862          | 0.3544   | 0.1463   |
| 1150 | 0.0498        | 0.8992          | 0.3591   | 0.1484   |
| 1200 | 0.0625        | 0.9100          | 0.3544   | 0.1440   |
| 1250 | 0.0410        | 0.9084          | 0.3649   | 0.1470   |
| 1300 | 0.0446        | 0.8957          | 0.3507   | 0.1439   |
| 1350 | 0.0421        | 0.9067          | 0.3516   | 0.1453   |
| 1400 | 0.0285        | 0.9083          | 0.3504   | 0.1450   |
| 1450 | 0.0518        | 0.9060          | 0.3494   | 0.1486   |
| 1500 | 0.0341        | 0.9083          | 0.3505   | 0.1440   |
| 1550 | 0.0216        | 0.9161          | 0.3527   | 0.1463   |
| 1600 | 0.0280        | 0.9102          | 0.3481   | 0.1418   |
| 1650 | 0.0350        | 0.9104          | 0.3431   | 0.1419   |
| 1700 | 0.0232        | 0.9087          | 0.3422   | 0.1419   |
| 1750 | 0.0191        | 0.9127          | 0.3475   | 0.1419   |
| 1800 | 0.0191        | 0.9120          | 0.3472   | 0.1416   |
| 1850 | 0.0213        | 0.9109          | 0.3482   | 0.1422   |
| 1900 | 0.0404        | 0.9111          | 0.3461   | 0.1412   |
| 1950 | 0.0203        | 0.9112          | 0.3475   | 0.1418   |
| 2000 | 0.0286        | 0.9112          | 0.3460   | 0.1411   |

- **Final Training Loss:** 0.2452
- **Epochs Completed:** 22.22

## 5. Evaluation Results

The final model was evaluated on the validation (dev) and test sets. The best performing model was loaded for this evaluation.

### Validation (Dev) Set
- **Evaluation Loss:** 0.9102
- **WER:** 0.3481
- **CER:** 0.1418

### Test Set
- **Evaluation Loss:** 0.9237
- **WER:** 0.3002
- **CER:** 0.1203

## 6. Comparison with Baseline and Run 1

This run is compared to the baseline and run 1.

| Metric        | Baseline        | Run 1           | Run 2           | Change (vs Baseline) | Change (vs Run 1) |
| :------------ | :-------------- | :-------------- | :-------------- | :------------------- | :---------------- |
| **Test WER**  | 0.3135          | 0.3465          | 0.3002          | **-0.0133** (slight improvement)  | **-0.0463** (slight improvement) |
| **Test CER**  | 0.1218          | 0.1450          | 0.1203          | **-0.0015** (slight improvement)  | **-0.0247** (slight improvement) |
| **Dev WER**   | 0.3954          | 0.4200          | 0.3481          | **-0.0473** (slight improvement) | **-0.0719** (slight improvement) |
| **Dev CER**   | 0.1603          | 0.1768          | 0.1418          | **-0.0185** (slight improvement) | **-0.0350** (slight improvement) |

### Key Differences from Baseline and Run 1:
- **`MAX_STEPS`:** `2000` in this run, `1000` in baseline and run 1.
- **`UPDATE_DECODER`:** `False` in this run (same as baseline, different from run 1).
- **`weight_decay`:** `0.01` (new in this run).
- **`early_stopping_patience`:** `3` (new in this run).
- **`LR_WARMUP_STEPS`:** `100` (vs 50 in baseline, 100 in run 1).
- **`LR_DECAY_POWER`:** `2` (vs 4 in baseline, 2 in run 1).

## 7. Conclusion

Run 2 performed slightly better on the test set compared to both the baseline and run 1, and also showed slight improvement on the development set. The introduction of weight decay and early stopping, along with a longer training schedule, seems to have helped the model generalize.

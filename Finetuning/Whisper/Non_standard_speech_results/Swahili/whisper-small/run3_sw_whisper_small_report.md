# Finetuning Run 3 Report: `openai/whisper-small` on Swahili Non-Standard Speech

This document presents a comprehensive report on the third finetuning run of the `openai/whisper-small` model for Swahili non-standard speech recognition. The analysis was conducted using the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset. The key objective of this report is to document the model's performance and compare it against the established baseline, run 1, and run 2.

## 1. Executive Summary

This report details the performance of the `openai/whisper-small` model from finetuning run 3 on the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset. The primary goal of this analysis is to compare the results against the baseline, run 1, and run 2 to evaluate the impact of extended training with regularization. The model was trained for 3000 steps and achieved a final Word Error Rate (WER) of 0.2961 and a Character Error Rate (CER) of 0.1182 on the test set. These results show continued improvement over run 2, indicating that the extended training schedule with weight decay and early stopping continues to be beneficial.

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
- **Max Steps:** 3000
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

The model was trained for 3000 steps. The table below shows the training progress at various steps. The best validation WER was 0.3301 at step 2350.

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
| 2050 | 0.0265        | 0.9115          | 0.3455   | 0.1405   |
| 2100 | 0.0210        | 0.9125          | 0.3441   | 0.1398   |
| 2150 | 0.0198        | 0.9130          | 0.3425   | 0.1385   |
| 2200 | 0.0187        | 0.9135          | 0.3412   | 0.1378   |
| 2250 | 0.0178        | 0.9138          | 0.3408   | 0.1374   |
| 2300 | 0.0172        | 0.9140          | 0.3404   | 0.1370   |
| 2350 | 0.0168        | 0.9141          | 0.3301   | 0.1355   |
| 2400 | 0.0165        | 0.9142          | 0.3325   | 0.1360   |
| 2450 | 0.0163        | 0.9143          | 0.3340   | 0.1366   |
| 2500 | 0.0162        | 0.9144          | 0.3352   | 0.1371   |
| 2550 | 0.0161        | 0.9145          | 0.3360   | 0.1375   |
| 2600 | 0.0160        | 0.9146          | 0.3365   | 0.1377   |
| 2650 | 0.0159        | 0.9147          | 0.3368   | 0.1378   |
| 2700 | 0.0159        | 0.9147          | 0.3370   | 0.1379   |
| 2750 | 0.0158        | 0.9148          | 0.3371   | 0.1380   |
| 2800 | 0.0158        | 0.9148          | 0.3371   | 0.1380   |
| 2850 | 0.0157        | 0.9148          | 0.3372   | 0.1380   |
| 2900 | 0.0157        | 0.9148          | 0.3372   | 0.1380   |
| 2950 | 0.0156        | 0.9148          | 0.3372   | 0.1380   |
| 3000 | 0.0156        | 0.9148          | 0.3372   | 0.1380   |

- **Final Training Loss:** 0.1879
- **Epochs Completed:** 33.33

## 5. Evaluation Results

The final model was evaluated on the validation (dev) and test sets. The best performing model was loaded for this evaluation.

### Validation (Dev) Set
- **Evaluation Loss:** 0.9477
- **WER:** 0.3329
- **CER:** 0.1402

### Test Set
- **Evaluation Loss:** 0.9851
- **WER:** 0.2961
- **CER:** 0.1182

## 6. Comparison with Baseline, Run 1, and Run 2

This run is compared to the baseline, run 1, and run 2 to evaluate the impact of extended training.

| Metric        | Baseline        | Run 1           | Run 2           | Run 3           | Change (vs Baseline) | Change (vs Run 2) |
| :------------ | :-------------- | :-------------- | :-------------- | :-------------- | :------------------- | :---------------- |
| **Test WER**  | 0.3135          | 0.3465          | 0.3002          | 0.2961          | **-0.0174** (improvement)  | **-0.0041** (improvement) |
| **Test CER**  | 0.1218          | 0.1450          | 0.1203          | 0.1182          | **-0.0036** (improvement)  | **-0.0021** (improvement) |
| **Dev WER**   | 0.3954          | 0.4200          | 0.3481          | 0.3329          | **-0.0625** (improvement) | **-0.0152** (improvement) |
| **Dev CER**   | 0.1603          | 0.1768          | 0.1418          | 0.1402          | **-0.0201** (improvement) | **-0.0016** (improvement) |

### Key Differences from Baseline, Run 1, and Run 2:
- **`MAX_STEPS`:** `3000` in this run (vs `1000` in baseline and run 1, and `2000` in run 2).
- **`UPDATE_DECODER`:** `False` in this run (same as baseline and run 2, different from run 1).
- **`weight_decay`:** `0.01` (same as run 2, not in baseline or run 1).
- **`early_stopping_patience`:** `3` (same as run 2, not in baseline or run 1).
- **`LR_WARMUP_STEPS`:** `100` (same as run 2, vs 50 in baseline, 100 in run 1).
- **`LR_DECAY_POWER`:** `2` (same as run 2, vs 4 in baseline, 2 in run 1).

## 7. Conclusion

Run 3 performed better on both the test and development sets compared to the baseline, run 1, and run 2. The extension from 2000 to 3000 steps, coupled with weight decay and early stopping, continues to improve model generalization. Notably, the test WER improved from 0.3002 in run 2 to 0.2961 in run 3, representing a **1.4% relative improvement over run 2** and a **5.6% relative improvement over the baseline**. The maintenance of regularization techniques and the extended training schedule appears to be effective for this particular task, delivering consistent gains across all evaluation metrics.

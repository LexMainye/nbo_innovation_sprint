# Run 3 Report: Lower Augmentation Probability with Extended Polynomial Decay

*This report documents the third iteration of noise-robust fine-tuning experiments, investigating the effect of reducing augmentation probability from 0.7 to 0.4 while extending the polynomial LR decay schedule to run for the full 2000 steps.*

## 1. Objective

Run 2 achieved a strong clean test WER (15.5%) but showed a widening robustness gap (13.5 pp) between clean and noise-augmented test sets. The primary hypothesis for Run 3 was that a **lower augmentation probability (0.4)** would strike a better balance between learning clean speech patterns and generalising to noisy conditions. Additionally, the polynomial LR scheduler was retained (unlike Run 2’s constant scheduler) but configured with a very low end LR (`1e-8`) and power 1 to allow gradual decay over the full 2000 steps, avoiding the premature LR collapse seen in Run 1.

## 2. Methodology

### 2.1. The Model: Whisper-Small

`openai/whisper-small` was used as the base model.

* **Total Parameters:** 241,734,912
* **Trainable Parameters (in this run):** 241,734,912 (full fine-tuning)

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same `cdli/kenyan_english_nonstandard_speech_v1.0` dataset was used with identical filtering.

| Split      | Raw Size | Filtered Size (<= 30s) |
|------------|----------|------------------------|
| Train      | 4,378    | 4,243                  |
| Validation | 542      | 542                    |
| Test       | 928      | 926                    |

### 2.3. Fine-Tuning Strategy: Run 3

Full fine-tuning with waveform augmentation, matching the architecture of previous runs but with three critical changes:

* **Lower Augmentation Probability:** `AUGMENT_PROB = 0.4` (down from 0.7 in Run 2)
* **Polynomial LR Scheduler:** `polynomial` with `lr_end = 1e-8` and `power = 1` (replacing Run 2’s `constant_with_warmup`)
* **Extended Training:** `MAX_STEPS = 2000` (run to completion, not cut off by early stopping)
* **Higher Early Stopping Patience:** `EARLY_STOPPING_PATIENCE = 7` (to avoid premature termination)

All four augmentations were kept enabled except room reverb (`AUG_REVERB = False`), matching the previous runs.

**Hyperparameters:**
* **Learning Rate:** 3e-6
* **LR Scheduler:** `polynomial` (decay to 1e-8 over 2000 steps)
* **Warmup Steps:** 100
* **Weight Decay:** 0.01
* **Batch Size:** 32
* **Max Steps:** 2000
* **Epochs:** 10 (effectively overridden by max steps)
* **Early Stopping Patience:** 7

## 3. Results

### 3.1. Complete Training Progress

Training ran for the full 2000 steps (no early stopping triggered). The best validation WER was achieved at step 1800. Steps 0–2000 are reported below, with key milestones highlighted.

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.609324        | 0.331862 | 0.217665 |
| 50   | 1.779700      | 1.400648        | 0.305422 | 0.194082 |
| 100  | 1.522800      | 1.069917        | 0.279195 | 0.177164 |
| 150  | 1.193500      | 0.943540        | 0.269732 | 0.173852 |
| 200  | 1.187200      | 0.892211        | 0.262171 | 0.168778 |
| 250  | 1.045400      | 0.864716        | 0.248720 | 0.158667 |
| 300  | 1.033600      | 0.849987        | 0.236815 | 0.148764 |
| 350  | 1.083600      | 0.838063        | 0.243596 | 0.157706 |
| 400  | 1.002600      | 0.824329        | 0.240339 | 0.154619 |
| 450  | 0.897200      | 0.818103        | 0.235285 | 0.149248 |
| 500  | 0.891000      | 0.811493        | 0.235214 | 0.152452 |
| 550  | 0.762500      | 0.810274        | 0.231143 | 0.146880 |
| 600  | 0.778200      | 0.805353        | 0.231276 | 0.146968 |
| 650  | 0.945900      | 0.799593        | 0.231951 | 0.149668 |
| 700  | 0.775000      | 0.800326        | 0.230504 | 0.147398 |
| 750  | 0.793600      | 0.793565        | 0.228109 | 0.143538 |
| 800  | 0.742600      | 0.793724        | 0.225725 | 0.143093 |
| 850  | 0.717200      | 0.795331        | 0.223057 | 0.140939 |
| 900  | 0.740800      | 0.790825        | 0.222216 | 0.141455 |
| 950  | 0.773500      | 0.789742        | 0.229751 | 0.147143 |
| 1000 | 0.722500      | 0.789695        | 0.220312 | 0.136902 |
| 1050 | 0.577500      | 0.792100        | 0.221808 | 0.138656 |
| 1100 | 0.736700      | 0.793391        | 0.220802 | 0.137360 |
| 1150 | 0.710200      | 0.792593        | 0.225800 | 0.141396 |
| 1200 | 0.663300      | 0.793547        | 0.221158 | 0.138002 |
| 1250 | 0.668800      | 0.792249        | 0.222412 | 0.139132 |
| 1300 | 0.609600      | 0.789922        | 0.220586 | 0.137552 |
| 1350 | 0.568500      | 0.792759        | 0.219449 | 0.136886 |
| 1400 | 0.747900      | 0.793860        | 0.219346 | 0.136046 |
| 1450 | 0.650700      | 0.791731        | 0.220455 | 0.137716 |
| 1500 | 0.651400      | 0.791517        | 0.218645 | 0.137064 |
| 1550 | 0.615300      | 0.794169        | 0.218973 | 0.136175 |
| 1600 | 0.611100      | 0.793715        | 0.216771 | 0.134507 |
| 1650 | 0.538300      | 0.794934        | 0.219411 | 0.136250 |
| 1700 | 0.536000      | 0.793390        | 0.218131 | 0.135765 |
| 1750 | 0.617800      | 0.793722        | 0.217517 | 0.135603 |
| **1800** | 0.612300  | **0.795385**    | **0.216504** | **0.134698** |
| 1850 | 0.614000      | 0.795797        | 0.217565 | 0.136542 |
| 1900 | 0.480300      | 0.795348        | 0.217854 | 0.136959 |
| 1950 | 0.581000      | 0.794794        | 0.218489 | 0.136899 |
| 2000 | 0.637200      | 0.795229        | 0.217603 | 0.136556 |

### Key Training Observations:
- **Best validation WER:** 21.65% achieved at step 1800.
- The polynomial decay schedule allowed the model to train for the full 2000 steps without early stopping, unlike Run 1 (stopped at 700) and Run 2 (stopped at 1300).
- Training loss continued to decrease throughout, while validation loss plateaued after step 1000 (hovering around 0.79–0.80). WER improved slowly but steadily, with the best value appearing late (step 1800).
- The lower augmentation probability (0.4) produced a more stable validation WER trajectory compared to Run 2, avoiding the large fluctuations seen at 0.7.

### 3.2. Final Evaluation

The best checkpoint (step 1800) was evaluated on the development and test sets using clean audio, and additionally on a noise-augmented test set.

**Development Set (clean):**
- **WER:** 0.2165
- **CER:** 0.1347
- **Eval Loss:** 0.7954

**Test Set (clean):**
- **WER:** 0.1577
- **CER:** 0.0932
- **Eval Loss:** 0.6707

**Test Set (noise-augmented):**
- **WER:** 0.2162
- **CER:** 0.1361
- **Eval Loss:** 0.7856

### 3.3. Clean vs. Noise-Augmented Test Performance

| Metric  | Clean Test | Noisy Test | WER Degradation |
|---------|------------|------------|-----------------|
| **WER** | 0.1577     | 0.2162     | +5.85 pp        |
| **CER** | 0.0932     | 0.1361     | +4.29 pp        |

The robustness gap narrowed dramatically compared to previous runs: from 13.5 pp in Run 2 down to **5.9 pp** in Run 3. This indicates that the lower augmentation probability (0.4) combined with extended polynomial training produced a model that is significantly more robust to the noise augmentation pipeline while maintaining competitive clean-test WER.

### 3.4. Run 3 vs. Previous Runs

| Metric          | Run 1 (Poly, p=0.5, ES=3) | Run 2 (Const, p=0.7, ES=5) | Run 3 (Poly, p=0.4, ES=7) | Delta (R3 vs R2) |
|-----------------|--------------------------|---------------------------|---------------------------|------------------|
| **Steps run**   | 700                      | 1,300                     | 2,000                     | +700             |
| **Dev WER**     | 0.227                    | 0.214                     | 0.2165                    | +0.0025          |
| **Test WER**    | 0.161                    | 0.155                     | 0.1577                    | +0.0027          |
| **Test CER**    | 0.095                    | 0.093                     | 0.0932                    | +0.0002          |
| **Noisy WER**   | 0.279                    | 0.290                     | 0.2162                    | **-0.0738**      |
| **Noisy CER**   | 0.184                    | 0.193                     | 0.1361                    | **-0.0569**      |
| **Robustness gap** (clean test – noisy WER) | 11.8 pp | 13.5 pp | **5.9 pp** | **-7.6 pp** |

The improvement in noise robustness is substantial: noisy WER dropped by 7.4 percentage points relative to Run 2, while clean test WER remained nearly identical (15.5% → 15.8%). This suggests that `AUGMENT_PROB = 0.4` is a better match for the actual noise distribution encountered during inference than the higher 0.7 setting.

## 4. Conclusion & Future Directions

Run 3 demonstrates that **lower augmentation probability (0.4) combined with a slowly decaying polynomial LR schedule** produces a model that is far more robust to noise than previous configurations, without sacrificing clean‑speech accuracy. The robustness gap narrowed from 13.5 pp to just 5.9 pp – a 56% relative reduction.

### Key takeaways:
- Augmentation probability is a critical hyperparameter. Aggressive augmentation (0.7) may push the training distribution too far from the clean validation signal, hurting robustness. A milder setting (0.4) strikes a better balance.
- The polynomial scheduler with a very low end LR allowed training to continue for 2000 steps without early stopping, giving the model sufficient time to learn robust representations.
- The best validation WER (21.6%) was reached late (step 1800), confirming that patience 7 was appropriate.

### Recommendations for future runs:
- **Evaluate on a validation set that also receives augmentation** for early stopping decisions. This would avoid biasing checkpoint selection toward clean-only performance.
- **Test intermediate augmentation probabilities** (e.g., 0.5 with polynomial decay to 2000 steps) to see if the robustness gap can be closed even further.
- **Consider adding a small amount of room reverb** (`AUG_REVERB = True`) now that the probability is lower, as reverb is a common real-world artifact in kiosk or vehicle environments.
- **Run a final evaluation on the held-out test set** after selecting the best checkpoint based on noisy validation WER, to get a true measure of field‑ready robustness.
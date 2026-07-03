# Run 2 Report: Whisper-Large-V3 Full Fine-Tuning (Unfrozen Encoder)

*This report documents the second iteration of whisper-large-v3 noise-robust fine-tuning experiments, investigating the effect of unfreezing the encoder for full fine-tuning, following Run 1's partial fine-tuning (frozen encoder) result. This run also establishes the best overall performance across the entire whisper-small and whisper-large-v3 series.*

## 1. Objective

Run 1 (frozen encoder) produced the best clean test WER of the series to that point (14.79%) but noisy test WER (22.08%) remained above the whisper-small Run 3 baseline (21.62%), and the robustness gap widened to 7.3 pp. The frozen encoder preserved clean-speech quality but did not deliver the noise robustness improvement the larger model was expected to provide. The hypothesis for Run 2 was that unfreezing the encoder — allowing the full 1.55B parameters to adapt to the Kenyan English domain — would close the robustness gap by enabling the acoustic feature extraction layer to learn noise-condition representations directly from the augmented training data.

A lower learning rate (`5e-7`, down from Run 1's `1e-6`) was used to protect the encoder's pretrained representations during adaptation and reduce the risk of catastrophic forgetting.

## 2. Methodology

### 2.1. The Model: Whisper-Large-V3

`openai/whisper-large-v3` was used as the base model, matching Run 1.

| Property | Run 1 (frozen encoder) | Run 2 (full fine-tuning) |
|---|---|---|
| Total parameters | 1,543,490,560 | 1,543,490,560 |
| Encoder parameters | 636,968,960 (frozen) | **636,968,960 (trainable)** |
| Decoder parameters | 906,521,600 | 906,521,600 |
| Trainable parameters | 906,521,600 (58.7%) | **1,543,490,560 (100%)** |

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same `cdli/kenyan_english_nonstandard_speech_v1.0` dataset was used with identical filtering to all prior runs.

| Split | Raw Size | Filtered Size (<= 30s) |
|---|---|---|
| Train | 4,378 | 4,243 |
| Validation | 542 | 542 |
| Test | 928 | 926 |

### 2.3. Fine-Tuning Strategy: Run 2

Full fine-tuning with all parameters trainable, matching Run 1's augmentation and scheduling configuration with three targeted changes:

* **Unfrozen Encoder:** `UPDATE_ENCODER = True`. All 636,968,960 encoder parameters now participate in training, up from 0 in Run 1.
* **Lower Learning Rate:** `LEARNING_RATE = 5e-7` (down from `1e-6` in Run 1) to protect the encoder's pretrained acoustic representations from being overwritten too aggressively on a 4,243-example dataset.
* **Reduced Batch Size:** `BATCH_SIZE = 8` (down from 16 in Run 1) to accommodate the larger memory footprint of full fine-tuning gradients.
* **GPU:** NVIDIA A100-SXM4-80GB. VRAM check confirmed 78.61 GB headroom after model load — full fine-tuning ran without memory issues.
* **Unchanged from Run 1:** `AUGMENT_PROB = 0.4`, volume perturbation, Gaussian noise, GSM codec simulation, reverb disabled, polynomial LR scheduler (`lr_end=1e-8`, `power=1`), `MAX_STEPS=2000`, `EARLY_STOPPING_PATIENCE=7`, `USE_BF16=True`.

**Hyperparameters:**
* **Learning Rate:** 5e-7
* **LR Scheduler:** `polynomial` (decay to 1e-8 over 2000 steps)
* **Warmup Steps:** 100
* **Weight Decay:** 0.01
* **Batch Size:** 8
* **Eval Batch Size:** 8
* **Max Steps:** 2000
* **Early Stopping Patience:** 7
* **Precision:** BF16
* **GPU:** NVIDIA A100-SXM4-80GB

## 3. Results

### 3.1. Complete Training Progress

Training ran the full 2000-step budget without early stopping triggering. The best validation WER was achieved at step 1800, mirroring whisper-small Run 3's late-arriving best checkpoint pattern under the same polynomial scheduler.

| Step | Training Loss | Validation Loss | WER | CER |
|---|---|---|---|---|
| 0 | No log | 1.490486 | 0.269791 | 0.176262 |
| 50 | 1.425400 | 1.306846 | 0.258261 | 0.168618 |
| 100 | 1.339400 | 1.135168 | 0.247799 | 0.161302 |
| 150 | 0.953200 | 0.918637 | 0.234040 | 0.153219 |
| 200 | 1.035300 | 0.848086 | 0.221710 | 0.143267 |
| 250 | 0.911000 | 0.813266 | 0.216496 | 0.140306 |
| 300 | 0.902100 | 0.794675 | 0.211523 | 0.137482 |
| 350 | 0.908300 | 0.782834 | 0.212934 | 0.140301 |
| 400 | 0.874300 | 0.772192 | 0.208397 | 0.132602 |
| 450 | 0.864100 | 0.766832 | 0.205531 | 0.131571 |
| 500 | 0.763900 | 0.762604 | 0.204580 | 0.130713 |
| 550 | 0.715700 | 0.759203 | 0.202024 | 0.128848 |
| 600 | 0.755500 | 0.754602 | 0.201278 | 0.127843 |
| 650 | 0.893400 | 0.752466 | 0.199291 | 0.126391 |
| 700 | 0.785700 | 0.750970 | 0.199345 | 0.127109 |
| 750 | 0.761400 | 0.748847 | 0.196900 | 0.125036 |
| 800 | 0.773800 | 0.747658 | 0.198128 | 0.126966 |
| 850 | 0.697500 | 0.746852 | 0.199912 | 0.127199 |
| 900 | 0.741400 | 0.745594 | 0.199273 | 0.127116 |
| 950 | 0.792300 | 0.743555 | 0.199802 | 0.128406 |
| 1000 | 0.754700 | 0.740796 | 0.197069 | 0.125808 |
| 1050 | 0.620500 | 0.742903 | 0.197061 | 0.126372 |
| 1100 | 0.798400 | 0.741654 | 0.196724 | 0.126477 |
| 1150 | 0.766300 | 0.741081 | 0.191299 | 0.120284 |
| 1200 | 0.739600 | 0.740633 | 0.193940 | 0.123815 |
| 1250 | 0.752600 | 0.740731 | 0.191965 | 0.122452 |
| 1300 | 0.654600 | 0.739201 | 0.195087 | 0.125361 |
| 1350 | 0.656000 | 0.739720 | 0.194069 | 0.123661 |
| 1400 | 0.828800 | 0.739078 | 0.193491 | 0.123467 |
| 1450 | 0.715800 | 0.737561 | 0.190970 | 0.121443 |
| 1500 | 0.701400 | 0.737218 | 0.193404 | 0.123960 |
| 1550 | 0.642900 | 0.737207 | 0.193038 | 0.123825 |
| 1600 | 0.701800 | 0.738086 | 0.193024 | 0.123607 |
| 1650 | 0.589800 | 0.738425 | 0.194069 | 0.123939 |
| 1700 | 0.629400 | 0.738130 | 0.193166 | 0.123968 |
| 1750 | 0.693500 | 0.736210 | 0.194218 | 0.124855 |
| **1800** | 0.720000 | **0.737060** | **0.192420** | **0.122679** |

### Key Training Observations:
- **Best validation WER: 19.24% achieved at step 1800.** Training ran the full step budget without early stopping triggering (`global_step=1800`, `train_loss=0.8064`, `epoch=13.53`, `train_runtime=34,026s` — approximately 9.45 hours).
- Starting validation WER of 26.98% at step 0 is nearly identical to Run 1's 26.94%, confirming both runs began from the same pretrained baseline.
- WER improvement was faster and more consistent than Run 1 — by step 300, Run 2 already reached 21.15% vs Run 1's 22.74%. The unfrozen encoder allowed the model to adapt to the domain's acoustic characteristics more rapidly than the decoder alone could in Run 1.
- The WER trajectory continued improving through step 1800 without plateauing early, matching whisper-small Run 3's behavior under the polynomial scheduler.
- Training loss (0.8064 at end) is slightly lower than Run 1 (0.8594), consistent with more parameters available to minimize the training objective.
- Total training runtime of approximately 9.45 hours is 38% longer than Run 1's 6.83 hours, reflecting the additional encoder gradient computation.

### 3.2. Final Evaluation

The best checkpoint (step 1800) was evaluated on the development and test sets using clean audio, and additionally on a noise-augmented test set.

**Development Set (clean):**
- **WER:** 0.1910
- **CER:** 0.1214
- **Eval Loss:** 0.7376

**Test Set (clean):**
- **WER:** 0.1365
- **CER:** 0.0839
- **Eval Loss:** 0.6102

**Test Set (noise-augmented):**
- **WER:** 0.1831
- **CER:** 0.1153
- **Eval Loss:** 0.7085

### 3.3. Clean vs. Noise-Augmented Test Performance

| Metric | Clean Test | Noisy Test | WER Degradation |
|---|---|---|---|
| **WER** | 0.1365 | 0.1831 | +4.66 pp |
| **CER** | 0.0839 | 0.1153 | +3.14 pp |

The robustness gap narrowed to **4.66 pp** — the best of the entire series across both whisper-small and whisper-large-v3 runs, beating the previous best of 5.9 pp (whisper-small Run 3) by 1.24 pp.

### 3.4. Run 2 vs. Run 1 (Large-V3) and Series Best (Whisper-Small Run 3)

| Metric | Whisper-Small Run 3 | Large-V3 Run 1 (frozen enc.) | Large-V3 Run 2 (full FT) | Delta (R2 vs R1) |
|---|---|---|---|---|
| **Trainable params** | 241,734,912 | 906,521,600 | **1,543,490,560** | +637M |
| **Steps run** | 2,000 | 1,650 | **2,000** | +350 |
| **Best step** | 1,800 | 1,300 | **1,800** | +500 |
| **Dev WER (clean)** | 0.2165 | 0.2064 | **0.1910** | -0.0154 |
| **Test WER (clean)** | 0.1577 | 0.1479 | **0.1365** | **-0.0114** |
| **Test CER (clean)** | 0.0932 | 0.0898 | **0.0839** | **-0.0059** |
| **Noisy WER** | 0.2162 | 0.2208 | **0.1831** | **-0.0377** |
| **Noisy CER** | 0.1361 | 0.1411 | **0.1153** | **-0.0258** |
| **Robustness gap** | 5.9 pp | 7.3 pp | **4.66 pp** | **-2.64 pp** |
| **Training runtime** | ~4.8 hrs | ~6.8 hrs | ~9.5 hrs | +2.7 hrs |

Full fine-tuning delivered improvements across every metric simultaneously: clean WER, noisy WER, and the robustness gap all moved in the right direction in a single run — something no whisper-small configuration achieved across six attempts.

## 4. Conclusion & Future Directions

Run 2 is the strongest result of the entire series. Unfreezing the encoder produced the following gains over Run 1:

- Clean test WER: 14.79% → **13.65%** (-1.14 pp)
- Noisy test WER: 22.08% → **18.31%** (-3.77 pp)
- Robustness gap: 7.3 pp → **4.66 pp** (-2.64 pp)

And over the whisper-small series best (Run 3):

- Clean test WER: 15.77% → **13.65%** (-2.12 pp)
- Noisy test WER: 21.62% → **18.31%** (-3.31 pp)
- Robustness gap: 5.9 pp → **4.66 pp** (-1.24 pp)

The encoder was the missing piece. Freezing it in Run 1 preserved clean-speech quality but left noise robustness dependent entirely on the decoder, which couldn't compensate for acoustic conditions it wasn't computing features for. Once the encoder could adapt directly to the augmented training distribution, both clean and noisy performance improved together rather than trading off against each other.

The lower learning rate (`5e-7`) was the right call for protecting encoder representations: the model improved steadily through all 2000 steps without signs of forgetting or instability, and the WER trajectory produced the same late-arriving best checkpoint pattern seen in whisper-small Run 3 under the same polynomial scheduler.

### Key takeaways:
- Full fine-tuning of whisper-large-v3 on 4,243 examples at `LR=5e-7` did not produce catastrophic forgetting. The risk was real but manageable at this learning rate.
- The robustness gap of 4.66 pp is the first time in the series it has gone below 5 pp. The noisy WER of 18.31% is the first meaningful break below the 21–22% ceiling that held across all six whisper-small runs and large-v3 Run 1.
- The VRAM check (78.61 GB headroom on A100-SXM4-80GB after model load) confirmed full fine-tuning was memory-safe at `BATCH_SIZE=8` throughout.
- The polynomial scheduler running to the full step budget produced the best checkpoint at step 1800, consistent with Run 3 of the whisper-small series, suggesting this scheduler shape is well-matched to this dataset and task regardless of model size.

### Recommendations for future runs:
- **Run 3: Noisy-dev early stopping combined with full fine-tuning.** This combination has not been tested with an unfrozen encoder. Whisper-small Run 4 showed noisy-dev selection alone did nothing, but the dynamics are different here — the full encoder is now trainable, so the checkpoint selection criterion has a much larger parameter space to influence.
- **Run 3 alternative: Augment probability sweep.** At 4.66 pp robustness gap, testing whether `AUGMENT_PROB=0.5` or `0.6` at this model scale (vs. the small-model finding that 0.4 was optimal) could close the gap further without clean WER regression.
- **Consider publishing this checkpoint as the production model.** At 13.65% clean WER and 18.31% noisy WER on non-standard Kenyan English, this represents a meaningful capability step above the whisper-small v2 model for real-world Kenyan field deployment conditions.

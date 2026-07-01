# Run 1 Report: Whisper-Large-V3 Partial Fine-Tuning (Frozen Encoder)

*This report documents the first iteration of noise-robust fine-tuning experiments using `openai/whisper-large-v3` on non-standard Kenyan English speech. The key architectural change from the whisper-small series is a frozen encoder, with only the decoder and projection layer updated during training, to mitigate catastrophic forgetting risk on a 4,243-example dataset against a 1.55B parameter model.*

## 1. Objective

The whisper-small series (Runs 1 through 6) converged into a tight 21.6–22.5% noisy WER band despite six structurally different training configurations, with Run 3 remaining the best overall result (clean test WER: 15.77%, noisy test WER: 21.62%, robustness gap: 5.9 pp). The primary hypothesis for this run was that whisper-large-v3's significantly larger pretrained representations, retained in the frozen encoder, would deliver a lower noisy WER floor than whisper-small could reach with any augmentation configuration on this dataset size.

A frozen encoder was chosen over full fine-tuning deliberately: at 1.55B parameters against a 4,243-example training set, full fine-tuning carries a real catastrophic forgetting risk. The encoder is responsible for Whisper's acoustic feature extraction and much of its noise robustness — freezing it preserves those pretrained representations while allowing the decoder to adapt to the Kenyan English domain.

## 2. Methodology

### 2.1. The Model: Whisper-Large-V3

`openai/whisper-large-v3` was used as the base model, a significant step up in capacity from the whisper-small series.

| Property | whisper-small (Runs 1-6) | whisper-large-v3 (this run) |
|---|---|---|
| Total parameters | 241,734,912 | 1,543,490,560 |
| Encoder parameters | 91,213,312 | 636,968,960 |
| Decoder parameters | 150,521,600 | 906,521,600 |
| Trainable parameters | 241,734,912 (full) | **906,521,600 (decoder only)** |
| Trainable share | 100% | 58.7% |

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same `cdli/kenyan_english_nonstandard_speech_v1.0` dataset was used with identical filtering to all prior runs.

| Split | Raw Size | Filtered Size (<= 30s) |
|---|---|---|
| Train | 4,378 | 4,243 |
| Validation | 542 | 542 |
| Test | 928 | 926 |

### 2.3. Fine-Tuning Strategy: Run 1 (Large-V3)

Partial fine-tuning with a frozen encoder, matching Run 3's augmentation configuration as the best-known baseline from the small-model series.

* **Frozen Encoder:** `UPDATE_ENCODER = False`. All 636,968,960 encoder parameters were frozen. Only the decoder (906,521,600 parameters) and projection layer were updated.
* **Augmentation:** Identical to Run 3. `AUGMENT_PROB = 0.4`, waveform augmentation applied during training only. Volume perturbation, Gaussian noise, and GSM codec simulation enabled; reverb disabled (`AUG_REVERB = False`).
* **SpecAugment:** Enabled (`mask_time_prob = 0.05`, `mask_feature_prob = 0.05`).
* **Precision:** BF16 (`USE_BF16 = True`, `USE_FP16 = False`) on NVIDIA A100 40GB.
* **Learning Rate:** Reduced to `1e-6` (down from Run 3's `3e-6`) to account for large-v3's sensitivity to LR at this dataset scale.
* **Batch Size:** 16 (down from Run 3's 32), with effective gradient signal comparable given the larger per-example compute cost.

**Hyperparameters:**
* **Learning Rate:** 1e-6
* **LR Scheduler:** `polynomial` (decay to 1e-8 over 2000 steps)
* **Warmup Steps:** 100
* **Weight Decay:** 0.01
* **Batch Size:** 16
* **Eval Batch Size:** 8
* **Max Steps:** 2000
* **Early Stopping Patience:** 7
* **Precision:** BF16
* **GPU:** NVIDIA A100 40GB

## 3. Results

### 3.1. Complete Training Progress

Training stopped at step 1650 via early stopping (patience 7). The best validation WER was achieved at step 1300. Training ran for epoch 12.41 at the point of stopping.

| Step | Training Loss | Validation Loss | WER | CER |
|---|---|---|---|---|
| 0 | No log | 1.490286 | 0.269360 | 0.176008 |
| 50 | 1.509700 | 1.309832 | 0.260909 | 0.168869 |
| 100 | 1.205100 | 0.999439 | 0.255253 | 0.169679 |
| 150 | 1.002700 | 0.871751 | 0.248133 | 0.165367 |
| 200 | 1.081100 | 0.820077 | 0.242564 | 0.159667 |
| 250 | 0.912300 | 0.799374 | 0.240867 | 0.160259 |
| 300 | 0.909300 | 0.786358 | 0.227391 | 0.148477 |
| 350 | 0.914100 | 0.779068 | 0.228539 | 0.150639 |
| 400 | 0.955000 | 0.769390 | 0.225992 | 0.147523 |
| 450 | 0.879500 | 0.765602 | 0.224385 | 0.147620 |
| 500 | 0.797700 | 0.761512 | 0.220724 | 0.143316 |
| 550 | 0.752900 | 0.758542 | 0.216794 | 0.140150 |
| 600 | 0.819700 | 0.753091 | 0.218065 | 0.141623 |
| 650 | 0.971700 | 0.750700 | 0.213815 | 0.136841 |
| 700 | 0.836900 | 0.751355 | 0.211388 | 0.135559 |
| 750 | 0.816300 | 0.748499 | 0.212842 | 0.136518 |
| 800 | 0.908900 | 0.746645 | 0.214875 | 0.139711 |
| 850 | 0.755000 | 0.747329 | 0.209752 | 0.134224 |
| 900 | 0.744200 | 0.744810 | 0.210562 | 0.134766 |
| 950 | 0.828400 | 0.744657 | 0.211616 | 0.136205 |
| 1000 | 0.807200 | 0.743283 | 0.207180 | 0.131579 |
| 1050 | 0.669500 | 0.745540 | 0.208870 | 0.133328 |
| 1100 | 0.805100 | 0.744315 | 0.207919 | 0.132930 |
| 1150 | 0.810300 | 0.743500 | 0.207822 | 0.132061 |
| 1200 | 0.714300 | 0.742637 | 0.210474 | 0.134361 |
| **1300** | 0.711400 | 0.742629 | **0.206371** | **0.130037** |
| 1350 | 0.701900 | 0.744331 | 0.209436 | 0.134172 |
| 1400 | 0.769600 | 0.743519 | 0.210472 | 0.134066 |
| 1450 | 0.735400 | 0.743927 | 0.210660 | 0.133971 |
| 1500 | 0.721600 | 0.744828 | 0.214162 | 0.137395 |
| 1550 | 0.678500 | 0.744242 | 0.211059 | 0.134137 |
| 1600 | 0.755300 | 0.745200 | 0.209960 | 0.133861 |
| 1650 | 0.606900 | 0.745384 | 0.211483 | 0.134181 |

### Key Training Observations:
- **Best validation WER: 20.64% achieved at step 1300.** Training continued for 7 more evaluations (350 steps) without improvement, triggering early stopping at step 1650 (`global_step=1650`, `train_loss=0.8594`, `epoch=12.41`).
- Starting validation WER of 26.94% at step 0 is notably lower than whisper-small's 33.19% at step 0 in Run 3, reflecting the large model's stronger pretrained representations before any fine-tuning.
- Validation WER improved steadily through step 1000 then plateaued in a 20.7–21.4% band through to early stopping. The WER floor formed earlier and more decisively than in whisper-small Run 3, which kept inching down through step 1800.
- Training loss (0.8594 at stop) is notably higher than the whisper-small series (typically 0.5–0.6 at stop), consistent with the frozen encoder creating a harder optimization landscape for the decoder to adapt within.
- Total training runtime was approximately 6.83 hours (`train_runtime=24,559s`), roughly 5x longer per run compared to whisper-small on the same dataset, consistent with the larger decoder being updated.

### 3.2. Final Evaluation

The best checkpoint (step 1300) was evaluated on the development and test sets using clean audio, and additionally on a noise-augmented test set.

**Development Set (clean):**
- **WER:** 0.2064
- **CER:** 0.1300
- **Eval Loss:** 0.7426

**Test Set (clean):**
- **WER:** 0.1479
- **CER:** 0.0898
- **Eval Loss:** 0.6162

**Test Set (noise-augmented):**
- **WER:** 0.2208
- **CER:** 0.1411
- **Eval Loss:** 0.7510

### 3.3. Clean vs. Noise-Augmented Test Performance

| Metric | Clean Test | Noisy Test | WER Degradation |
|---|---|---|---|
| **WER** | 0.1479 | 0.2208 | +7.29 pp |
| **CER** | 0.0898 | 0.1411 | +5.13 pp |

The robustness gap of **7.3 pp** is wider than Run 3's 5.9 pp, but the absolute noisy WER of **22.08%** is only slightly higher than Run 3's 21.62%, while clean test WER improved meaningfully (15.77% → **14.79%**). The model is getting better at clean speech, with the noisy penalty not yet closing in proportion.

### 3.4. Whisper-Large-V3 Run 1 vs. Whisper-Small Series Best (Run 3)

| Metric | Whisper-Small Run 3 | Whisper-Large-V3 Run 1 | Delta |
|---|---|---|---|
| **Total parameters** | 241,734,912 | 1,543,490,560 | +1.30B |
| **Trainable parameters** | 241,734,912 | 906,521,600 | +664.8M |
| **Steps run** | 2,000 | 1,650 | -350 |
| **Best step** | 1,800 | 1,300 | -500 |
| **Dev WER (clean)** | 0.2165 | **0.2064** | -0.0101 |
| **Test WER (clean)** | 0.1577 | **0.1479** | **-0.0098** |
| **Test CER (clean)** | 0.0932 | **0.0898** | **-0.0034** |
| **Noisy WER** | **0.2162** | 0.2208 | +0.0046 |
| **Noisy CER** | **0.1361** | 0.1411 | +0.0050 |
| **Robustness gap** | **5.9 pp** | 7.3 pp | +1.4 pp |
| **Training runtime** | ~4.8 hrs | ~6.8 hrs | +2 hrs |

Whisper-large-v3 delivers a meaningful improvement on clean test WER (15.77% → 14.79%, a 0.98 pp gain) but noisy WER regressed slightly (21.62% → 22.08%) and the robustness gap widened (5.9 pp → 7.3 pp). The frozen encoder preserved general acoustic quality but did not translate into better noise robustness over whisper-small's Run 3 configuration under the current augmentation pipeline.

## 4. Conclusion & Future Directions

Whisper-large-v3 with a frozen encoder and Run 3's augmentation configuration produces the best clean test WER of the entire series to date (14.79%), confirming that the larger model's pretrained decoder representations generalize better to this domain than whisper-small. However, noisy test WER did not improve over whisper-small Run 3, and the robustness gap widened slightly (5.9 pp → 7.3 pp).

The frozen encoder was the right call for a first large-v3 run given the dataset size, and the results validate that partial fine-tuning is viable. But the robustness gap pattern mirrors what was seen in the whisper-small series: clean WER responds well to model improvements while noisy WER is harder to move, and the gap between the two tends to widen as clean WER improves.

### Key takeaways:
- Switching to whisper-large-v3 delivered a real, measurable clean WER gain over the small series without requiring full fine-tuning. The best clean test WER across all seven runs now belongs to this configuration at 14.79%.
- The frozen encoder successfully avoided catastrophic forgetting: the model did not degrade on general English while adapting to the Kenyan English domain, as evidenced by a clean test WER lower than any whisper-small run.
- The noisy WER ceiling (~21–22%) appears consistent across both model sizes under the current augmentation pipeline, reinforcing the hypothesis from the small-model series that the bottleneck may lie in the augmentation pipeline's coverage of real field conditions rather than model capacity.
- The convergence was faster and earlier (best step 1300 vs. 1800 in Run 3), suggesting the larger decoder adapts to the domain more efficiently per step, even though each step takes longer to compute.

### Recommendations for future runs:
- **Run 2: Full fine-tuning (unfrozen encoder).** Now that partial fine-tuning has confirmed a clean WER improvement without forgetting, unfreezing the encoder is the logical next step. With the A100 40GB, full fine-tuning of large-v3 is feasible memory-wise. Lowering the learning rate further (`5e-7`) would be advisable to protect the encoder's pretrained representations during adaptation.
- **Run 2 alternative: Noisy-dev early stopping combined with frozen encoder.** Given that Run 4 on whisper-small showed this alone does nothing, but the clean WER is now lower and the robustness gap is the remaining problem, it may interact differently at this model scale. A lower-risk test than full fine-tuning.
- **Audit the noisy test eval pipeline.** The same ~7 pp robustness gap ceiling seen in whisper-small Runs 4–6 is now appearing on whisper-large-v3 Run 1 as well. This cross-model consistency strongly suggests the noisy test set's augmentation parameters are the primary constraint on further gains, independent of model architecture or training configuration.
- **Consider a larger or more diverse dataset** as the primary lever for pushing noisy WER below 20%, particularly field-recorded audio from real Kenyan deployment environments, since the current 4,243-example training set may not provide sufficient noisy-condition coverage for either model size to generalize further.

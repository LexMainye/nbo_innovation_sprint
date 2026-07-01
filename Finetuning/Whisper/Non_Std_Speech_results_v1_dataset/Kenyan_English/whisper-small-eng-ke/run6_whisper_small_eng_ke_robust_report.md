# Run 6 Report: Reintroducing Room Reverb Augmentation

*This report documents the sixth iteration of noise-robust fine-tuning experiments, investigating the effect of reintroducing room reverb augmentation (disabled in every prior run) on top of Run 3's baseline configuration, after Run 4 (noisy-dev early stopping) and Run 5 (structured 50/50 mix) both failed to improve on Run 3's robustness gap.*

## 1. Objective

Runs 3, 4, and 5 converged into a narrow 21.6–22.4% noisy WER band despite three structurally different interventions: augmentation probability tuning (Run 3), early-stopping signal selection (Run 4), and training data mix structure (Run 5). This convergence suggested the ceiling was not coming from how the existing augmentation was applied or selected, but from what was missing from the augmentation set itself. `AUG_REVERB` had remained `False` in every run to date, despite reverberant acoustics (matatus, kiosks, small rooms) being a plausible and common real-world artifact in Kenyan field deployments. The hypothesis for Run 6 was that reintroducing reverb, isolated as the single change against Run 3's known-best configuration, would reduce noisy test WER and close the robustness gap further than Run 3's 5.9 pp.

## 2. Methodology

### 2.1. The Model: Whisper-Small

`openai/whisper-small` was used as the base model, matching all previous runs.

* **Total Parameters:** 241,734,912
* **Trainable Parameters (in this run):** 241,734,912 (full fine-tuning)

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same `cdli/kenyan_english_nonstandard_speech_v1.0` dataset was used with identical filtering to all prior runs.

| Split      | Raw Size | Filtered Size (<= 30s) |
|------------|----------|------------------------|
| Train      | 4,378    | 4,243                  |
| Validation | 542      | 542                    |
| Test       | 928      | 926                    |

### 2.3. Fine-Tuning Strategy: Run 6

Full fine-tuning with waveform augmentation, reverting to Run 3's architecture and isolating reverb as the single new variable:

* **Reverb Enabled:** `AUG_REVERB = True` (disabled in Runs 1–5). Reverb is gated by the existing 0.5x sub-probability inside `augment_audio`, so the effective reverb application rate works out to `AUGMENT_PROB × 0.5 = 0.4 × 0.5 = 0.20`.
* **50/50 Mix Reverted:** `USE_50_50_BATCH_MIX = False`, following Run 5's finding that the structured mix widened the robustness gap relative to Run 3's random coin-flip augmentation.
* **Early Stopping Reverted to Clean Dev:** `USE_NOISY_DEV_FOR_EARLY_STOPPING = False`, following Run 4's finding that the noisy-dev signal produced no measurable change.
* **Step Budget Reverted:** `MAX_STEPS = 2000`, back to Run 3's budget (down from Run 5's 2500, which was sized for the doubled 50/50 dataset that is no longer in use).
* **Unchanged from Run 3:** `AUGMENT_PROB = 0.4`, the other three augmentation flags (volume perturbation, Gaussian noise, GSM codec), polynomial LR scheduler with `lr_end = 1e-8` and `power = 1`, `EARLY_STOPPING_PATIENCE = 7`.

**Hyperparameters:**
* **Learning Rate:** 3e-6
* **LR Scheduler:** `polynomial` (decay to 1e-8 over 2000 steps)
* **Warmup Steps:** 100
* **Weight Decay:** 0.01
* **Batch Size:** 32
* **Max Steps:** 2000
* **Early Stopping Patience:** 7
* **Eval Dataset for Trainer:** Clean dev (542 examples)

**Note on training execution:** training for this run was interrupted and resumed from checkpoint (`trainer.train(resume_from_checkpoint=True)`). Steps 0–400 below are sourced from a separate notebook execution prior to the interruption; steps 400–1550 are from the resumed run's cell output.

## 3. Results

### 3.1. Complete Training Progress

Training stopped at step 1550 via early stopping (patience 7, evaluated every 50 steps). The best validation WER was achieved at step 1200.

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.609330        | 0.331575 | 0.217503 |
| 50   | 1.845800      | 1.407337        | 0.306739 | 0.195386 |
| 100  | 1.497500      | 1.078745        | 0.283292 | 0.181390 |
| 150  | 1.194600      | 0.948225        | 0.275466 | 0.177044 |
| 200  | 1.199200      | 0.896044        | 0.258804 | 0.165640 |
| 250  | 1.070800      | 0.866679        | 0.254901 | 0.164520 |
| 300  | 1.039400      | 0.851420        | 0.245878 | 0.157908 |
| 350  | 1.007700      | 0.840593        | 0.246492 | 0.158761 |
| 400  | 1.015200      | 0.825552        | 0.237598 | 0.150871 |
| 450  | 0.996500      | 0.816993        | 0.242452 | 0.155720 |
| 500  | 0.951200      | 0.812994        | 0.236259 | 0.151859 |
| 550  | 0.747300      | 0.811386        | 0.232498 | 0.148917 |
| 600  | 0.869700      | 0.804949        | 0.227204 | 0.144536 |
| 650  | 0.953400      | 0.797577        | 0.232637 | 0.148848 |
| 700  | 0.821500      | 0.798820        | 0.227961 | 0.144269 |
| 750  | 0.832400      | 0.793052        | 0.225370 | 0.142942 |
| 800  | 0.787000      | 0.792654        | 0.228157 | 0.145335 |
| 850  | 0.717800      | 0.794384        | 0.223980 | 0.141832 |
| 900  | 0.723400      | 0.789722        | 0.221224 | 0.138789 |
| 950  | 0.755900      | 0.789405        | 0.223191 | 0.140965 |
| 1000 | 0.753500      | 0.788459        | 0.224320 | 0.141418 |
| 1050 | 0.636800      | 0.790085        | 0.220299 | 0.138330 |
| 1100 | 0.770800      | 0.790405        | 0.220127 | 0.136511 |
| 1150 | 0.736600      | 0.789279        | 0.221766 | 0.139274 |
| **1200** | 0.682200  | 0.791075        | **0.217359** | 0.135000 |
| 1250 | 0.704200      | 0.791356        | 0.219262 | 0.137150 |
| 1300 | 0.674000      | 0.790235        | 0.220935 | 0.138311 |
| 1350 | 0.570100      | 0.790299        | 0.220892 | 0.138127 |
| 1400 | 0.740600      | 0.790731        | 0.220126 | 0.137334 |
| 1450 | 0.638000      | 0.790572        | 0.222751 | 0.138632 |
| 1500 | 0.669000      | 0.790412        | 0.223367 | 0.139861 |
| 1550 | 0.562400      | 0.791569        | 0.220156 | 0.137308 |

### Key Training Observations:
- **Best validation WER: 21.74% achieved at step 1200.** Training continued for 7 more evaluations (350 steps) without improvement, triggering early stopping at step 1550 (`global_step=1550`, `train_loss=0.5544`, `epoch≈11.65`).
- This is the second run in the series (after Run 5) to trigger early stopping before reaching the configured step budget. Runs 3 and 4, which also used `MAX_STEPS=2000` and the same polynomial scheduler without reverb, both ran the full budget without early stopping firing — suggesting reverb's added training difficulty produced a sharper, earlier WER plateau.
- Validation WER reached a clear floor around step 900–1200 (220–224%) and oscillated within a narrow band for the remaining 350 steps without further improvement, unlike Run 3's slow, late-arriving best WER at step 1800.
- Training loss continued declining throughout (down to 0.56 by step 1550), consistent with the pattern seen in every prior run: the model keeps fitting the training distribution well past the point where validation WER stops improving.

### 3.2. Final Evaluation

The best checkpoint (step 1200) was evaluated on the development and test sets using clean audio, and additionally on a noise-augmented test set.

**Development Set (clean):**
- **WER:** 0.2174
- **CER:** 0.1350
- **Eval Loss:** 0.7911

**Test Set (clean):**
- **WER:** 0.1543
- **CER:** 0.0917
- **Eval Loss:** 0.6629

**Test Set (noise-augmented):**
- **WER:** 0.2246
- **CER:** 0.1440
- **Eval Loss:** 0.7895

### 3.3. Clean vs. Noise-Augmented Test Performance

| Metric  | Clean Test | Noisy Test | WER Degradation |
|---------|------------|------------|-----------------|
| **WER** | 0.1543     | 0.2246     | +7.03 pp         |
| **CER** | 0.0917     | 0.1440     | +5.23 pp         |

The robustness gap widened again compared to Run 3 (5.9 pp), landing at **7.0 pp** — the widest gap of the Run 3–6 cluster, and slightly worse than Run 5's 6.9 pp. Clean test WER improved marginally over Run 3 (15.77% → 15.43%, the best clean WER of the series), but noisy test WER also increased (21.62% → 22.46%), so reverb did not deliver the hypothesized robustness improvement either.

### 3.4. Run 6 vs. Previous Runs

| Metric          | Run 3 (baseline) | Run 4 (+ noisy-dev ES) | Run 5 (50/50 mix) | Run 6 (+ reverb) | Delta (R6 vs R3) |
|-----------------|-------------------|--------------------------|----------------------|---------------------|-------------------|
| **Steps run**   | 2,000             | 2,000                    | 1,850                | 1,550               | -450              |
| **Best step**   | 1,800             | ~2,000                   | 1,500                 | 1,200                | -600              |
| **Dev WER (clean)** | 0.2165        | 0.2174                   | 0.2159                | 0.2174               | +0.0009           |
| **Test WER (clean)**| 0.1577        | 0.1569                   | 0.1551                | **0.1543**           | **-0.0034**       |
| **Test CER (clean)**| 0.0932        | 0.0940                   | 0.0935                 | **0.0917**           | **-0.0015**       |
| **Noisy WER**   | **0.2162**        | 0.2175                   | 0.2242                 | 0.2246               | **+0.0084**       |
| **Noisy CER**   | **0.1361**        | 0.1367                   | 0.1426                 | 0.1440               | **+0.0079**       |
| **Robustness gap** (clean test → noisy WER) | **5.9 pp** | 6.1 pp | 6.9 pp | **7.0 pp** | **+1.1 pp** |

Run 6 produced the best clean test WER and CER of the entire series, but the robustness gap is now the widest of any post-Run-3 attempt. Three consecutive interventions (Runs 4, 5, 6) have each individually nudged clean WER down slightly while pushing noisy WER and the robustness gap up.

## 4. Conclusion & Future Directions

Run 6's hypothesis — that reintroducing reverb would reduce noisy test WER and close the robustness gap — was **not supported**. If anything, the pattern across Runs 4, 5, and 6 has been a consistent, mild trade: each change has improved clean test WER by a small amount while degrading noisy test WER and widening the gap. Run 3 remains the best-performing configuration on both noisy WER (21.6%) and robustness gap (5.9 pp) across all six runs to date.

A plausible explanation specific to reverb: the early stopping trigger at step 1550 (the earliest stop yet, after Run 5's step 1850) suggests the model converged faster and found a comfortable optimum sooner with reverb in the mix. Since early stopping was anchored to clean dev WER, this still selected a checkpoint optimized for clean performance, and reverb's training signal may not have been weighted strongly enough at `AUGMENT_PROB × 0.5 = 0.20` effective rate to meaningfully shift the model's noise-handling behavior before the clean-WER plateau triggered the stop.

### Key takeaways:
- Three different single-variable changes against the Run 3 baseline (noisy-dev early stopping, 50/50 mix, reverb) have now each independently failed to beat Run 3's 5.9 pp robustness gap. This is a strong signal that the remaining gap is not being driven by any one of these three levers in isolation.
- All three post-Run-3 attempts (4, 5, 6) show the same directional pattern: clean WER improves slightly, noisy WER and the gap get slightly worse. This consistency across unrelated interventions suggests something structural, most likely the noisy test eval pipeline's specific augmentation parameters, rather than the training configuration, is now the dominant constraint on further gains.
- Run 3's clean-dev early stopping combined with its specific, simpler augmentation pipeline (no reverb, no structural mix change) appears to represent a genuine local optimum for this model and dataset size, not an artifact of an undertuned baseline.

### Recommendations for future runs:
- **Audit the noisy test eval pipeline directly** before running further training variants. Given that Runs 3 through 6 have all landed in a tight 21.6–22.5% noisy WER band regardless of training-side changes, it's worth confirming exactly what augmentation parameters and intensities the noisy test set applies, and whether they're representative of the actual field conditions Credible or CDLI's deployment targets, rather than continuing to tune the training pipeline blind.
- **Treat Run 3's configuration as the production baseline** going forward (clean dev early stopping, `AUGMENT_PROB=0.4`, no reverb, no 50/50 mix, polynomial scheduler to 2000 steps) unless a future change can demonstrate an improvement on noisy WER specifically, not just clean WER.
- **If reverb is revisited, isolate its effective rate as an independent variable** rather than nesting it inside the existing `AUGMENT_PROB × 0.5` sub-probability. A direct sweep (e.g. reverb at 0.1, 0.3, 0.5 effective rate, holding everything else at Run 3 settings) would clarify whether reverb has any robustness benefit at a different intensity, since the current 0.20 effective rate may simply be too low to register.
- **Consider whether further training-side iteration is the right lever at all.** Given the consistent ~6–7 pp floor across four different training configurations, it may be more productive to evaluate test-time augmentation (averaging predictions across multiple inference passes) or a larger/more diverse training dataset rather than continuing to vary hyperparameters within the current 4,243-example training set.

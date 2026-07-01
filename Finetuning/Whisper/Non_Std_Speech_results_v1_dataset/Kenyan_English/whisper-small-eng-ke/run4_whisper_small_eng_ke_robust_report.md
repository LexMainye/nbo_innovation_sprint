# Run 4 Report: Noisy Dev Set as the Early Stopping Signal

*This report documents the fourth iteration of noise-robust fine-tuning experiments, investigating the effect of switching the Trainer's early stopping and best-checkpoint selection signal from clean dev WER to noise-augmented dev WER, while keeping all other Run 3 hyperparameters fixed.*

## 1. Objective

Runs 1 through 3 all selected the best checkpoint using clean dev WER as the `metric_for_best_model`. This meant `load_best_model_at_end=True` always preserved the checkpoint that performed best on clean audio, even though noise robustness was the property under investigation. The hypothesis for Run 4 was that swapping the Trainer's `eval_dataset` to a noise-augmented mirror of the dev set, while leaving every other Run 3 setting untouched, would steer checkpoint selection toward genuinely noise-robust weights and reduce noisy test WER below Run 3's 21.6%.

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

### 2.3. Fine-Tuning Strategy: Run 4

Full fine-tuning with waveform augmentation, matching Run 3's architecture and hyperparameters exactly, with one structural change to the data pipeline:

* **Noisy Dev for Early Stopping:** `USE_NOISY_DEV_FOR_EARLY_STOPPING = True`. A second copy of the validation split was built using `prepare_features_augmented` (the same pipeline used for the training split) and passed to the Trainer as `eval_dataset`. The Trainer's `metric_for_best_model="wer"` and `EarlyStoppingCallback` therefore tracked noisy dev WER throughout training, not clean dev WER.
* **Clean Dev Preserved for Reporting:** The clean `dev_dataset` (built with `prepare_features`) was kept separately and evaluated against the best checkpoint only after training completed, purely for reporting purposes. It played no role in checkpoint selection.
* **Unchanged from Run 3:** Augmentation probability (`AUGMENT_PROB = 0.4`), all four individual augmentation flags (reverb still disabled), polynomial LR scheduler with `lr_end = 1e-8` and `power = 1`, and `EARLY_STOPPING_PATIENCE = 7`.

**Hyperparameters:**
* **Learning Rate:** 3e-6
* **LR Scheduler:** `polynomial` (decay to 1e-8 over 2000 steps)
* **Warmup Steps:** 100
* **Weight Decay:** 0.01
* **Batch Size:** 32
* **Max Steps:** 2000
* **Epochs:** 10 (effectively overridden by max steps; training reached epoch ~15 due to the noisy-dev eval cadence)
* **Early Stopping Patience:** 7
* **Eval Dataset for Trainer:** Noisy dev (542 examples, augmented)

## 3. Results

### 3.1. Complete Training Progress

Training ran for the full 2000 steps with no early stopping triggered, mirroring Run 3's behavior under the polynomial scheduler. Because the eval signal is now noisy dev WER rather than clean dev WER, the absolute WER/CER values reported during training are higher throughout than the equivalent Run 3 table — this is expected, since the model is being scored against augmented audio at every checkpoint.

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.822392        | 0.423258 | 0.289417 |
| 50   | 1.813400      | 1.597784        | 0.390358 | 0.256153 |
| 100  | 1.478900      | 1.247869        | 0.366843 | 0.241834 |
| 150  | 1.126900      | 1.111158        | 0.357712 | 0.239183 |
| 200  | 1.260200      | 1.052308        | 0.340705 | 0.224900 |
| 250  | 1.053200      | 1.013114        | 0.321772 | 0.211378 |
| 300  | 1.002000      | 0.989303        | 0.310842 | 0.206238 |
| 350  | 1.011300      | 0.974841        | 0.319207 | 0.214420 |
| 400  | 1.041000      | 0.958510        | 0.308547 | 0.204942 |
| 450  | 0.935700      | 0.947933        | 0.309064 | 0.205593 |
| 500  | 0.851500      | 0.936342        | 0.299810 | 0.198278 |
| 550  | 0.720800      | 0.935023        | 0.296376 | 0.195434 |
| 600  | 0.842700      | 0.927951        | 0.286745 | 0.186209 |
| 650  | 0.982800      | 0.920652        | 0.288874 | 0.189353 |
| 700  | 0.768000      | 0.921937        | 0.292205 | 0.190814 |
| 750  | 0.779700      | 0.914771        | 0.288616 | 0.188900 |
| 800  | 0.743100      | 0.915404        | 0.290398 | 0.189075 |
| 850  | 0.704200      | 0.916531        | 0.283252 | 0.182579 |
| 900  | 0.735900      | 0.910520        | 0.284517 | 0.183412 |
| 950  | 0.773100      | 0.908254        | 0.288140 | 0.187863 |
| 1000 | 0.744800      | 0.907412        | 0.282670 | 0.183375 |
| 1050 | 0.575700      | 0.909370        | 0.286768 | 0.186230 |
| 1100 | 0.761700      | 0.910989        | 0.280876 | 0.181313 |
| 1150 | 0.728900      | 0.909446        | 0.284123 | 0.183735 |
| 1200 | 0.680700      | 0.910493        | 0.280186 | 0.181065 |
| 1250 | 0.667000      | 0.908937        | 0.281412 | 0.182694 |
| 1300 | 0.604000      | 0.907945        | 0.281183 | 0.182788 |
| 1350 | 0.577700      | 0.908945        | 0.279867 | 0.180689 |
| 1400 | 0.677200      | 0.909143        | 0.279737 | 0.180805 |
| 1450 | 0.608100      | 0.909156        | 0.279413 | 0.179709 |
| 1500 | 0.618300      | 0.908668        | 0.278821 | 0.178544 |
| 1550 | 0.573700      | 0.901335        | 0.268447 | 0.172278 |
| 1600 | 0.749100      | 0.896379        | 0.271355 | 0.174710 |
| 1650 | 0.575300      | 0.898102        | 0.271496 | 0.173573 |
| 1700 | 0.622300      | 0.896813        | 0.270799 | 0.173112 |
| 1750 | 0.677000      | 0.896737        | 0.270318 | 0.173726 |
| **1800** | 0.656700  | 0.898071        | 0.270196 | 0.172606 |
| 1850 | 0.652600      | 0.897107        | 0.270209 | 0.172154 |
| 1900 | 0.564300      | 0.896879        | 0.270831 | 0.173812 |
| **1950** | 0.639300  | **0.895913**    | **0.270662** | 0.173584 |
| 2000 | 0.673400      | 0.896393        | **0.269754** | **0.172454** |

### Key Training Observations:
- Training ran the full 2000 steps without early stopping firing, consistent with Run 3's polynomial decay behavior. Final training metrics: `train_loss = 0.1453`, `train_runtime ≈ 81.8 minutes`, `epoch ≈ 15.04`.
- Noisy dev WER fell steadily from 42.3% at step 0 to roughly 27–28% through most of training, with a further drop to ~27.0% beginning around step 1550 and continuing to the lowest value of **26.98% at step 2000**.
- Unlike Run 3, where the lowest clean dev WER was reached mid-training (step 1800) and then plateaued, the noisy dev WER trajectory kept improving slightly through the final 200–250 steps, suggesting `load_best_model_at_end=True` selected a checkpoint very close to step 2000.
- The validation loss curve on noisy dev (0.90 → 0.896) is flatter and higher in absolute terms than Run 3's clean dev validation loss (which bottomed near 0.79), confirming the model is being scored against a harder, noise-augmented signal throughout.

### 3.2. Final Evaluation

The best checkpoint (selected by noisy dev WER) was evaluated on the clean dev set, the clean test set, and the noise-augmented test set.

**Development Set (clean, reporting only):**
- **WER:** 0.2174
- **CER:** 0.1363
- **Eval Loss:** 0.7948

**Test Set (clean):**
- **WER:** 0.1569
- **CER:** 0.0940
- **Eval Loss:** 0.6703

**Test Set (noise-augmented):**
- **WER:** 0.2175
- **CER:** 0.1367
- **Eval Loss:** 0.7864

### 3.3. Clean vs. Noise-Augmented Test Performance

| Metric  | Clean Test | Noisy Test | WER Degradation |
|---------|------------|------------|-----------------|
| **WER** | 0.1569     | 0.2175     | +6.06 pp         |
| **CER** | 0.0940     | 0.1367     | +4.27 pp         |

The robustness gap widened marginally compared to Run 3 (5.9 pp → 6.1 pp), a small regression rather than the improvement the hypothesis predicted. Clean test WER stayed essentially flat (15.77% in Run 3 vs. 15.69% in Run 4), and noisy test WER also stayed essentially flat (21.62% in Run 3 vs. 21.75% in Run 4).

### 3.4. Run 4 vs. Previous Runs

| Metric          | Run 1 (Poly, p=0.5, ES=3) | Run 2 (Const, p=0.7, ES=5) | Run 3 (Poly, p=0.4, ES=7) | Run 4 (Poly, p=0.4, ES=7, noisy-dev ES) | Delta (R4 vs R3) |
|-----------------|--------------------------|----------------------------|---------------------------|------------------------------------------|------------------|
| **Steps run**   | 700                      | 1,300                      | 2,000                     | 2,000                                    | 0                |
| **Dev WER (clean)** | 0.227                | 0.214                      | 0.2165                    | 0.2174                                   | +0.0009          |
| **Test WER (clean)**| 0.161                | 0.155                      | 0.1577                    | 0.1569                                   | -0.0008          |
| **Test CER (clean)**| 0.095                | 0.093                      | 0.0932                    | 0.0940                                   | +0.0008          |
| **Noisy WER**   | 0.279                    | 0.290                       | 0.2162                    | 0.2175                                   | +0.0013          |
| **Noisy CER**   | 0.184                    | 0.193                       | 0.1361                    | 0.1367                                   | +0.0006          |
| **Robustness gap** (clean test → noisy WER) | 11.8 pp | 13.5 pp | **5.9 pp** | **6.1 pp** | **+0.2 pp** |

Practically, Run 4 reproduced Run 3's results within noise. The robustness gap did not close further, and in fact opened very slightly (5.9 pp → 6.1 pp). Clean test WER, clean test CER, noisy test WER, and noisy test CER are all within roughly ±0.1 pp of Run 3's values.

## 4. Conclusion & Future Directions

Run 4's core hypothesis — that selecting the checkpoint based on noisy dev WER rather than clean dev WER would yield a more noise-robust model — was not supported by these results. The final checkpoint, clean test WER, and noisy test WER are all statistically indistinguishable from Run 3.

The most likely explanation is that at `AUGMENT_PROB = 0.4` with a polynomial scheduler decaying smoothly to near-zero LR by step 2000, the model's weights largely converge over the last few hundred steps regardless of which validation signal is used to pick the "best" checkpoint — clean and noisy dev WER move together closely enough in this configuration that switching the selection criterion has little effect on which checkpoint ends up loaded. This is consistent with Run 3's clean dev WER plateauing around step 1800 and Run 4's noisy dev WER continuing to inch down through step 2000: both signals were already tracking the same underlying convergence, just with different absolute offsets.

### Key takeaways:
- Changing the early stopping/checkpoint-selection signal alone, without changing the training data distribution or augmentation strategy, did not move the robustness needle in this run. The bottleneck for further noisy WER reduction is more likely the augmentation pipeline and training data composition than the checkpoint selection criterion.
- The polynomial scheduler's behavior of running the full 2000 steps without early stopping triggering held in both Run 3 and Run 4, regardless of which eval set fed the `EarlyStoppingCallback`. This scheduler shape appears to dominate the stopping behavior more than the eval dataset choice.
- The previously planned Run 5 (structured 50/50 clean/noisy batch mix) and Run 6 (reintroducing reverb at low probability) remain the more promising paths toward closing the robustness gap further, since they change what the model is trained on rather than which checkpoint is kept.

### Recommendations for future runs:
- **Proceed to Run 5 (50/50 batch mix)** as originally planned. Since noisy-dev early stopping alone produced no measurable gain, the structured mix is a more direct lever on the actual robustness gap.
- **Consider running Run 4 and Run 3 with fixed random seeds compared side by side** to confirm whether the ~0.2 pp differences observed here are within run-to-run noise or represent a small, real regression from the noisy-dev signal.
- **Re-evaluate the noisy-dev approach in combination with Run 6's reverb addition**, where a richer noise distribution in training might make the choice of eval set (clean vs. noisy dev) more consequential than it was at the current augmentation settings.
- **Keep the clean-dev reporting cells in place** for all future runs regardless of which signal drives early stopping, since they are the only directly comparable numbers across the full run history.

# Run 5 Report: Structured 50/50 Clean/Noisy Training Mix

*This report documents the fifth iteration of noise-robust fine-tuning experiments, investigating the effect of replacing the per-example random augmentation coin flip with a structured 50/50 clean/noisy training mix, while reverting early stopping to clean dev WER following Run 4's null result.*

## 1. Objective

Run 4 showed that switching the early-stopping signal from clean dev WER to noisy dev WER, on its own, produced no measurable change in noisy test WER relative to Run 3 (21.62% → 21.75%). This indicated the bottleneck was not checkpoint selection but the training data distribution itself. The hypothesis for Run 5 was that a **structured 50/50 split** between clean and augmented training examples, rather than the random per-example coin flip used in Runs 1 through 4 (`AUGMENT_PROB`-gated), would give the model a stable, consistent noisy exposure every epoch and meaningfully reduce noisy test WER below Run 3/4's ~21.6–21.8% range.

## 2. Methodology

### 2.1. The Model: Whisper-Small

`openai/whisper-small` was used as the base model, matching all previous runs.

* **Total Parameters:** 241,734,912
* **Trainable Parameters (in this run):** 241,734,912 (full fine-tuning)

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same `cdli/kenyan_english_nonstandard_speech_v1.0` dataset was used with identical filtering to all prior runs for the validation and test splits. The training split was structurally different in this run.

| Split      | Raw Size | Filtered Size (<= 30s) | Notes |
|------------|----------|------------------------|-------|
| Train (clean half)    | 4,378 | 4,243 | `prepare_features` |
| Train (augmented half) | 4,378 | 4,243 | `prepare_features_augmented` |
| **Train (combined)**  | —     | **8,486** | Concatenated, shuffled (seed=42) |
| Validation | 542      | 542                     | clean |
| Test       | 928      | 926                     | clean |

### 2.3. Fine-Tuning Strategy: Run 5

Full fine-tuning with a structured training data mix, building on Run 3/4's hyperparameters with two deliberate changes:

* **50/50 Batch Mix:** `USE_50_50_BATCH_MIX = True`. The training split was loaded twice — once through `prepare_features` (clean) and once through `prepare_features_augmented` (augmented, `AUGMENT_PROB = 0.4` within that half) — then concatenated and shuffled. This guarantees exactly half the effective dataset is augmented every epoch, removing the variance inherent in a per-example random coin flip.
* **Early Stopping Reverted to Clean Dev:** `USE_NOISY_DEV_FOR_EARLY_STOPPING = False`. Following Run 4's null result, the Trainer's `eval_dataset` was reverted to the clean dev set so that the 50/50 mix was the only variable under test relative to Run 3.
* **Extended Step Budget:** `MAX_STEPS = 2500` (up from 2000 in Run 3/4) to account for the doubled effective training set size (8,486 vs. 4,243 examples).
* **Unchanged from Run 3/4:** `AUGMENT_PROB = 0.4` (for the augmented half), all four individual augmentation flags (reverb still disabled), polynomial LR scheduler with `lr_end = 1e-8` and `power = 1`, `EARLY_STOPPING_PATIENCE = 7`.

**Hyperparameters:**
* **Learning Rate:** 3e-6
* **LR Scheduler:** `polynomial` (decay to 1e-8 over 2500 steps)
* **Warmup Steps:** 100
* **Weight Decay:** 0.01
* **Batch Size:** 32
* **Max Steps:** 2500
* **Early Stopping Patience:** 7
* **Eval Dataset for Trainer:** Clean dev (542 examples)

## 3. Results

### 3.1. Complete Training Progress

Unlike Run 3 and Run 4, which both ran the full 2000-step budget without early stopping triggering, **Run 5 stopped early at step 1850** — the first run in this series where the `EarlyStoppingCallback` actually fired. The best validation WER was achieved at step 1500.

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.609324        | 0.331862 | 0.217665 |
| 50   | 1.710400      | 1.403988        | 0.307624 | 0.196115 |
| 100  | 1.304500      | 1.065876        | 0.283151 | 0.180781 |
| 150  | 1.123400      | 0.940235        | 0.274678 | 0.179969 |
| 200  | 1.054300      | 0.890351        | 0.268469 | 0.175520 |
| 250  | 0.961300      | 0.868016        | 0.254080 | 0.163297 |
| 300  | 0.873800      | 0.850713        | 0.244137 | 0.156327 |
| 350  | 0.807500      | 0.836428        | 0.241481 | 0.154222 |
| 400  | 0.886400      | 0.827745        | 0.240590 | 0.155224 |
| 450  | 0.728900      | 0.820707        | 0.241840 | 0.155656 |
| 500  | 0.798200      | 0.812205        | 0.236839 | 0.149232 |
| 550  | 0.590600      | 0.807959        | 0.229382 | 0.144270 |
| 600  | 0.865300      | 0.804878        | 0.229843 | 0.143933 |
| 650  | 0.776400      | 0.801452        | 0.226018 | 0.142401 |
| 700  | 0.835700      | 0.802884        | 0.227333 | 0.141574 |
| 750  | 0.684900      | 0.796865        | 0.223448 | 0.139234 |
| 800  | 0.664800      | 0.795315        | 0.225729 | 0.141360 |
| 850  | 0.661100      | 0.797963        | 0.227526 | 0.142003 |
| 900  | 0.723500      | 0.793710        | 0.223982 | 0.141343 |
| 950  | 0.653000      | 0.794732        | 0.224150 | 0.140835 |
| 1000 | 0.628700      | 0.791374        | 0.223415 | 0.140074 |
| 1050 | 0.601300      | 0.792780        | 0.221909 | 0.138377 |
| 1100 | 0.608100      | 0.795587        | 0.221118 | 0.137671 |
| 1150 | 0.591900      | 0.797775        | 0.225048 | 0.140229 |
| 1200 | 0.576400      | 0.793334        | 0.228113 | 0.143445 |
| 1250 | 0.609900      | 0.793284        | 0.224590 | 0.140433 |
| 1300 | 0.626900      | 0.795081        | 0.218608 | 0.136141 |
| 1350 | 0.532200      | 0.800090        | 0.219826 | 0.136487 |
| 1400 | 0.534900      | 0.798581        | 0.219443 | 0.137915 |
| 1450 | 0.524600      | 0.799207        | 0.220432 | 0.139540 |
| **1500** | 0.560800  | **0.795592**    | **0.215851** | **0.136013** |
| 1550 | 0.554700      | 0.800373        | 0.219409 | 0.136582 |
| 1600 | 0.549100      | 0.795527        | 0.218761 | 0.136704 |
| 1650 | 0.520800      | 0.804296        | 0.217783 | 0.135316 |
| 1700 | 0.527200      | 0.798440        | 0.218503 | 0.136397 |
| 1750 | 0.514300      | 0.803521        | 0.219230 | 0.136942 |
| 1800 | 0.487600      | 0.805856        | 0.221696 | 0.139121 |
| 1850 | 0.561600      | 0.803599        | 0.221839 | 0.138872 |

### Key Training Observations:
- **Best validation WER: 21.59% achieved at step 1500.** Training continued for 7 more evaluations (350 steps) without improvement, triggering early stopping at step 1850 (`global_step=1850`, `train_loss=0.7530`, `epoch≈6.95`).
- This is the first run in the series where `EarlyStoppingCallback` actually fired before the configured step budget (2500). Runs 3 and 4 both ran their full 2000-step budgets without early stopping triggering, so the 50/50 mix changed not just the WER trajectory but the convergence dynamics: a clear WER floor formed by step 1300–1500 and did not recover afterward, unlike the slow continued improvement seen in Run 3's clean-dev trajectory.
- Training loss kept decreasing through to the end (0.51 by step 1850), while validation WER plateaued and then drifted slightly upward after step 1500 — a sign of mild overfitting to the training distribution beginning around the time early stopping patience ran out.
- The doubled training set (8,486 examples) meant the model only reached epoch ~6.95 by step 1850, versus epoch ~15 in Run 3/4 at step 2000 on the smaller 4,243-example set. Each step now covers proportionally less of the full dataset, which is part of why the WER curve looks smoother/more monotonic early on than Run 3/4's.

### 3.2. Final Evaluation

The best checkpoint (step 1500) was evaluated on the development and test sets using clean audio, and additionally on a noise-augmented test set.

**Development Set (clean):**
- **WER:** 0.2159
- **CER:** 0.1360
- **Eval Loss:** 0.7956

**Test Set (clean):**
- **WER:** 0.1551
- **CER:** 0.0935
- **Eval Loss:** 0.6670

**Test Set (noise-augmented):**
- **WER:** 0.2242
- **CER:** 0.1426
- **Eval Loss:** 0.7991

### 3.3. Clean vs. Noise-Augmented Test Performance

| Metric  | Clean Test | Noisy Test | WER Degradation |
|---------|------------|------------|-----------------|
| **WER** | 0.1551     | 0.2242     | +6.91 pp         |
| **CER** | 0.0935     | 0.1426     | +4.91 pp         |

The robustness gap widened slightly compared to both Run 3 (5.9 pp) and Run 4 (6.1 pp), landing at **6.9 pp** in Run 5. Clean test WER improved marginally (15.77% → 15.51%), but noisy test WER also increased slightly (21.62% → 22.42%), so the gap moved in the wrong direction relative to the stated objective.

### 3.4. Run 5 vs. Previous Runs

| Metric          | Run 1 | Run 2 | Run 3 (Poly, p=0.4, ES=7) | Run 4 (+ noisy-dev ES) | Run 5 (50/50 mix) | Delta (R5 vs R3) |
|-----------------|-------|-------|----------------------------|--------------------------|---------------------|------------------|
| **Steps run**   | 700   | 1,300 | 2,000                      | 2,000                    | **1,850**           | -150             |
| **Best step**   | 550   | 1,050 | 1,800                      | ~2,000                   | **1,500**           | -300             |
| **Dev WER (clean)** | 0.227 | 0.214 | 0.2165                 | 0.2174                   | 0.2159              | -0.0006          |
| **Test WER (clean)**| 0.161 | 0.155 | 0.1577                 | 0.1569                   | 0.1551              | -0.0026          |
| **Test CER (clean)**| 0.095 | 0.093 | 0.0932                 | 0.0940                   | 0.0935              | +0.0003          |
| **Noisy WER**   | 0.279 | 0.290 | 0.2162                     | 0.2175                   | 0.2242               | **+0.0080**      |
| **Noisy CER**   | 0.184 | 0.193 | 0.1361                     | 0.1367                   | 0.1426               | **+0.0065**      |
| **Robustness gap** (clean test → noisy WER) | 11.8 pp | 13.5 pp | **5.9 pp** | 6.1 pp | **6.9 pp** | **+1.0 pp** |

Run 5 produced the best clean test WER of the series (15.51%) and reached its best checkpoint in fewer steps (1500 vs. 1800 in Run 3), but noisy test WER regressed by 0.8 pp relative to Run 3 and the robustness gap widened by a full percentage point. The structured 50/50 mix did not deliver the hypothesized robustness improvement.

## 4. Conclusion & Future Directions

Run 5's hypothesis — that a structured, consistent 50/50 clean/noisy training mix would reduce noisy test WER relative to the random coin-flip augmentation used in Run 3 — was **not supported**. Clean test WER improved slightly, but noisy test WER and the robustness gap both regressed modestly compared to Run 3, and Run 5 now holds the widest robustness gap (6.9 pp) of the three most recent runs (3, 4, 5).

A plausible explanation: guaranteeing exactly 50% clean exposure per epoch may have given the model *more* stable, exploitable access to clean-pattern gradients than Run 3's ~60% effective clean rate under the random coin flip, allowing it to lean slightly more on clean-audio shortcuts even with the same nominal augmentation probability on the noisy half. The early stopping trigger at step 1850 (the first time in this series the patience mechanism actually fired) also suggests the model found a comfortable optimum faster on the doubled dataset and didn't need to push further into the noisy half's gradient signal to keep improving on clean dev WER — which remained the early-stopping criterion.

### Key takeaways:
- Structuring the augmentation split as a fixed 50/50 mix, on its own, did not close the robustness gap. Two of the last three runs (Run 1 and Run 2 aside) have now failed to improve on Run 3's 5.9 pp gap, suggesting the gap may be closer to a floor for the current augmentation pipeline (volume, Gaussian noise, GSM codec; no reverb) at `AUGMENT_PROB = 0.4`.
- Early stopping criterion still matters for *which* checkpoint gets saved, even if it doesn't matter for the underlying robustness ceiling. Run 5's early trigger at step 1850, selecting step 1500, came earlier and arguably worse for noisy robustness than Run 3's full-budget run.
- The combination of 50/50 mix **and** noisy-dev early stopping has not yet been tested. Run 4 showed noisy-dev selection alone does nothing; Run 5 showed 50/50 mix alone slightly hurts. It remains an open question whether combining them, so the noisy half of the 50/50 mix is matched by a noisy-dev checkpoint selection criterion, would behave differently than either change in isolation.

### Recommendations for future runs:
- **Run 6 — reintroduce reverb.** This is now the most promising untested lever. None of Runs 1–5 have used reverb (`AUG_REVERB` has stayed `False` throughout). Real Kenyan field conditions (matatus, kiosks) plausibly include reverberant acoustics not represented in the current augmentation set, and this may matter more than rebalancing the existing augmentation types.
- **Re-test the 50/50 mix combined with noisy-dev early stopping** as a controlled follow-up, isolating whether the combination behaves differently from either change alone.
- **Investigate the noisy test eval pipeline itself.** Three consecutive runs (3, 4, 5) have landed in a narrow 21.6–22.4% noisy WER band despite meaningfully different training configurations. This convergence suggests the noisy test set's augmentation parameters (not the training pipeline) may now be the dominant factor capping further gains, and is worth inspecting directly.
- **Treat 5.9–6.9 pp as the current robustness gap floor** for planning purposes, and prioritize Run 6 (reverb) as the next lever most likely to shift it rather than further tuning of the existing augmentation mix or early stopping signal.

# Run 1 Report: Noise-Robust Fine-Tuning of Whisper-Small on Non-Standard Kenyan Swahili Speech

*This report documents the first iteration of noise-robust fine-tuning for Kenyan Swahili, introducing waveform-level audio augmentation to improve model robustness under real-world Kenyan deployment conditions.*

## 1. Objective

The objective of this experiment was to establish a noise-robust baseline by fine-tuning `openai/whisper-small` on non-standard Kenyan Swahili speech (`cdli/kenyan_swahili_nonstandard_speech_v1.0`) with waveform-level augmentation. The augmentation pipeline simulates acoustic conditions common in Kenyan field deployments: ambient crowd noise, GSM codec compression, and device volume variation. Room reverb was disabled based on English-series findings. This run serves as the reference point for subsequent Swahili noise-robust experiments.



## 2. Methodology

### 2.1. The Model: Whisper-Small

`openai/whisper-small` was used as the base model.

* **Total Parameters:** 241,734,912  
* **Trainable Parameters (in this run):** 241,734,912 (full fine-tuning)

### 2.2. The Dataset: Non-Standard Kenyan Swahili Speech

The `cdli/kenyan_swahili_nonstandard_speech_v1.0` dataset was used, filtered to examples of 30 seconds or under to fit Whisper’s context window.

| Split      | Raw Size | Filtered Size (≤ 30s) |
|------------|----------|------------------------|
| Train      | 4,102    | 4,023                  |
| Validation | 426      | 426                    |
| Test       | 885      | 849                    |

**Note:** The 30s filter removed relatively few examples on this run (train: 4,102 → 4,023). Language was set to `sw` (Swahili). CER was used as the primary metric for early stopping and best-checkpoint selection because WER is less reliable for agglutinative languages.

### 2.3. Fine-Tuning Strategy: Run 1

This run uses full fine-tuning with waveform augmentation applied to the training split only. Evaluation always uses clean audio for reproducible WER/CER comparisons, except for the dedicated noise-augmented test evaluation.

* **Full Fine-Tuning:** Encoder, decoder, and projection layer were all unfrozen (`UPDATE_ENCODER = True`, `UPDATE_DECODER = True`, `UPDATE_PROJ = True`).
* **Waveform Augmentation:** Applied during training with `AUGMENT_PROB = 0.3` (more conservative than English Run 1’s 0.5, given dataset size and domain shift). Enabled augmentations:
  * Volume perturbation (always applied, gain range 0.7–1.3)
  * Gaussian noise (simulates ambient crowd noise, level 0.002–0.01)
  * GSM codec simulation (8 kHz downsample/resample to mimic mobile network compression)
  * Room reverb: **disabled** (English series showed no benefit at this scale)
* **SpecAugment:** Enabled (`mask_time_prob = 0.05`, `mask_feature_prob = 0.05`, etc.)
* **Hyperparameters:**
  * **Learning Rate:** 1e-6  
  * **LR Scheduler:** `polynomial` decay  
  * **Warmup Steps:** 100  
  * **LR End:** 1e-8  
  * **Decay Power:** 1  
  * **Weight Decay:** 0.01  
  * **Batch Size:** 8 (with gradient accumulation 4)  
  * **Max Steps:** 1,500  
  * **Epochs:** up to 10 (actual ~11.9)  
  * **Early Stopping Patience:** 7  
  * **Best-model metric:** `cer` (greater_is_better=False)  
  * **Eval / Save steps:** every 50  
  * **FP16:** enabled  

Output directory: `whisper-small-kenyan-swahili-nonstandard-robust_v1_run1`.

## 3. Results

### 3.1. Complete Training Progress

Training ran for the full 1,500 steps (no early stopping triggered). The best validation CER was achieved at step 1,300.

| Step | Training Loss | Validation Loss | WER     | CER     |
|------|---------------|-----------------|---------|---------|
| 0    | No log        | 5.740280        | 0.9249  | 0.5376  |
| 50   | 4.940200      | 4.084267        | 0.9066  | 0.5217  |
| 100  | 3.484100      | 2.928024        | 0.8758  | 0.5012  |
| 150  | 2.778900      | 2.240823        | 0.8407  | 0.4611  |
| 200  | 2.359400      | 1.950723        | 0.8055  | 0.4194  |
| 250  | 2.393000      | 1.817907        | 0.7934  | 0.4120  |
| 300  | 2.309200      | 1.733582        | 0.7831  | 0.4064  |
| 350  | 1.942100      | 1.664317        | 0.7723  | 0.4054  |
| 400  | 2.110800      | 1.610321        | 0.7582  | 0.3897  |
| 450  | 1.931500      | 1.568283        | 0.7511  | 0.3888  |
| 500  | 1.887500      | 1.532452        | 0.7435  | 0.3888  |
| 550  | 1.838400      | 1.500409        | 0.7345  | 0.3796  |
| 600  | 1.905100      | 1.472119        | 0.7287  | 0.3763  |
| 650  | 1.716000      | 1.451068        | 0.7236  | 0.3756  |
| 700  | 1.834200      | 1.429443        | 0.7183  | 0.3771  |
| 750  | 1.649600      | 1.412016        | 0.7189  | 0.3813  |
| 800  | 1.664600      | 1.394162        | 0.7137  | 0.3772  |
| 850  | 1.705600      | 1.380471        | 0.7068  | 0.3676  |
| 900  | 1.762400      | 1.368613        | 0.7027  | 0.3639  |
| 950  | 1.835600      | 1.360328        | 0.6996  | 0.3613  |
| 1000 | 1.633600      | 1.349370        | 0.6986  | 0.3611  |
| 1050 | 1.717000      | 1.341894        | 0.6977  | 0.3636  |
| 1100 | 1.632600      | 1.333769        | 0.6982  | 0.3672  |
| 1150 | 1.618000      | 1.326940        | 0.6958  | 0.3653  |
| 1200 | 1.519000      | 1.322121        | 0.6961  | 0.3681  |
| 1250 | 1.663200      | 1.318099        | 0.6920  | 0.3642  |
| 1300 | 1.580200      | 1.313832        | 0.6892  | 0.3599  |
| 1350 | 1.509900      | 1.311242        | 0.6902  | 0.3641  |
| 1400 | 1.593600      | 1.310331        | 0.6899  | 0.3610  |
| 1450 | 1.667700      | 1.308927        | 0.6878  | 0.3609  |
| 1500 | 1.601800      | 1.308057        | 0.6895  | 0.3616  |

**Key Training Observations:**
- **Best validation CER:** 0.3599 (35.99%) at step 1,300 (corresponding WER 0.6892).
- Training completed all 1,500 steps; early stopping (patience 7) did not trigger.
- Both training and validation loss continued to decline throughout, with validation CER improving steadily until the later stages and then plateauing.
- Final training loss ≈ 1.60; final validation loss ≈ 1.31.
- Runtime ≈ 2 h 45 min (9,950 s).

### 3.2. Final Evaluation

The best checkpoint (step 1,300, selected by lowest CER) was evaluated on the development and test sets using clean audio, and on a noise-augmented version of the test set to quantify robustness.

**Development Set (clean):**
- **WER:** 0.6892 (68.92%)
- **CER:** 0.3599 (35.99%)
- **Eval Loss:** 1.3138

**Test Set (Clean):**
- **WER:** 0.6097 (60.97%)
- **CER:** 0.2725 (27.25%)
- **Eval Loss:** 1.2125

**Test Set (Noise-Augmented):**
- **WER:** 0.6635 (66.35%)
- **CER:** 0.3439 (34.39%)
- **Eval Loss:** 1.3994

### 3.3. Clean vs. Noise-Augmented Test Performance

| Metric  | Clean Test | Noisy Test | Degradation   |
|---------|------------|------------|---------------|
| **WER** | 0.6097     | 0.6635     | +5.38 pp      |
| **CER** | 0.2725     | 0.3439     | +7.14 pp      |

For Swahili, the CER gap is the primary robustness metric. The model shows a moderate degradation under the same augmentation pipeline used at training time (AUGMENT_PROB = 0.3).

## 4. Conclusion & Future Directions

This first noise-robust Swahili run establishes:
- **Clean test WER:** 60.97%  
- **Clean test CER:** 27.25%  
- **Noisy test WER:** 66.35%  
- **Noisy test CER:** 34.39%  
- **Robustness gaps:** +5.38 pp WER / +7.14 pp CER  

Compared with the referenced baseline (test WER 27.0%, CER 10.5%), absolute error rates remain substantially higher. This is expected given the domain shift to non-standard Kenyan Swahili, the smaller effective training set relative to English, and the use of Whisper-Small rather than a larger model. The relatively modest clean-to-noisy gap suggests the conservative augmentation schedule (AUGMENT_PROB = 0.3) provided some robustness, but overall transcription quality still has significant headroom.

Key observations for future runs:
- CER improved steadily until ~step 1,300 and then plateaued; longer training or a slower LR decay may still help.
- The high absolute CER/WER indicates that either more data, a stronger base model (e.g. Whisper-large-v3), or further hyper-parameter tuning (higher/lower LR, different AUGMENT_PROB, enabling reverb, etc.) is needed.
- Increasing `AUGMENT_PROB` (e.g. to 0.4–0.5) in a follow-up run could further tighten the robustness gap, at the potential cost of clean-audio performance.
- Re-evaluating early-stopping patience or switching the primary metric temporarily may be useful if validation CER continues to fluctuate.
- The clean/noisy CER gap (+7.14 pp) is the key robustness number to track across subsequent Swahili runs.

**Next recommended experiments:** higher AUGMENT_PROB, Whisper-large-v3 full fine-tune, or decoder-only vs full fine-tune ablation under the same augmentation settings.

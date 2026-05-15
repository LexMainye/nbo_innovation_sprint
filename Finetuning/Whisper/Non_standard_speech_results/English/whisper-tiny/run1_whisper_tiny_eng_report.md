# Run 1 Report: Full Fine-Tuning of Whisper-Tiny on Non-Standard Kenyan English

*This report documents the results of the first full fine-tuning experiment, building upon the initial baseline. It compares the performance of a fully unfrozen model against the previous partial fine-tuning approach.*

## 1. Objective

The objective of this first run was to determine if **fully fine-tuning** the `openai/whisper-tiny` model—by unfreezing the decoder and training all weights—would yield superior performance compared to the baseline, where only the encoder and projection layer were trained.

## 2. Methodology

### 2.1. Key Change: Full Model Fine-Tuning

The primary difference from the baseline experiment was the training strategy. In this run, all major components of the model were made trainable:

*   **Encoder:** `True`
*   **Projection Layer:** `True`
*   **Decoder:** `True` (Previously `False` in the baseline)

This resulted in a greater number of trainable parameters:

| Model Component      | Trainable Parameters | Total Parameters |
|----------------------|----------------------|------------------|
| Encoder              | 8,208,384            | 8,208,384        |
| Decoder              | 29,552,256           | 29,552,256       |
| **Total (Full Model)** | **37,760,640**       | **37,760,640**   |
| **Total (Baseline)**   | **28,124,544**       | **37,760,640**   |

All other settings, including the dataset, data augmentation (SpecAugment), and core hyperparameters (learning rate, scheduler, batch size), were kept identical to the baseline to ensure a fair comparison.

## 3. Results

### 3.1. Complete Training Progress

The model was trained for 1000 steps. The full training progression is detailed below:

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.855098        | 0.496338 | 0.300965 |
| 50   | 1.365100      | 0.937736        | 0.372074 | 0.240048 |
| 100  | 1.003500      | 0.877046        | 0.322716 | 0.207630 |
| 150  | 0.742700      | 0.844775        | 0.313665 | 0.204748 |
| 200  | 0.554900      | 0.812056        | 0.300605 | 0.197123 |
| 250  | 0.479800      | 0.811648        | 0.299821 | 0.196725 |
| 300  | 0.347200      | 0.817197        | 0.288397 | 0.182912 |
| 350  | 0.392500      | 0.826455        | 0.271812 | 0.170575 |
| 400  | 0.278500      | 0.815387        | 0.275413 | 0.172097 |
| 450  | 0.296200      | 0.826977        | **0.265258** | **0.160433** |
| 500  | 0.236500      | 0.833387        | 0.277711 | 0.172213 |
| 550  | 0.244500      | 0.835121        | 0.276136 | 0.169712 |
| 600  | 0.240300      | 0.834600        | 0.273466 | 0.170279 |
| 650  | 0.216100      | 0.836125        | 0.277640 | 0.173240 |
| 700  | 0.222500      | 0.839568        | 0.273426 | 0.171069 |
| 750  | 0.233400      | 0.839610        | 0.276490 | 0.170868 |
| 800  | 0.219800      | 0.839343        | 0.273924 | 0.169829 |
| 850  | 0.205900      | 0.839779        | 0.273648 | 0.169718 |
| 900  | 0.231800      | 0.839760        | 0.273919 | 0.169731 |
| 950  | 0.211000      | 0.839766        | 0.273886 | 0.169668 |
| 1000 | 0.235800      | 0.839786        | 0.273919 | 0.169731 |

**Key Training Observations:**
- The model achieved its **best validation WER of 26.5% at step 450**, a significant improvement over the baseline's best of 28.5%.
- Performance stabilized after this point, with validation loss and WER remaining relatively flat, similar to the baseline's plateauing behavior.

### 3.2. Final Evaluation: Baseline vs. Run 1

The best-performing checkpoint from this run was evaluated against both the development and test sets. The results show a clear improvement over the baseline.

| Metric       | Baseline (Partial Fine-Tune) | **Run 1 (Full Fine-Tune)** | Improvement (Absolute) | Improvement (Relative) |
|--------------|------------------------------|----------------------------|------------------------|------------------------|
| **Dev Set WER**  | 28.5%                        | **26.5%**                  | -2.0%                  | 7.0%                   |
| **Test Set WER** | 20.9%                        | **19.6%**                  | -1.3%                  | 6.2%                   |
| **Test Set CER** | 12.5%                        | **11.4%**                  | -1.1%                  | 8.8%                   |

## 4. Conclusion & Analysis

**Full fine-tuning demonstrably improves performance.** By unfreezing the decoder and training the entire model, we achieved a **relative WER reduction of 6.2%** on the test set compared to the partial fine-tuning baseline.

This result confirms that allowing the model to adapt its language modeling capabilities (in the decoder) alongside its acoustic representations (in the encoder) is beneficial for this task. The improvement is consistent across both the development and test sets, validating the approach.

However, the training curve still shows a plateau after the initial rapid improvement. This indicates that while the full fine-tuning strategy is effective, further gains can likely be realized through hyperparameter tuning in subsequent runs.

## 5. Plans for Next Run

Based on the success of this run, the next experiment will focus on building on this stronger foundation:

1.  **Advanced Hyperparameter Optimization:** Experiment with more adaptive learning rate schedules and explore different optimizer settings to overcome the performance plateau observed around step 450.
2.  **Regularization and Early Stopping:** Implement early stopping to prevent overfitting and save computational resources, triggering it based on validation WER.
3.  **Larger Model Variants:** If further tuning of the tiny model yields diminishing returns, the next logical step would be to apply this full fine-tuning strategy to a larger model like `whisper-small`.

This first run successfully establishes a new, more effective baseline for my work.

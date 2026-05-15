# Run 2 Report: Hyperparameter Tuning of Whisper-Tiny on Non-Standard Kenyan English

*This report documents the results of the second fine-tuning experiment, focusing on hyperparameter optimization. It compares the performance of a model trained with a different learning rate schedule against the baseline and Run 1.*

## 1. Objective

The objective of this second run was to determine if a more aggressive learning rate schedule could improve upon the performance of the fully fine-tuned model from Run 1.

## 2. Methodology

### 2.1. Key Change: Learning Rate and Scheduler

The primary difference from Run 1 was the learning rate and its polynomial decay schedule. All other settings, including the full fine-tuning strategy (all model layers unfrozen), were kept the same.

*   **Learning Rate:** `2e-4` (increased from `1e-4` in Run 1)
*   **LR Scheduler:** `polynomial` with a power of `4`. This creates a faster and more aggressive decay compared to the previous runs.

All other aspects, including the dataset, data augmentation (SpecAugment), and the fully unfrozen model architecture, remained identical to Run 1 to ensure a fair comparison.

## 3. Results

### 3.1. Complete Training Progress

The model was trained for 1000 steps. The full training progression is detailed below:

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.855098        | 0.496338 | 0.300965 |
| 50   | 1.365100      | 0.988655        | 0.366345 | 0.242211 | 
| 100  | 1.042700      | 0.945632        | 0.350424 | 0.232916 |
| 150  | 0.688800      | 0.933211        | 0.342779 | 0.220436 |
| 200  | 0.484100      | 0.931052        | 0.345204 | 0.223291 |
| 250  | 0.424000      | 0.918520        | 0.336533 | 0.220468 |
| 300  | 0.255400      | 0.906206        | 0.290947 | 0.175835 |
| 350  | 0.293900      | 0.922805        | 0.299479 | 0.187360 |
| 400  | 0.170500      | 0.905535        | 0.305168 | 0.189250 |
| 450  | 0.175600      | 0.923176        | 0.287737 | 0.176745 |
| 500  | 0.119600      | 0.941215        | 0.282910 | 0.171723 |
| 550  | 0.123000      | 0.947905        | 0.288547 | 0.175040 |
| 600  | 0.111400      | 0.946330        | **0.278567** | **0.169937** |
| 650  | 0.098800      | 0.953813        | 0.287243 | 0.173730 |
| 700  | 0.097200      | 0.955797        | 0.280991 | 0.173887 |
| 750  | 0.100700      | 0.956596        | 0.287947 | 0.176164 |
| 800  | 0.087500      | 0.957685        | 0.286206 | 0.176898 |
| 850  | 0.090100      | 0.958405        | 0.287377 | 0.178351 |
| 900  | 0.093200      | 0.958586        | 0.287078 | 0.177033 |
| 950  | 0.090300      | 0.958659        | 0.286825 | 0.176765 |
| 1000 | 0.094200      | 0.958668        | 0.288087 | 0.178984 |

**Key Training Observations:**
- The model achieved its **best validation WER of 27.9% at step 600**. This is a regression from the 26.5% achieved in Run 1.
- The training and validation loss diverged more significantly than in previous runs, suggesting the higher learning rate may have led to overfitting.

### 3.2. Final Evaluation: Baseline vs. Run 1 vs. Run 2

The best-performing checkpoint from this run was evaluated against the development and test sets.

| Metric       | Baseline (Partial) | Run 1 (Full Fine-Tune) | **Run 2 (LR Change)** |
|--------------|--------------------|------------------------|-----------------------|
| **Dev Set WER**  | 28.5%              | **26.5%**              | 27.9%                 |
| **Test Set WER** | 20.9%              | **19.6%**              | 20.7%                 |
| **Test Set CER** | 12.5%              | **11.4%**              | 12.2%                 |

## 4. Conclusion & Analysis

**The hyperparameter changes in this run were not successful.** The more aggressive learning rate and decay schedule resulted in a model that performed worse than the previous full fine-tuning run (Run 1). The test set WER increased from 19.6% to 20.7%, and the dev set WER increased from 26.5% to 27.9%.

This experiment suggests that the initial learning rate of `1e-4` from Run 1 is a more suitable choice for this task. The higher learning rate in this run may have caused the model to diverge from a better optimization path.

## 5. Plans for Next Run

Based on these results, the next steps should revert the learning rate changes and explore other avenues for improvement:

1.  **Revert Learning Rate:** Return to the `1e-4` learning rate used in Run 1, as it provided superior results.
2.  **Experiment with Optimizers:** Instead of changing the learning rate schedule, experiment with different optimizers like AdamW with different beta values.
3.  **Focus on Regularization:** The divergence between training and validation loss suggests that more aggressive regularization techniques, such as dropout or weight decay, could be beneficial.
4.  **Explore Larger Models:** Now that a solid fine-tuning strategy has been established with `whisper-tiny`, applying the successful methodology from Run 1 to a `whisper-small` model is a logical next step.

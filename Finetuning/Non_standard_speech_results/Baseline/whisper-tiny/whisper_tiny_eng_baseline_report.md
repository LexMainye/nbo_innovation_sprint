# Baseline Report: Fine-tuning the Whisper-Tiny Model on Non-Standard Kenyan English

*This report documents my initial baseline experiment and establishes a starting point for future improvements.*

## 1. Objective

The primary objective of this **baseline experiment** was to establish an initial proof-of-concept for adapting a pre-trained Whisper model to improve transcription accuracy on non-standard Kenyan English. This serves as my foundation for more sophisticated fine-tuning approaches in future iterations.

## 2. Methodology

### 2.1. The Model: Whisper-Tiny

I selected `openai/whisper-tiny` as my starting point for this baseline test, prioritizing computational efficiency for initial experimentation.

*   **Total Parameters:** 37,760,640
*   **Trainable Parameters (in this baseline):** 28,124,544

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The `cdli/kenyan_english_nonstandard_speech_v0.9` dataset was filtered to match Whisper's 30-second input constraint:

| Split      | Original Size | Filtered Size (<= 30s) |
|------------|---------------|------------------------|
| Train      | 4,236         | 3,130                  |
| Validation | 572           | 342                    |
| Test       | 993           | 705                    |

### 2.3. Baseline Fine-Tuning Strategy

For this initial approach, I implemented a conservative fine-tuning strategy:

*   **Partial Fine-tuning:** I froze the decoder weights to preserve language modeling capabilities, training only the **encoder** and **projection layer**.
*   **Basic Data Augmentation:** Used SpecAugment as a starting point for robustness.
*   **Initial Hyperparameters:** These represent my first configuration attempt and will be optimized in future work:
    *   **Learning Rate:** 1e-4
    *   **LR Scheduler:** Polynomial decay
    *   **Warmup Steps:** 50
    *   **Batch Size:** 32
    *   **Max Steps:** 1000
    *   **Epochs:** 10

## 3. Baseline Results

### 3.1. Complete Training Progress

The model was trained for 1000 steps with detailed monitoring throughout the process. The table below shows the complete training progression:

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.855072        | 0.496192 | 0.300682 |
| 50   | 1.577400      | 1.143882        | 0.382455 | 0.234951 |
| 100  | 1.122600      | 0.943556        | 0.320331 | 0.201145 |
| 150  | 0.907900      | 0.893870        | 0.310699 | 0.193778 |
| 200  | 0.737300      | 0.863549        | 0.299429 | 0.183945 |
| 250  | 0.650600      | 0.859953        | 0.309731 | 0.201053 |
| 300  | 0.546500      | 0.847804        | 0.309717 | 0.205854 |
| 350  | 0.615400      | 0.848164        | 0.289881 | 0.182723 |
| 400  | 0.512400      | 0.843910        | 0.299942 | 0.192762 |
| 450  | 0.530400      | 0.842340        | 0.303923 | 0.198941 |
| 500  | 0.478900      | 0.839813        | 0.292326 | 0.185351 |
| 550  | 0.469000      | 0.839845        | 0.287333 | 0.182577 |
| 600  | 0.491300      | 0.837253        | 0.287989 | 0.179562 |
| 650  | 0.444300      | 0.836542        | 0.289142 | 0.180851 |
| 700  | 0.501400      | 0.837258        | 0.285067 | 0.178262 |
| 750  | 0.486600      | 0.837185        | 0.288033 | 0.180756 |
| 800  | 0.479100      | 0.837094        | 0.288515 | 0.180901 |
| 850  | 0.450300      | 0.836998        | 0.285153 | 0.177648 |
| 900  | 0.481200      | 0.837003        | 0.285539 | 0.177671 |
| 950  | 0.459000      | 0.837014        | 0.286778 | 0.179822 |
| 1000 | 0.507800      | 0.836995        | 0.287535 | 0.180143 |

### Key Training Observations:
- **Rapid initial improvement**: WER dropped significantly from 49.6% to 28.5% in the first 700 steps.
- **Stabilization phase**: Performance plateaued around step 700, with minor fluctuations until the end of training.
- **Best validation WER**: ~28.5% achieved at steps 700 and 850.
- **Training loss continued decreasing** while validation metrics stabilized, indicating potential for improved regularization.

### 3.2. Final Baseline Evaluation

After training, the model with the best validation WER was loaded for final evaluation:

**Development Set:**
- **Loss:** 0.837
- **WER:** 0.285
- **CER:** 0.178

**Test Set:**
- **Loss:** 0.745
- **WER:** 0.209
- **CER:** 0.125

## 4. Current Deployment

This baseline model is available as a starting point for the modelling research:
[smainye/eng_finetunned_tune_whisper_tiny_model_baseline](https://huggingface.co/smainye/eng_finetunned_tune_whisper_tiny_model_baseline)

## 5. Conclusion & Future Directions

This baseline experiment successfully demonstrates that even with a very small model and a conservative fine-tuning strategy, significant improvements can be achieved for non standard Kenyan English transcription. The test set WER of 20.9% provides a solid foundation, but I consider this just the beginning.

### Key Limitations of This Baseline:
- Suboptimal convergence in later training stages.
- Conservative approach with a frozen decoder.
- Limited hyperparameter exploration.
- Basic data augmentation strategy.
- Training plateau after step 700 suggests a need for better optimization.

### Planned Improvements:
I'm actively working on the following enhancements:
- **Full model fine-tuning** (unfreezing the decoder).
- **Advanced hyperparameter optimization** with more adaptive learning rate scheduling.
- **More sophisticated data augmentation** techniques.
- **Larger model variants** (Whisper-small, medium, large).
- **Early stopping** strategies to prevent plateauing and save computational resources.
- **Cross-validation** for more robust evaluation.

### Training Insights for Future Work:
The complete training table reveals several opportunities:
- Earlier learning rate adjustments could improve convergence.
- Additional regularization might help with the validation loss plateau.
- The gap between training and validation metrics suggests room for better generalization techniques.

This baseline model serves as a reproducible starting point and performance benchmark. I welcome community feedback and collaboration to build upon these initial results.

---

*This report documents my initial baseline findings. I'm committed to iterating and improving upon these results in subsequent versions.*
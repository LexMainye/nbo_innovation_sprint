# Run 2 Report: Partially Fine-tuning of Whisper-Small on Non-Standard Kenyan English

*This report documents the second iteration of my experiments, investigating the impact of partial fine-tuning.*

## 1. Objective

The objective of this experiment was to explore whether a more conservative fine-tuning approach could yield comparable or better results than full fine-tuning, potentially reducing the risk of overfitting and preserving more of the model's original language modeling capabilities.

## 2. Methodology

### 2.1. The Model: Whisper-Small

I continued to use `openai/whisper-small` for this experiment.

*   **Total Parameters:** 241,734,912
*   **Trainable Parameters (in this run):** 144,855,552

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same filtered `cdli/kenyan_english_nonstandard_speech_v0.9` dataset was used:

| Split      | Filtered Size (<= 30s) |
|------------|------------------------|
| Train      | 3,130                  |
| Validation | 342                    |
| Test       | 705                    |

### 2.3. Fine-Tuning Strategy: Run 2

This run implemented a partial fine-tuning strategy:

*   **Partial Fine-tuning:** The encoder and projection layer were unfrozen, but only the **last 6 of the 12 decoder layers** were trained.
*   **Data Augmentation:** SpecAugment was used.
*   **Hyperparameters:** The learning rate was kept at `1e-5`.
    *   **Learning Rate:** 1e-5
    *   **LR Scheduler:** Polynomial decay
    *   **Warmup Steps:** 50
    *   **Batch Size:** 32
    *   **Max Steps:** 1000
    *   **Epochs:** 10

The following code was used to implement the partial unfreezing of the decoder:

```python
# --- Partial Unfreeze ---

print("Updating encoder:", UPDATE_ENCODER)
print("Updating projection layer:", UPDATE_PROJ)
print("Updating decoder: PARTIAL (last 6 layers)")

# 1. Unfreeze Encoder and Projection Layer as usual
base_model.model.encoder.requires_grad_(UPDATE_ENCODER)
base_model.proj_out.requires_grad_(UPDATE_PROJ)

# 2. Freeze the ENTIRE decoder first
base_model.model.decoder.requires_grad_(False)

# 3. Manually unfreeze ONLY the last 6 decoder layers
# whisper-small has 12 layers (0-11). We unfreeze 6, 7, 8, 9, 10, 11.
num_layers_to_unfreeze = 6
for layer in base_model.model.decoder.layers[-num_layers_to_unfreeze:]:
    layer.requires_grad_(True)

print("\nOverview to number of model parameters to be updated:")
print(f'* encoder params to update/total: {count_trainable_parameters(base_model.model.encoder)} / {base_model.model.encoder.num_parameters()}')
print(f'* decoder params to update/total: {count_trainable_parameters(base_model.model.decoder)} / {base_model.model.decoder.num_parameters()}')
print(f'* overall # trainable parameters: {count_trainable_parameters(base_model)}')
print(f'* overall # model parameters: {base_model.model.num_parameters()}')
```

## 3. Results

### 3.1. Complete Training Progress

The model was trained for 1000 steps. The training progression is as follows:

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.424863        | 0.278408 | 0.166250 |
| 50   | 1.093700      | 0.801271        | 0.210507 | 0.123854 |
| 100  | 0.842000      | 0.669326        | 0.195289 | 0.118191 |
| 150  | 0.710800      | 0.642502        | 0.190177 | 0.111880 |
| 200  | 0.650400      | 0.623584        | 0.180917 | 0.103797 |
| 250  | 0.579000      | 0.616913        | 0.184278 | 0.105580 |
| 300  | 0.543300      | 0.608861        | 0.178610 | 0.102962 |
| 350  | 0.651400      | 0.608421        | 0.180002 | 0.105405 |
| 400  | 0.563000      | 0.604676        | 0.179115 | 0.102318 |
| 450  | 0.578100      | 0.605900        | 0.174585 | 0.098645 |
| 500  | 0.511800      | 0.604217        | 0.172745 | 0.097590 |
| 550  | 0.528700      | 0.604252        | 0.173170 | 0.097758 |
| 600  | 0.547400      | 0.604074        | 0.173976 |.098591 |
| 650  | 0.523500      | 0.604294        | 0.173424 | 0.098144 |
| 700  | 0.566700      | 0.604130        | 0.174848 | 0.099139 |
| 750  | 0.557800      | 0.604074        | 0.175173 | 0.099269 |
| 800  | 0.562100      | 0.604055        | 0.175158 | 0.099185 |
| 850  | 0.489900      | 0.604078        | 0.175113 | 0.099176 |
| 900  | 0.559400      | 0.604091        | 0.175158 | 0.099250 |
| 950  | 0.532300      | 0.604065        | 0.174814 | 0.099082 |
| 1000 | 0.587800      | 0.604058        | 0.174912 | 0.099085 |

### Key Training Observations:
- **Best validation WER:** 17.27% achieved at step 500, a slight degradation from Run 1's 17.1%.
- The training curve is very similar to Run 1, indicating that the final layers of the decoder are the most impactful for this task.

### 3.2. Final Evaluation: Run 2 vs. Baseline and Run 1

The model with the best validation WER was evaluated on the development and test sets.

**Development Set:**
- **Run 2 WER:** 0.173
- **Run 1 WER:** 0.171
- **Baseline WER:** 0.180

**Test Set:**
- **Run 2 WER:** 0.113
- **Run 1 WER:** 0.109
- **Baseline WER:** 0.123

| Metric | Baseline | Run 1 (Full FT) | Run 2 (Partial FT) |
|---|---|---|---|
| **Dev WER** | 0.180 | 0.171 | **0.173** |
| **Test WER** | 0.123 | **0.109** | 0.113 |
| **Dev CER** | 0.102 | **0.098** | 0.098 |
| **Test CER** | 0.065 | **0.058** | 0.058 |


## 4. Conclusion & Future Directions

This second experimental run with **partial fine-tuning shows a slight degradation in performance compared to full fine-tuning (Run 1)**. While it still represents a significant improvement over the baseline, the full fine-tuning approach appears to be more effective for this dataset.

### Planned Improvements:
- Revisit the learning rate and scheduler, as the plateau persists.
- Test if a cosine scheduler improves the model with settings similar to Run 1.
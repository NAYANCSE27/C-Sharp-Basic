# EfficientNetV2 for Cucumber Dataset (8 Classes)

This folder contains a TensorFlow/Keras training script that trains **EfficientNetV2** on an 8‑class cucumber dataset with the requested settings:

- Image size: **128x128**
- Batch size: **16**
- Epochs: **20**
- EfficientNetV2 model with **weights=None** (training from scratch)
- Best‑model checkpoint saving
- Multiple descriptive plots for training/validation
- XAI with Grad‑CAM

## Expected Dataset Layout

```
/datasets/
  class_1/
    img1.jpg
  class_2/
    img2.jpg
  ...
```

The script auto-splits this single-folder layout into train/val/test splits.

## Quick Start

```bash
python train_efficientnetv2.py \
  --data_dir /kaggle/input/cucumber-dataset/Original Image \
  --output_dir /kaggle/working
```

## Kaggle/Notebook Note

This script uses `parse_known_args()` so notebook kernels (e.g., Kaggle/Jupyter) can pass extra flags (like `-f <kernel.json>`) without errors. If you see a `FileNotFoundError`, update `--data_dir` to your dataset root.

If Kaggle stops mid-training when you set a high epoch count, lower `--epochs` (the default is 20) or rely on EarlyStopping to finish early and avoid runtime limits.

## Outputs

- `outputs/best_model.keras` — best model checkpoint
- `outputs/training_curves.png` — loss/accuracy curves
- `outputs/confusion_matrix.png` — confusion matrix
- `outputs/classification_report.txt` — precision/recall/F1
- `outputs/roc_curves.png` — One‑vs‑Rest ROC curves
- `outputs/gradcam_examples.png` — Grad‑CAM XAI visualization

## Notes on Resource Usage

The script enables mixed precision and conservative augmentation, and uses `prefetch` to keep GPU utilization efficient while staying within a 15GB GPU limit.

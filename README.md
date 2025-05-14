## Ovarian Cancer Prediction via Multi-Model Fusion

This repository contains code, trained models, and visualizations for a research project aimed at improving ovarian cancer diagnosis by distinguishing benign from malignant cases. Our approach leverages domain-specific Random Forest models for tumor markers and clinical/hematological data, then fuses their outputs in a meta-learner to boost overall diagnostic accuracy.

### Project Motivation

Early and accurate detection of ovarian cancer is critical for improving patient outcomes. Traditional single-domain models often miss complementary signals present across different data sources. By training separate models on biochemical tumor markers and on clinical/hematological features—and then fusing their predictions—we capture a broader range of diagnostic patterns, reducing false negatives and enhancing reliability.

### Repository Overview

* **models/**: Stores all trained model artifacts and preprocessing scalers. These include the Random Forest classifiers and their associated data scalers for each data domain.
* **training/**: Contains Jupyter notebooks used for data preprocessing, model training, evaluation, and fusion of domain-specific models.
* **visualizations/**: Holds the notebook for exploratory data analysis and plotting, showcasing feature distributions, correlations, and imputation details.

### Getting Started

1. Clone the repository:

   ```bash
   git clone <repo_url>
   ```
2. Install dependencies (e.g., scikit-learn, pandas, joblib, matplotlib).
3. Explore the notebooks in the `training/` directory to understand data processing steps and model training.
4. Use the artifacts in `models/` within your own inference scripts or APIs.
5. Review `visualizations/data-visualization.ipynb` for insights into data quality, feature behavior, and imputation strategies.

### Usage

Load the fused model and scalers to make predictions on new patient data:

```python
import joblib

# Load models and scalers
scaler_tumor = joblib.load('models/random-forest/scaler_tumor_markers.joblib')
model_tumor  = joblib.load('models/random-forest/rf_model_tumor_markers.joblib')
# ... similarly for clinical

# Preprocess, predict probabilities, and fuse
...
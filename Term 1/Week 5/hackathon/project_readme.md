# Adult Income Classification — Model Showdown

## Project Overview

This project compares three supervised machine-learning classifiers on the UCI Adult Income dataset. The task is to predict whether a person's recorded annual income is **above $50,000** (`>50K`) or **at most $50,000** (`<=50K`) using demographic and employment-related attributes. The project connects to **Sustainable Development Goal 8 (Decent Work and Economic Growth)** by examining income distributions to support targeted economic development programs.

## Target User and Decision Context

- **Target User:** Regional Economic Development Officers and Workforce Investment Boards.
- **Intended Decision:** Identifying demographic cohorts and income distributions to allocate targeted career-upskilling grants and vocational training subsidies.
- **Cost of Errors:**
  - A **false negative** (predicting `<=50K` when true income is `>50K`) risks misallocating limited public grant funds to higher earners who do not require aid.
  - A **false positive** (predicting `>50K` when true income is `<=50K`) unfairly denies financial support and vocational training to low-income individuals seeking upward economic mobility.
- **Metric Choice:** Because denying support to low earners severely hinders mobility, our primary evaluation metric is **F1-score for the positive class (`>50K`)**, striking a balance between precision and recall on an imbalanced dataset.

## Dataset Card

- **Source & Link:** [UCI Machine Learning Repository — Adult Dataset](https://archive.ics.uci.edu/dataset/2/adult)
- **Collector:** Extracted by **Barry Becker** from the **1994 US Census Bureau** database (Current Population Survey).
- **Collection Date & Method:** Extracted in 1994 using population filtering constraints (e.g., age > 16, record weight > 100).
- **License:** **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
- **Dimensions:** **32,561 records** across **15 columns** (14 input features and 1 target variable).
- **Target & Class Balance:** Target column is `income`. Highly imbalanced: **75.9% `<=50K`** (24,720 records) and **24.1% `>50K`** (7,841 records).
- **Known Limitations:** Contains missing values in `workclass`, `occupation`, and `native_country`. Reflects historical 1994 US wage gaps and demographic biases, underrepresenting women and minority demographics relative to modern workforce distributions.

## Methods

**Data Split.** The dataset is split into **80% training** and **20% test** data using a stratified split (`random_state=42`) to preserve class proportions before applying any cleaning or scaling.

**Preprocessing.** Transformations occur strictly within scikit-learn's `ColumnTransformer` and `Pipeline`:
- **Numeric Features:** Median imputation followed by standard scaling.
- **Categorical Features:** Most-frequent value imputation followed by one-hot encoding (`handle_unknown='ignore'`).

**Baseline.** A `DummyClassifier(strategy='most_frequent')` provides a baseline by always predicting the majority income class (`<=50K`).

**Models Compared:**
- **K-Nearest Neighbors (KNN)**, tuning `n_neighbors`.
- **Logistic Regression**, tuning regularization parameter `C`.
- **Random Forest**, tuning `max_depth` and `min_samples_leaf` (with 200 trees).

**Validation.** Hyperparameters are selected via `GridSearchCV` using **5-fold stratified cross-validation** on the training set using F1-score. Final fitted models are evaluated on the held-out test set.

## Results

The evaluation results on the held-out test set are summarized below:

| Model | Best tuned hyperparameters | Cross-validation F1 | Test precision | Test recall | Test F1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Majority-class baseline | — | 0.000 | 0.000 | 0.000 | 0.000 |
| KNN | `n_neighbors=15` | 0.647 | 0.706 | 0.614 | 0.657 |
| Logistic Regression | `C=10` | 0.656 | 0.740 | 0.617 | 0.673 |
| Random Forest | `max_depth=20`, `min_samples_leaf=1` | **0.675** | **0.790** | **0.621** | **0.695** |

Cross-validation F1 standard deviations across folds: **0.008** (KNN), **0.011** (Logistic Regression), and **0.009** (Random Forest).

## Subgroup Error & Fairness Analysis

To check for algorithmic bias across demographics, test-set performance was evaluated separately by sex:
- **Female Group:** Test Precision = 0.762 | Recall = 0.541 | F1 = 0.633
- **Male Group:** Test Precision = 0.796 | Recall = 0.640 | F1 = 0.710

**Key Finding:** The model exhibits lower recall for female candidates compared to male candidates. This reflects historical wage disparities encoded in the 1994 census dataset, leading the model to underpredict high income for women.

## Recommended Model & Pipeline Defense

- **Recommended Model:** **Random Forest** (`max_depth=20`, `min_samples_leaf=1`). It achieves the highest cross-validation F1 score (0.675) as well as the highest test precision (0.790) and test F1 score (0.695).
- **Pipeline Decision to Defend:** Performing the train-test split **prior to imputation and feature scaling within a unified `Pipeline`**. Fitting imputers and scaling parameters strictly on training folds prevents data leakage from the test set, guaranteeing an honest, uninflated performance estimate.

## Example Prediction

The notebook demonstrates submitting a new record to the trained Random Forest pipeline. The input array is processed through the full transformer pipeline to return a final predicted income class and class probability.

## Limitations and Ethical Considerations

The dataset contains sensitive demographic attributes recorded in 1994. Learned patterns reflect historical structural inequality. Models derived from this data must not be used as an automated decision tool for hiring, credit extension, or individual grant eligibility determinations without human oversight, modern data re-sampling, and fairness audits.

## Running the Notebook

1. Open **`adult_income_combined.ipynb`** in Jupyter Notebook, JupyterLab, or Google Colab.
2. Download `adult.data` from UCI or run the automated ingestion cell in the notebook.
3. Install required packages:

```bash
pip install pandas numpy matplotlib scikit-learn>=1.2
```

4. Run all cells in sequence (`Restart and Run All`).

## Files

- `adult_income_combined.ipynb` — Primary notebook containing data exploration, pipeline definition, model tuning, subgroup evaluation, and live inference.
- `README.md` — Project documentation and dataset card.
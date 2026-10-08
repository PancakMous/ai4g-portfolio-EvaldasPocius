# Adult Income Classification — Model Showdown

## Project overview

This project compares three supervised machine-learning classifiers on the UCI Adult Income dataset. The task is to predict whether a person's recorded annual income is **above $50,000** (`>50K`) or **at most $50,000** (`<=50K`) using demographic and employment-related attributes. The project is connected to **Sustainable Development Goal 8 (Decent Work and Economic Growth)** through its examination of income patterns. The models identify statistical patterns in this dataset; they do not establish why individuals earn different amounts.

## Dataset

The project uses the **Adult Income** dataset, loaded from a local file named `adult.data`. The notebook defines 15 columns: 14 input features and the target `income`. There are **32,561 records**. Features include age, education, workclass, occupation, marital status, working hours, capital gains and losses, and demographic attributes.

The target is imbalanced: approximately **75.9%** of records are `<=50K` and **24.1%** are `>50K`. Missing values are present in `workclass`, `occupation`, and `native_country`. The exploratory analysis includes dataset shape, data types, missing values, target distribution, and descriptive statistics.

Source: [UCI Machine Learning Repository — Adult](https://archive.ics.uci.edu/dataset/2/adult).

## Methods

**Data split.** The dataset is split into **80% training** and **20% test** data using a stratified split (`random_state=42`) to preserve the income-class proportions.

**Preprocessing.** Scikit-learn's `ColumnTransformer` and `Pipeline` are used so that transformations are learned from the training data. Numeric columns receive median imputation and standard scaling. Categorical columns receive most-frequent-value imputation and one-hot encoding (`handle_unknown='ignore'`).

**Baseline.** A `DummyClassifier(strategy='most_frequent')` provides a baseline by always predicting the majority income class.

**Models.** Three classifiers are compared:

- **K-Nearest Neighbors (KNN)**, tuning `n_neighbors`.
- **Logistic Regression**, tuning regularization parameter `C`.
- **Random Forest**, tuning `max_depth` and `min_samples_leaf` (with 200 trees).

**Validation.** Hyperparameters are selected with `GridSearchCV` using **five-fold stratified cross-validation** on the training set. The primary optimization metric is **F1-score for the positive class (`>50K`)**. The notebook then evaluates fitted models on the held-out test set using precision, recall, F1-score, and confusion matrices.

F1-score balances precision and recall, which is useful because the income classes are imbalanced and a majority-class prediction would otherwise achieve relatively high accuracy.

## Results

The following are the results saved in the original notebook, rounded to three decimals.

| Model | Best tuned hyperparameters | Cross-validation F1 | Test precision | Test recall | Test F1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Majority-class baseline | — | 0.000 | 0.000 | 0.000 | 0.000 |
| KNN | `n_neighbors=15` | 0.647 | 0.706 | 0.614 | 0.657 |
| Logistic Regression | `C=10` | 0.656 | 0.740 | 0.617 | 0.673 |
| Random Forest | `max_depth=20`, `min_samples_leaf=1` | **0.675** | **0.790** | **0.621** | **0.695** |

The cross-validation F1 standard deviations shown in the notebook are **0.008** for KNN, **0.011** for Logistic Regression, and **0.009** for Random Forest.

**Interpretation.** Random Forest has the highest recorded test F1-score (0.695), as well as the highest test precision and recall among the tested models. However, the notebook sets **Logistic Regression** as its selected model for the example prediction. Logistic Regression is simpler to interpret, although the current numerical comparison favors Random Forest on F1. A final deployment recommendation would need to consider interpretability alongside the costs of different prediction errors.

## Example prediction

The notebook demonstrates how to submit a new record to the chosen model. For the example record defined in the notebook, Logistic Regression predicts **`>50K`** and estimates a **0.56 probability** of the positive class. This is a model output on an illustrative record, not a verified real-world income estimate.

## Limitations and ethical considerations

The dataset contains sensitive demographic attributes, and patterns learned from historical income data may reflect existing inequalities. Income classification based on such variables should not be used as the sole basis for employment, credit, or other consequential decisions. The dataset's class imbalance also means that overall accuracy can be misleading. The notebook reports precision, recall, F1-score and confusion matrices, but it does not yet establish fairness across demographic groups or validate performance on a modern, external dataset. Predictions should therefore be interpreted cautiously.

## Running the notebook

1. Open **`adult_income_combined.ipynb`** in Jupyter Notebook, JupyterLab, or Google Colab.
2. Download the Adult dataset from the UCI repository, and place the file **`adult.data`** in the notebook's working directory (or update the path in the first code cell).
3. Ensure Python has these libraries installed: `pandas`, `numpy`, `matplotlib`, and `scikit-learn`.
4. Run the notebook cells in order, starting with data loading and ending with the model evaluation and example prediction.

A compatible installation command is:

```bash
pip install pandas numpy matplotlib scikit-learn
```

The notebook's one-hot encoder uses `sparse_output=False`, which requires a compatible recent scikit-learn version (1.2 or later).

## Files

- `adult_income_combined.ipynb` — original notebook containing data exploration, preprocessing, model training, validation, testing, and example prediction.
- `README.md` — this project description.

## Summary

Three classification models were trained and compared using a consistent preprocessing and validation approach. All three outperform the majority-class baseline on F1-score. **Random Forest achieves the highest measured F1-score**, while **Logistic Regression is the model currently selected in the notebook for the demonstration prediction**.

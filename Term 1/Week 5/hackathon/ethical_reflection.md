# Ethical Reflection

**Context & Application:**  
This model uses the 1994 US Census Adult dataset to predict income eligibility for targeted career upskilling grants allocated by regional workforce investment boards.

**Data Representation & Demographic Coverage:**  
The underlying dataset reflects severe demographic sampling biases and historical wage inequalities. It is heavily skewed toward US-born working-age men from the mid-1990s, while significantly underrepresenting women, non-US immigrants, and workers in non-traditional or informal employment sectors.

**Impact of Classification Errors:**  
- **False Negative (predicting `<=50K` for a true `>50K` earner):** Misallocates public career subsidies and grant funds to individuals who do not require financial assistance.
- **False Positive (predicting `>50K` for a true `<=50K` earner):** Unfairly denies critical vocational training and economic support to low-income workers seeking upward mobility.

**Subgroup Bias & Proxy Leakage:**  
A subgroup performance check across sex revealed a notable disparity: the tuned Random Forest model achieved a recall of **64.0% for men**, but only **54.1% for women**. Because the 1994 dataset incorporates systemic wage gaps, female high-earners are disproportionately misclassified. Even if sensitive demographic attributes like `sex` or `race` were dropped from feature sets, strong proxy variables—such as `occupation`, `hours-per-week`, and `marital-status`—continue to propagate these structural patterns.

**Consent & Licensing:**  
Census respondents in 1994 provided information for government statistical collection, not for automated AI eligibility scoring. However, the dataset's public domain license permits research reuse.

**Action Taken to Mitigate Risk:**  
To address these risks, we:
1. Replaced raw accuracy with **F1-score for the positive class** as our primary optimization metric to prevent majority-class bias.
2. Performed an explicit **subgroup error analysis** across demographic categories to measure disparity in error rates.
3. Added an **explicit restriction in the documentation** stating that this model must never serve as an automated, standalone decision tool for grant eligibility without human oversight and modern bias audits.
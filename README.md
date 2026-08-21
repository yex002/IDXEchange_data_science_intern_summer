# IDXchange_data_science
## Repository Structure

- `data/` contains the cleaned and preprocessed data.
- `results/`
    - `baseline_result/` contains the results of the baseline models: Ordinary Linear Regression, Ridge Regression, Lasso Regression, and ElasticNet.
    - `models_result/` contains the results of the advanced models: Decision Tree, Random Forest, XGBoost, and LightGBM.
- `01_exploration.ipynb` performs exploratory data analysis (EDA) on the dataset.
- `02_preprocessing.ipynb` contains the data preprocessing pipeline used to generate the cleaned dataset.
- `03_baseline_model.ipynb` contains experiments with the baseline models.
- `04_model_comparision.ipynb` compares baseline and advanced models before and after feature engineering.
- `05_advanced_model.ipynb` contains experiments with the advanced models.
- `06_evaluation.ipynb` evaluates the final selected model on the dataset.
- `07_app.ipynb` contains the model training process for the Streamlit application.
- `app.py` implements the Streamlit application.
- `house_price_model.pkl` is the trained model used by the Streamlit application.


## Dataset Overview
This dataset is derived from the California Regional Multiple Listing Service (CRMLS), a regional Multiple Listing Service (MLS) that serves much of Southern California. MLS is a cooperative database where licensed real estate agents share property listings and transaction information. The dataset contains residential property transaction records from May 2025 through Jun 2026, including property characteristics, pricing, location, lot information, and other key real estate attributes. It is suitable for exploratory data analysis, data visualization, and predictive modeling tasks such as house price analysis.

### Key Dataset Fields

| Field | Description |
|-------|-------------|
| **ListingKey** | Unique identifier for each property listing. |
| **ListingContractDate** | Date when the property was listed on the MLS. |
| **ListPrice** | Seller's asking price at the time of listing. |
| **PurchaseContractDate** | Date when the purchase agreement was signed by both buyer and seller. |
| **ClosePrice** | Final sale price after the transaction was completed (target variable). |
| **CloseDate** | Date when the transaction officially closed. |
| **LivingArea** | Interior living area (square feet). |
| **BedroomsTotal** | Total number of bedrooms. |
| **BathroomsTotalInteger** | Total number of bathrooms (integer). |
| **Latitude / Longitude** | Geographic coordinates of the property. |
| **UnparsedAddress** | Full property address as entered into the MLS. |

### Transaction Lifecycle

The residential property transaction process in the MLS can be summarized into four stages:

1. **Listing** – The seller lists the property through a licensed real estate agent. Property information such as the listing price, address, living area, bedrooms, and lot size is entered into the MLS, making the property available on the market.

2. **Offer & Purchase Agreement** – Buyers submit offers, and once an offer is accepted, both parties sign a purchase agreement that establishes the sale price and closing timeline. The property status changes from **Active** to **Pending**.

3. **Escrow & Due Diligence** – During the escrow period, inspections, appraisals, financing approval, title verification, and other contractual contingencies are completed. If any contingency is not satisfied, the transaction may be canceled and the property can return to the market.

4. **Closing** – After all contingencies are cleared, ownership is transferred, the transaction is finalized, and the final **ClosePrice** and **CloseDate** are recorded in the MLS.

### Exploration of the dataset
#### Dataset info
The filtered dataset contains 188,550 residential property records with 79 features. Among these variables, there are 27 floating-point features, 3 integer features, and 49 categorical features. While the dataset is largely complete for the variables required in this assignment, several optional attributes contain substantial missing values, and a few columns are entirely empty (e.g., TaxAnnualAmount and FireplacesTotal). Therefore, these variables are excluded from the exploratory analysis. Following the project requirements, the subsequent EDA focuses on the distributions of ClosePrice, LivingArea, BedroomsTotal, BathroomsTotalInteger, and LotSizeSquareFeet, using only Residential Single Family Residence properties.


## Dataset Notes

### Price Fields

- **ListPrice**: Seller's asking price before the property is sold.
- **ClosePrice**: Final transaction price (target variable).
- **Sale-to-List Ratio = ClosePrice / ListPrice**
  - > 1.0 → Sold above asking price (seller's market).
  - < 1.0 → Sold below asking price (buyer's market).

---

### Agent Information

- Listing agent and buyer agent information are included.
- Can be used for:
  - Brokerage performance analysis.
  - Agent market share analysis.
  - Sale-to-list ratio comparison.

---

### Listings vs. Sold Dataset

- **Listings Dataset**
  - Includes Active, Pending, Expired, Withdrawn, and Closed properties.
  - Mainly used for inventory/supply analysis.

- **Sold Dataset**
  - Contains completed transactions only.
  - Always includes **ClosePrice** and **CloseDate**.
  - Used for price analysis.

---

### MLS Status

Common listing statuses:

- Active
- Pending
- Closed
- Back on Market
- Expired
- Withdrawn

> **Note:** Price analysis should only use records with **MLSStatus = Closed**.

---

### Days on Market (DOM)

- **DOM** measures the number of days a property remains on the market before selling.
- Interpretation:
  - **1–7 days:** Very competitive market.
  - **8–30 days:** Healthy market.
  - **31–60 days:** Moderate demand.
  - **60+ days:** Weak demand or possible overpricing.

---

### Property Types

Common property types include:

- Single Family Residence
- Condominium
- Townhouse
- Multi-Family
- Manufactured Home

> **Note:** Different property types have different market characteristics and should not be mixed during analysis.

---

### Mortgage Background

Typical down payments:

- 3–5%
- 10%
- 20% (standard)
- 25%+ (investment/jumbo loans)

Higher mortgage interest rates generally reduce buyer affordability and may decrease market activity.

---

### Project Scope

This project follows the task requirements:

- Use at least **6 months** of historical data.
- Restrict the dataset to:
  - **PropertyType = Residential**
  - **PropertySubType = SingleFamilyResidence**
- Perform exploratory analysis on:
  - ClosePrice
  - LivingArea
  - Bedrooms
  - Bathrooms
  - Lot Size
    
## Preprocess

1. **Handle features with excessive missing values**
   - Features with more than 10% missing values were removed.
   - This step was performed before removing individual records with missing values, since directly dropping all incomplete records could result in a substantial loss of useful data.

2. **Remove unreasonable records**
   - Records with invalid or logically inconsistent values were removed.
   - For example, records that did not satisfy `CloseDate >= ListingContractDate` were considered invalid.

3. **Remove irrelevant and leakage-prone features**
   - Irrelevant features that do not provide useful information for house price prediction were removed.
   - Features that could potentially introduce future information leakage were also excluded.

4. **Handle unrealistic and missing values**
   - Unrealistic numerical values were replaced with `NaN` for subsequent processing.
   - For example, `LotSizeSquareFeet = 0` was considered invalid and treated as a missing value.
   - For some categorical features, missing values were replaced with `"Unknown"` to preserve potentially useful records instead of removing them entirely.

5. **Encode categorical features**
   - Categorical features with a relatively small number of categories were converted using one-hot encoding.

6. **Feature engineering**
   - After obtaining the cleaned dataset, additional features were created to provide more useful information for house price prediction.
   - These features include `BedBathRatio`, property age-related features, and geographic features.

7. **Train-test split and outlier removal**
   - The cleaned dataset was split into training and test sets.
   - Extreme outliers were removed from the training set using the 0.5th and 99.5th percentiles (0.005–0.995).
   - Outlier removal was applied only to the training set to avoid modifying the test distribution.

8. **Encode high-cardinality categorical features**
   - For categorical features with a large number of categories, the top 10 most frequent categories were retained.
   - All remaining categories were grouped into an `"Other"` category.
   - The resulting categorical features were then converted using one-hot encoding.


## Model tested
We trained and evaluated five regression models on the dataset: **ElasticNet, Decision Tree, Random Forest, XGBoost, and LightGBM**.
### Model Comparison

| Model | R² | MdAPE | MAPE | MAE | RMSE |
|---|---:|---:|---:|---:|---:|
| ElasticNet | -0.5648 | 32.93% | 2179.37% | 347,199.82 | 1,436,940.58 |
| Decision Tree | 0.6446 | 14.66% | 43.98% | 194,431.04 | 684,824.67 |
| Random Forest | 0.6889 | **9.13%** | **34.78%** | 138,977.82 | 640,705.50 |
| XGBoost | 0.6918 | 11.86% | 43.57% | **134,340.31** | 637,684.63 |
| LightGBM | **0.7122** | 14.44% | 179.20% | 140,642.22 | **616,283.11** |

### Analysis

The five regression models showed substantial differences in predictive performance. ElasticNet performed poorly, with a negative R² of **-0.5648** and a MdAPE of **32.93%**, indicating that a linear model is not sufficient to capture the complex relationships between housing features and sale prices.

All tree-based models significantly outperformed ElasticNet. The Decision Tree achieved an R² of **0.6446** and a MdAPE of **14.66%**, demonstrating that modeling nonlinear relationships substantially improves prediction performance.

Among the ensemble models, Random Forest, XGBoost, and LightGBM achieved similar overall performance but showed different strengths. **LightGBM achieved the highest R² (0.7122) and the lowest RMSE (616,283.11)**, indicating the strongest overall fit and better performance in terms of squared prediction errors. **XGBoost achieved the lowest MAE (134,340.31)**, while **Random Forest achieved the lowest MdAPE (9.13%) and MAPE (34.78%)**, indicating better typical percentage prediction accuracy.

The relatively large MAPE values, particularly for ElasticNet and LightGBM, suggest that percentage errors are strongly affected by some observations. Since MAPE can become very large when actual values are relatively small, **MdAPE provides a more robust measure of typical percentage prediction error** for this dataset.

Overall, the results demonstrate that ensemble tree-based models are substantially more effective than the linear baseline for housing price prediction. While **LightGBM provides the highest R² and lowest RMSE**, **Random Forest provides the lowest percentage-based prediction errors**. Therefore, the preferred model depends on whether overall variance explanation or typical relative prediction accuracy is prioritized.

## Best Result

Although LightGBM achieved the highest R², Random Forest produced substantially lower MdAPE and MAPE, indicating better relative prediction accuracy across individual properties. Since the primary objective of this project is accurate house price prediction, Random Forest was selected as the final model.

### Overall Performance

The final Random Forest model achieved the following performance on the test dataset:

- **R²:** 0.6889
- **MdAPE:** 9.13%
- **MAPE:** 34.78%
- **MAE:** 138,977.82
- **RMSE:** 640,705.50

The model achieved a test **MdAPE of 9.13%** and an **R² of 0.6889**. The low MdAPE indicates that the typical relative prediction error is relatively small, while the R² value suggests that the model explains approximately **69% of the variance in house prices**.

Overall, the model provides reasonably accurate predictions and demonstrates good generalization performance on the test dataset.

### Performance by Price Band

| Price Band | Count | MdAPE | MAPE |
|---|---:|---:|---:|
| < $300K | 1,802 | 10.30% | 85.21% |
| $300K–$600K | 1,317 | 7.92% | 13.60% |
| $600K–$1M | 1,411 | **7.05%** | **11.31%** |
| > $1M | 1,514 | 11.67% | 15.03% |

The model achieves the lowest MdAPE for houses priced between **$600K and $1M (7.05%)**, followed by houses priced between **$300K and $600K (7.92%)**, indicating better prediction accuracy in the mid-price range.

In comparison, the MdAPE increases for houses priced below **$300K (10.30%)** and above **$1M (11.67%)**, suggesting that the model performs less accurately at the lower and upper ends of the housing market. These price ranges may exhibit greater variability or contain properties with characteristics that are more difficult for the model to capture.

### Error Distribution

The distribution of absolute percentage error is right-skewed, with most observations concentrated in the lower error range. Most properties have an absolute percentage error below **40%**, indicating that the model provides relatively accurate predictions for the majority of houses.

Only a small proportion of properties exhibit errors greater than 40%, suggesting that large relative prediction errors are comparatively uncommon.

### Feature Importance

The feature importance analysis shows that `PropertyType_ResidentialLease` and `LivingArea` are the two most influential features in the Random Forest model. Their importance scores are substantially higher than those of the remaining features, indicating that property type and living area play particularly important roles in the model's house price predictions.



# IDXchange_data_science

## Dataset Overview
This dataset is derived from the California Regional Multiple Listing Service (CRMLS), a regional Multiple Listing Service (MLS) that serves much of Southern California. MLS is a cooperative database where licensed real estate agents share property listings and transaction information. The dataset contains residential property transaction records from May 2025 through May 2026, including property characteristics, pricing, location, lot information, and other key real estate attributes. It is suitable for exploratory data analysis, data visualization, and predictive modeling tasks such as house price analysis.

## Key Dataset Fields

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

## Transaction Lifecycle

The residential property transaction process in the MLS can be summarized into four stages:

1. **Listing** – The seller lists the property through a licensed real estate agent. Property information such as the listing price, address, living area, bedrooms, and lot size is entered into the MLS, making the property available on the market.

2. **Offer & Purchase Agreement** – Buyers submit offers, and once an offer is accepted, both parties sign a purchase agreement that establishes the sale price and closing timeline. The property status changes from **Active** to **Pending**.

3. **Escrow & Due Diligence** – During the escrow period, inspections, appraisals, financing approval, title verification, and other contractual contingencies are completed. If any contingency is not satisfied, the transaction may be canceled and the property can return to the market.

4. **Closing** – After all contingencies are cleared, ownership is transferred, the transaction is finalized, and the final **ClosePrice** and **CloseDate** are recorded in the MLS.

## Exploration of the dataset
### Dataset info
The filtered dataset contains 188,550 residential property records with 79 features. Among these variables, there are 27 floating-point features, 3 integer features, and 49 categorical features. While the dataset is largely complete for the variables required in this assignment, several optional attributes contain substantial missing values, and a few columns are entirely empty (e.g., TaxAnnualAmount and FireplacesTotal). Therefore, these variables are excluded from the exploratory analysis. Following the project requirements, the subsequent EDA focuses on the distributions of ClosePrice, LivingArea, BedroomsTotal, BathroomsTotalInteger, and LotSizeSquareFeet, using only Residential Single Family Residence properties.


# Dataset Notes

## Price Fields

- **ListPrice**: Seller's asking price before the property is sold.
- **ClosePrice**: Final transaction price (target variable).
- **Sale-to-List Ratio = ClosePrice / ListPrice**
  - > 1.0 → Sold above asking price (seller's market).
  - < 1.0 → Sold below asking price (buyer's market).

---

## Agent Information

- Listing agent and buyer agent information are included.
- Can be used for:
  - Brokerage performance analysis.
  - Agent market share analysis.
  - Sale-to-list ratio comparison.

---

## Listings vs. Sold Dataset

- **Listings Dataset**
  - Includes Active, Pending, Expired, Withdrawn, and Closed properties.
  - Mainly used for inventory/supply analysis.

- **Sold Dataset**
  - Contains completed transactions only.
  - Always includes **ClosePrice** and **CloseDate**.
  - Used for price analysis.

---

## MLS Status

Common listing statuses:

- Active
- Pending
- Closed
- Back on Market
- Expired
- Withdrawn

> **Note:** Price analysis should only use records with **MLSStatus = Closed**.

---

## Days on Market (DOM)

- **DOM** measures the number of days a property remains on the market before selling.
- Interpretation:
  - **1–7 days:** Very competitive market.
  - **8–30 days:** Healthy market.
  - **31–60 days:** Moderate demand.
  - **60+ days:** Weak demand or possible overpricing.

---

## Property Types

Common property types include:

- Single Family Residence
- Condominium
- Townhouse
- Multi-Family
- Manufactured Home

> **Note:** Different property types have different market characteristics and should not be mixed during analysis.

---

## Mortgage Background

Typical down payments:

- 3–5%
- 10%
- 20% (standard)
- 25%+ (investment/jumbo loans)

Higher mortgage interest rates generally reduce buyer affordability and may decrease market activity.

---

## Project Scope

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

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
# 做一个更完整的app

# 注意这里模型最后应该做整体的fit

# home - 介绍我们的信息的
st.set_page_config(
    page_title="Housing Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# =========================
# Sidebar Navigation
# =========================
st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Go to",
    ["🏠 Home", "💰 Prediction", "🔍 EDA Analysis"]
)

if page == "🏠 Home":
    st.title("🏠 Housing Price Prediction")

    st.write("""
Welcome to the Housing Price Prediction App.

This application uses a LightGBM model to predict property closing prices based on housing characteristics.

The model was trained on a dataset derived from the California Regional Multiple Listing Service (CRMLS), containing residential property transaction records from June 2025 through May 2026.

The exploratory data analysis (EDA) was conducted on the dataset containing transaction records from June 2025 through June 2026.""")

elif page == "💰 Prediction":
    # Load the trained pipeline
    st.title("💰 Prediction")
    model = joblib.load("house_price_model.pkl")
    st.title("House Price Prediction")
    # User inputs
    living_area = st.number_input("Living Area", min_value=0.0)
    beds = st.number_input("Bedrooms", min_value=0)
    baths = st.number_input("Bathrooms", min_value=0)
    lot_size = st.number_input("Lot Size (SquareFeet)", min_value=0.0)
    BedBathRatio = beds/baths if baths > 0 else 0
    # Prediction
    if st.button("Predict"):
        input_data = pd.DataFrame({
        "LivingArea": [living_area],
        "Beds": [beds],
        "Baths": [baths],
        "LotSize": [lot_size],
        "BedBathRatio": [BedBathRatio],
        })

        prediction = model.predict(input_data)[0]
        if living_area > 60000:
            st.warning("The living area is unusually large. Prediction may be less reliable.")
        elif living_area <= 0:
            st.warning("Living area must be greater than 0.")
        elif beds <= 0:
            st.warning("Number of bedrooms must be greater than 0.")

        elif baths <= 0:
            st.warning("Number of bathrooms must be greater than 0.")

        elif lot_size <= 0:
            st.warning("Lot size must be greater than 0.")
        else:
            st.success(f"Estimated House Price: ${prediction:,.2f}")

elif page == "🔍 EDA Analysis":
    # data explore之类的介绍:比如现有模型的一些图之类的
    # 主题就是home,EDA， model的介绍以及prediction
    st.title("🔍 Exploratory Data Analysis")
    df=pd.read_csv(r"C:\Users\23035\cleaned_dataset.csv")
    map_df = df.dropna(
        subset=["Latitude", "Longitude", "ClosePrice"]
    )

    # Price ranges
    bins = [
        0,
        300_000,
        500_000,
        750_000,
        1_000_000,
        1_500_000,
        3_000_000,
        float("inf")
    ]

    labels = [
        "$0–300K",
        "$300K–500K",
        "$500K–750K",
        "$750K–1M",
        "$1M–1.5M",
        "$1.5M–3M",
        "$3M+"
    ]

    map_df["PriceBand"] = pd.cut(
        map_df["ClosePrice"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    st.write(
        "This section provides an exploratory analysis "
        "of the cleaned housing transaction dataset."
    )

    # Price distribution
    st.subheader("Closing Price Distribution")

    st.write("Most property transactions are concentrated below $1.5M$, with the largest number of properties in the $0–300K$ and $500K–750K$ price ranges. As the closing price increases, the number of transactions generally decreases, with relatively few properties sold above $3M$.")

    price_counts = (
        map_df["PriceBand"]
        .value_counts()
        .sort_index()
    )

    st.bar_chart(price_counts)

    # Geographic analysis
    st.subheader("Geographic Distribution of Closing Prices")
    st.write("Property transactions are distributed across California, with particularly dense concentrations in major metropolitan and coastal areas. Different price ranges also show noticeable geographic variation, suggesting that location is an important factor affecting housing prices.")


    # Map
    fig = px.scatter_map(
        map_df,
        lat="Latitude",
        lon="Longitude",
        color="PriceBand",
        category_orders={
            "PriceBand": labels
        },
        zoom=5,
        height=700,
        hover_data={
            "ClosePrice": ":$,.0f",
            "PriceBand": True,
            "Latitude": False,
            "Longitude": False
        }
    )

    # Smaller points + higher transparency
    fig.update_traces(
        marker={
            "size": 3,
            "opacity": 0.35
        }
    )

    fig.update_layout(
        #title="Geographic Distribution of Closing Prices",
        map_style="open-street-map"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Living area

    st.subheader("Living Area Distribution")
    st.write("Most properties have a living area between $1,000$ and $2,500$ square feet. The $1,000$–$1,500$ sq ft range contains the largest number of properties, followed by the $1,500$–$2,000$ sq ft range. The number of properties gradually decreases as living area increases, with relatively few properties larger than $4,000$ sq ft.")

    area_bins = [
        0,
        500,
        1000,
        1500,
        2000,
        2500,
        3000,
        4000,
        5000,
        float("inf")
    ]

    area_labels = [
        "0–500",
        "500–1,000",
        "1,000–1,500",
        "1,500–2,000",
        "2,000–2,500",
        "2,500–3,000",
        "3,000–4,000",
        "4,000–5,000",
        "5,000+"
    ]

    df["LivingAreaBand"] = pd.cut(
        df["LivingArea"],
        bins=area_bins,
        labels=area_labels,
        include_lowest=True
    )

    area_counts = (
        df["LivingAreaBand"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    area_counts.columns = [
        "Living Area (sq ft)",
        "Number of Properties"
    ]

    fig_area = px.bar(
        area_counts,
        x="Living Area (sq ft)",
        y="Number of Properties",
        text="Number of Properties"
    )

    fig_area.update_layout(
        xaxis_title="Living Area (sq ft)",
        yaxis_title="Number of Properties"
    )

    st.plotly_chart(
        fig_area,
        use_container_width=True
    )

    col1, col2 = st.columns(2)
    st.write("Most properties have between 2 and 5 bedrooms, with 3 bedrooms being the most common configuration. Similarly, most properties have between 1 and 4 bathrooms, with 2 bathrooms occurring most frequently."
             "Both distributions are right-skewed, with a small number of properties having unusually large numbers of bedrooms or bathrooms. These observations likely represent larger or specialized properties and account for only a small proportion of the dataset.")

    with col1:
        st.subheader("Bedrooms Distribution")

        bedroom_counts = (
            df["BedroomsTotal"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        bedroom_counts.columns = ["Bedrooms", "Count"]

        fig_bed = px.bar(
            bedroom_counts,
            x="Bedrooms",
            y="Count"
        )

        st.plotly_chart(fig_bed, use_container_width=True)

    with col2:
        st.subheader("Bathrooms Distribution")

        bathroom_counts = (
            df["BathroomsTotalInteger"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        bathroom_counts.columns = ["Bathrooms", "Count"]

        fig_bath = px.bar(
            bathroom_counts,
            x="Bathrooms",
            y="Count"
        )

        st.plotly_chart(fig_bath, use_container_width=True)

    st.subheader("Feature Correlation")
    st.write("Living area, bedrooms, and bathrooms are strongly correlated with each other. In particular, living area has a correlation of 0.76 with the number of bathrooms and 0.66 with the number of bedrooms. However, the linear correlations between closing price and these individual features are relatively weak, suggesting that housing prices are influenced by more complex and potentially nonlinear relationships among multiple features.")
    corr_features = [
            "ClosePrice",
            "LivingArea",
            "BedroomsTotal",
            "BathroomsTotalInteger",
            "LotSizeSquareFeet",
            "YearBuilt"
        ]

    corr = df[corr_features].corr()

    fig_corr = px.imshow(
            corr,
            text_auto=".2f",
            #aspect="auto",
            #title="Correlation Matrix"
    )

    st.plotly_chart(fig_corr, use_container_width=True)






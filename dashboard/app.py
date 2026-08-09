
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Banking Intelligence Platform", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/master_customer_table.csv")

df = load_data()

st.title("Banking Intelligence Platform")
st.caption("Customer analytics: churn risk, segmentation, and cross-sell propensity")

section = st.sidebar.radio(
    "Navigate",
    ["Executive Overview", "Customer Intelligence", "Cross-Sell / Propensity"]
)

# ---------------- EXECUTIVE OVERVIEW ----------------
if section == "Executive Overview":
    col1, col2, col3, col4 = st.columns(4)

    total_customers = len(df)
    churn_rate = df["churned"].mean() * 100
    avg_trans_amt = df["Total_Trans_Amt"].mean()
    high_risk_count = (df["churn_probability"] >= 0.7).sum()

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Churn Rate", f"{churn_rate:.1f}%")
    col3.metric("Avg Transaction Amount", f"${avg_trans_amt:,.0f}")
    col4.metric("High Churn Risk (>=70%)", f"{high_risk_count:,}")

    st.subheader("Churn Rate by Cluster")
    cluster_churn = df.groupby("cluster")["churned"].mean().reset_index()
    cluster_churn["churned"] = cluster_churn["churned"] * 100
    fig = px.bar(cluster_churn, x="cluster", y="churned",
                 labels={"churned": "Churn Rate (%)", "cluster": "Cluster"},
                 title="Churn Rate by Customer Cluster")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Churn Risk Distribution")
    fig2 = px.histogram(df, x="churn_probability", nbins=30,
                         title="Distribution of Predicted Churn Probability")
    st.plotly_chart(fig2, use_container_width=True)

    st.caption(
        "Note: churn probabilities shown here are model outputs on the full customer base, "
        "including customers used in training. Reported model performance metrics "
        "(precision 0.89, recall 0.91, ROC-AUC 0.99) are test-set only."
    )

# ---------------- CUSTOMER INTELLIGENCE ----------------
elif section == "Customer Intelligence":
    st.subheader("Segment Explorer")

    cluster_names = {
        0: "Revolvers / Credit-Dependent",
        1: "High-Value Transactors, Under-Penetrated",
        2: "At-Risk / Disengaged",
        3: "Stable Loyalists"
    }
    df["cluster_name"] = df["cluster"].map(cluster_names)

    selected_cluster = st.multiselect(
        "Filter by segment", options=df["cluster_name"].unique(),
        default=df["cluster_name"].unique()
    )
    filtered = df[df["cluster_name"].isin(selected_cluster)]

    col1, col2 = st.columns(2)
    with col1:
        fig3 = px.box(filtered, x="cluster_name", y="Total_Trans_Ct",
                       title="Transaction Count by Segment")
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        fig4 = px.box(filtered, x="cluster_name", y="churn_probability",
                       title="Churn Risk by Segment")
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("High-Risk Customer Table")
    risk_table = filtered[filtered["churn_probability"] >= 0.5][
        ["customer_id", "cluster_name", "Total_Trans_Amt", "Total_Trans_Ct",
         "Months_Inactive_12_mon", "churn_probability"]
    ].sort_values("churn_probability", ascending=False)
    st.dataframe(risk_table, use_container_width=True)

# ---------------- CROSS-SELL / PROPENSITY ----------------
elif section == "Cross-Sell / Propensity":
    st.subheader("Cross-Sell Targeting")

    prop_df = df.dropna(subset=["propensity_score"])

    band_counts = prop_df["targeting_band"].value_counts().reset_index()
    band_counts.columns = ["Targeting Band", "Customer Count"]
    fig5 = px.bar(band_counts, x="Targeting Band", y="Customer Count",
                  title="Cross-Sell Targeting Bands (1-2 Product Customers Only)")
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Priority Targeting List")
    priority_list = prop_df[prop_df["targeting_band"] == "Priority"][
        ["customer_id", "Total_Relationship_Count", "Total_Trans_Amt",
         "propensity_score"]
    ].sort_values("propensity_score", ascending=False)
    st.dataframe(priority_list, use_container_width=True)

    st.caption(
        "Propensity model ROC-AUC: 0.69 (moderate). Scores are a behavioral "
        "prioritization signal, not a high-confidence prediction, since this dataset "
        "lacks campaign-response or offer-history data."
    )

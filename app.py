import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
import streamlit.components.v1 as components

st.set_page_config(
    page_title="E-Commerce BI Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = os.path.dirname(__file__)


@st.cache_data
def load_executive_summary():
    df = pd.read_csv(os.path.join(DATA_DIR, "executive_summary.csv"))
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


@st.cache_data
def load_rfm():
    return pd.read_csv(os.path.join(DATA_DIR, "customer_rfm_segments.csv"))


@st.cache_data
def load_cohort():
    return pd.read_csv(os.path.join(DATA_DIR, "cohort_retention_data.csv"))


@st.cache_data
def load_ab1():
    return pd.read_csv(os.path.join(DATA_DIR, "ab_test_h1_reactivation.csv"))


@st.cache_data
def load_ab2():
    return pd.read_csv(os.path.join(DATA_DIR, "ab_test_h2_aov.csv"))


@st.cache_data
def load_orders():
    df = pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"], errors="coerce"
    )
    df["order_estimated_delivery_date"] = pd.to_datetime(
        df["order_estimated_delivery_date"], errors="coerce"
    )
    df["on_time"] = (
        df["order_delivered_customer_date"] <= df["order_estimated_delivery_date"]
    )
    return df


@st.cache_data
def load_reviews():
    return pd.read_csv(
        os.path.join(DATA_DIR, "olist_order_reviews_dataset.csv"),
        usecols=["order_id", "review_score"],
    )


@st.cache_data
def load_payments():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_order_payments_dataset.csv"))


@st.cache_data
def load_order_items():
    return pd.read_csv(
        os.path.join(DATA_DIR, "olist_order_items_dataset.csv"),
        usecols=["order_id", "seller_id", "price", "freight_value"],
    )


@st.cache_data
def load_sellers():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_sellers_dataset.csv"))


# ── Sidebar navigation ────────────────────────────────────────────────────────

PAGES = [
    "Executive Summary",
    "Customer Segmentation (RFM)",
    "Cohort & Retention",
    "Product & Category",
    "A/B Test Results",
    "Delivery & Reviews",
    "Seller Leaderboard",
    "Geographic Deep Dive",
    "Payment Behavior",
    "Tableau Dashboards",
    "Analysis Notebook",
]

with st.sidebar:
    st.title("🛒 E-Commerce BI")
    st.caption("Brazilian E-Commerce · 2016–2018")
    st.divider()
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Executive Summary
# ══════════════════════════════════════════════════════════════════════════════
if page == "Executive Summary":
    st.title("Executive Summary")
    st.caption("High-level KPIs across the full 2016–2018 dataset")

    df = load_executive_summary()

    total_revenue = df["payment_value"].sum()
    total_orders = df["order_id"].nunique()
    unique_customers = df["customer_id"].nunique()
    aov = total_revenue / total_orders

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${total_revenue:,.0f}")
    c2.metric("Total Orders", f"{total_orders:,}")
    c3.metric("Unique Customers", f"{unique_customers:,}")
    c4.metric("Avg Order Value", f"${aov:.2f}")

    st.divider()

    # Monthly revenue & order trend
    monthly = (
        df.groupby("year_month")
        .agg(revenue=("payment_value", "sum"), orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("year_month")
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=monthly["year_month"], y=monthly["revenue"], name="Revenue ($)", marker_color="#4C78A8"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=monthly["year_month"], y=monthly["orders"], name="Orders", mode="lines+markers", line=dict(color="#F58518")),
        secondary_y=True,
    )
    fig.update_layout(title="Monthly Revenue & Order Volume", xaxis_tickangle=-45, height=400, legend=dict(orientation="h"))
    fig.update_yaxes(title_text="Revenue ($)", secondary_y=False)
    fig.update_yaxes(title_text="Orders", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    # Revenue by state
    st.subheader("Revenue by State")
    state_rev = df.groupby("state")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
    fig2 = px.bar(state_rev, x="state", y="payment_value", color="payment_value",
                  color_continuous_scale="Blues", labels={"payment_value": "Revenue ($)", "state": "State"})
    fig2.update_layout(height=380, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Customer Segmentation (RFM)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Customer Segmentation (RFM)":
    st.title("Customer Segmentation — RFM")
    st.caption("96,096 customers scored on Recency, Frequency, and Monetary value")

    rfm = load_rfm()

    seg_colors = {
        "Champions": "#2ecc71",
        "Loyal Customers": "#3498db",
        "Potential Loyalists": "#9b59b6",
        "At Risk": "#e67e22",
        "Hibernating": "#e74c3c",
    }

    seg_counts = rfm["Customer_Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]

    col1, col2 = st.columns([1, 1])

    with col1:
        fig = px.pie(seg_counts, names="Segment", values="Count",
                     color="Segment", color_discrete_map=seg_colors,
                     title="Segment Distribution", hole=0.4)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        seg_metrics = rfm.groupby("Customer_Segment").agg(
            Customers=("Customer_Unique_ID", "count"),
            Avg_Recency=("Recency_Days", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean"),
        ).reset_index().round(1)
        seg_metrics.columns = ["Segment", "Customers", "Avg Recency (days)", "Avg Frequency", "Avg Monetary ($)"]
        st.subheader("Metrics by Segment")
        st.dataframe(seg_metrics.sort_values("Customers", ascending=False), use_container_width=True, hide_index=True)

    st.divider()

    # Scatter: Recency vs Monetary, colored by segment
    st.subheader("Recency vs Monetary Value by Segment")
    selected_segs = st.multiselect(
        "Filter Segments",
        options=rfm["Customer_Segment"].unique().tolist(),
        default=rfm["Customer_Segment"].unique().tolist(),
    )
    rfm_filtered = rfm[rfm["Customer_Segment"].isin(selected_segs)]
    sample = rfm_filtered.sample(min(5000, len(rfm_filtered)), random_state=42)

    fig3 = px.scatter(
        sample, x="Recency_Days", y="Monetary",
        color="Customer_Segment", color_discrete_map=seg_colors,
        opacity=0.5, labels={"Recency_Days": "Recency (days)", "Monetary": "Monetary Value ($)"},
        height=420,
    )
    fig3.update_layout(legend_title="Segment")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("R Score vs F Score Heatmap")
    rfm_heatmap = rfm.groupby(["R_Score", "F_Score"]).size().reset_index(name="Count")
    pivot = rfm_heatmap.pivot(index="R_Score", columns="F_Score", values="Count").fillna(0)
    fig4 = px.imshow(pivot, color_continuous_scale="Blues", text_auto=True,
                     labels={"x": "F Score", "y": "R Score", "color": "Customers"},
                     title="Customer Count by R and F Score")
    fig4.update_layout(height=360)
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Cohort & Retention
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Cohort & Retention":
    st.title("Cohort & Retention Analysis")
    st.caption("Monthly cohorts tracking repeat purchase behavior")

    cohort = load_cohort()
    cohort.columns = ["cohort_month", "month_index", "total_users"]
    cohort = cohort.sort_values(["cohort_month", "month_index"])

    # Cohort sizes (month_index == 0)
    cohort_sizes = cohort[cohort["month_index"] == 0].set_index("cohort_month")["total_users"]
    cohort["cohort_size"] = cohort["cohort_month"].map(cohort_sizes)
    cohort["retention_rate"] = (cohort["total_users"] / cohort["cohort_size"] * 100).round(2)

    pivot = cohort.pivot(index="cohort_month", columns="month_index", values="retention_rate")
    pivot = pivot.sort_index()

    st.subheader("Retention Heatmap (% of Cohort Returning)")
    fig = px.imshow(
        pivot,
        color_continuous_scale="Blues",
        text_auto=".1f",
        labels={"x": "Months Since First Purchase", "y": "Cohort Month", "color": "Retention %"},
        aspect="auto",
        height=500,
    )
    fig.update_layout(xaxis_title="Months Since First Purchase", yaxis_title="Cohort Month")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Retention curves for selected cohorts
    st.subheader("Retention Curves by Cohort")
    available_cohorts = sorted(cohort["cohort_month"].unique().tolist())
    selected_cohorts = st.multiselect(
        "Select Cohorts",
        options=available_cohorts,
        default=available_cohorts[:6],
    )

    cohort_filtered = cohort[cohort["cohort_month"].isin(selected_cohorts)]
    fig2 = px.line(
        cohort_filtered, x="month_index", y="retention_rate",
        color="cohort_month", markers=True,
        labels={"month_index": "Months Since First Purchase", "retention_rate": "Retention Rate (%)", "cohort_month": "Cohort"},
        height=420,
    )
    fig2.update_layout(yaxis_ticksuffix="%")
    st.plotly_chart(fig2, use_container_width=True)

    st.info("💡 Only **3.12%** of customers make a repeat purchase — retention is the biggest growth lever.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — Product & Category
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Product & Category":
    st.title("Product & Category Performance")

    df = load_executive_summary()
    reviews = load_reviews()
    orders_raw = load_orders()

    # Merge reviews onto executive_summary via order_id
    df_rev = df.merge(reviews, on="order_id", how="left")

    cat_stats = (
        df_rev.groupby("category")
        .agg(
            Revenue=("payment_value", "sum"),
            Orders=("order_id", "nunique"),
            Avg_Review=("review_score", "mean"),
        )
        .reset_index()
        .round(2)
    )
    cat_stats.columns = ["Category", "Revenue ($)", "Orders", "Avg Review Score"]

    top_n = st.slider("Show top N categories", 5, 30, 10)
    top_cats = cat_stats.nlargest(top_n, "Revenue ($)")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(top_cats.sort_values("Revenue ($)"), x="Revenue ($)", y="Category",
                     orientation="h", color="Revenue ($)", color_continuous_scale="Blues",
                     title=f"Top {top_n} Categories by Revenue", height=420)
        fig.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(top_cats.sort_values("Avg Review Score"), x="Avg Review Score", y="Category",
                      orientation="h", color="Avg Review Score", color_continuous_scale="RdYlGn",
                      range_color=[3, 5], title=f"Avg Review Score — Top {top_n} Categories", height=420)
        fig2.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Category Deep Dive")
    selected_cat = st.selectbox("Select a category", sorted(cat_stats["Category"].dropna().unique()))
    cat_row = cat_stats[cat_stats["Category"] == selected_cat].iloc[0]
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Revenue", f"${cat_row['Revenue ($)']:,.2f}")
    cc2.metric("Orders", f"{int(cat_row['Orders']):,}")
    cc3.metric("Avg Review Score", f"{cat_row['Avg Review Score']:.2f} / 5")

    # Revenue trend for selected category
    cat_trend = df[df["category"] == selected_cat].groupby("year_month")["payment_value"].sum().reset_index()
    cat_trend.columns = ["Month", "Revenue ($)"]
    fig3 = px.line(cat_trend, x="Month", y="Revenue ($)", markers=True,
                   title=f"Monthly Revenue — {selected_cat}")
    fig3.update_layout(xaxis_tickangle=-45, height=320)
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — A/B Test Results
# ══════════════════════════════════════════════════════════════════════════════
elif page == "A/B Test Results":
    st.title("A/B Test Results")

    ab1 = load_ab1()
    ab2 = load_ab2()

    # ── Hypothesis 1 ──────────────────────────────────────────────────────────
    st.subheader("Hypothesis 1 — Win-Back Discount (20% off for At-Risk customers)")

    h1_reactivated = ab1[ab1["Outcome"] == "Reactivated"].set_index("Group")["Count"]
    h1_total = ab1.groupby("Group")["Count"].sum()
    h1_rate = (h1_reactivated / h1_total * 100).reset_index()
    h1_rate.columns = ["Group", "Reactivation Rate (%)"]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Control Reactivation Rate", f"{h1_rate.loc[h1_rate['Group']=='Control', 'Reactivation Rate (%)'].values[0]:.2f}%")
        st.metric("Treatment Reactivation Rate", f"{h1_rate.loc[h1_rate['Group']=='Treatment', 'Reactivation Rate (%)'].values[0]:.2f}%")
        st.success("✅ Statistically Significant — p = 0.0003")
        st.caption("The 20% win-back discount significantly improves reactivation of At-Risk customers.")

    with col2:
        fig = px.bar(h1_rate, x="Group", y="Reactivation Rate (%)",
                     color="Group", color_discrete_map={"Control": "#95a5a6", "Treatment": "#2ecc71"},
                     text="Reactivation Rate (%)", title="Reactivation Rate by Group", height=350)
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig.update_layout(showlegend=False, yaxis_range=[0, 12])
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Hypothesis 2 ──────────────────────────────────────────────────────────
    st.subheader("Hypothesis 2 — Free Shipping Threshold ($150+) Impact on 2nd-Order AOV")

    h2_aov = ab2.groupby("Group")["Order_Value"].mean().reset_index()
    h2_aov.columns = ["Group", "Avg Order Value ($)"]

    col3, col4 = st.columns([1, 2])
    with col3:
        ctrl_aov = h2_aov.loc[h2_aov["Group"] == "Control", "Avg Order Value ($)"].values[0]
        trt_aov = h2_aov.loc[h2_aov["Group"] == "Treatment", "Avg Order Value ($)"].values[0]
        uplift = (trt_aov - ctrl_aov) / ctrl_aov * 100
        st.metric("Control AOV", f"${ctrl_aov:.2f}")
        st.metric("Treatment AOV", f"${trt_aov:.2f}", delta=f"+{uplift:.1f}% uplift")
        st.success("✅ Highly Significant — p < 0.00001")
        st.caption("Free shipping for orders >$150 drives a ~10% lift in second-order AOV.")

    with col4:
        fig2 = px.box(ab2, x="Group", y="Order_Value", color="Group",
                      color_discrete_map={"Control": "#95a5a6", "Treatment": "#3498db"},
                      title="Order Value Distribution by Group", height=380,
                      labels={"Order_Value": "Order Value ($)"})
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Histogram overlay
    st.subheader("Order Value Distribution Overlay")
    fig3 = px.histogram(ab2, x="Order_Value", color="Group", barmode="overlay",
                        color_discrete_map={"Control": "#95a5a6", "Treatment": "#3498db"},
                        opacity=0.7, nbins=60,
                        labels={"Order_Value": "Order Value ($)", "count": "Frequency"},
                        height=360)
    fig3.update_layout(bargap=0.05)
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — Delivery & Reviews
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Delivery & Reviews":
    st.title("Delivery Performance & Review Quality")

    orders = load_orders()
    reviews = load_reviews()

    # On-time delivery
    delivered = orders[orders["order_status"] == "delivered"].dropna(
        subset=["order_delivered_customer_date", "order_estimated_delivery_date"]
    )
    on_time_pct = delivered["on_time"].mean() * 100
    late_pct = 100 - on_time_pct

    col1, col2, col3 = st.columns(3)
    col1.metric("On-Time Delivery Rate", f"{on_time_pct:.2f}%")
    col2.metric("Late Delivery Rate", f"{late_pct:.2f}%")
    col3.metric("Total Delivered Orders", f"{len(delivered):,}")

    col_a, col_b = st.columns(2)

    with col_a:
        delivery_data = pd.DataFrame({
            "Status": ["On Time", "Late"],
            "Count": [delivered["on_time"].sum(), (~delivered["on_time"]).sum()],
        })
        fig = px.pie(delivery_data, names="Status", values="Count", hole=0.5,
                     color="Status", color_discrete_map={"On Time": "#2ecc71", "Late": "#e74c3c"},
                     title="On-Time vs Late Deliveries")
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=False, height=360)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        review_dist = reviews["review_score"].value_counts().sort_index().reset_index()
        review_dist.columns = ["Score", "Count"]
        review_dist["Pct"] = (review_dist["Count"] / review_dist["Count"].sum() * 100).round(2)
        score_colors = {1: "#e74c3c", 2: "#e67e22", 3: "#f1c40f", 4: "#3498db", 5: "#2ecc71"}
        fig2 = px.bar(review_dist, x="Score", y="Count",
                      color="Score", color_discrete_map=score_colors,
                      text="Pct", title="Review Score Distribution",
                      labels={"Score": "Review Score (1–5)", "Count": "Number of Reviews"}, height=360)
        fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig2.update_layout(showlegend=False, xaxis=dict(tickmode="linear"))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Days Late Distribution (for Late Orders)")
    delivered["days_late"] = (
        delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]
    ).dt.days
    late_orders = delivered[delivered["days_late"] > 0]
    fig3 = px.histogram(late_orders, x="days_late", nbins=40,
                        labels={"days_late": "Days Late", "count": "Orders"},
                        color_discrete_sequence=["#e74c3c"],
                        title=f"Late Orders — Days Overdue ({len(late_orders):,} orders)", height=320)
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — Seller Leaderboard
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Seller Leaderboard":
    st.title("Seller Performance Leaderboard")

    items = load_order_items()
    reviews = load_reviews()
    sellers = load_sellers()
    orders_df = load_orders()[["order_id", "customer_id", "order_status"]]

    # Join items → orders → reviews
    merged = items.merge(orders_df, on="order_id", how="left")
    merged = merged.merge(reviews, on="order_id", how="left")

    seller_stats = (
        merged.groupby("seller_id")
        .agg(
            Items_Sold=("order_id", "count"),
            Revenue=("price", "sum"),
            Unique_Customers=("customer_id", "nunique"),
            Avg_Review=("review_score", "mean"),
            Five_Star_Reviews=(
                "review_score",
                lambda x: (x == 5).sum(),
            ),
        )
        .reset_index()
        .round(2)
    )
    seller_stats = seller_stats.merge(
        sellers[["seller_id", "seller_city", "seller_state"]], on="seller_id", how="left"
    )
    seller_stats.columns = [
        "Seller ID", "Items Sold", "Revenue ($)", "Unique Customers",
        "Avg Review", "5-Star Reviews", "City", "State",
    ]
    seller_stats["Seller ID"] = seller_stats["Seller ID"].str[:8] + "..."

    sort_col = st.selectbox("Sort by", ["Revenue ($)", "Items Sold", "Unique Customers", "5-Star Reviews", "Avg Review"])
    top_n = st.slider("Show top N sellers", 10, 50, 20)

    top_sellers = seller_stats.nlargest(top_n, sort_col)

    fig = px.bar(
        top_sellers.sort_values(sort_col),
        x=sort_col, y="Seller ID", orientation="h",
        color=sort_col, color_continuous_scale="Blues",
        title=f"Top {top_n} Sellers by {sort_col}", height=max(400, top_n * 22),
    )
    fig.update_layout(coloraxis_showscale=False, yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Full Leaderboard Table")
    st.dataframe(
        top_sellers.sort_values(sort_col, ascending=False).reset_index(drop=True),
        use_container_width=True, hide_index=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — Geographic Deep Dive
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Geographic Deep Dive":
    st.title("Geographic Revenue Deep Dive")

    df = load_executive_summary()

    state_rev = df.groupby("state")["payment_value"].sum().reset_index()
    state_rev.columns = ["State", "Revenue ($)"]

    city_rev = (
        df.groupby(["city", "state"])["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
    )
    city_rev.columns = ["City", "State", "Revenue ($)"]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            state_rev.sort_values("Revenue ($)", ascending=False).head(15),
            x="State", y="Revenue ($)", color="Revenue ($)",
            color_continuous_scale="Blues",
            title="Top 15 States by Revenue", height=380,
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            city_rev.head(15).sort_values("Revenue ($)"),
            x="Revenue ($)", y="City", orientation="h",
            color="Revenue ($)", color_continuous_scale="Blues",
            title="Top 15 Cities by Revenue", height=380,
        )
        fig2.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("Revenue Share — State Treemap")
    fig3 = px.treemap(
        state_rev, path=["State"], values="Revenue ($)",
        color="Revenue ($)", color_continuous_scale="Blues",
        title="Revenue Share by State", height=420,
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    st.subheader("State Deep Dive")
    selected_state = st.selectbox("Select a state", sorted(df["state"].unique()))
    state_cities = (
        df[df["state"] == selected_state]
        .groupby("city")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
        .head(20)
    )
    state_cities.columns = ["City", "Revenue ($)"]
    fig4 = px.bar(
        state_cities, x="City", y="Revenue ($)",
        color="Revenue ($)", color_continuous_scale="Blues",
        title=f"Top Cities in {selected_state}", height=360,
    )
    fig4.update_layout(coloraxis_showscale=False, xaxis_tickangle=-35)
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — Payment Behavior
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Payment Behavior":
    st.title("Payment Behavior Analysis")

    payments = load_payments()

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", f"{len(payments):,}")
    col2.metric("Total Payment Value", f"${payments['payment_value'].sum():,.0f}")
    col3.metric("Avg Installments (Credit)", f"{payments[payments['payment_type']=='credit_card']['payment_installments'].mean():.1f}")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        pay_type = payments.groupby("payment_type")["payment_value"].sum().reset_index()
        pay_type.columns = ["Payment Type", "Revenue ($)"]
        pay_type["Payment Type"] = pay_type["Payment Type"].str.replace("_", " ").str.title()
        fig = px.pie(pay_type, names="Payment Type", values="Revenue ($)", hole=0.45,
                     title="Revenue Share by Payment Method", height=360)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        pay_count = payments.groupby("payment_type").size().reset_index(name="Transactions")
        pay_count["Payment Type"] = pay_count["payment_type"].str.replace("_", " ").str.title()
        fig2 = px.bar(pay_count.sort_values("Transactions", ascending=False),
                      x="Payment Type", y="Transactions", color="Transactions",
                      color_continuous_scale="Blues",
                      title="Transaction Count by Payment Method", height=360)
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("Installment Distribution (Credit Card)")
    cc = payments[payments["payment_type"] == "credit_card"]
    installment_dist = cc["payment_installments"].value_counts().sort_index().reset_index()
    installment_dist.columns = ["Installments", "Count"]
    fig3 = px.bar(installment_dist, x="Installments", y="Count",
                  color="Count", color_continuous_scale="Blues",
                  title="Credit Card Installment Choices", height=360,
                  labels={"Installments": "Number of Installments", "Count": "Orders"})
    fig3.update_layout(coloraxis_showscale=False, xaxis=dict(tickmode="linear"))
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Avg Order Value by Payment Method")
    aov_by_type = payments.groupby("payment_type")["payment_value"].mean().reset_index()
    aov_by_type.columns = ["Payment Type", "Avg Order Value ($)"]
    aov_by_type["Payment Type"] = aov_by_type["Payment Type"].str.replace("_", " ").str.title()
    fig4 = px.bar(aov_by_type.sort_values("Avg Order Value ($)", ascending=False),
                  x="Payment Type", y="Avg Order Value ($)",
                  color="Avg Order Value ($)", color_continuous_scale="Blues",
                  title="Avg Order Value by Payment Method", height=340)
    fig4.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 10 — Tableau Dashboards
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Tableau Dashboards":
    st.title("Tableau Dashboards")
    st.caption("Interactive dashboards published on Tableau Public")

    TABLEAU_EMBED_1 = (
        "https://public.tableau.com/views/E-commerceRevenueDynamicGeographicDistribution/Dashboard1"
        "?:embed=yes&:showVizHome=no&:toolbar=yes&:animate_transition=yes"
    )
    TABLEAU_EMBED_2 = (
        "https://public.tableau.com/views/CustomerLifecycleRevenueOptimization/Dashboard1"
        "?:embed=yes&:showVizHome=no&:toolbar=yes&:animate_transition=yes"
    )

    def tableau_js_embed(workbook_name, view_name, height=900):
        html = f"""
        <div class="tableauPlaceholder" style="position:relative; width:100%;">
          <object class="tableauViz" style="display:none;">
            <param name="host_url"           value="https%3A%2F%2Fpublic.tableau.com%2F" />
            <param name="embed_code_version" value="3" />
            <param name="site_root"          value="" />
            <param name="name"               value="{workbook_name}/{view_name}" />
            <param name="tabs"               value="no" />
            <param name="toolbar"            value="yes" />
            <param name="animate_transition" value="yes" />
            <param name="display_static_image" value="yes" />
            <param name="display_spinner"    value="yes" />
            <param name="display_overlay"    value="yes" />
            <param name="display_count"      value="yes" />
            <param name="language"           value="en-US" />
          </object>
        </div>
        <script type="text/javascript">
          var divEl  = document.querySelector(".tableauPlaceholder");
          var vizEl  = divEl.getElementsByTagName("object")[0];
          vizEl.style.width  = "100%";
          vizEl.style.height = "{height}px";
          var s = document.createElement("script");
          s.src = "https://public.tableau.com/javascripts/api/viz_v1.js";
          divEl.parentNode.insertBefore(s, divEl);
        </script>
        """
        components.html(html, height=height + 20, scrolling=True)

    tab1, tab2 = st.tabs([
        "E-Commerce Revenue & Geographic Distribution",
        "Customer Lifecycle & Revenue Optimization",
    ])

    with tab1:
        st.markdown(
            "Explores **revenue dynamics across Brazilian states and cities** — "
            "geographic heatmaps, top-performing regions, and revenue trends over time."
        )
        tableau_js_embed("E-commerceRevenueDynamicGeographicDistribution", "Dashboard1", height=900)

    with tab2:
        st.markdown(
            "Covers the **customer lifecycle** — RFM segmentation, cohort retention curves, "
            "and revenue optimization opportunities."
        )
        components.html("""
        <div class='tableauPlaceholder' id='viz1777522052277' style='position: relative'>
          <noscript>
            <a href='#'>
              <img alt='Dashboard 1'
                src='https://public.tableau.com/static/images/Cu/CustomerLifecycleRevenueOptimization/Dashboard1/1_rss.png'
                style='border: none' />
            </a>
          </noscript>
          <object class='tableauViz' style='display:none;'>
            <param name='host_url'           value='https%3A%2F%2Fpublic.tableau.com%2F' />
            <param name='embed_code_version' value='3' />
            <param name='site_root'          value='' />
            <param name='name'               value='CustomerLifecycleRevenueOptimization/Dashboard1' />
            <param name='tabs'               value='no' />
            <param name='toolbar'            value='yes' />
            <param name='static_image'
              value='https://public.tableau.com/static/images/Cu/CustomerLifecycleRevenueOptimization/Dashboard1/1.png' />
            <param name='animate_transition'   value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner'      value='yes' />
            <param name='display_overlay'      value='yes' />
            <param name='display_count'        value='yes' />
            <param name='language'             value='en-US' />
            <param name='filter'               value='publish=yes' />
          </object>
        </div>
        <script type='text/javascript'>
          var divElement = document.getElementById('viz1777522052277');
          var vizElement = divElement.getElementsByTagName('object')[0];
          if (divElement.offsetWidth > 800) {
            vizElement.style.width  = '1200px';
            vizElement.style.height = '827px';
          } else if (divElement.offsetWidth > 500) {
            vizElement.style.width  = '1200px';
            vizElement.style.height = '827px';
          } else {
            vizElement.style.width  = '100%';
            vizElement.style.height = '1777px';
          }
          var scriptElement = document.createElement('script');
          scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
          vizElement.parentNode.insertBefore(scriptElement, vizElement);
        </script>
        """, height=870, scrolling=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 11 — Analysis Notebook
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Analysis Notebook":
    st.title("Analysis Notebook")
    st.caption("Full SQL & Python pipeline — 89 cells covering data ingestion, 12 SQL queries, customer lifecycle analysis, RFM segmentation, cohort retention, and A/B testing.")

    notebook_html_path = os.path.join(DATA_DIR, "notebook_rendered.html")
    if os.path.exists(notebook_html_path):
        with open(notebook_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=900, scrolling=True)
    else:
        st.error("Rendered notebook not found. Please run the pre-render script first.")
        st.code("JUPYTER_DATA_DIR=/opt/homebrew/share/jupyter python3.11 -c \"\nimport nbformat\nfrom nbconvert import HTMLExporter\nnb = nbformat.read('Scalable_BI_Pipeline_SQL_&_Tableau_Executive_Intelligence_System.ipynb', as_version=4)\nexporter = HTMLExporter(template_name='classic')\nhtml_body, _ = exporter.from_notebook_node(nb)\nopen('notebook_rendered.html', 'w').write(html_body)\n\"")

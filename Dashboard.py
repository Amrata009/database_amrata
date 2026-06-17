import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PAGE CONFIG & THEME
# =========================
st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced responsive Glassmorphism Theme (Completely Cleaned Layout)
st.markdown("""
    <style>
    /* Main container background setup */
    .main {
        background: linear-gradient(135deg, #0b1120 0%, #020617 100%);
        color: #f8fafc;
    }
    
    /* Executive Metric Display Custom Styling */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 22px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        transition: all 0.25s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 255, 204, 0.4);
        box-shadow: 0 15px 30px -5px rgba(0, 255, 204, 0.1);
    }
    
    /* Text layout overrides for responsive sizing */
    [data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, #00FFCC, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    [data-testid="stMetricLabel"] {
        font-size: 11px !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    
    /* Clean Glass Cards for Insights */
    .executive-card {
        padding: 22px;
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.35);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    /* Action Items Cards inside Scroll Area */
    .action-card {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .status-weak { border-left: 4px solid #ef4444; }
    .status-avg { border-left: 4px solid #f59e0b; }
    .status-good { border-left: 4px solid #10b981; }
    </style>
""", unsafe_allow_html=True)

# Main Title Section
st.markdown("""
    <div style='text-align: center; padding: 15px 0 35px 0;'>
        <p style='color: #00FFCC; font-weight: 700; letter-spacing: 2px; margin: 0; text-transform: uppercase; font-size: 12px;'>Data Stream Monitor</p>
        <h1 style='color: #ffffff; font-size: 38px; font-weight: 800; margin: 5px 0 0 0; letter-spacing: -1px;'>Social Media Analytics</h1>
    </div>
""", unsafe_allow_html=True)

# =========================
# MONGODB CONNECTION
# =========================
MONGO_URI = "mongodb+srv://amrataailani1_db_student:Amrata_Ailani09@clusterincubien.016ut4y.mongodb.net/?appName=Clusterincubien"

@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)

client = init_connection()
db = client["Incubien_Foundaion"]
collection = db["social_media_analytics"]

# =========================
# FETCH & CLEAN DATA
# =========================
@st.cache_data(ttl=60)
def load_data():
    data = list(collection.find())
    if len(data) == 0:
        return None
    
    df = pd.DataFrame(data)
    
    required_columns = [
        "content_id", "platform", "likes", "comments", "shares", 
        "saves", "views", "followers", "growth_rate", "ctr", "consistency_score"
    ]
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0
            
    df["likes"] = df["likes"].fillna(0).astype(int)
    df["comments"] = df["comments"].fillna(0).astype(int)
    df["shares"] = df["shares"].fillna(0).astype(int)
    df["saves"] = df["saves"].fillna(0).astype(int)
    df["views"] = df["views"].fillna(1).astype(int)
    df["followers"] = df["followers"].fillna(0).astype(int)
    df["growth_rate"] = df["growth_rate"].fillna(0).astype(float)
    df["ctr"] = df["ctr"].fillna(0).astype(float)
    df["consistency_score"] = df["consistency_score"].fillna(0).astype(float)
    
    # Core mathematical modeling formulas
    df["engagement_rate"] = ((df["likes"] + df["comments"] + df["shares"] + df["saves"]) / df["views"]) * 100
    df["viral_score"] = (df["likes"] * 0.4) + (df["comments"] * 0.2) + (df["shares"] * 0.3) + (df["saves"] * 0.1)
    df["performance_score"] = (df["engagement_rate"] * 0.4) + (df["growth_rate"] * 0.3) + (df["ctr"] * 0.2) + (df["consistency_score"] * 0.1)
    
    return df

df = load_data()

if df is None:
    st.error("❌ System Error: Real-time data sync failed from MongoDB Atlas Cluster.")
    st.stop()

# =========================
# SIDEBAR RECONFIGURED
# =========================
st.sidebar.markdown("<p style='color: #94a3b8; font-weight:700; font-size:12px; uppercase; letter-spacing:1px;'>WORKSPACE FILTERS</p>", unsafe_allow_html=True)
platform_options = ["All Platforms"] + sorted(df["platform"].dropna().unique().tolist())

selected_platform = st.sidebar.selectbox(
    "Data Scope Target",
    platform_options
)

if selected_platform != "All Platforms":
    filtered_df = df[df["platform"] == selected_platform]
else:
    filtered_df = df.copy()

# =========================
# HIGH RESPONSIVE KPI ROW
# =========================
st.markdown("<p style='font-weight:700; color:#cbd5e1; font-size:15px; margin-bottom:12px;'>📈 High-Level Metrics Overview</p>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric("Total Publications", f"{len(filtered_df):,}")
with kpi2:
    st.metric("Gross Views", f"{filtered_df['views'].sum():,}")
with kpi3:
    st.metric("Total Appreciations", f"{filtered_df['likes'].sum():,}")
with kpi4:
    st.metric("Avg Engagement", f"{filtered_df['engagement_rate'].mean():.2f}%")
with kpi5:
    st.metric("Avg Conversion (CTR)", f"{filtered_df['ctr'].mean():.2f}%")

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# INSIGHT HIGHLIGHT CARDS
# =========================
best_content = filtered_df.loc[filtered_df["performance_score"].idxmax()]
worst_content = filtered_df.loc[filtered_df["performance_score"].idxmin()]

c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
    <div class="executive-card" style="border-top: 4px solid #10b981;">
        <span style="color:#10b981; font-weight:700; font-size:10px; text-transform:uppercase; letter-spacing:1px;">Top Performer</span>
        <h3 style="margin: 4px 0 8px 0; font-size: 20px; font-weight:800; color: white;">🏆 Highest Efficiency Asset</h3>
        <p style="font-size:14px; margin:0; color:#cbd5e1;">Content ID: <span style="color:#00FFCC; font-weight:600;">{best_content['content_id']}</span> | Platform: <b>{best_content['platform'].upper()}</b></p>
        <p style="margin: 6px 0 0 0; font-size:13px; color:#94a3b8;">Index Vector Score: <b style="color:#10b981;">{best_content['performance_score']:.2f}</b></p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="executive-card" style="border-top: 4px solid #ef4444;">
        <span style="color:#ef4444; font-weight:700; font-size:10px; text-transform:uppercase; letter-spacing:1px;">Action Needed</span>
        <h3 style="margin: 4px 0 8px 0; font-size: 20px; font-weight:800; color: white;">⚠️ Lowest Efficiency Asset</h3>
        <p style="font-size:14px; margin:0; color:#cbd5e1;">Content ID: <span style="color:#ff6b6b; font-weight:600;">{worst_content['content_id']}</span> | Platform: <b>{worst_content['platform'].upper()}</b></p>
        <p style="margin: 6px 0 0 0; font-size:13px; color:#94a3b8;">Index Vector Score: <b style="color:#ef4444;">{worst_content['performance_score']:.2f}</b></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'><br>", unsafe_allow_html=True)

# Helper for layout injection to matching theme
def clean_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor='rgba(15, 23, 42, 0.25)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="sans-serif",
        font_color="#94a3b8",
        margin=dict(l=15, r=15, t=35, b=15),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor='rgba(255,255,255,0.03)', tickfont=dict(size=11)),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=11))
    )
    return fig

# =========================
# INTERACTIVE VISUAL GRID
# =========================
st.markdown("<p style='font-weight:700; color:#cbd5e1; font-size:16px; margin-bottom:15px;'>📊 Real-time Visual Analytics Trends</p>", unsafe_allow_html=True)

grid_col1, grid_col2 = st.columns(2)
with grid_col1:
    st.markdown("<p style='font-weight:600; color:#94a3b8; font-size:14px; margin-bottom:5px;'>Engagement Distribution Matrix</p>", unsafe_allow_html=True)
    f1 = px.bar(filtered_df, x="content_id", y="engagement_rate", color="platform", text_auto='.1f', template="plotly_dark", color_discrete_sequence=['#00FFCC', '#38BDF8', '#818CF8'])
    st.plotly_chart(clean_chart_theme(f1), use_container_width=True)

with grid_col2:
    st.markdown("<p style='font-weight:600; color:#94a3b8; font-size:14px; margin-bottom:5px;'>Performance Weights Index</p>", unsafe_allow_html=True)
    f2 = px.bar(filtered_df, x="content_id", y="performance_score", color="platform", template="plotly_dark", color_discrete_sequence=['#A78BFA', '#F472B6', '#FB923C'])
    st.plotly_chart(clean_chart_theme(f2), use_container_width=True)

grid_col3, grid_col4 = st.columns(2)
with grid_col3:
    st.markdown("<p style='font-weight:600; color:#94a3b8; font-size:14px; margin-bottom:5px;'>Virality Speed Benchmark</p>", unsafe_allow_html=True)
    f3 = px.bar(filtered_df, x="content_id", y="viral_score", color="platform", template="plotly_dark", color_discrete_sequence=['#34D399', '#6EE7B7', '#A7F3D0'])
    st.plotly_chart(clean_chart_theme(f3), use_container_width=True)

with grid_col4:
    st.markdown("<p style='font-weight:600; color:#94a3b8; font-size:14px; margin-bottom:5px;'>View Volume Market Share</p>", unsafe_allow_html=True)
    p_views = filtered_df.groupby("platform")["views"].sum().reset_index()
    f4 = px.pie(p_views, names="platform", values="views", template="plotly_dark", hole=0.55, color_discrete_sequence=['#00FFCC', '#818CF8', '#F472B6'])
    f4.update_layout(paper_bgcolor='rgba(15, 23, 42, 0.25)', plot_bgcolor='rgba(0,0,0,0)', font_color="#94a3b8", margin=dict(l=15, r=15, t=35, b=15))
    st.plotly_chart(f4, use_container_width=True)

grid_col5, grid_col6 = st.columns(2)
with grid_col5:
    st.markdown("<p style='font-weight:600; color:#94a3b8; font-size:14px; margin-bottom:5px;'>Growth Trajectory Line Matrix</p>", unsafe_allow_html=True)
    f5 = px.line(filtered_df, x="content_id", y="growth_rate", markers=True, color="platform", template="plotly_dark", color_discrete_sequence=['#F59E0B', '#10B981'])
    st.plotly_chart(clean_chart_theme(f5), use_container_width=True)

with grid_col6:
    st.markdown("<p style='font-weight:600; color:#94a3b8; font-size:14px; margin-bottom:5px;'>Click-Through Verification (CTR)</p>", unsafe_allow_html=True)
    f6 = px.bar(filtered_df, x="content_id", y="ctr", color="platform", template="plotly_dark", color_discrete_sequence=['#EC4899', '#8B5CF6'])
    st.plotly_chart(clean_chart_theme(f6), use_container_width=True)

st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'><br>", unsafe_allow_html=True)

# =========================
# REGISTRY TABLE & AI PANEL
# =========================
data_split1, data_split2 = st.columns([11, 8])

with data_split1:
    st.markdown("<p style='font-weight:700; color:#ffffff; font-size:16px; margin-bottom:12px;'>📋 Ledger Performance Registry</p>", unsafe_allow_html=True)
    table_df = filtered_df[[
        "content_id", "platform", "engagement_rate", "viral_score", 
        "performance_score", "likes", "comments", "shares", "saves", "views"
    ]]
    st.dataframe(
        table_df.sort_values(by="performance_score", ascending=False),
        use_container_width=True,
        height=450
    )

with data_split2:
    st.markdown("<p style='font-weight:700; color:#ffffff; font-size:16px; margin-bottom:12px;'>🧠 AI Optimization Strategy Engine</p>", unsafe_allow_html=True)
    
    with st.container(height=450):
        for _, row in filtered_df.iterrows():
            score = row["performance_score"]
            
            if score < 10:
                st.markdown(f"""
                <div class="action-card status-weak">
                    <b style="color:#f87171; font-size:13px;">❌ {row['content_id']} [{row['platform'].upper()}] — Critical Check Needed</b><br>
                    <span style="color:#cbd5e1; font-size:12px; line-height:1.5; display:block; margin-top:5px;">
                    • Better hashtags use karo<br>
                    • Strong CTA add karo<br>
                    • Posting frequency increase karo<br>
                    • Audience targeting improve karo
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
            elif score < 12:
                st.markdown(f"""
                <div class="action-card status-avg">
                    <b style="color:#fbbf24; font-size:13px;">⚠️ {row['content_id']} [{row['platform'].upper()}] — Stable Metrics</b><br>
                    <span style="color:#cbd5e1; font-size:12px; line-height:1.5; display:block; margin-top:5px;">
                    • Caption improve karo<br>
                    • Trending hashtags add karo<br>
                    • More shares generate karo
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div class="action-card status-good">
                    <b style="color:#34d399; font-size:13px;">🔥 {row['content_id']} [{row['platform'].upper()}] — High-Yield Strategy</b><br>
                    <span style="color:#cbd5e1; font-size:12px; line-height:1.5; display:block; margin-top:5px;">
                    • Similar content aur banao<br>
                    • Promote this content<br>
                    • Reuse successful strategy
                    </span>
                </div>
                """, unsafe_allow_html=True)
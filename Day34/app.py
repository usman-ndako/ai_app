# ============================================================
# 💼 AI Financial Analyzer — Enterprise SaaS Edition (ENHANCED)
# Sidebar Navigation + KPI Cards + Groq AI + Advanced Analytics
# ============================================================

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
from groq import Groq
from datetime import datetime, timedelta

# === Page Config ============================================
st.set_page_config(
    page_title="Boss | AI Financial Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Enhanced Premium Styling ===============================
st.markdown("""
    <style>
        /* Main Title Styling */
        .title {
            font-size: 38px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.2em;
            letter-spacing: -1px;
        }
        .subtitle {
            text-align: center;
            font-size: 16px;
            color: #888;
            margin-bottom: 1.5em;
            font-weight: 500;
        }
        
        /* Premium KPI Cards */
        .kpi-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 28px 20px;
            text-align: center;
            box-shadow: 0px 8px 24px rgba(102, 126, 234, 0.25);
            margin-bottom: 15px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 12px 32px rgba(102, 126, 234, 0.35);
        }
        .metric-label {
            font-size: 13px;
            color: rgba(255,255,255,0.85);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 32px;
            font-weight: 800;
            color: #ffffff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Sidebar Enhanced Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            border-right: 1px solid #dee2e6;
        }
        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
        }
        
        /* Radio Navigation Buttons */
        div[role="radiogroup"] label {
            background: white;
            padding: 14px 18px;
            border-radius: 10px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        div[role="radiogroup"] label:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: translateX(5px);
            border-color: #667eea;
        }
        div[role="radiogroup"] label[data-checked="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        /* Info Boxes */
        .info-box {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            margin: 15px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Summary Box */
        .summary-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 16px;
            color: white;
            box-shadow: 0px 8px 24px rgba(0,0,0,0.15);
            line-height: 1.8;
            font-size: 15px;
        }
        
        /* Data Tables */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 12px 24px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        
        /* Download Buttons */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 12px 24px;
            width: 100%;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #2c3e50;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💼 AI-Powered Financial Report Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enterprise Analytics • AI Intelligence • Predictive Forecasting</div>', unsafe_allow_html=True)
st.divider()

# === Sidebar Navigation =====================================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_key = st.text_input(
        "🔐 Groq API Key",
        type="password",
        help="Enter your Groq API key from console.groq.com",
        placeholder="gsk_..."
    )
    model_choice = st.selectbox(
        "🧠 AI Model",
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama-3.1-70b-versatile"],
        help="Select the AI model for analysis"
    )
    uploaded_file = st.file_uploader(
        "📂 Upload Financial Data",
        type=["xlsx", "csv"],
        help="Upload your sales/revenue dataset"
    )
    st.markdown("---")
    st.markdown("## 📁 Navigation")
    selected_tab = st.radio(
        "Choose View",
        [
            "🏠 Dashboard Home",
            "📋 Data & KPIs",
            "📊 Visual Analytics",
            "🧠 AI Insights",
            "📈 Forecast & Trends",
            "📤 Export Reports"
        ],
        key="navigation_radio",
        label_visibility="collapsed"
    )
    st.markdown("---")
    if uploaded_file:
        st.success("✅ Data Loaded")
    else:
        st.warning("⏳ Awaiting Data")
    if api_key:
        st.success("✅ API Connected")
    else:
        st.info("🔑 API Key Needed")
    st.markdown("---")
    st.markdown("💡 **[Get Groq API Key](https://console.groq.com)**")
    st.markdown("---")
    st.caption("🚀 Built by Boss | Enterprise Edition v2.0")

# === Initialize Session State ===============================
if 'ai_summary' not in st.session_state:
    st.session_state.ai_summary = None
if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None

# === Main Application Logic =================================
if not uploaded_file:
    st.markdown("""
    <div class="info-box">
        <h2 style="color: white; margin-top: 0;">🚀 Welcome to Your AI Financial Dashboard</h2>
        <p style="font-size: 16px;">Upload your financial dataset to unlock powerful analytics and insights.</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 📊 Smart Analytics
        - Automatic column detection
        - KPI calculations
        - Trend analysis
        - Performance metrics
        """)
    with col2:
        st.markdown("""
        ### 🤖 AI-Powered
        - Executive summaries
        - Insight generation
        - Pattern recognition
        - Strategic recommendations
        """)
    with col3:
        st.markdown("""
        ### 🔮 Forecasting
        - 30-day predictions
        - Confidence intervals
        - Seasonal patterns
        - Growth projections
        """)
    st.info("👆 **Upload your .csv or .xlsx file in the sidebar to begin analysis**")
    st.stop()

# === File Processing ========================================
try:
    ext = uploaded_file.name.split(".")[-1].lower()
    df = pd.read_excel(uploaded_file) if ext == "xlsx" else pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    cols_lower = [c.lower() for c in df.columns]
    date_col, amount_col, product_col, payment_col, category_col = None, None, None, None, None
    for i, c in enumerate(cols_lower):
        if not date_col and any(kw in c for kw in ["date", "day", "time", "period", "timestamp"]):
            date_col = df.columns[i]
        if not amount_col and any(kw in c for kw in ["revenue", "sales", "amount", "money", "total", "price", "value"]):
            amount_col = df.columns[i]
        if not product_col and any(kw in c for kw in ["product", "coffee", "item", "name", "goods"]):
            product_col = df.columns[i]
        if not payment_col and any(kw in c for kw in ["payment", "method", "cash", "card"]):
            payment_col = df.columns[i]
        if not category_col and any(kw in c for kw in ["category", "type", "class", "group"]):
            category_col = df.columns[i]
    detected = {
        "📅 Date Column": date_col or "Not detected",
        "💰 Amount Column": amount_col or "Not detected",
        "☕ Product Column": product_col or "Not detected",
        "💳 Payment Column": payment_col or "Not detected",
        "📂 Category Column": category_col or "Not detected"
    }
    if not date_col or not amount_col:
        st.error("❌ **Critical columns missing!** Ensure your data has date and amount columns.")
        st.json(detected)
        st.stop()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    df = df.dropna(subset=[date_col, amount_col])
    daily = df.groupby(date_col)[amount_col].sum().reset_index()
    daily.columns = ["ds", "y"]
    daily = daily.sort_values("ds")
    total_revenue = daily["y"].sum()
    avg_daily_revenue = daily["y"].mean()
    max_rev_day = daily["y"].max()
    min_rev_day = daily["y"].min()
    num_transactions = len(df)
    avg_transaction = total_revenue / num_transactions if num_transactions > 0 else 0
    num_days = len(daily)
    start_date = daily["ds"].min()
    end_date = daily["ds"].max()
    date_range_days = (end_date - start_date).days
    if len(daily) >= 7:
        recent_week = daily.tail(7)["y"].mean()
        previous_week = daily.head(7)["y"].mean() if len(daily) >= 14 else avg_daily_revenue
        growth_rate = ((recent_week - previous_week) / previous_week * 100) if previous_week > 0 else 0
    else:
        growth_rate = 0
except Exception as e:
    st.error(f"❌ **Error processing file:** {str(e)}")
    st.info("Please check your file format and try again.")
    st.stop()

# === 🏠 DASHBOARD HOME ======================================
if selected_tab == "🏠 Dashboard Home":
    st.header("🏠 Executive Dashboard Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='metric-label'>💰 Total Revenue</div>
            <div class='metric-value'>${total_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='metric-label'>📅 Daily Average</div>
            <div class='metric-value'>${avg_daily_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='metric-label'>📈 Peak Day</div>
            <div class='metric-value'>${max_rev_day:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='metric-label'>🔢 Transactions</div>
            <div class='metric-value'>{num_transactions:,}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 📊 Revenue Trend Overview")
        fig = px.line(
            daily,
            x="ds",
            y="y",
            title="Daily Revenue Performance",
            labels={"ds": "Date", "y": "Revenue ($)"}
        )
        fig.update_traces(
            line_color='#667eea',
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        )
        fig.update_layout(
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(
            fig,
            config={"displayModeBar": False},
            use_container_width=True
        )
    with col2:
        st.markdown("### 📋 Data Summary")
        st.markdown(f"""
        **📆 Date Range**  
        `{start_date.strftime('%Y-%m-%d')}` to `{end_date.strftime('%Y-%m-%d')}`
        
        **📊 Analysis Period**  
        `{date_range_days}` days
        
        **💳 Avg Transaction**  
        `${avg_transaction:,.2f}`
        
        **📈 Growth Rate**  
        `{growth_rate:+.1f}%` (Last 7 days)
        
        **⬆️ Highest Day**  
        `${max_rev_day:,.2f}`
        
        **⬇️ Lowest Day**  
        `${min_rev_day:,.2f}`
        """)
        st.markdown("### 🔍 Detected Columns")
        for key, value in detected.items():
            status = "✅" if value != "Not detected" else "❌"
            st.markdown(f"{status} {key}: `{value}`")

# === 📋 DATA & KPIs =========================================
elif selected_tab == "📋 Data & KPIs":
    st.header("📋 Comprehensive Data Analysis")
    st.markdown("### 💎 Primary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='metric-label'>💰 Total Revenue</div>
            <div class='metric-value'>${total_revenue:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='metric-label'>📅 Avg Daily</div>
            <div class='metric-value'>${avg_daily_revenue:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='metric-label'>⬆️ Peak Day</div>
            <div class='metric-value'>${max_rev_day:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='metric-label'>⬇️ Low Day</div>
            <div class='metric-value'>${min_rev_day:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("### 📊 Secondary Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("🔢 Transactions", f"{num_transactions:,}")
    with col2:
        st.metric("💳 Avg Transaction", f"${avg_transaction:,.2f}")
    with col3:
        st.metric("📆 Days Analyzed", f"{num_days:,}")
    with col4:
        revenue_range = max_rev_day - min_rev_day
        st.metric("📊 Revenue Range", f"${revenue_range:,.2f}")
    with col5:
        st.metric("📈 Growth Rate", f"{growth_rate:+.1f}%")
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📄 Raw Data", "📊 Daily Summary", "🔍 Statistics"])
    with tab1:
        st.markdown("### 📄 Complete Dataset")
        st.dataframe(df, width='stretch', height=400)
        st.caption(f"Showing all {len(df):,} records")
    with tab2:
        st.markdown("### 📊 Daily Revenue Summary")
        st.dataframe(daily, width='stretch', height=400)
        st.caption(f"Showing {len(daily):,} days of aggregated data")
    with tab3:
        st.markdown("### 🔍 Statistical Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Revenue Statistics**")
            stats = daily["y"].describe()
            st.dataframe(stats, width='stretch')
        with col2:
            st.markdown("**Data Quality**")
            quality_metrics = {
                "Total Records": len(df),
                "Date Range (Days)": date_range_days,
                "Missing Dates": date_range_days - len(daily),
                "Duplicate Check": "No duplicates" if df.duplicated().sum() == 0 else f"{df.duplicated().sum()} duplicates"
            }
            st.json(quality_metrics)

# === 📊 VISUAL ANALYTICS ====================================
elif selected_tab == "📊 Visual Analytics":
    st.header("📊 Advanced Visual Analytics")
    st.markdown("### 📈 Revenue Trend Analysis")
    fig1 = px.area(
        daily,
        x="ds",
        y="y",
        title="Daily Revenue Performance Over Time",
        labels={"ds": "Date", "y": "Revenue ($)"}
    )
    fig1.update_traces(
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    )
    fig1.update_layout(hovermode='x unified', plot_bgcolor='white')
    st.plotly_chart(fig1, config={"displayModeBar": False}, use_container_width=True)
    col1, col2 = st.columns(2)
    if product_col:
        with col1:
            st.markdown("### ☕ Top Products by Revenue")
            top_products = df.groupby(product_col)[amount_col].sum().reset_index()
            top_products = top_products.sort_values(by=amount_col, ascending=False).head(10)
            fig2 = px.bar(
                top_products,
                x=amount_col,
                y=product_col,
                orientation='h',
                title="Top 10 Revenue Generators",
                labels={product_col: "Product", amount_col: "Revenue ($)"},
                color=amount_col,
                color_continuous_scale="Viridis"
            )
            fig2.update_layout(plot_bgcolor='white', showlegend=False)
            st.plotly_chart(fig2, config={"displayModeBar": False}, use_container_width=True)
    if payment_col:
        with col2:
            st.markdown("### 💳 Payment Methods")
            payment_data = df.groupby(payment_col)[amount_col].sum().reset_index()
            fig3 = px.pie(
                payment_data,
                names=payment_col,
                values=amount_col,
                title="Revenue by Payment Method",
                hole=0.4
            )
            fig3.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='white', width=2))
            )
            st.plotly_chart(fig3, config={"displayModeBar": False}, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Revenue Distribution")
        fig4 = px.histogram(
            daily,
            x="y",
            nbins=25,
            title="Distribution of Daily Revenue",
            labels={"y": "Daily Revenue ($)"},
            color_discrete_sequence=['#764ba2']
        )
        fig4.update_layout(plot_bgcolor='white', showlegend=False)
        st.plotly_chart(fig4, config={"displayModeBar": False}, use_container_width=True)
    with col2:
        st.markdown("### 📅 Day of Week Pattern")
        daily_copy = daily.copy()
        daily_copy['day_of_week'] = daily_copy['ds'].dt.day_name()
        dow_data = daily_copy.groupby('day_of_week')['y'].mean().reset_index()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_data['day_of_week'] = pd.Categorical(dow_data['day_of_week'], categories=day_order, ordered=True)
        dow_data = dow_data.sort_values('day_of_week')
        fig5 = px.bar(
            dow_data,
            x='day_of_week',
            y='y',
            title="Average Revenue by Day of Week",
            labels={'day_of_week': 'Day', 'y': 'Avg Revenue ($)'},
            color='y',
            color_continuous_scale='Blues'
        )
        fig5.update_layout(plot_bgcolor='white', showlegend=False)
        st.plotly_chart(fig5, config={"displayModeBar": False}, use_container_width=True)

# === 🧠 AI INSIGHTS =========================================
elif selected_tab == "🧠 AI Insights":
    st.header("🧠 AI-Powered Executive Intelligence")
    if not api_key:
        st.warning("⚠️ **API Key Required** - Enter your Groq API key in the sidebar to unlock AI insights.")
        st.info("Get your free API key at [console.groq.com](https://console.groq.com)")
        st.stop()
    kpi_context = {
        "dataset_overview": {
            "total_revenue": round(total_revenue, 2),
            "date_range": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "days_analyzed": num_days,
            "total_transactions": num_transactions
        },
        "performance_metrics": {
            "average_daily_revenue": round(avg_daily_revenue, 2),
            "average_transaction_value": round(avg_transaction, 2),
            "max_day_revenue": round(max_rev_day, 2),
            "min_day_revenue": round(min_rev_day, 2),
            "revenue_volatility": round(daily["y"].std(), 2),
            "growth_rate_7days": round(growth_rate, 2)
        },
        "data_columns": {
            "product_column": product_col or "N/A",
            "payment_column": payment_col or "N/A",
            "category_column": category_col or "N/A"
        }
    }
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🎯 Generate Executive Summary")
        st.markdown("Click below to generate a comprehensive AI-powered analysis of your financial data.")
        if st.button("🚀 Generate AI Analysis", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your financial data... This may take 10-15 seconds"):
                try:
                    client = Groq(api_key=api_key)
                    system_prompt = """You are an elite financial analyst AI with deep expertise in business intelligence, 
                    data analysis, and strategic planning. You work for Fortune 500 companies and provide C-suite executives 
                    with actionable insights.
                    
                    Analyze the provided financial KPIs and generate a comprehensive 300-word executive summary that includes:
                    
                    1. **Performance Assessment**: Overall health and trajectory
                    2. **Key Patterns**: Trends, seasonality, anomalies
                    3. **Strategic Insights**: Opportunities for growth and optimization
                    4. **Risk Analysis**: Potential concerns or red flags
                    5. **Actionable Recommendations**: Specific next steps
                    
                    Write in a professional, confident tone suitable for executive presentation. Use specific numbers 
                    and percentages from the data. Be direct and actionable."""
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Analyze these financial metrics and provide strategic insights:\n\n{json.dumps(kpi_context, indent=2)}"}
                        ],
                        temperature=0.4,
                        max_tokens=600
                    )
                    st.session_state.ai_summary = response.choices[0].message.content.strip()
                    st.success("✅ AI Analysis Complete!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ AI Analysis Failed: {str(e)}")
                    st.info("Please verify your API key and internet connection.")
    with col2:
        st.markdown("### 📊 Analysis Context")
        st.json(kpi_context)
    if st.session_state.ai_summary:
        st.markdown("---")
        st.markdown("### 📝 Executive Summary")
        st.markdown(f"""
        <div class='summary-box'>
            {st.session_state.ai_summary.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("### 💡 Key Takeaways")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**📊 Performance**\nTotal Revenue: ${total_revenue:,.0f}\nGrowth: {growth_rate:+.1f}%")
        with col2:
            st.success(f"**📈 Trends**\nAvg Daily: ${avg_daily_revenue:,.0f}\nPeak: ${max_rev_day:,.0f}")
        with col3:
            st.warning(f"**⚠️ Attention**\nVolatility: ${daily['y'].std():,.0f}\nRange: ${max_rev_day - min_rev_day:,.0f}")

# === 📈 FORECAST & TRENDS ===================================
elif selected_tab == "📈 Forecast & Trends":
    st.header("📈 Revenue Forecasting & Predictive Analytics")
    try:
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            forecast_days = st.slider("Forecast Period (Days)", 7, 90, 30)
        with col2:
            confidence_interval = st.slider("Confidence Level", 0.80, 0.99, 0.95, 0.01)
        if st.button("🔮 Generate Forecast", type="primary"):
            with st.spinner("🔮 Generating forecast with Prophet algorithm..."):
                model = Prophet(
                    daily_seasonality=True,
                    weekly_seasonality=True,
                    yearly_seasonality=False,
                    interval_width=confidence_interval
                )
                model.fit(daily)
                future = model.make_future_dataframe(periods=forecast_days)
                forecast = model.predict(future)
                st.session_state.forecast_data = {
                    'forecast': forecast,
                    'days': forecast_days,
                    'confidence': confidence_interval
                }
                st.success(f"✅ {forecast_days}-day forecast generated successfully!")
        if st.session_state.forecast_data:
            forecast = st.session_state.forecast_data['forecast']
            forecast_days = st.session_state.forecast_data['days']
            st.markdown("---")
            st.markdown("### 📊 Forecast Visualization")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily['ds'],
                y=daily['y'],
                mode='markers',
                name='Actual Revenue',
                marker=dict(color='red', size=6)
            ))
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat'],
                mode='lines',
                name='Forecast',
                line=dict(color='#667eea', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_upper'],
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_lower'],
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(102, 126, 234, 0.2)',
                fill='tonexty',
                name=f'{int(confidence_interval*100)}% Confidence',
                hoverinfo='skip'
            ))
            fig.update_layout(
                title=f"Revenue Forecast - Next {forecast_days} Days",
                xaxis_title="Date",
                yaxis_title="Revenue ($)",
                hovermode='x unified',
                plot_bgcolor='white',
                height=500
            )
            st.plotly_chart(fig, config={"displayModeBar": False}, use_container_width=True)
            st.markdown("### 📊 Forecast Metrics")
            future_forecast = forecast.tail(forecast_days)
            avg_forecast = future_forecast['yhat'].mean()
            total_forecast = future_forecast['yhat'].sum()
            forecast_growth = ((avg_forecast - avg_daily_revenue) / avg_daily_revenue * 100)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "📊 Avg Forecasted Daily",
                    f"${avg_forecast:,.2f}",
                    f"{forecast_growth:+.1f}%"
                )
            with col2:
                st.metric(
                    "💰 Total Forecast",
                    f"${total_forecast:,.2f}"
                )
            with col3:
                st.metric(
                    "📈 Expected Growth",
                    f"{forecast_growth:+.1f}%"
                )
            with col4:
                upper_bound_avg = future_forecast['yhat_upper'].mean()
                potential_upside = ((upper_bound_avg - avg_forecast) / avg_forecast * 100)
                st.metric(
                    "🎯 Upside Potential",
                    f"{potential_upside:+.1f}%"
                )
            st.markdown("### 📋 Detailed Forecast (Next 14 Days)")
            forecast_table = future_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head(14).copy()
            forecast_table.columns = ['Date', 'Predicted', 'Lower Bound', 'Upper Bound']
            forecast_table['Date'] = forecast_table['Date'].dt.strftime('%Y-%m-%d')
            forecast_table['Predicted'] = forecast_table['Predicted'].apply(lambda x: f"${x:,.2f}")
            forecast_table['Lower Bound'] = forecast_table['Lower Bound'].apply(lambda x: f"${x:,.2f}")
            forecast_table['Upper Bound'] = forecast_table['Upper Bound'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(forecast_table, width='stretch', height=400)
            st.markdown("### 🔍 Forecast Components Analysis")
            col1, col2 = st.columns(2)
            with col1:
                fig_trend = px.line(
                    forecast,
                    x='ds',
                    y='trend',
                    title='Overall Trend Component',
                    labels={'ds': 'Date', 'trend': 'Trend'}
                )
                fig_trend.update_traces(line_color='#667eea')
                fig_trend.update_layout(plot_bgcolor='white')
                st.plotly_chart(fig_trend, config={"displayModeBar": False}, use_container_width=True)
            with col2:
                if 'weekly' in forecast.columns:
                    fig_weekly = px.line(
                        forecast,
                        x='ds',
                        y='weekly',
                        title='Weekly Seasonality Pattern',
                        labels={'ds': 'Date', 'weekly': 'Weekly Effect'}
                    )
                    fig_weekly.update_traces(line_color='#764ba2')
                    fig_weekly.update_layout(plot_bgcolor='white')
                    st.plotly_chart(fig_weekly, config={"displayModeBar": False}, use_container_width=True)
        else:
            st.info("👆 Click 'Generate Forecast' above to create predictions")
    except Exception as e:
        st.error(f"❌ Forecasting Error: {str(e)}")
        st.info("Ensure you have at least 2 weeks of historical data for accurate forecasting.")

# === 📤 EXPORT REPORTS ======================================
elif selected_tab == "📤 Export Reports":
    st.header("📤 Export & Download Reports")
    st.markdown("""
    <div class="info-box">
        <h3 style="margin-top: 0; color: white;">📦 Download Your Analysis</h3>
        <p>Export all your reports, insights, and data in various formats.</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📄 AI Insights & Reports")
        if st.session_state.ai_summary:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_content = f"""
AI FINANCIAL ANALYSIS REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Dataset: {uploaded_file.name}
Analysis Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}

{'='*60}
EXECUTIVE SUMMARY
{'='*60}

{st.session_state.ai_summary}

{'='*60}
KEY METRICS
{'='*60}

Total Revenue: ${total_revenue:,.2f}
Average Daily Revenue: ${avg_daily_revenue:,.2f}
Total Transactions: {num_transactions:,}
Average Transaction: ${avg_transaction:,.2f}
Peak Day Revenue: ${max_rev_day:,.2f}
Low Day Revenue: ${min_rev_day:,.2f}
Growth Rate (7-day): {growth_rate:+.1f}%
Days Analyzed: {num_days}

{'='*60}
End of Report
{'='*60}
"""
            st.download_button(
                label="⬇️ Download AI Summary (TXT)",
                data=summary_content.encode('utf-8'),
                file_name=f"ai_financial_report_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )
            report_json = {
                "generated": datetime.now().isoformat(),
                "dataset": uploaded_file.name,
                "date_range": {
                    "start": start_date.strftime('%Y-%m-%d'),
                    "end": end_date.strftime('%Y-%m-%d')
                },
                "metrics": {
                    "total_revenue": float(total_revenue),
                    "avg_daily_revenue": float(avg_daily_revenue),
                    "total_transactions": int(num_transactions),
                    "avg_transaction": float(avg_transaction),
                    "peak_day": float(max_rev_day),
                    "low_day": float(min_rev_day),
                    "growth_rate": float(growth_rate),
                    "days_analyzed": int(num_days)
                },
                "ai_summary": st.session_state.ai_summary
            }
            st.download_button(
                label="⬇️ Download Analysis (JSON)",
                data=json.dumps(report_json, indent=2).encode('utf-8'),
                file_name=f"financial_analysis_{timestamp}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.warning("⚠️ Generate AI insights first in the '🧠 AI Insights' tab to download the report.")
    with col2:
        st.markdown("### 📊 Data Exports")
        csv_raw = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Raw Data (CSV)",
            data=csv_raw,
            file_name=f"financial_data_raw_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        csv_daily = daily.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Daily Summary (CSV)",
            data=csv_daily,
            file_name=f"daily_revenue_summary_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        if st.session_state.forecast_data:
            forecast_export = st.session_state.forecast_data['forecast'][['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
            forecast_export.columns = ['Date', 'Predicted', 'Lower_Bound', 'Upper_Bound']
            csv_forecast = forecast_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Forecast (CSV)",
                data=csv_forecast,
                file_name=f"revenue_forecast_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("📈 Generate a forecast to download predictions")
    st.markdown("---")
    st.markdown("### 📊 Export Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📁 Dataset Records", f"{len(df):,}")
    with col2:
        st.metric("📅 Days of Data", f"{num_days:,}")
    with col3:
        ai_status = "✅ Available" if st.session_state.ai_summary else "❌ Not Generated"
        st.metric("🤖 AI Report", ai_status)
    with col4:
        forecast_status = "✅ Available" if st.session_state.forecast_data else "❌ Not Generated"
        st.metric("📈 Forecast", forecast_status)
    st.success("✅ All available reports are ready for download!")

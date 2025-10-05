# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # -----------------------------
# # Page Config
# # -----------------------------
# st.set_page_config(page_title="🚀 Modern KPI Dashboard", layout="wide")

# # -----------------------------
# # Sidebar Theme Toggle
# # -----------------------------
# theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

# if theme == "Dark":
#     st.markdown(
#         """
#         <style>
#             body { background-color: #0e1117; color: #fafafa; }
#             .block-container { background-color: #0e1117; color: #fafafa; }
#             div[data-testid="stMetric"] {
#                 background-color: #1a1d23;
#                 color: #fafafa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #fafafa;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
# else:  # Light mode
#     st.markdown(
#         """
#         <style>
#             .block-container { background-color: #ffffff; color: #000000; }
#             div[data-testid="stMetric"] {
#                 background-color: #f8f9fa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #000000;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # -----------------------------
# # Title
# # -----------------------------
# st.title("📊 Business KPI Dashboard")
# st.caption("Upload your CSV or explore with sample data")

# # -----------------------------
# # Sidebar Upload
# # -----------------------------
# uploaded_file = st.sidebar.file_uploader("📂 Upload CSV", type="csv")

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
#     st.success(f"✅ File loaded: {df.shape[0]} rows, {df.shape[1]} cols")
# else:
#     df = pd.read_csv("../Day8/superstore_customer_enriched.csv")
#     st.info("📌 Using sample dataset (Superstore, 9,994 rows)")

# st.dataframe(df.head(), use_container_width=True)

# # -----------------------------
# # KPIs
# # -----------------------------
# col1, col2, col3 = st.columns(3)

# gross = df['Profit'].sum().round(0)
# net = df['Net Profit'].sum().round(0) if 'Net Profit' in df.columns else gross
# drag = (gross - net).round(0)

# with col1: st.metric("💰 Gross Profit", f"${gross:,}")
# with col2: st.metric("📈 Net Profit", f"${net:,}")
# with col3: st.metric("📉 Returns Drag", f"${drag:,}")

# # -----------------------------
# # Filters
# # -----------------------------
# if 'Segment' in df.columns:
#     segment_options = ['All'] + list(df['Segment'].unique())
#     selected_segment = st.sidebar.selectbox("🎯 Filter by Segment", segment_options)

#     if selected_segment == "All":
#         df_filtered = df
#     else:
#         df_filtered = df[df['Segment'] == selected_segment]
# else:
#     df_filtered = df
#     st.sidebar.warning("⚠️ No 'Segment' column found")

# # -----------------------------
# # Tabs
# # -----------------------------
# tab1, tab2, tab3 = st.tabs(["📊 Sales by Segment", "📆 Revenue Trends", "🌍 Profit Heatmap"])

# with tab1:
#     st.subheader(f"Sales Overview – {selected_segment}")

#     if 'Net Profit' in df_filtered.columns:
#         net_seg = df_filtered.groupby('Segment')['Net Profit'].sum().reset_index()
#         fig1 = px.bar(net_seg, x='Segment', y='Net Profit',
#                       text='Net Profit', color='Segment',
#                       color_discrete_sequence=px.colors.qualitative.Pastel)
#     else:
#         net_seg = df_filtered.groupby('Segment')['Sales'].sum().reset_index()
#         fig1 = px.bar(net_seg, x='Segment', y='Sales',
#                       text='Sales', color='Segment',
#                       color_discrete_sequence=px.colors.qualitative.Pastel)

#     fig1.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
#     fig1.update_layout(title="Net Profit / Sales by Segment", yaxis_title="Amount ($)")
#     st.plotly_chart(fig1, use_container_width=True)

# with tab2:
#     st.subheader("Monthly Revenue Trend")

#     df_filtered['Month'] = pd.to_datetime(df_filtered['Order Date']).dt.to_period('M')
#     monthly = df_filtered.groupby('Month')['Sales'].sum().reset_index()
#     monthly['Month'] = monthly['Month'].astype(str)

#     fig2 = px.line(monthly, x='Month', y='Sales', markers=True,
#                    line_shape="spline", color_discrete_sequence=["#6f42c1"])
#     fig2.update_layout(title="Monthly Sales Trend", yaxis_title="Sales ($)")
#     st.plotly_chart(fig2, use_container_width=True)

# with tab3:
#     st.subheader("Profit Heatmap: Region vs Segment")

#     if 'Region' in df_filtered.columns and 'Net Profit' in df_filtered.columns:
#         pivot_heat = df_filtered.pivot_table(values='Net Profit',
#                                              index='Region',
#                                              columns='Segment',
#                                              aggfunc='sum',
#                                              fill_value=0).round(0)
#         fig3 = px.imshow(pivot_heat,
#                          text_auto=True,
#                          aspect="auto",
#                          color_continuous_scale="RdYlGn")
#         st.plotly_chart(fig3, use_container_width=True)
#     else:
#         st.warning("⚠️ Needs 'Region' & 'Net Profit' columns for heatmap")

# # -----------------------------
# # Footer
# # -----------------------------
# st.markdown("---")
# st.caption("🚀 Modern Dashboard v3 – AI-ready insights coming soon!")

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os

# # -----------------------------
# # Page Config
# # -----------------------------
# st.set_page_config(page_title="🚀 Modern KPI Dashboard", layout="wide")

# # -----------------------------
# # Sidebar Theme Toggle
# # -----------------------------
# theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

# if theme == "Dark":
#     st.markdown(
#         """
#         <style>
#             body { background-color: #0e1117; color: #fafafa; }
#             .block-container { background-color: #0e1117; color: #fafafa; }
#             div[data-testid="stMetric"] {
#                 background-color: #1a1d23;
#                 color: #fafafa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #fafafa;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
# else:  # Light mode
#     st.markdown(
#         """
#         <style>
#             .block-container { background-color: #ffffff; color: #000000; }
#             div[data-testid="stMetric"] {
#                 background-color: #f8f9fa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #000000;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # -----------------------------
# # Title
# # -----------------------------
# st.title("📊 Business KPI Dashboard")
# st.caption("Upload any file (CSV, XLSX, PDF) – Auto-handles & charts")

# # -----------------------------
# # Sidebar Upload with Better Error Handling
# # -----------------------------
# uploaded_file = st.sidebar.file_uploader("📂 Upload File", type=['csv', 'xlsx'])

# if uploaded_file is not None:
#     file_ext = os.path.splitext(uploaded_file.name)[1].lower()
#     try:
#         if file_ext == '.csv':
#             # Try multiple encodings and strip whitespace from columns
#             for encoding in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
#                 try:
#                     df = pd.read_csv(uploaded_file, encoding=encoding)
#                     # Strip whitespace from column names
#                     df.columns = df.columns.str.strip()
#                     st.success(f"✅ CSV loaded ({encoding}): {df.shape[0]} rows, {df.shape[1]} cols")
#                     break
#                 except (UnicodeDecodeError, pd.errors.ParserError):
#                     uploaded_file.seek(0)  # Reset file pointer
#                     continue
#         elif file_ext == '.xlsx':
#             df = pd.read_excel(uploaded_file)
#             df.columns = df.columns.str.strip()
#             st.success(f"✅ XLSX loaded: {df.shape[0]} rows, {df.shape[1]} cols")
#         else:
#             st.warning("⚠️ Please upload CSV or XLSX file")
#             st.stop()
#     except Exception as e:
#         st.error(f"❌ Load error: {e}")
#         st.stop()
# else:
#     # Fallback to sample data
#     try:
#         df = pd.read_csv("../Day8/superstore_customer_enriched.csv", encoding='latin1')
#         df.columns = df.columns.str.strip()
#         st.info("📌 Using sample data (9,994 rows)")
#     except:
#         st.error("❌ No file uploaded and sample data not found. Please upload a CSV/XLSX file.")
#         st.stop()

# # -----------------------------
# # Debug: Show Available Columns
# # -----------------------------
# with st.expander("🔍 Debug: Available Columns", expanded=False):
#     st.write("**Detected columns:**")
#     st.write(list(df.columns))
#     st.write(f"**Total columns:** {len(df.columns)}")

# # -----------------------------
# # Auto-Clean with Better Column Detection
# # -----------------------------
# original_shape = df.shape

# # Clean column names (remove extra spaces, special characters)
# df.columns = df.columns.str.strip().str.replace('\s+', ' ', regex=True)

# # Date columns - try common date column names
# date_columns = ['Order Date', 'Date', 'OrderDate', 'order_date']
# for date_col in date_columns:
#     if date_col in df.columns:
#         df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
#         st.info(f"📅 Parsed date column: {date_col}")
#         break

# # Numeric columns - handle common profit/sales columns
# numeric_mappings = {
#     'Profit': ['Profit', 'profit', 'PROFIT', 'Net Profit', 'net_profit'],
#     'Sales': ['Sales', 'sales', 'SALES', 'Revenue', 'revenue'],
#     'Quantity': ['Quantity', 'quantity', 'QTY', 'qty']
# }

# for standard_name, variations in numeric_mappings.items():
#     for var in variations:
#         if var in df.columns:
#             if standard_name not in df.columns or var == standard_name:
#                 df[standard_name] = pd.to_numeric(df[var], errors='coerce').fillna(0)
#                 if var != standard_name:
#                     st.info(f"🔄 Mapped '{var}' → '{standard_name}'")
#             break

# # Drop completely empty rows
# df = df.dropna(how='all')

# cleaned_info = f"🧹 Auto-cleaned: {df.shape[0]} rows × {df.shape[1]} cols"
# if original_shape != df.shape:
#     cleaned_info += f" (removed {original_shape[0] - df.shape[0]} empty rows)"
# st.success(cleaned_info)

# # Show preview
# st.dataframe(df.head(10), use_container_width=True)

# # -----------------------------
# # KPIs with Smart Fallbacks
# # -----------------------------
# st.markdown("### 📊 Key Performance Indicators")
# col1, col2, col3 = st.columns(3)

# # Check if required columns exist
# has_profit = 'Profit' in df.columns
# has_net_profit = 'Net Profit' in df.columns
# has_sales = 'Sales' in df.columns

# if has_profit:
#     gross = df['Profit'].sum().round(0)
#     net = df['Net Profit'].sum().round(0) if has_net_profit else gross
#     drag = (gross - net).round(0)
    
#     with col1: 
#         st.metric("💰 Gross Profit", f"${gross:,}")
#     with col2: 
#         st.metric("📈 Net Profit", f"${net:,}")
#     with col3: 
#         st.metric("📉 Returns Drag", f"${drag:,}")
# elif has_sales:
#     total_sales = df['Sales'].sum().round(0)
#     avg_sales = df['Sales'].mean().round(2)
#     max_sales = df['Sales'].max().round(0)
    
#     with col1: 
#         st.metric("💰 Total Sales", f"${total_sales:,}")
#     with col2: 
#         st.metric("📊 Average Sale", f"${avg_sales:,}")
#     with col3: 
#         st.metric("🏆 Max Sale", f"${max_sales:,}")
# else:
#     st.warning("⚠️ No 'Profit' or 'Sales' columns found. Please check your data.")
#     # Show summary of numeric columns instead
#     numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
#     if numeric_cols:
#         st.info(f"📊 Found numeric columns: {', '.join(numeric_cols[:5])}")
#         for i, col in enumerate(numeric_cols[:3]):
#             with [col1, col2, col3][i]:
#                 st.metric(f"📈 {col}", f"{df[col].sum():,.0f}")

# # -----------------------------
# # Filters with Smart Detection
# # -----------------------------
# segment_columns = ['Segment', 'segment', 'Category', 'category', 'Type', 'type']
# segment_col = None

# for col in segment_columns:
#     if col in df.columns:
#         segment_col = col
#         break

# if segment_col:
#     segment_options = ['All'] + sorted(df[segment_col].dropna().unique().tolist())
#     selected_segment = st.sidebar.selectbox(f"🎯 Filter by {segment_col}", segment_options)

#     if selected_segment == "All":
#         df_filtered = df
#     else:
#         df_filtered = df[df[segment_col] == selected_segment]
    
#     st.sidebar.info(f"📊 Filtered: {len(df_filtered):,} records")
# else:
#     df_filtered = df
#     st.sidebar.warning("⚠️ No segment column found")
#     segment_col = 'Segment'  # Default for display

# # -----------------------------
# # Tabs with Dynamic Column Detection
# # -----------------------------
# tab1, tab2, tab3 = st.tabs(["📊 Sales by Segment", "📆 Revenue Trends", "🌍 Profit Heatmap"])

# with tab1:
#     st.subheader(f"Sales Overview – {selected_segment if segment_col else 'All Data'}")

#     if segment_col and segment_col in df_filtered.columns:
#         # Determine metric column
#         if 'Net Profit' in df_filtered.columns:
#             metric_col = 'Net Profit'
#             title_suffix = 'Net Profit'
#         elif 'Profit' in df_filtered.columns:
#             metric_col = 'Profit'
#             title_suffix = 'Profit'
#         elif 'Sales' in df_filtered.columns:
#             metric_col = 'Sales'
#             title_suffix = 'Sales'
#         else:
#             numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
#             if numeric_cols:
#                 metric_col = numeric_cols[0]
#                 title_suffix = metric_col
#             else:
#                 st.warning("⚠️ No numeric columns found for charting")
#                 st.stop()

#         agg_data = df_filtered.groupby(segment_col)[metric_col].sum().reset_index()
        
#         fig1 = px.bar(
#             agg_data, 
#             x=segment_col, 
#             y=metric_col,
#             text=metric_col, 
#             color=segment_col,
#             color_discrete_sequence=px.colors.qualitative.Pastel
#         )
#         fig1.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
#         fig1.update_layout(
#             title=f"{title_suffix} by {segment_col}",
#             yaxis_title="Amount ($)",
#             showlegend=False
#         )
#         st.plotly_chart(fig1, use_container_width=True)
#     else:
#         st.warning(f"⚠️ '{segment_col}' column not found. Cannot generate segment chart.")

# with tab2:
#     st.subheader("Monthly Revenue Trend")

#     # Find date column
#     date_col = None
#     for col_name in ['Order Date', 'Date', 'OrderDate', 'order_date', 'date']:
#         if col_name in df_filtered.columns:
#             date_col = col_name
#             break

#     if date_col and 'Sales' in df_filtered.columns:
#         df_temp = df_filtered.copy()
#         df_temp['Month'] = pd.to_datetime(df_temp[date_col], errors='coerce').dt.to_period('M')
#         df_temp = df_temp.dropna(subset=['Month'])
        
#         if len(df_temp) > 0:
#             monthly = df_temp.groupby('Month')['Sales'].sum().reset_index()
#             monthly['Month'] = monthly['Month'].astype(str)
            
#             fig2 = px.line(
#                 monthly, 
#                 x='Month', 
#                 y='Sales', 
#                 markers=True,
#                 line_shape="spline", 
#                 color_discrete_sequence=["#6f42c1"]
#             )
#             fig2.update_layout(
#                 title="Monthly Sales Trend",
#                 yaxis_title="Sales ($)",
#                 xaxis_title="Month"
#             )
#             st.plotly_chart(fig2, use_container_width=True)
#         else:
#             st.warning("⚠️ No valid dates found in the date column.")
#     else:
#         missing = []
#         if not date_col:
#             missing.append("date column")
#         if 'Sales' not in df_filtered.columns:
#             missing.append("'Sales' column")
#         st.warning(f"⚠️ Missing {' and '.join(missing)} for trend analysis.")

# with tab3:
#     st.subheader("Profit Heatmap: Region vs Segment")

#     # Find index column (Region, Category, etc.)
#     index_options = ['Region', 'region', 'Category', 'category', 'State', 'state']
#     index_col = None
#     for opt in index_options:
#         if opt in df_filtered.columns:
#             index_col = opt
#             break

#     # Find value column
#     value_col = None
#     value_options = ['Net Profit', 'Profit', 'Sales']
#     for opt in value_options:
#         if opt in df_filtered.columns:
#             value_col = opt
#             break

#     if index_col and value_col and segment_col and segment_col in df_filtered.columns:
#         pivot_heat = df_filtered.pivot_table(
#             values=value_col,
#             index=index_col,
#             columns=segment_col,
#             aggfunc='sum',
#             fill_value=0
#         ).round(0)
        
#         fig3 = px.imshow(
#             pivot_heat,
#             text_auto=True,
#             aspect="auto",
#             color_continuous_scale="RdYlGn",
#             labels=dict(color=value_col)
#         )
#         fig3.update_layout(title=f"{value_col} Heatmap: {index_col} vs {segment_col}")
#         st.plotly_chart(fig3, use_container_width=True)
#     else:
#         missing_cols = []
#         if not index_col:
#             missing_cols.append("index column (Region/Category)")
#         if not value_col:
#             missing_cols.append("value column (Profit/Sales)")
#         if not segment_col or segment_col not in df_filtered.columns:
#             missing_cols.append("segment column")
        
#         st.warning(f"⚠️ Heatmap requires: {', '.join(missing_cols)}")

# # -----------------------------
# # Preview & Export
# # -----------------------------
# st.markdown("---")
# st.markdown("### 💾 Data Export")

# with st.expander("👀 Full Cleaned Data Preview", expanded=False):
#     st.dataframe(df_filtered, use_container_width=True)

# csv_clean = df_filtered.to_csv(index=False).encode('utf-8')
# st.download_button(
#     label="💾 Download Cleaned CSV",
#     data=csv_clean,
#     file_name="cleaned_kpis.csv",
#     mime="text/csv"
# )

# # -----------------------------
# # Footer
# # -----------------------------
# st.markdown("---")
# st.caption("🚀 Modern Dashboard v3 – AI-ready insights | Now with smart column detection!")

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import logging
# from prophet import Prophet

# # Suppress Prophet verbose output
# logging.getLogger('prophet').setLevel(logging.ERROR)
# logging.getLogger('cmdstanpy').setLevel(logging.ERROR)

# # -----------------------------
# # Page Config
# # -----------------------------
# st.set_page_config(page_title="🚀 Modern KPI Dashboard", layout="wide")

# # -----------------------------
# # Sidebar Theme Toggle
# # -----------------------------
# theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

# if theme == "Dark":
#     st.markdown(
#         """
#         <style>
#             body { background-color: #0e1117; color: #fafafa; }
#             .block-container { background-color: #0e1117; color: #fafafa; }
#             div[data-testid="stMetric"] {
#                 background-color: #1a1d23;
#                 color: #fafafa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #fafafa;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
# else:  # Light mode
#     st.markdown(
#         """
#         <style>
#             .block-container { background-color: #ffffff; color: #000000; }
#             div[data-testid="stMetric"] {
#                 background-color: #f8f9fa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #000000;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # -----------------------------
# # Title
# # -----------------------------
# st.title("📊 Business KPI Dashboard")
# st.caption("Upload any file (CSV, XLSX) – Auto-handles & charts with AI forecasting")

# # -----------------------------
# # Sidebar Upload with Better Error Handling
# # -----------------------------
# uploaded_file = st.sidebar.file_uploader("📂 Upload File", type=['csv', 'xlsx'])

# if uploaded_file is not None:
#     file_ext = os.path.splitext(uploaded_file.name)[1].lower()
#     try:
#         if file_ext == '.csv':
#             # Try multiple encodings and strip whitespace from columns
#             for encoding in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
#                 try:
#                     df = pd.read_csv(uploaded_file, encoding=encoding)
#                     df.columns = df.columns.str.strip()
#                     st.success(f"✅ CSV loaded ({encoding}): {df.shape[0]} rows, {df.shape[1]} cols")
#                     break
#                 except (UnicodeDecodeError, pd.errors.ParserError):
#                     uploaded_file.seek(0)
#                     continue
#         elif file_ext == '.xlsx':
#             df = pd.read_excel(uploaded_file)
#             df.columns = df.columns.str.strip()
#             st.success(f"✅ XLSX loaded: {df.shape[0]} rows, {df.shape[1]} cols")
#         else:
#             st.warning("⚠️ Please upload CSV or XLSX file")
#             st.stop()
#     except Exception as e:
#         st.error(f"❌ Load error: {e}")
#         st.stop()
# else:
#     # Fallback to sample data
#     try:
#         df = pd.read_csv("../Day8/superstore_customer_enriched.csv", encoding='latin1')
#         df.columns = df.columns.str.strip()
#         st.info("📌 Using sample data (9,994 rows)")
#     except:
#         st.error("❌ No file uploaded and sample data not found. Please upload a CSV/XLSX file.")
#         st.stop()

# # -----------------------------
# # Debug: Show Available Columns
# # -----------------------------
# with st.expander("🔍 Debug: Available Columns", expanded=False):
#     st.write("**Detected columns:**")
#     st.write(list(df.columns))
#     st.write(f"**Total columns:** {len(df.columns)}")

# # -----------------------------
# # Auto-Clean with Better Column Detection
# # -----------------------------
# original_shape = df.shape

# # Clean column names (remove extra spaces, special characters)
# df.columns = df.columns.str.strip().str.replace('\s+', ' ', regex=True)

# # Date columns - try common date column names
# date_columns = ['Order Date', 'Date', 'OrderDate', 'order_date']
# date_col_found = None
# for date_col in date_columns:
#     if date_col in df.columns:
#         df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
#         date_col_found = date_col
#         st.info(f"📅 Parsed date column: {date_col}")
#         break

# # Numeric columns - handle common profit/sales columns
# numeric_mappings = {
#     'Profit': ['Profit', 'profit', 'PROFIT', 'Net Profit', 'net_profit'],
#     'Sales': ['Sales', 'sales', 'SALES', 'Revenue', 'revenue'],
#     'Quantity': ['Quantity', 'quantity', 'QTY', 'qty']
# }

# for standard_name, variations in numeric_mappings.items():
#     for var in variations:
#         if var in df.columns:
#             if standard_name not in df.columns or var == standard_name:
#                 df[standard_name] = pd.to_numeric(df[var], errors='coerce').fillna(0)
#                 if var != standard_name:
#                     st.info(f"🔄 Mapped '{var}' → '{standard_name}'")
#             break

# # Drop completely empty rows
# df = df.dropna(how='all')

# cleaned_info = f"🧹 Auto-cleaned: {df.shape[0]} rows × {df.shape[1]} cols"
# if original_shape != df.shape:
#     cleaned_info += f" (removed {original_shape[0] - df.shape[0]} empty rows)"
# st.success(cleaned_info)

# # Show preview
# st.dataframe(df.head(10), use_container_width=True)

# # -----------------------------
# # KPIs with Smart Fallbacks
# # -----------------------------
# st.markdown("### 📊 Key Performance Indicators")
# col1, col2, col3 = st.columns(3)

# # Check if required columns exist
# has_profit = 'Profit' in df.columns
# has_net_profit = 'Net Profit' in df.columns
# has_sales = 'Sales' in df.columns

# if has_profit:
#     gross = df['Profit'].sum().round(0)
#     net = df['Net Profit'].sum().round(0) if has_net_profit else gross
#     drag = (gross - net).round(0)
    
#     with col1: 
#         st.metric("💰 Gross Profit", f"${gross:,}")
#     with col2: 
#         st.metric("📈 Net Profit", f"${net:,}")
#     with col3: 
#         st.metric("📉 Returns Drag", f"${drag:,}")
# elif has_sales:
#     total_sales = df['Sales'].sum().round(0)
#     avg_sales = df['Sales'].mean().round(2)
#     max_sales = df['Sales'].max().round(0)
    
#     with col1: 
#         st.metric("💰 Total Sales", f"${total_sales:,}")
#     with col2: 
#         st.metric("📊 Average Sale", f"${avg_sales:,}")
#     with col3: 
#         st.metric("🏆 Max Sale", f"${max_sales:,}")
# else:
#     st.warning("⚠️ No 'Profit' or 'Sales' columns found. Please check your data.")
#     # Show summary of numeric columns instead
#     numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
#     if numeric_cols:
#         st.info(f"📊 Found numeric columns: {', '.join(numeric_cols[:5])}")
#         for i, col in enumerate(numeric_cols[:3]):
#             with [col1, col2, col3][i]:
#                 st.metric(f"📈 {col}", f"{df[col].sum():,.0f}")

# # -----------------------------
# # Filters with Smart Detection
# # -----------------------------
# segment_columns = ['Segment', 'segment', 'Category', 'category', 'Type', 'type']
# segment_col = None

# for col in segment_columns:
#     if col in df.columns:
#         segment_col = col
#         break

# if segment_col:
#     segment_options = ['All'] + sorted(df[segment_col].dropna().unique().tolist())
#     selected_segment = st.sidebar.selectbox(f"🎯 Filter by {segment_col}", segment_options)

#     if selected_segment == "All":
#         df_filtered = df
#     else:
#         df_filtered = df[df[segment_col] == selected_segment]
    
#     st.sidebar.info(f"📊 Filtered: {len(df_filtered):,} records")
# else:
#     df_filtered = df
#     st.sidebar.warning("⚠️ No segment column found")
#     segment_col = 'Segment'  # Default for display

# # -----------------------------
# # Tabs with Dynamic Column Detection
# # -----------------------------
# tab1, tab2, tab3, tab4 = st.tabs(["📊 Sales by Segment", "📆 Revenue Trends", "🌍 Profit Heatmap", "🔮 Forecast"])

# with tab1:
#     st.subheader(f"Sales Overview – {selected_segment if segment_col else 'All Data'}")

#     if segment_col and segment_col in df_filtered.columns:
#         # Determine metric column
#         if 'Net Profit' in df_filtered.columns:
#             metric_col = 'Net Profit'
#             title_suffix = 'Net Profit'
#         elif 'Profit' in df_filtered.columns:
#             metric_col = 'Profit'
#             title_suffix = 'Profit'
#         elif 'Sales' in df_filtered.columns:
#             metric_col = 'Sales'
#             title_suffix = 'Sales'
#         else:
#             numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
#             if numeric_cols:
#                 metric_col = numeric_cols[0]
#                 title_suffix = metric_col
#             else:
#                 st.warning("⚠️ No numeric columns found for charting")
#                 st.stop()

#         agg_data = df_filtered.groupby(segment_col)[metric_col].sum().reset_index()
        
#         fig1 = px.bar(
#             agg_data, 
#             x=segment_col, 
#             y=metric_col,
#             text=metric_col, 
#             color=segment_col,
#             color_discrete_sequence=px.colors.qualitative.Pastel
#         )
#         fig1.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
#         fig1.update_layout(
#             title=f"{title_suffix} by {segment_col}",
#             yaxis_title="Amount ($)",
#             showlegend=False
#         )
#         st.plotly_chart(fig1, use_container_width=True)
#     else:
#         st.warning(f"⚠️ '{segment_col}' column not found. Cannot generate segment chart.")

# with tab2:
#     st.subheader("Monthly Revenue Trend")

#     # Find date column
#     date_col = None
#     for col_name in ['Order Date', 'Date', 'OrderDate', 'order_date', 'date']:
#         if col_name in df_filtered.columns:
#             date_col = col_name
#             break

#     if date_col and 'Sales' in df_filtered.columns:
#         df_temp = df_filtered.copy()
#         df_temp['Month'] = pd.to_datetime(df_temp[date_col], errors='coerce').dt.to_period('M')
#         df_temp = df_temp.dropna(subset=['Month'])
        
#         if len(df_temp) > 0:
#             monthly = df_temp.groupby('Month')['Sales'].sum().reset_index()
#             monthly['Month'] = monthly['Month'].astype(str)
            
#             fig2 = px.line(
#                 monthly, 
#                 x='Month', 
#                 y='Sales', 
#                 markers=True,
#                 line_shape="spline", 
#                 color_discrete_sequence=["#6f42c1"]
#             )
#             fig2.update_layout(
#                 title="Monthly Sales Trend",
#                 yaxis_title="Sales ($)",
#                 xaxis_title="Month"
#             )
#             st.plotly_chart(fig2, use_container_width=True)
#         else:
#             st.warning("⚠️ No valid dates found in the date column.")
#     else:
#         missing = []
#         if not date_col:
#             missing.append("date column")
#         if 'Sales' not in df_filtered.columns:
#             missing.append("'Sales' column")
#         st.warning(f"⚠️ Missing {' and '.join(missing)} for trend analysis.")

# with tab3:
#     st.subheader("Profit Heatmap: Region vs Segment")

#     # Find index column (Region, Category, etc.)
#     index_options = ['Region', 'region', 'Category', 'category', 'State', 'state']
#     index_col = None
#     for opt in index_options:
#         if opt in df_filtered.columns:
#             index_col = opt
#             break

#     # Find value column
#     value_col = None
#     value_options = ['Net Profit', 'Profit', 'Sales']
#     for opt in value_options:
#         if opt in df_filtered.columns:
#             value_col = opt
#             break

#     if index_col and value_col and segment_col and segment_col in df_filtered.columns:
#         pivot_heat = df_filtered.pivot_table(
#             values=value_col,
#             index=index_col,
#             columns=segment_col,
#             aggfunc='sum',
#             fill_value=0
#         ).round(0)
        
#         fig3 = px.imshow(
#             pivot_heat,
#             text_auto=True,
#             aspect="auto",
#             color_continuous_scale="RdYlGn",
#             labels=dict(color=value_col)
#         )
#         fig3.update_layout(title=f"{value_col} Heatmap: {index_col} vs {segment_col}")
#         st.plotly_chart(fig3, use_container_width=True)
#     else:
#         missing_cols = []
#         if not index_col:
#             missing_cols.append("index column (Region/Category)")
#         if not value_col:
#             missing_cols.append("value column (Profit/Sales)")
#         if not segment_col or segment_col not in df_filtered.columns:
#             missing_cols.append("segment column")
        
#         st.warning(f"⚠️ Heatmap requires: {', '.join(missing_cols)}")

# with tab4:
#     st.subheader("🔮 Sales Forecasting – Next 6 Months")

#     # Find date and sales columns
#     date_col = None
#     for col_name in ['Order Date', 'Date', 'OrderDate', 'order_date', 'date']:
#         if col_name in df_filtered.columns:
#             date_col = col_name
#             break

#     sales_col = None
#     for col_name in ['Sales', 'sales', 'SALES', 'Revenue', 'revenue']:
#         if col_name in df_filtered.columns:
#             sales_col = col_name
#             break

#     if date_col and sales_col:
#         # Prep for Prophet
#         df_prophet = df_filtered[[date_col, sales_col]].copy()
#         df_prophet = df_prophet.dropna()
#         df_prophet = df_prophet.sort_values(date_col)
#         df_prophet = df_prophet.rename(columns={date_col: 'ds', sales_col: 'y'})

#         if len(df_prophet) > 10:
#             with st.spinner("🔮 Training forecast model..."):
#                 try:
#                     # Fit Prophet model
#                     m = Prophet(
#                         daily_seasonality=False,
#                         weekly_seasonality=True,
#                         yearly_seasonality=True
#                     )
#                     m.fit(df_prophet)

#                     # Forecast 6 months (180 days)
#                     future = m.make_future_dataframe(periods=180)
#                     forecast = m.predict(future)

#                     # Create custom Plotly chart
#                     fig4 = px.line(
#                         forecast, 
#                         x='ds', 
#                         y='yhat',
#                         labels={'ds': 'Date', 'yhat': 'Predicted Sales ($)'},
#                         title='Sales Forecast: Actual vs Predicted'
#                     )
                    
#                     # Add actual data points
#                     fig4.add_scatter(
#                         x=df_prophet['ds'], 
#                         y=df_prophet['y'], 
#                         mode='markers', 
#                         name='Actual Sales',
#                         marker=dict(color='#6f42c1', size=6)
#                     )
                    
#                     # Add confidence interval
#                     fig4.add_scatter(
#                         x=forecast['ds'], 
#                         y=forecast['yhat_upper'],
#                         fill=None, 
#                         mode='lines', 
#                         line_color='rgba(111, 66, 193, 0.2)',
#                         showlegend=False, 
#                         name='Upper Bound'
#                     )
#                     fig4.add_scatter(
#                         x=forecast['ds'], 
#                         y=forecast['yhat_lower'],
#                         fill='tonexty', 
#                         mode='lines', 
#                         line_color='rgba(111, 66, 193, 0.2)',
#                         showlegend=True, 
#                         name='Confidence Interval'
#                     )
                    
#                     fig4.update_layout(yaxis_title="Sales ($)", xaxis_title="Date")
#                     st.plotly_chart(fig4, use_container_width=True)

#                     # Show forecast metrics
#                     col_f1, col_f2, col_f3 = st.columns(3)
                    
#                     next_6mo = forecast['yhat'].tail(180).sum().round(0)
#                     current_6mo = df_prophet['y'].tail(180).sum().round(0) if len(df_prophet) > 180 else df_prophet['y'].sum()
#                     growth = ((next_6mo / current_6mo - 1) * 100) if current_6mo > 0 else 0
                    
#                     with col_f1:
#                         st.metric("📊 Predicted 6-Month Total", f"${next_6mo:,.0f}")
#                     with col_f2:
#                         st.metric("📈 Expected Growth", f"{growth:.1f}%", delta=f"{growth:.1f}%")
#                     with col_f3:
#                         next_month_avg = forecast['yhat'].tail(30).mean().round(0)
#                         st.metric("🎯 Next Month Avg/Day", f"${next_month_avg:,.0f}")
                    
#                     # Show forecast table
#                     with st.expander("📋 Detailed Forecast Data (Next 30 Days)", expanded=False):
#                         forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30)
#                         forecast_display.columns = ['Date', 'Predicted', 'Lower Bound', 'Upper Bound']
#                         forecast_display['Predicted'] = forecast_display['Predicted'].round(2)
#                         forecast_display['Lower Bound'] = forecast_display['Lower Bound'].round(2)
#                         forecast_display['Upper Bound'] = forecast_display['Upper Bound'].round(2)
#                         st.dataframe(forecast_display, use_container_width=True)
                
#                 except Exception as e:
#                     st.error(f"❌ Forecasting error: {e}")
#                     st.info("💡 Tip: Ensure you have enough historical data points (at least 2 weeks)")
#         else:
#             st.warning("⚠️ Need at least 10 rows with valid dates & sales for forecast.")
#             st.info(f"📊 Current data has {len(df_prophet)} valid rows")
#     else:
#         missing = []
#         if not date_col:
#             missing.append("date column")
#         if not sales_col:
#             missing.append("'Sales' column")
#         st.warning(f"⚠️ Forecasting needs {' and '.join(missing)}.")

# # -----------------------------
# # Preview & Export
# # -----------------------------
# st.markdown("---")
# st.markdown("### 💾 Data Export & Preview")

# with st.expander("👀 Full Cleaned Data Preview", expanded=False):
#     st.dataframe(df_filtered, use_container_width=True)

# csv_clean = df_filtered.to_csv(index=False).encode('utf-8')
# st.download_button(
#     label="💾 Download Cleaned CSV",
#     data=csv_clean,
#     file_name="cleaned_kpis.csv",
#     mime="text/csv"
# )

# # -----------------------------
# # Footer
# # -----------------------------
# st.markdown("---")
# st.caption("🚀 Modern Dashboard v4 – AI-ready insights with Prophet forecasting | Smart column detection enabled")

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import logging
# from prophet import Prophet

# # Suppress Prophet verbose output
# logging.getLogger('prophet').setLevel(logging.ERROR)
# logging.getLogger('cmdstanpy').setLevel(logging.ERROR)

# # -----------------------------
# # Page Config
# # -----------------------------
# st.set_page_config(page_title="🚀 Modern KPI Dashboard", layout="wide")

# # -----------------------------
# # Sidebar Theme Toggle
# # -----------------------------
# theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

# if theme == "Dark":
#     st.markdown(
#         """
#         <style>
#             body { background-color: #0e1117; color: #fafafa; }
#             .block-container { background-color: #0e1117; color: #fafafa; }
#             div[data-testid="stMetric"] {
#                 background-color: #1a1d23;
#                 color: #fafafa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #fafafa;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
# else:  # Light mode
#     st.markdown(
#         """
#         <style>
#             .block-container { background-color: #ffffff; color: #000000; }
#             div[data-testid="stMetric"] {
#                 background-color: #f8f9fa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #000000;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # -----------------------------
# # Title
# # -----------------------------
# st.title("📊 Business KPI Dashboard")
# st.caption("Upload any file (CSV, XLSX) – Auto-handles & charts with AI forecasting")

# # -----------------------------
# # Sidebar Upload with Better Error Handling
# # -----------------------------
# uploaded_file = st.sidebar.file_uploader("📂 Upload File", type=['csv', 'xlsx'])

# if uploaded_file is not None:
#     file_ext = os.path.splitext(uploaded_file.name)[1].lower()
#     try:
#         if file_ext == '.csv':
#             # Try multiple encodings and strip whitespace from columns
#             for encoding in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
#                 try:
#                     df = pd.read_csv(uploaded_file, encoding=encoding)
#                     df.columns = df.columns.str.strip()
#                     st.success(f"✅ CSV loaded ({encoding}): {df.shape[0]} rows, {df.shape[1]} cols")
#                     break
#                 except (UnicodeDecodeError, pd.errors.ParserError):
#                     uploaded_file.seek(0)
#                     continue
#         elif file_ext == '.xlsx':
#             df = pd.read_excel(uploaded_file)
#             df.columns = df.columns.str.strip()
#             st.success(f"✅ XLSX loaded: {df.shape[0]} rows, {df.shape[1]} cols")
#         else:
#             st.warning("⚠️ Please upload CSV or XLSX file")
#             st.stop()
#     except Exception as e:
#         st.error(f"❌ Load error: {e}")
#         st.stop()
# else:
#     # Fallback to sample data
#     try:
#         df = pd.read_csv("../Day8/superstore_customer_enriched.csv", encoding='latin1')
#         df.columns = df.columns.str.strip()
#         st.info("📌 Using sample data (9,994 rows)")
#     except:
#         st.error("❌ No file uploaded and sample data not found. Please upload a CSV/XLSX file.")
#         st.stop()

# # -----------------------------
# # Debug: Show Available Columns
# # -----------------------------
# with st.expander("🔍 Debug: Available Columns", expanded=False):
#     st.write("**Detected columns:**")
#     st.write(list(df.columns))
#     st.write(f"**Total columns:** {len(df.columns)}")

# # -----------------------------
# # Auto-Clean with Better Column Detection
# # -----------------------------
# original_shape = df.shape

# # Clean column names (remove extra spaces, special characters)
# df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)

# # Date columns - try common date column names
# date_columns = ['Order Date', 'Date', 'OrderDate', 'order_date']
# date_col_found = None
# for date_col in date_columns:
#     if date_col in df.columns:
#         df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
#         date_col_found = date_col
#         st.info(f"📅 Parsed date column: {date_col}")
#         break

# # Numeric columns - handle common profit/sales columns
# numeric_mappings = {
#     'Profit': ['Profit', 'profit', 'PROFIT', 'Net Profit', 'net_profit'],
#     'Sales': ['Sales', 'sales', 'SALES', 'Revenue', 'revenue'],
#     'Quantity': ['Quantity', 'quantity', 'QTY', 'qty']
# }

# for standard_name, variations in numeric_mappings.items():
#     for var in variations:
#         if var in df.columns:
#             if standard_name not in df.columns or var == standard_name:
#                 df[standard_name] = pd.to_numeric(df[var], errors='coerce').fillna(0)
#                 if var != standard_name:
#                     st.info(f"🔄 Mapped '{var}' → '{standard_name}'")
#             break

# # Drop completely empty rows
# df = df.dropna(how='all')

# cleaned_info = f"🧹 Auto-cleaned: {df.shape[0]} rows × {df.shape[1]} cols"
# if original_shape != df.shape:
#     cleaned_info += f" (removed {original_shape[0] - df.shape[0]} empty rows)"
# st.success(cleaned_info)

# # Show preview
# st.dataframe(df.head(10), use_container_width=True)

# # -----------------------------
# # KPIs with Smart Fallbacks
# # -----------------------------
# st.markdown("### 📊 Key Performance Indicators")
# col1, col2, col3 = st.columns(3)

# # Check if required columns exist
# has_profit = 'Profit' in df.columns
# has_net_profit = 'Net Profit' in df.columns
# has_sales = 'Sales' in df.columns

# if has_profit:
#     gross = df['Profit'].sum().round(0)
#     net = df['Net Profit'].sum().round(0) if has_net_profit else gross
#     drag = (gross - net).round(0)
    
#     with col1: 
#         st.metric("💰 Gross Profit", f"${gross:,}")
#     with col2: 
#         st.metric("📈 Net Profit", f"${net:,}")
#     with col3: 
#         st.metric("📉 Returns Drag", f"${drag:,}")
# elif has_sales:
#     total_sales = df['Sales'].sum().round(0)
#     avg_sales = df['Sales'].mean().round(2)
#     max_sales = df['Sales'].max().round(0)
    
#     with col1: 
#         st.metric("💰 Total Sales", f"${total_sales:,}")
#     with col2: 
#         st.metric("📊 Average Sale", f"${avg_sales:,}")
#     with col3: 
#         st.metric("🏆 Max Sale", f"${max_sales:,}")
# else:
#     st.warning("⚠️ No 'Profit' or 'Sales' columns found. Please check your data.")
#     # Show summary of numeric columns instead
#     numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
#     if numeric_cols:
#         st.info(f"📊 Found numeric columns: {', '.join(numeric_cols[:5])}")
#         for i, col in enumerate(numeric_cols[:3]):
#             with [col1, col2, col3][i]:
#                 st.metric(f"📈 {col}", f"{df[col].sum():,.0f}")

# # -----------------------------
# # Filters with Smart Detection
# # -----------------------------
# segment_columns = ['Segment', 'segment', 'Category', 'category', 'Type', 'type']
# segment_col = None

# for col in segment_columns:
#     if col in df.columns:
#         segment_col = col
#         break

# if segment_col:
#     segment_options = ['All'] + sorted(df[segment_col].dropna().unique().tolist())
#     selected_segment = st.sidebar.selectbox(f"🎯 Filter by {segment_col}", segment_options)

#     if selected_segment == "All":
#         df_filtered = df
#     else:
#         df_filtered = df[df[segment_col] == selected_segment]
    
#     st.sidebar.info(f"📊 Filtered: {len(df_filtered):,} records")
# else:
#     df_filtered = df
#     st.sidebar.warning("⚠️ No segment column found")
#     segment_col = 'Segment'  # Default for display

# # -----------------------------
# # Tabs with Dynamic Column Detection
# # -----------------------------
# tab1, tab2, tab3, tab4 = st.tabs(["📊 Sales by Segment", "📆 Revenue Trends", "🌍 Profit Heatmap", "🔮 Forecast"])

# with tab1:
#     st.subheader(f"Sales Overview – {selected_segment if segment_col else 'All Data'}")

#     if segment_col and segment_col in df_filtered.columns:
#         # Determine metric column
#         if 'Net Profit' in df_filtered.columns:
#             metric_col = 'Net Profit'
#             title_suffix = 'Net Profit'
#         elif 'Profit' in df_filtered.columns:
#             metric_col = 'Profit'
#             title_suffix = 'Profit'
#         elif 'Sales' in df_filtered.columns:
#             metric_col = 'Sales'
#             title_suffix = 'Sales'
#         else:
#             numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
#             if numeric_cols:
#                 metric_col = numeric_cols[0]
#                 title_suffix = metric_col
#             else:
#                 st.warning("⚠️ No numeric columns found for charting")
#                 st.stop()

#         agg_data = df_filtered.groupby(segment_col)[metric_col].sum().reset_index()
        
#         fig1 = px.bar(
#             agg_data, 
#             x=segment_col, 
#             y=metric_col,
#             text=metric_col, 
#             color=segment_col,
#             color_discrete_sequence=px.colors.qualitative.Pastel
#         )
#         fig1.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
#         fig1.update_layout(
#             title=f"{title_suffix} by {segment_col}",
#             yaxis_title="Amount ($)",
#             showlegend=False
#         )
#         st.plotly_chart(fig1, use_container_width=True)
#     else:
#         st.warning(f"⚠️ '{segment_col}' column not found. Cannot generate segment chart.")

# with tab2:
#     st.subheader("Monthly Revenue Trend")

#     # Find date column
#     date_col = None
#     for col_name in ['Order Date', 'Date', 'OrderDate', 'order_date', 'date']:
#         if col_name in df_filtered.columns:
#             date_col = col_name
#             break

#     if date_col and 'Sales' in df_filtered.columns:
#         df_temp = df_filtered.copy()
#         df_temp['Month'] = pd.to_datetime(df_temp[date_col], errors='coerce').dt.to_period('M')
#         df_temp = df_temp.dropna(subset=['Month'])
        
#         if len(df_temp) > 0:
#             monthly = df_temp.groupby('Month')['Sales'].sum().reset_index()
#             monthly['Month'] = monthly['Month'].astype(str)
            
#             fig2 = px.line(
#                 monthly, 
#                 x='Month', 
#                 y='Sales', 
#                 markers=True,
#                 line_shape="spline", 
#                 color_discrete_sequence=["#6f42c1"]
#             )
#             fig2.update_layout(
#                 title="Monthly Sales Trend",
#                 yaxis_title="Sales ($)",
#                 xaxis_title="Month"
#             )
#             st.plotly_chart(fig2, use_container_width=True)
#         else:
#             st.warning("⚠️ No valid dates found in the date column.")
#     else:
#         missing = []
#         if not date_col:
#             missing.append("date column")
#         if 'Sales' not in df_filtered.columns:
#             missing.append("'Sales' column")
#         st.warning(f"⚠️ Missing {' and '.join(missing)} for trend analysis.")

# with tab3:
#     st.subheader("Profit Heatmap: Region vs Segment")

#     # Find index column (Region, Category, etc.)
#     index_options = ['Region', 'region', 'Category', 'category', 'State', 'state']
#     index_col = None
#     for opt in index_options:
#         if opt in df_filtered.columns:
#             index_col = opt
#             break

#     # Find value column
#     value_col = None
#     value_options = ['Net Profit', 'Profit', 'Sales']
#     for opt in value_options:
#         if opt in df_filtered.columns:
#             value_col = opt
#             break

#     if index_col and value_col and segment_col and segment_col in df_filtered.columns:
#         pivot_heat = df_filtered.pivot_table(
#             values=value_col,
#             index=index_col,
#             columns=segment_col,
#             aggfunc='sum',
#             fill_value=0
#         ).round(0)
        
#         fig3 = px.imshow(
#             pivot_heat,
#             text_auto=True,
#             aspect="auto",
#             color_continuous_scale="RdYlGn",
#             labels=dict(color=value_col)
#         )
#         fig3.update_layout(title=f"{value_col} Heatmap: {index_col} vs {segment_col}")
#         st.plotly_chart(fig3, use_container_width=True)
#     else:
#         missing_cols = []
#         if not index_col:
#             missing_cols.append("index column (Region/Category)")
#         if not value_col:
#             missing_cols.append("value column (Profit/Sales)")
#         if not segment_col or segment_col not in df_filtered.columns:
#             missing_cols.append("segment column")
        
#         st.warning(f"⚠️ Heatmap requires: {', '.join(missing_cols)}")

# with tab4:
#     st.subheader("🔮 Sales Forecasting – Next 6 Months")

#     # Find date and sales columns
#     date_col = None
#     for col_name in ['Order Date', 'Date', 'OrderDate', 'order_date', 'date']:
#         if col_name in df_filtered.columns:
#             date_col = col_name
#             break

#     sales_col = None
#     for col_name in ['Sales', 'sales', 'SALES', 'Revenue', 'revenue']:
#         if col_name in df_filtered.columns:
#             sales_col = col_name
#             break

#     if date_col and sales_col:
#         # Prep for Prophet
#         df_prophet = df_filtered[[date_col, sales_col]].copy()
#         df_prophet = df_prophet.dropna()
#         df_prophet = df_prophet.sort_values(date_col)
#         df_prophet = df_prophet.rename(columns={date_col: 'ds', sales_col: 'y'})

#         if len(df_prophet) > 10:
#             with st.spinner("🔮 Training forecast model..."):
#                 try:
#                     # Fit Prophet model
#                     m = Prophet(
#                         daily_seasonality=False,
#                         weekly_seasonality=True,
#                         yearly_seasonality=True
#                     )
#                     m.fit(df_prophet)

#                     # Forecast 6 months (180 days)
#                     future = m.make_future_dataframe(periods=180)
#                     forecast = m.predict(future)

#                     # Create custom Plotly chart
#                     fig4 = px.line(
#                         forecast, 
#                         x='ds', 
#                         y='yhat',
#                         labels={'ds': 'Date', 'yhat': 'Predicted Sales ($)'},
#                         title='Sales Forecast: Actual vs Predicted'
#                     )
                    
#                     # Add actual data points
#                     fig4.add_scatter(
#                         x=df_prophet['ds'], 
#                         y=df_prophet['y'], 
#                         mode='markers', 
#                         name='Actual Sales',
#                         marker=dict(color='#6f42c1', size=6)
#                     )
                    
#                     # Add confidence interval
#                     fig4.add_scatter(
#                         x=forecast['ds'], 
#                         y=forecast['yhat_upper'],
#                         fill=None, 
#                         mode='lines', 
#                         line_color='rgba(111, 66, 193, 0.2)',
#                         showlegend=False, 
#                         name='Upper Bound'
#                     )
#                     fig4.add_scatter(
#                         x=forecast['ds'], 
#                         y=forecast['yhat_lower'],
#                         fill='tonexty', 
#                         mode='lines', 
#                         line_color='rgba(111, 66, 193, 0.2)',
#                         showlegend=True, 
#                         name='Confidence Interval'
#                     )
                    
#                     fig4.update_layout(yaxis_title="Sales ($)", xaxis_title="Date")
#                     st.plotly_chart(fig4, use_container_width=True)

#                     # Show forecast metrics
#                     col_f1, col_f2, col_f3 = st.columns(3)
                    
#                     next_6mo = forecast['yhat'].tail(180).sum().round(0)
#                     current_6mo = df_prophet['y'].tail(180).sum().round(0) if len(df_prophet) > 180 else df_prophet['y'].sum()
#                     growth = ((next_6mo / current_6mo - 1) * 100) if current_6mo > 0 else 0
                    
#                     with col_f1:
#                         st.metric("📊 Predicted 6-Month Total", f"${next_6mo:,.0f}")
#                     with col_f2:
#                         st.metric("📈 Expected Growth", f"{growth:.1f}%", delta=f"{growth:.1f}%")
#                     with col_f3:
#                         next_month_avg = forecast['yhat'].tail(30).mean().round(0)
#                         st.metric("🎯 Next Month Avg/Day", f"${next_month_avg:,.0f}")
                    
#                     # Show forecast table
#                     with st.expander("📋 Detailed Forecast Data (Next 30 Days)", expanded=False):
#                         forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30)
#                         forecast_display.columns = ['Date', 'Predicted', 'Lower Bound', 'Upper Bound']
#                         forecast_display['Predicted'] = forecast_display['Predicted'].round(2)
#                         forecast_display['Lower Bound'] = forecast_display['Lower Bound'].round(2)
#                         forecast_display['Upper Bound'] = forecast_display['Upper Bound'].round(2)
#                         st.dataframe(forecast_display, use_container_width=True)
                
#                 except Exception as e:
#                     st.error(f"❌ Forecasting error: {e}")
#                     st.info("💡 Tip: Ensure you have enough historical data points (at least 2 weeks)")
#         else:
#             st.warning("⚠️ Need at least 10 rows with valid dates & sales for forecast.")
#             st.info(f"📊 Current data has {len(df_prophet)} valid rows")
#     else:
#         missing = []
#         if not date_col:
#             missing.append("date column")
#         if not sales_col:
#             missing.append("'Sales' column")
#         st.warning(f"⚠️ Forecasting needs {' and '.join(missing)}.")

# # -----------------------------
# # Preview & Export
# # -----------------------------
# st.markdown("---")
# st.markdown("### 💾 Data Export & Preview")

# with st.expander("👀 Full Cleaned Data Preview", expanded=False):
#     st.dataframe(df_filtered, use_container_width=True)

# csv_clean = df_filtered.to_csv(index=False).encode('utf-8')
# st.download_button(
#     label="💾 Download Cleaned CSV",
#     data=csv_clean,
#     file_name="cleaned_kpis.csv",
#     mime="text/csv"
# )

# # -----------------------------
# # Footer
# # -----------------------------
# st.markdown("---")
# st.caption("🚀 Modern Dashboard v4 – AI-ready insights with Prophet forecasting | Smart column detection enabled")

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import logging
# from prophet import Prophet

# # Suppress Prophet verbose output
# logging.getLogger('prophet').setLevel(logging.ERROR)
# logging.getLogger('cmdstanpy').setLevel(logging.ERROR)

# # -----------------------------
# # Page Config
# # -----------------------------
# st.set_page_config(page_title="🚀 Modern KPI Dashboard", layout="wide")

# # -----------------------------
# # Sidebar Theme Toggle
# # -----------------------------
# theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

# if theme == "Dark":
#     st.markdown(
#         """
#         <style>
#             body { background-color: #0e1117; color: #fafafa; }
#             .block-container { background-color: #0e1117; color: #fafafa; }
#             div[data-testid="stMetric"] {
#                 background-color: #1a1d23;
#                 color: #fafafa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #fafafa;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
# else:
#     st.markdown(
#         """
#         <style>
#             .block-container { background-color: #ffffff; color: #000000; }
#             div[data-testid="stMetric"] {
#                 background-color: #f8f9fa;
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
#             }
#             h1, h2, h3, h4, h5, h6 {
#                 color: #000000;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # -----------------------------
# # Title
# # -----------------------------
# st.title("📊 Business KPI Dashboard")
# st.caption("Upload any file (CSV, XLSX) – Auto-handles, analyzes & forecasts intelligently")

# # -----------------------------
# # Sidebar Upload
# # -----------------------------
# uploaded_file = st.sidebar.file_uploader("📂 Upload File", type=['csv', 'xlsx'])

# if uploaded_file is not None:
#     file_ext = os.path.splitext(uploaded_file.name)[1].lower()
#     try:
#         if file_ext == '.csv':
#             for encoding in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
#                 try:
#                     df = pd.read_csv(uploaded_file, encoding=encoding)
#                     df.columns = df.columns.str.strip()
#                     st.success(f"✅ CSV loaded ({encoding}): {df.shape[0]} rows, {df.shape[1]} cols")
#                     break
#                 except (UnicodeDecodeError, pd.errors.ParserError):
#                     uploaded_file.seek(0)
#                     continue
#         elif file_ext == '.xlsx':
#             df = pd.read_excel(uploaded_file)
#             df.columns = df.columns.str.strip()
#             st.success(f"✅ XLSX loaded: {df.shape[0]} rows, {df.shape[1]} cols")
#         else:
#             st.warning("⚠️ Please upload CSV or XLSX file")
#             st.stop()
#     except Exception as e:
#         st.error(f"❌ Load error: {e}")
#         st.stop()
# else:
#     try:
#         df = pd.read_csv("../Day8/superstore_customer_enriched.csv", encoding='latin1')
#         df.columns = df.columns.str.strip()
#         st.info("📌 Using sample data (9,994 rows)")
#     except:
#         st.error("❌ No file uploaded and sample data not found. Please upload a CSV/XLSX file.")
#         st.stop()

# # -----------------------------
# # Clean Columns
# # -----------------------------
# df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
# df = df.dropna(how='all')

# # Detect date column
# date_col = None
# for col in ['Order Date', 'Date', 'OrderDate', 'order_date']:
#     if col in df.columns:
#         df[col] = pd.to_datetime(df[col], errors='coerce')
#         date_col = col
#         st.info(f"📅 Parsed date column: {col}")
#         break

# # Detect numeric columns
# numeric_mappings = {
#     'Profit': ['Profit', 'profit', 'Net Profit', 'net_profit'],
#     'Sales': ['Sales', 'sales', 'Revenue', 'revenue'],
#     'Quantity': ['Quantity', 'quantity', 'QTY', 'qty']
# }
# for std, variations in numeric_mappings.items():
#     for var in variations:
#         if var in df.columns:
#             df[std] = pd.to_numeric(df[var], errors='coerce').fillna(0)
#             break

# # Detect segment
# segment_col = next((c for c in ['Segment', 'segment', 'Category', 'category', 'Type', 'type'] if c in df.columns), None)
# segment_options = ['All'] + sorted(df[segment_col].dropna().unique().tolist()) if segment_col else ['All']
# selected_segment = st.sidebar.selectbox("🎯 Filter by Segment", segment_options)

# df_filtered = df if selected_segment == "All" or not segment_col else df[df[segment_col] == selected_segment]

# # -----------------------------
# # KPIs
# # -----------------------------
# st.markdown("### 📈 Key Metrics Overview")
# col1, col2, col3 = st.columns(3)
# if 'Profit' in df.columns and 'Sales' in df.columns:
#     total_sales = df_filtered['Sales'].sum()
#     total_profit = df_filtered['Profit'].sum()
#     profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
#     with col1: st.metric("💰 Total Sales", f"${total_sales:,.0f}")
#     with col2: st.metric("📈 Total Profit", f"${total_profit:,.0f}")
#     with col3: st.metric("🏦 Profit Margin", f"{profit_margin:.2f}%")

# # -----------------------------
# # Tabs
# # -----------------------------
# tab1, tab2, tab3, tab4 = st.tabs(["📊 Sales by Segment", "📆 Revenue Trends", "🌍 Profit Heatmap", "🔮 Forecast"])

# # -----------------------------
# # TAB 1 – Sales by Segment
# # -----------------------------
# with tab1:
#     st.subheader("📊 Sales Overview by Segment")
#     if segment_col and 'Sales' in df.columns:
#         seg_data = df.groupby(segment_col)['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
#         fig1 = px.bar(seg_data, x=segment_col, y='Sales', text='Sales',
#                       color=segment_col, color_discrete_sequence=px.colors.qualitative.Pastel)
#         fig1.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
#         fig1.update_layout(title="Total Sales by Segment", yaxis_title="Sales ($)", showlegend=False)
#         st.plotly_chart(fig1, use_container_width=True)
#     else:
#         st.warning("⚠️ Segment or Sales column missing.")

# # -----------------------------
# # TAB 2 – Revenue Trends
# # -----------------------------
# with tab2:
#     st.subheader("📆 Monthly Revenue Trend")
#     if date_col and 'Sales' in df.columns:
#         df['Month'] = pd.to_datetime(df[date_col], errors='coerce').dt.to_period('M')
#         monthly = df.groupby('Month')['Sales'].sum().reset_index()
#         monthly['Month'] = monthly['Month'].astype(str)
#         fig2 = px.line(monthly, x='Month', y='Sales', markers=True, line_shape="spline", color_discrete_sequence=["#6f42c1"])
#         fig2.update_layout(title="Monthly Sales Trend", xaxis_title="Month", yaxis_title="Sales ($)")
#         st.plotly_chart(fig2, use_container_width=True)
#     else:
#         st.warning("⚠️ Missing date or sales columns.")

# # -----------------------------
# # TAB 3 – Profit Heatmap
# # -----------------------------
# with tab3:
#     st.subheader("🌍 Profit Heatmap: Region vs Segment")
#     index_col = next((c for c in ['Region', 'region', 'State', 'state'] if c in df.columns), None)
#     if index_col and segment_col and 'Profit' in df.columns:
#         pivot = df.pivot_table(values='Profit', index=index_col, columns=segment_col, aggfunc='sum', fill_value=0)
#         fig3 = px.imshow(pivot, text_auto=True, aspect="auto", color_continuous_scale="RdYlGn", labels=dict(color="Profit ($)"))
#         fig3.update_layout(title=f"Profit Heatmap: {index_col} vs {segment_col}")
#         st.plotly_chart(fig3, use_container_width=True)
#     else:
#         st.warning("⚠️ Need Region/State, Segment, and Profit columns for heatmap.")

# # -----------------------------
# # TAB 4 – Forecast (Fixed + Multi-Segment)
# # -----------------------------
# with tab4:
#     st.subheader("🔮 AI Forecast – Next 6 Months")

#     if date_col and 'Sales' in df.columns:
#         # ---- Train Prophet on global daily data ----
#         df_all = df[[date_col, 'Sales']].dropna()
#         df_all = df_all.rename(columns={date_col: 'ds', 'Sales': 'y'})
#         df_all = df_all.groupby('ds')['y'].sum().reset_index()

#         if len(df_all) > 10:
#             m = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=True)
#             m.fit(df_all)
#             future = m.make_future_dataframe(periods=180)
#             forecast = m.predict(future)

#             # ---- Base global forecast ----
#             fig4 = px.line(forecast, x='ds', y='yhat', title="Global Sales Forecast", labels={'ds': 'Date', 'yhat': 'Predicted Sales ($)'})
#             fig4.add_scatter(x=df_all['ds'], y=df_all['y'], mode='markers', name='Actual Sales', marker=dict(color='#6f42c1', size=6))

#             # ---- Segment scaling ----
#             if segment_col:
#                 segment_weights = (df.groupby(segment_col)['Sales'].sum() / df['Sales'].sum()).to_dict()
#                 for seg, w in segment_weights.items():
#                     seg_forecast = forecast.copy()
#                     seg_forecast['yhat'] = seg_forecast['yhat'] * w
#                     fig4.add_scatter(x=seg_forecast['ds'], y=seg_forecast['yhat'], mode='lines', name=f"{seg} (scaled)", line=dict(dash='dot'))

#             st.plotly_chart(fig4, use_container_width=True)

#             # ---- Segment or All selection display ----
#             if selected_segment != "All" and segment_col:
#                 seg_ratio = (df[df[segment_col] == selected_segment]['Sales'].sum() / df['Sales'].sum())
#             else:
#                 seg_ratio = 1.0

#             forecast_scaled = forecast.copy()
#             forecast_scaled['yhat'] *= seg_ratio
#             forecast_scaled['yhat_lower'] *= seg_ratio
#             forecast_scaled['yhat_upper'] *= seg_ratio

#             # ---- Forecast metrics ----
#             next_6mo = forecast_scaled['yhat'].tail(180).sum().round(0)
#             current_6mo = df_all['y'].tail(180).sum() * seg_ratio
#             growth = ((next_6mo / current_6mo - 1) * 100) if current_6mo > 0 else 0
#             next_month_avg = forecast_scaled['yhat'].tail(30).mean().round(0)

#             col_f1, col_f2, col_f3 = st.columns(3)
#             with col_f1: st.metric("📊 Predicted 6-Month Total", f"${next_6mo:,.0f}")
#             with col_f2: st.metric("📈 Expected Growth", f"{growth:.1f}%", delta=f"{growth:.1f}%")
#             with col_f3: st.metric("🎯 Next Month Avg/Day", f"${next_month_avg:,.0f}")

#             with st.expander("📋 Detailed Forecast (Next 30 Days)", expanded=False):
#                 forecast_display = forecast_scaled[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30)
#                 forecast_display.columns = ['Date', 'Predicted', 'Lower Bound', 'Upper Bound']
#                 forecast_display = forecast_display.round(2)
#                 st.dataframe(forecast_display, use_container_width=True)
#         else:
#             st.warning("⚠️ Need at least 10 valid daily records for Prophet.")
#     else:
#         st.warning("⚠️ Forecasting requires both Date and Sales columns.")

# # -----------------------------
# # Footer
# # -----------------------------
# st.markdown("---")
# st.caption("🚀 Business Dashboard v6 – Prophet-powered AI forecasts with segment-coherent scaling")


import streamlit as st
import pandas as pd
import plotly.express as px
import os
import logging
from prophet import Prophet

# -----------------------------
# Setup
# -----------------------------
st.set_page_config(page_title="🚀 Modern KPI Dashboard", layout="wide")
logging.getLogger('prophet').setLevel(logging.ERROR)
logging.getLogger('cmdstanpy').setLevel(logging.ERROR)

# -----------------------------
# Sidebar + Theme
# -----------------------------
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
            body { background-color: #0e1117; color: #fafafa; }
            .block-container { background-color: #0e1117; color: #fafafa; }
            div[data-testid="stMetric"] {
                background-color: #1a1d23;
                color: #fafafa;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
            }
            h1, h2, h3, h4, h5, h6 {
                color: #fafafa;
                font-family: 'Segoe UI', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .block-container { background-color: #ffffff; color: #000000; }
            div[data-testid="stMetric"] {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            }
            h1, h2, h3, h4, h5, h6 {
                color: #000000;
                font-family: 'Segoe UI', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("📊 Business KPI Dashboard")
st.caption("Upload any file (CSV, XLSX) – Auto-handles & charts with AI forecasting")

# -----------------------------
# Load Dataset
# -----------------------------
uploaded_file = st.sidebar.file_uploader("📂 Upload File", type=['csv', 'xlsx'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='latin1')
    st.success(f"✅ Loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")
else:
    df = pd.read_csv("../Day8/superstore_customer_enriched.csv", encoding='latin1')
    st.info("📌 Using your uploaded dataset")

df.columns = df.columns.str.strip()

# -----------------------------
# Detect Key Columns
# -----------------------------
date_col = "Order Date" if "Order Date" in df.columns else "Date"
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

segment_col = "Segment"
sales_col = "Sales"

# -----------------------------
# Sidebar Filter
# -----------------------------
segments = ["All"] + sorted(df[segment_col].dropna().unique().tolist())
selected_segment = st.sidebar.selectbox("🎯 Filter by Segment", segments)
df_filtered = df if selected_segment == "All" else df[df[segment_col] == selected_segment]

# -----------------------------
# KPI Summary
# -----------------------------
st.markdown("### 📊 Key Performance Indicators")
col1, col2, col3 = st.columns(3)

if 'Profit' in df_filtered.columns:
    gross = df_filtered['Profit'].sum()
    if 'Net Profit' in df_filtered.columns:
        net = df_filtered['Net Profit'].sum()
        drag = gross - net
    else:
        net = gross
        drag = 0
    col1.metric("💰 Gross Profit", f"${gross:,.0f}")
    col2.metric("📈 Net Profit", f"${net:,.0f}")
    col3.metric("📉 Returns Drag", f"${drag:,.0f}")
else:
    total_sales = df_filtered['Sales'].sum()
    avg_sales = df_filtered.groupby(date_col)['Sales'].sum().mean()
    max_sales = df_filtered['Sales'].max()
    col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
    col2.metric("📊 Avg Daily Sales", f"${avg_sales:,.0f}")
    col3.metric("🏆 Max Sale", f"${max_sales:,.0f}")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Sales by Segment",
    "📆 Revenue Trends",
    "🌍 Profit Heatmap",
    "🔮 Forecast"
])

# -----------------------------
# Tab 1 – Sales by Segment
# -----------------------------
with tab1:
    st.subheader("Sales by Segment")
    segment_sales = df.groupby(segment_col)['Sales'].sum().reset_index()
    fig1 = px.bar(segment_sales, x=segment_col, y='Sales', text='Sales', color=segment_col)
    fig1.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig1.update_layout(title="Sales by Segment", yaxis_title="Sales ($)")
    st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Tab 2 – Revenue Trend
# -----------------------------
with tab2:
    st.subheader("Monthly Revenue Trend")
    monthly = (
        df.groupby(pd.Grouper(key=date_col, freq='M'))['Sales']
        .sum().reset_index()
    )
    fig2 = px.line(monthly, x=date_col, y='Sales', markers=True)
    fig2.update_layout(title="Monthly Sales", yaxis_title="Sales ($)")
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Tab 3 – Profit Heatmap
# -----------------------------
with tab3:
    st.subheader("Profit Heatmap – Region vs Segment")
    region_col = "Region" if "Region" in df.columns else None
    if region_col and "Profit" in df.columns:
        heatmap_data = df.pivot_table(values='Profit', index=region_col, columns=segment_col, aggfunc='sum', fill_value=0)
        fig3 = px.imshow(heatmap_data, text_auto=True, aspect="auto", color_continuous_scale="RdYlGn")
        fig3.update_layout(title="Profit by Region and Segment")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("⚠️ 'Region' or 'Profit' column not found for heatmap.")

# -----------------------------
# Tab 4 – Forecast (Fixed)
# -----------------------------
with tab4:
    st.subheader("🔮 Prophet Forecast – Next 6 Months")

    def make_forecast(df_seg):
        df_prophet = df_seg.groupby(date_col)['Sales'].sum().reset_index()
        df_prophet = df_prophet.rename(columns={date_col: 'ds', 'Sales': 'y'})
        m = Prophet(weekly_seasonality=True, yearly_seasonality=True)
        m.fit(df_prophet)
        future = m.make_future_dataframe(periods=180)
        forecast = m.predict(future)
        return forecast, df_prophet

    if selected_segment != "All":
        forecast, df_prophet = make_forecast(df_filtered)

        total_forecast_6m = forecast['yhat'].tail(180).sum()
        total_hist_6m = df_prophet['y'].tail(180).sum()
        growth = (total_forecast_6m / total_hist_6m - 1) * 100 if total_hist_6m > 0 else 0
        avg_next_month = forecast['yhat'].tail(30).mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Total Forecast (6M)", f"${total_forecast_6m:,.0f}")
        col2.metric("📈 Growth vs Last 6M", f"{growth:.1f}%")
        col3.metric("🎯 Avg Daily Next Month", f"${avg_next_month:,.0f}")

        fig = px.line(forecast, x='ds', y='yhat', title=f"Forecast – {selected_segment}")
        fig.add_scatter(x=df_prophet['ds'], y=df_prophet['y'], name='Actual', mode='markers')
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("🧠 Generating per-segment forecasts...")
        forecasts = {}
        totals = []
        for seg in sorted(df[segment_col].dropna().unique()):
            df_seg = df[df[segment_col] == seg]
            forecast, _ = make_forecast(df_seg)
            forecasts[seg] = forecast
            totals.append((seg, forecast['yhat'].tail(180).sum()))

        breakdown = pd.DataFrame(totals, columns=['Segment', 'Predicted 6M Total ($)'])
        total_all = breakdown['Predicted 6M Total ($)'].sum()
        breakdown['Share (%)'] = breakdown['Predicted 6M Total ($)'] / total_all * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Total Forecast (6M)", f"${total_all:,.0f}")
        col2.metric("📈 Growth vs Last 6M", "—")
        col3.metric("🎯 Avg Daily Next Month", "—")

        st.dataframe(breakdown, use_container_width=True)

        fig_all = px.line(title="Forecast by Segment")
        for seg, fc in forecasts.items():
            fig_all.add_scatter(x=fc['ds'], y=fc['yhat'], mode='lines', name=seg)
        st.plotly_chart(fig_all, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("🚀 Modern Dashboard v6 | Prophet Forecasts per Segment | Consistent Totals + Full Tabs Restored")

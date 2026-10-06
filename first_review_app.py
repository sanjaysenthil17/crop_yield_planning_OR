import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import re

st.set_page_config(page_title="Operations Research: Crop Planning", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for bigger and more beautiful layout (Dark/Light mode compatible) ---
st.markdown("""
<style>
    /* Using Streamlit's native theme colors implicitly by not forcing color tags, except where needed */
    .main-title { font-size: 3.5rem !important; font-weight: 800; text-align: center; margin-bottom: 0;}
    .sub-title { font-size: 1.5rem !important; text-align: center; margin-top: 0; padding-bottom: 2rem; opacity: 0.8;}
    .section-header { font-size: 2.2rem !important; font-weight: bold; border-bottom: 2px solid gray; padding-bottom: 0.5rem; margin-top: 2rem;}
    
    /* Make the highlight box adapt nicely */
    .highlight-box { 
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        border-left: 5px solid #3B82F6; 
        margin: 1rem 0; 
        background-color: rgba(59, 130, 246, 0.1); /* Transparent blue for dark/light mode */
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🌾 Optimal Agricultural Crop Planning</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Operations Research: Linear & Goal Programming (First Review)</p>', unsafe_allow_html=True)
st.markdown("---")

# Beautiful Navigation Menu using streamlit-option-menu
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    nav = option_menu(
        menu_title=None,
        options=[
            "1. Intro & Objectives",
            "2. Literature Review",
            "3. Dataset & EDA",
            "4. Methodology Flow",
            "5. Linear Programming",
            "6. Goal Programming",
            "7. Final Dashboard",
            "8. Team Contribution"
        ],
        icons=[
            "house", "book", "bar-chart-line", "diagram-3", 
            "graph-up", "bullseye", "laptop", "people"
        ],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#3B82F6", "font-size": "1.2rem"}, 
            "nav-link": {"font-size": "1.1rem", "text-align": "left", "margin":"5px", "--hover-color": "rgba(59, 130, 246, 0.2)"},
            "nav-link-selected": {"background-color": "#3B82F6", "color": "white", "icon-color": "white"},
        }
    )

# --- 1. Introduction & Objectives ---
if nav == "1. Intro & Objectives":
    st.markdown('<p class="section-header">Problem Statement</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="highlight-box">
    <b>"Given historical crop yields, resource requirements (fertilizer, pesticide, water), and strict land availability, how can we mathematically allocate available land among selected crops to maximize expected production while satisfying all resource limitations?"</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Primary Objectives")
        st.info("""
        1. **Data-Driven Insights:** Analyze 23 years of Indian agricultural data to identify high-yield crops.
        2. **Resource Optimization:** Maximize total crop production using **Linear Programming (LP)**.
        3. **Balanced Decision Making:** Use **Goal Programming (GP)** to balance multiple conflicting goals, such as maximizing production while minimizing chemical (fertilizer/pesticide) usage.
        """)
    with col2:
        st.subheader("💡 Why is this important?")
        st.success("""
        - Farmers often rely on intuition, leading to over-utilization or under-utilization of land.
        - Environmental constraints demand stricter limits on fertilizers and pesticides.
        - Operations Research provides a mathematical guarantee of the *optimal* farming strategy.
        """)

# --- 2. Literature Review ---
elif nav == "2. Literature Review":
    st.markdown('<p class="section-header">Literature Review</p>', unsafe_allow_html=True)
    st.write("We studied several papers applying Operations Research to agriculture to guide our project:")
    
    st.info("**1. Optimization of Crop Planning using Linear Programming (Sharma et al.)**  \n*Key Takeaway:* LP is highly effective in maximizing monetary profit or pure yield by allocating land based on constraints like water and labor.")
    st.info("**2. Multicriteria Decision Making in Agriculture using Goal Programming (Romero & Rehman)**  \n*Key Takeaway:* Farmers rarely have a single objective. GP is necessary when trying to hit a production quota while also minimizing environmental impact (e.g., nitrogen runoff).")
    st.info("**3. Yield Prediction and Resource Allocation (Indian Context)**  \n*Key Takeaway:* Regional variations (State, Season) heavily impact yield. It is critical to calculate parameters (expected yield, fertilizer per hectare) specific to the state and season being optimized.")

# --- 3. Dataset & Advanced EDA ---
elif nav == "3. Dataset & EDA":
    st.markdown('<p class="section-header">Dataset & Interactive Exploratory Data Analysis</p>', unsafe_allow_html=True)
    
    try:
        df = pd.read_csv("crop_yield.csv")
        st.success("✅ Real Dataset Loaded Successfully! (Agricultural Crop Yield in Indian States 1997–2020)")
        
        st.subheader("Data Snapshot")
        st.dataframe(df.head(10), use_container_width=True)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Records", f"{len(df):,}")
        c2.metric("Features (Columns)", df.shape[1])
        c3.metric("States Covered", df['State'].nunique())
        c4.metric("Unique Crops", df['Crop'].nunique())
        
        st.markdown("### 📊 Interactive Visualizations")
        
        # Filter for top 10 crops to make graphs readable
        top_crops = df['Crop'].value_counts().head(10).index
        df_top = df[df['Crop'].isin(top_crops)]
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            prod_by_crop = df_top.groupby('Crop')['Production'].sum().reset_index()
            fig1 = px.bar(prod_by_crop, x='Crop', y='Production', title='Total Historical Production (Top 10 Crops)', color='Crop')
            st.plotly_chart(fig1, use_container_width=True)
            
            yield_by_state = df.groupby('State')['Yield'].mean().reset_index().sort_values('Yield', ascending=False).head(10)
            fig3 = px.bar(yield_by_state, x='State', y='Yield', title='Top 10 States by Average Yield', color='State')
            st.plotly_chart(fig3, use_container_width=True)
            
        with col_chart2:
            fig2 = px.pie(df_top, names='Season', title='Crop Distribution by Season')
            st.plotly_chart(fig2, use_container_width=True)
            
            # Scatter plot taking a sample for performance
            fig4 = px.scatter(df_top.sample(2000, random_state=42), x='Annual_Rainfall', y='Yield', color='Crop', title='Rainfall vs. Yield (Sampled)')
            st.plotly_chart(fig4, use_container_width=True)
            
    except FileNotFoundError:
        st.error("Dataset 'crop_yield.csv' not found. Please ensure it is in the same directory.")

# --- 4. Methodology Flow ---
elif nav == "4. Methodology Flow":
    st.markdown('<p class="section-header">Project Methodology</p>', unsafe_allow_html=True)
    st.write("Our project follows a structured data-to-decision pipeline.")
    
    # Fixed Mermaid syntax for Dark Mode visibility
    st.markdown("""
    ```mermaid
    flowchart TD
        A[Dataset Collection & Cleaning] --> B[Exploratory Data Analysis]
        B --> C[Parameter Calculation: Average Yield, Fertilizer/ha, Pesticide/ha]
        C --> D[Define Decision Variables]
        
        D --> E{Choose Optimization Model}
        E --> F[Linear Programming Formulation]
        E --> G[Goal Programming Formulation]
        
        F --> H[Maximize Total Production]
        G --> I[Minimize Goal Deviations]
        
        H --> J[Compare Results in Dashboard]
        I --> J
        
        J --> K[Final Optimal Land Allocation Recommendation]
        
        %% Colors optimized for dark and light modes with explicit high-contrast text %%
        style A fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:#ffffff
        style B fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:#ffffff
        style C fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:#ffffff
        style D fill:#1e293b,stroke:#0f172a,stroke-width:2px,color:#ffffff
        style E fill:#4b5563,stroke:#374151,stroke-width:2px,color:#ffffff
        style F fill:#6366f1,stroke:#4338ca,stroke-width:2px,color:#ffffff
        style G fill:#6366f1,stroke:#4338ca,stroke-width:2px,color:#ffffff
        style H fill:#10b981,stroke:#047857,stroke-width:2px,color:#ffffff
        style I fill:#10b981,stroke:#047857,stroke-width:2px,color:#ffffff
        style J fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#ffffff
        style K fill:#22c55e,stroke:#15803d,stroke-width:2px,color:#ffffff
    ```
    """)
    st.info("📌 **First Review Focus:** Steps A, B, C, and D are complete. The mathematical formulations (F, G) are designed. Implementations (H, I, J, K) are planned for the Final Review.")

# --- 5. Linear Programming (LP) ---
elif nav == "5. Linear Programming":
    st.markdown('<p class="section-header">Linear Programming Approach (Pure Maximization)</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("""
        ### Mathematical Formulation
        **Decision Variables:** Let **$x_i$** be the land (in hectares) allocated to crop $i$.
        
        **Objective Function:** Maximize the total production output.
        - Maximize: **$Z = \sum (Yield_i \cdot x_i)$**
        
        **Subject to strict constraints:**
        1. **Land:** $\sum x_i \leq Available\_Land$
        2. **Fertilizer:** $\sum (Fertilizer\_per\_ha_i \cdot x_i) \leq Max\_Fertilizer$
        3. **Pesticide:** $\sum (Pesticide\_per\_ha_i \cdot x_i) \leq Max\_Pesticide$
        4. **Non-negativity:** $x_i \geq 0$
        """)
        
    with col2:
        st.markdown("### Conceptual LP Graph")
        st.write("The algorithm finds the optimal point at the intersection of our strict constraints.")
        # Dummy LP feasible region graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0, 10, 0], y=[10, 0, 0], fill='toself', name='Feasible Region', fillcolor='rgba(59, 130, 246, 0.3)'))
        fig.update_layout(title="Feasible Region (Mock)", xaxis_title="Crop 1 (ha)", yaxis_title="Crop 2 (ha)")
        st.plotly_chart(fig, use_container_width=True)

# --- 6. Goal Programming (GP) ---
elif nav == "6. Goal Programming":
    st.markdown('<p class="section-header">Goal Programming Approach (Balanced Multi-Criteria)</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("""
        ### Why GP?
        LP pushes everything to the extreme to maximize production, which might drain the entire fertilizer budget on one high-yield crop. GP allows us to balance multiple targets.
        
        ### Mathematical Formulation
        **Deviation Variables:** 
        - $d_i^+$ : Overachievement of a goal.
        - $d_i^-$ : Underachievement of a goal.
        
        **Goals:**
        - **Goal 1 (Production Target $T_p$):** $\sum (Yield_i \cdot x_i) + d_1^- - d_1^+ = T_p$
        - **Goal 2 (Fertilizer Limit $T_f$):** $\sum (Fertilizer_i \cdot x_i) + d_2^- - d_2^+ = T_f$
        
        **Objective Function:** Minimize the weighted sum of unwanted deviations.
        - Minimize: **$Z = W_1 \cdot d_1^- + W_2 \cdot d_2^+$**
        *(We want to minimize falling short of production, and minimize going over our chemical limits).*
        """)
        
    with col2:
        st.markdown("### GP vs LP Expected Behavior")
        st.write("GP spreads the risk and resources much more evenly across crops to hit multiple targets.")
        # Mock GP vs LP radar chart
        categories = ['Production', 'Chemical Efficiency', 'Crop Diversity', 'Land Utilization']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=[100, 40, 30, 100], theta=categories, fill='toself', name='Linear Prog.'))
        fig.add_trace(go.Scatterpolar(r=[80, 90, 85, 95], theta=categories, fill='toself', name='Goal Prog.'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="Trade-off Comparison")
        st.plotly_chart(fig, use_container_width=True)

# --- 7. Final Dashboard ---
elif nav == "7. Final Dashboard":
    st.markdown('<p class="section-header">Real Optimization Simulation Engine</p>', unsafe_allow_html=True)
    st.info("⚙️ **Final Review Active:** Running live LP & GP solvers on real dataset. Choose State + Season + Year to get data-driven parameters and recommendations.")

    try:
        df = pd.read_csv("crop_yield.csv")
        df['Season'] = df['Season'].str.strip()
        df['State']  = df['State'].str.strip()
        df['Crop']   = df['Crop'].str.strip()
    except FileNotFoundError:
        st.error("❌ Dataset `crop_yield.csv` not found!")
        st.stop()

    # ── STEP 1: State / Season / Year ─────────────────────────────────────
    st.markdown("### 🎛️ Step 1 — Select Your Context")
    s1, s2, s3 = st.columns(3)
    states  = sorted(df['State'].dropna().unique())
    seasons = sorted(df['Season'].dropna().unique())
    years   = sorted(df['Crop_Year'].dropna().astype(int).unique())

    target_state  = s1.selectbox("📍 Target State",  states)
    target_season = s2.selectbox("🌾 Season",         seasons)
    target_year   = s3.selectbox("📅 Crop Year",      years, index=len(years)-1)

    df_yr = df[(df['State'] == target_state) &
               (df['Season'] == target_season) &
               (df['Crop_Year'] == target_year)]

    # Rainfall banner
    if 'Annual_Rainfall' in df.columns:
        rf_val = df[(df['State'] == target_state) & (df['Crop_Year'] == target_year)]['Annual_Rainfall'].mean()
        if not pd.isna(rf_val):
            st.info(f"🌧️ **Annual Rainfall** for **{target_state}** in **{target_year}**: **{rf_val:.1f} mm** "
                    f"(Constant for all crops in this state-year. High rainfall reduces irrigation cost but data is fixed per year.)")

    available_crops = sorted(df_yr['Crop'].dropna().unique())

    if not available_crops:
        st.warning(f"⚠️ No crop data found for **{target_state}** / **{target_season}** / **{target_year}**. "
                   "This combination may not exist in the dataset — try changing the Year or Season.")
        st.stop()

    # ── STEP 2: Crop Selection ─────────────────────────────────────────────
    st.markdown("### 🌿 Step 2 — Select Crops")
    selected_crops = st.multiselect(
        "Choose crops to include in the optimization:",
        available_crops,
        default=available_crops[:min(4, len(available_crops))]
    )

    if not selected_crops:
        st.warning("Please select at least 2 crops.")
        st.stop()

    # ── Calculate Parameters ───────────────────────────────────────────────
    params = {}
    # State-level totals for computing true per-ha averages
    all_crop_data = df_yr[df_yr['Crop'].isin(selected_crops)]
    state_total_area = all_crop_data['Area'].sum()
    state_total_fert = all_crop_data['Fertilizer'].sum()
    state_total_pest = all_crop_data['Pesticide'].sum()
    state_avg_fert_ha = state_total_fert / state_total_area if state_total_area > 0 else 50.0
    state_avg_pest_ha = state_total_pest / state_total_area if state_total_area > 0 else 5.0

    for crop in selected_crops:
        cd = df_yr[df_yr['Crop'] == crop]
        yld       = cd['Yield'].mean()
        area_hist = cd['Area'].mean()
        prod_hist = cd['Production'].mean()
        fert_hist = cd['Fertilizer'].mean()   # actual total fertilizer for this crop
        pest_hist = cd['Pesticide'].mean()    # actual total pesticide for this crop
        fpha      = fert_hist / area_hist if area_hist > 0 else state_avg_fert_ha
        ppha      = pest_hist / area_hist if area_hist > 0 else state_avg_pest_ha

        params[crop] = {
            'Yield':      float(yld)       if not pd.isna(yld)       else 1.0,
            'Fertilizer': float(fpha)      if not pd.isna(fpha)      else state_avg_fert_ha,
            'Pesticide':  float(ppha)      if not pd.isna(ppha)      else state_avg_pest_ha,
            'Area_hist':  float(area_hist) if not pd.isna(area_hist) else 0,
            'Prod_hist':  float(prod_hist) if not pd.isna(prod_hist) else 0,
            'Fert_hist':  float(fert_hist) if not pd.isna(fert_hist) else 0,
            'Pest_hist':  float(pest_hist) if not pd.isna(pest_hist) else 0,
        }

    # Check if fert/ha is nearly identical across all crops (dataset limitation)
    fert_values = [params[c]['Fertilizer'] for c in selected_crops]
    fert_cv = (np.std(fert_values) / np.mean(fert_values)) if np.mean(fert_values) > 0 else 0
    dataset_has_uniform_fert = fert_cv < 0.01  # less than 1% variation = essentially identical

    # ── Parameter Table + Coefficient Chart ───────────────────────────────
    with st.expander("📊 Step 3 — View Crop Parameters (Derived from Dataset)", expanded=True):
        if dataset_has_uniform_fert:
            st.warning("""
⚠️ **Dataset Limitation Detected:** The Fertilizer (kg/ha) and Pesticide (kg/ha) values are **identical across all crops**.
This is because this dataset stores **state-level total fertilizer** distributed proportionally by crop area —
so `Fertilizer ÷ Area = State_Total_Fertilizer ÷ State_Total_Area` = a constant for all crops in the same state-year.

**Impact on optimization:** The fertilizer constraint effectively becomes a second land constraint (just scaled).
The real differentiator between crops is **Yield (tons/ha)** — which varies significantly.
The historical Fertilizer and Pesticide **totals** below show the actual dataset values per crop (they differ because areas differ).
            """)
        else:
            st.markdown("""
**How parameters are computed:** For the selected **State × Season × Year**, `Yield` (tons/ha) is read directly.
`Fertilizer/ha` and `Pesticide/ha` are computed as `Total Fertilizer ÷ Area`. These become the **coefficients** in our LP and GP equations.
            """)

        param_df = pd.DataFrame({
            'Yield (tons/ha)':         {c: params[c]['Yield']      for c in selected_crops},
            'Fert/ha (kg)':            {c: params[c]['Fertilizer'] for c in selected_crops},
            'Pest/ha (kg)':            {c: params[c]['Pesticide']  for c in selected_crops},
            'Hist. Area (ha)':         {c: params[c]['Area_hist']  for c in selected_crops},
            'Hist. Fert Total (kg)':   {c: params[c]['Fert_hist']  for c in selected_crops},
            'Hist. Pest Total (kg)':   {c: params[c]['Pest_hist']  for c in selected_crops},
            'Hist. Production (tons)': {c: params[c]['Prod_hist']  for c in selected_crops},
        })
        st.dataframe(param_df.style.format("{:.2f}"), use_container_width=True)

        # Coefficient visualization
        st.markdown("#### 📈 Coefficient Comparison Charts")
        cc1, cc2 = st.columns(2)
        with cc1:
            fig_coef = go.Figure()
            fig_coef.add_trace(go.Bar(name='Yield (tons/ha)', x=selected_crops,
                                      y=[params[c]['Yield'] for c in selected_crops],
                                      marker_color='#22c55e',
                                      text=[f"{params[c]['Yield']:.2f}" for c in selected_crops],
                                      textposition='outside'))
            fig_coef.update_layout(title="Yield Coefficient per crop (LP Objective — LP allocates land to highest yield crops)",
                                   xaxis_tickangle=-35, height=350)
            st.plotly_chart(fig_coef, use_container_width=True)
        with cc2:
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Bar(name='Historical Fert Total (kg)', x=selected_crops,
                                      y=[params[c]['Fert_hist'] for c in selected_crops],
                                      marker_color='#f59e0b'))
            fig_hist.add_trace(go.Bar(name='Historical Pest Total (kg)', x=selected_crops,
                                      y=[params[c]['Pest_hist'] for c in selected_crops],
                                      marker_color='#ef4444'))
            fig_hist.update_layout(title="Historical Resource Totals per Crop (these DO vary — shows crop's actual resource footprint)",
                                   barmode='group', xaxis_tickangle=-35, height=350)
            st.plotly_chart(fig_hist, use_container_width=True)

        st.caption("""
**Why Area and Yield are not optimization variables/targets:**
- **Area (x_i)** IS our decision variable — it's what LP/GP *solves for*. You can't set it as a target at the same time.
- **Yield (tons/ha)** is a *fixed historical coefficient* from the dataset — nature/farming conditions determine yield, not us. We use it as the LP objective coefficient.
- **Rainfall** is a fixed exogenous parameter per state-year. It's informational only.
- **Max Area per crop** CAN be constrained via the Diversity slider below — this gives each crop a minimum guaranteed allocation.
        """)



    # ── Smart Recommendations ─────────────────────────────────────────────
    rec_land  = sum(params[c]['Area_hist']  for c in selected_crops)
    rec_prod  = sum(params[c]['Prod_hist']  for c in selected_crops)
    rec_fert  = sum(params[c]['Fert_hist']  for c in selected_crops)
    rec_pest  = sum(params[c]['Pest_hist']  for c in selected_crops)

    st.markdown("### 💡 Step 4 — Smart Recommendations (Based on Your Selection)")
    st.caption(f"These are the **actual historical values** from your dataset for **{target_state} / {target_season} / {target_year}**. Use them as a starting point for your constraints and targets.")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("📐 Historical Total Area", f"{rec_land:,.0f} ha")
    r2.metric("🌾 Historical Production",  f"{rec_prod:,.0f} tons")
    r3.metric("🧪 Historical Fertilizer",  f"{rec_fert:,.0f} kg")
    r4.metric("🐛 Historical Pesticide",   f"{rec_pest:,.0f} kg")

    with st.expander("📖 How to Choose Your Parameters Wisely"):
        st.markdown(f"""
        **Available Land** — Set this to the total land you plan to allocate. The historical data shows **{rec_land:,.0f} ha** was used.
        You can try values around this (e.g., 80%–120%) to see how production changes.

        **Max Fertilizer / Pesticide** — These are your budget limits. The dataset used **{rec_fert:,.0f} kg fertilizer** and
        **{rec_pest:,.0f} kg pesticide** historically. Set lower values if you want a more eco-friendly plan.

        **GP Target Production** — Start with **{rec_prod:,.0f} tons** (what was historically achieved). Then lower it
        to see if GP can achieve a more balanced crop mix, or raise it to stress-test the system.

        **GP Target Fertilizer** — Set this to **{rec_fert*0.8:,.0f} kg** (20% reduction) to simulate a fertilizer budget cut and see how GP redistributes land.

        **Why does LP pick only 1-2 crops?** LP is a pure mathematician — it finds the single most efficient crop (highest yield per fertilizer used) and puts everything there. This is mathematically correct but not realistic.

        **Why does GP also show 1-2 crops?** By default, GP also concentrates on the most efficient path to hit the production goal. The **Crop Diversity slider below** forces GP to allocate a minimum % of land to every selected crop, giving a realistic diverse allocation.
        """)

    # ── STEP 5: Constraints ───────────────────────────────────────────────
    st.markdown("### 📏 Step 5 — Set Resource Constraints")
    rc1, rc2, rc3 = st.columns(3)
    max_land = rc1.number_input("Available Land (ha)", min_value=100.0,
                                 value=float(max(rec_land, 100)), step=500.0,
                                 help=f"Historical: {rec_land:,.0f} ha")
    max_fert = rc2.number_input("Max Fertilizer (kg)", min_value=1000.0,
                                 value=float(max(rec_fert, 1000)), step=10000.0,
                                 help=f"Historical: {rec_fert:,.0f} kg")
    max_pest = rc3.number_input("Max Pesticide (kg)", min_value=10.0,
                                 value=float(max(rec_pest, 10)), step=1000.0,
                                 help=f"Historical: {rec_pest:,.0f} kg")

    # ── STEP 6: GP Targets ────────────────────────────────────────────────
    st.markdown("### 🎯 Step 6 — Set Goal Programming Targets")
    st.caption("GP tries to **reach** these targets, not just stay under them. It minimises deviation from each goal.")
    g1, g2, g3 = st.columns(3)
    target_prod = g1.number_input("🌾 Target Production (tons) [Goal 1]", min_value=100.0,
                                   value=float(max(rec_prod * 0.9, 100)), step=1000.0,
                                   help=f"Recommended: {rec_prod:,.0f} tons (historical)")
    target_fert = g2.number_input("🧪 Target Fertilizer Use (kg) [Goal 2]", min_value=100.0,
                                   value=float(max(rec_fert * 0.8, 100)), step=10000.0,
                                   help=f"Recommended: {rec_fert*0.8:,.0f} kg (20% reduction from historical)")
    target_pest = g3.number_input("🐛 Target Pesticide Use (kg) [Goal 3]", min_value=10.0,
                                   value=float(max(rec_pest * 0.8, 10)), step=500.0,
                                   help=f"Recommended: {rec_pest*0.8:,.0f} kg (20% reduction from historical)")

    # Diversity slider — KEY FIX for GP
    st.markdown("#### 🌈 Crop Diversity Control (for Goal Programming)")
    diversity_pct = st.slider(
        "Minimum land allocation per crop (%)",
        min_value=0, max_value=30, value=5, step=1,
        help="This forces GP to allocate at least this % of total land to EACH selected crop. "
             "Set to 0 for pure mathematical optimum (1-2 crops). Set to 10-15% for realistic diverse farming."
    )
    st.caption(f"➡️ With {len(selected_crops)} crops and {diversity_pct}% minimum, each crop gets at least "
               f"**{diversity_pct/100 * max_land / len(selected_crops):,.0f} ha** guaranteed.")

    # ── RUN ───────────────────────────────────────────────────────────────
    if st.button("🚀 Run Operations Research Solvers", use_container_width=True, type="primary"):
        from scipy.optimize import linprog

        n = len(selected_crops)
        yields = np.array([params[c]['Yield']      for c in selected_crops])
        ferts  = np.array([params[c]['Fertilizer'] for c in selected_crops])
        pests  = np.array([params[c]['Pesticide']  for c in selected_crops])

        # ── LINEAR PROGRAMMING ────────────────────────────────────────────
        # Maximize: Z = Σ yield_i · x_i  →  Minimize: -Z
        lp_c      = -yields
        lp_A      = np.vstack([np.ones(n), ferts, pests])
        lp_b      = [max_land, max_fert, max_pest]
        lp_bounds = [(0, None)] * n

        lp_res = linprog(lp_c, A_ub=lp_A, b_ub=lp_b, bounds=lp_bounds, method='highs')

        lp_alloc       = lp_res.x if lp_res.success else np.zeros(n)
        lp_status_text = "Optimal ✅" if lp_res.success else "Infeasible ❌"
        lp_results     = {c: float(lp_alloc[i]) for i, c in enumerate(selected_crops)}
        lp_total_prod  = float(yields @ lp_alloc)
        lp_fert_used   = float(ferts @ lp_alloc)
        lp_pest_used   = float(pests @ lp_alloc)
        lp_land_used   = float(lp_alloc.sum())

        # ── GOAL PROGRAMMING ──────────────────────────────────────────────
        # Variables: x_0..x_{n-1}, d1-(n), d1+(n+1), d2-(n+2), d2+(n+3), d3-(n+4), d3+(n+5)
        # Minimize: d1- + d2+ + d3+
        nv       = n + 6
        gp_c     = np.zeros(nv)
        gp_c[n]   = 1    # d1- : under-achieve production (bad)
        gp_c[n+3] = 1    # d2+ : over-shoot fertilizer target (bad)
        gp_c[n+5] = 1    # d3+ : over-shoot pesticide target (bad)

        # Land constraint: Σ x_i <= max_land
        gp_A_ub = np.zeros((1, nv)); gp_A_ub[0, :n] = 1
        gp_b_ub = [max_land]

        # Goal equality constraints
        gp_A_eq = np.zeros((3, nv))
        gp_A_eq[0, :n] = yields; gp_A_eq[0, n]   =  1; gp_A_eq[0, n+1] = -1   # prod goal
        gp_A_eq[1, :n] = ferts;  gp_A_eq[1, n+2] =  1; gp_A_eq[1, n+3] = -1   # fert goal
        gp_A_eq[2, :n] = pests;  gp_A_eq[2, n+4] =  1; gp_A_eq[2, n+5] = -1   # pest goal
        gp_b_eq = [target_prod, target_fert, target_pest]

        # Diversity: minimum allocation per crop
        min_alloc = (diversity_pct / 100.0) * max_land / n
        gp_bounds = [(min_alloc, None)] * n + [(0, None)] * 6

        gp_res = linprog(gp_c, A_ub=gp_A_ub, b_ub=gp_b_ub,
                         A_eq=gp_A_eq, b_eq=gp_b_eq,
                         bounds=gp_bounds, method='highs')

        gp_alloc       = gp_res.x[:n] if gp_res.success else np.zeros(n)
        gp_status_text = "Optimal ✅" if gp_res.success else "Infeasible ❌"
        gp_results     = {c: float(gp_alloc[i]) for i, c in enumerate(selected_crops)}
        gp_total_prod  = float(yields @ gp_alloc)
        gp_fert_used   = float(ferts @ gp_alloc)
        gp_pest_used   = float(pests @ gp_alloc)
        gp_land_used   = float(gp_alloc.sum())

        # Deviation vars from GP
        if gp_res.success:
            gp_devs = gp_res.x[n:]
            d1m, d1p = gp_devs[0], gp_devs[1]  # production
            d2m, d2p = gp_devs[2], gp_devs[3]  # fertilizer
            d3m, d3p = gp_devs[4], gp_devs[5]  # pesticide
        else:
            d1m = d1p = d2m = d2p = d3m = d3p = 0

        # ── RESULTS ───────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("## 🏆 Optimization Results")

        # Status banner
        b1, b2 = st.columns(2)
        b1.success(f"**LP:** {lp_status_text} | Max Production: **{lp_total_prod:,.2f} tons**")
        b2.info(f"**GP:** {gp_status_text} | Balanced Production: **{gp_total_prod:,.2f} tons**")

        # ── Land Allocation Chart ──────────────────────────────────────────
        st.markdown("### 📊 Land Allocation Comparison")
        fig_alloc = go.Figure()
        fig_alloc.add_trace(go.Bar(name='LP Allocation (ha)', x=selected_crops,
                                   y=[lp_results[c] for c in selected_crops],
                                   marker_color='#3b82f6', text=[f"{lp_results[c]:,.0f}" for c in selected_crops],
                                   textposition='outside'))
        fig_alloc.add_trace(go.Bar(name='GP Allocation (ha)', x=selected_crops,
                                   y=[gp_results[c] for c in selected_crops],
                                   marker_color='#f97316', text=[f"{gp_results[c]:,.0f}" for c in selected_crops],
                                   textposition='outside'))
        fig_alloc.update_layout(barmode='group', title="Optimal Land Allocation per Crop (Hectares)",
                                xaxis_tickangle=-30, height=420,
                                annotations=[dict(text="LP concentrates land; GP distributes across crops",
                                                  showarrow=False, xref='paper', yref='paper', x=0.5, y=1.1)])
        st.plotly_chart(fig_alloc, use_container_width=True)

        # ── Resource Utilization ───────────────────────────────────────────
        st.markdown("### 🏭 Resource Utilization")
        ru1, ru2 = st.columns(2)
        with ru1:
            resources  = ['Land', 'Fertilizer', 'Pesticide']
            lp_pct     = [lp_land_used/max_land*100, lp_fert_used/max_fert*100, lp_pest_used/max_pest*100]
            gp_pct     = [gp_land_used/max_land*100, gp_fert_used/max_fert*100, gp_pest_used/max_pest*100]
            fig_res = go.Figure()
            fig_res.add_trace(go.Bar(name='LP Used (%)', x=resources, y=lp_pct,
                                     marker_color='#3b82f6',
                                     text=[f"{v:.1f}%" for v in lp_pct], textposition='outside'))
            fig_res.add_trace(go.Bar(name='GP Used (%)', x=resources, y=gp_pct,
                                     marker_color='#f97316',
                                     text=[f"{v:.1f}%" for v in gp_pct], textposition='outside'))
            fig_res.update_layout(barmode='group', title="Resource Utilization vs Limits (%)",
                                  yaxis=dict(range=[0, 120]), height=350)
            st.plotly_chart(fig_res, use_container_width=True)

        with ru2:
            # Radar chart: LP vs GP profile
            cat = ['Production\n(% of Max LP)', 'Land\nEfficiency', 'Fert\nEfficiency', 'Pest\nEfficiency', 'Crop\nDiversity']
            lp_div_score = sum(1 for c in selected_crops if lp_results[c] > 1) / n * 100
            gp_div_score = sum(1 for c in selected_crops if gp_results[c] > 1) / n * 100
            lp_radar = [100,
                        (1 - lp_land_used/max_land) * 100,
                        (1 - lp_fert_used/max_fert) * 100,
                        (1 - lp_pest_used/max_pest) * 100,
                        lp_div_score]
            gp_radar = [gp_total_prod / max(lp_total_prod, 1) * 100,
                        (1 - gp_land_used/max_land) * 100,
                        (1 - gp_fert_used/max_fert) * 100,
                        (1 - gp_pest_used/max_pest) * 100,
                        gp_div_score]
            fig_rad = go.Figure()
            fig_rad.add_trace(go.Scatterpolar(r=lp_radar, theta=cat, fill='toself',
                                               name='Linear Programming', line_color='#3b82f6'))
            fig_rad.add_trace(go.Scatterpolar(r=gp_radar, theta=cat, fill='toself',
                                               name='Goal Programming', line_color='#f97316'))
            fig_rad.update_layout(polar=dict(radialaxis=dict(range=[0, 110])),
                                  title="LP vs GP Profile Comparison", height=350)
            st.plotly_chart(fig_rad, use_container_width=True)

        # ── Mathematical Model Breakdown ───────────────────────────────────
        st.markdown("### 🔢 What the Math Looks Like (With Your Numbers)")

        with st.expander("📐 LP Objective Function & Constraints — Expanded", expanded=True):
            lp_obj_terms = " + ".join([f"({params[c]['Yield']:.2f} × x_{i+1}[{c}])" for i, c in enumerate(selected_crops)])
            st.markdown(f"""
**Objective Function (Maximize Production):**
$$Z_{{LP}} = {lp_obj_terms}$$

**Subject to:**
- **Land:** {' + '.join([f'x_{i+1}' for i in range(n)])} ≤ **{max_land:,.0f} ha**
- **Fertilizer:** {' + '.join([f'({params[c]["Fertilizer"]:.1f} × x_{i+1})' for i,c in enumerate(selected_crops)])} ≤ **{max_fert:,.0f} kg**
- **Pesticide:** {' + '.join([f'({params[c]["Pesticide"]:.2f} × x_{i+1})' for i,c in enumerate(selected_crops)])} ≤ **{max_pest:,.0f} kg**
- **Non-negativity:** x₁, x₂, ... ≥ 0

**Why LP picks {sum(1 for v in lp_results.values() if v > 1)} crop(s):**
The crop with the highest yield-per-fertilizer-unit wins all the available budget.
{'Crop: ' + max(selected_crops, key=lambda c: params[c]['Yield']/max(params[c]['Fertilizer'],0.01))} has the best ratio at
{max(params[c]['Yield']/max(params[c]['Fertilizer'],0.01) for c in selected_crops):.4f} tons/kg-fertilizer.
LP exploits this and puts maximum land there until a constraint binds.
            """)

        with st.expander("🎯 GP Objective Function & Goal Constraints — Expanded", expanded=True):
            gp_obj = "d₁⁻ + d₂⁺ + d₃⁺"
            st.markdown(f"""
**Objective Function (Minimize Deviations):**
$$Z_{{GP}} = d_1^- + d_2^+ + d_3^+$$

- **d₁⁻** = amount we **fall short** of production target (we don't want this)
- **d₂⁺** = amount we **exceed** the fertilizer target (we don't want this)
- **d₃⁺** = amount we **exceed** the pesticide target (we don't want this)

**Goal Constraints:**
- **Goal 1 (Production):** Σ(yield × x) + d₁⁻ − d₁⁺ = **{target_prod:,.0f} tons**
- **Goal 2 (Fertilizer):** Σ(fert × x) + d₂⁻ − d₂⁺ = **{target_fert:,.0f} kg**
- **Goal 3 (Pesticide):** Σ(pest × x) + d₃⁻ − d₃⁺ = **{target_pest:,.0f} kg**

**Actual Deviations After Solving:**
| Goal | Target | Achieved | Under (d⁻) | Over (d⁺) | Status |
|---|---|---|---|---|---|
| Production | {target_prod:,.0f} tons | {gp_total_prod:,.0f} tons | {d1m:,.0f} | {d1p:,.0f} | {"✅ Hit" if d1m < 1 and d1p < 1 else "⚠️ Deviated"} |
| Fertilizer | {target_fert:,.0f} kg | {gp_fert_used:,.0f} kg | {d2m:,.0f} | {d2p:,.0f} | {"✅ Hit" if d2m < 1 and d2p < 1 else "⚠️ Deviated"} |
| Pesticide | {target_pest:,.0f} kg | {gp_pest_used:,.0f} kg | {d3m:,.0f} | {d3p:,.0f} | {"✅ Hit" if d3m < 1 and d3p < 1 else "⚠️ Deviated"} |

**Why Area & Yield are not separate GP goals:**
- *Area* is already the **decision variable** (x_i = land allocated to crop i) — making it a goal would be circular.
- *Yield* per hectare is a **fixed coefficient** from the dataset (not controllable). We use it in the objective, not as a target.
- *Rainfall* is not a variable — it is a **fixed exogenous parameter** for the chosen state-year.
            """)

        # ── Deviation & Target Fulfillment Analysis ─────────────────────────
        st.markdown("### 📉 GP Goal Fulfillment & Deviation Analysis")

        col_dev1, col_dev2 = st.columns(2)

        with col_dev1:
            # Chart 1: Target vs Achieved Comparison (%)
            prod_pct = (gp_total_prod / target_prod * 100) if target_prod > 0 else 0
            fert_pct = (gp_fert_used / target_fert * 100) if target_fert > 0 else 0
            pest_pct = (gp_pest_used / target_pest * 100) if target_pest > 0 else 0

            fig_goal_pct = go.Figure()
            fig_goal_pct.add_trace(go.Bar(
                name='Target Set (100%)',
                x=['Production Goal', 'Fertilizer Goal', 'Pesticide Goal'],
                y=[100, 100, 100],
                marker_color='#94a3b8'
            ))
            fig_goal_pct.add_trace(go.Bar(
                name='Achieved by GP (%)',
                x=['Production Goal', 'Fertilizer Goal', 'Pesticide Goal'],
                y=[prod_pct, fert_pct, pest_pct],
                marker_color=['#22c55e' if prod_pct >= 100 else '#f59e0b',
                              '#22c55e' if fert_pct <= 100 else '#ef4444',
                              '#22c55e' if pest_pct <= 100 else '#ef4444'],
                text=[f"{prod_pct:.1f}%", f"{fert_pct:.1f}%", f"{pest_pct:.1f}%"],
                textposition='outside'
            ))
            fig_goal_pct.update_layout(
                barmode='group',
                title="Goal Achievement Rate (% of Target Met)",
                yaxis=dict(title="Percentage (%)", range=[0, max(130, prod_pct+10, fert_pct+10, pest_pct+10)]),
                height=350
            )
            st.plotly_chart(fig_goal_pct, use_container_width=True)

        with col_dev2:
            # Chart 2: Unwanted Deviation Values (d1-, d2+, d3+)
            dev_fig = go.Figure()
            dev_fig.add_trace(go.Bar(
                name='Under-achievement (d⁻)',
                x=['Production (d₁⁻)', 'Fertilizer (d₂⁻)', 'Pesticide (d₃⁻)'],
                y=[d1m, d2m, d3m],
                marker_color='#ef4444',
                text=[f"{d1m:,.0f}", f"{d2m:,.0f}", f"{d3m:,.0f}"],
                textposition='outside'
            ))
            dev_fig.add_trace(go.Bar(
                name='Over-achievement (d⁺)',
                x=['Production (d₁⁺)', 'Fertilizer (d₂⁺)', 'Pesticide (d₃⁺)'],
                y=[d1p, d2p, d3p],
                marker_color='#22c55e',
                text=[f"{d1p:,.0f}", f"{d2p:,.0f}", f"{d3p:,.0f}"],
                textposition='outside'
            ))
            dev_fig.update_layout(
                barmode='group',
                title="Raw Goal Deviations (d⁻ and d⁺)",
                yaxis_title="Units (tons / kg)",
                height=350
            )
            st.plotly_chart(dev_fig, use_container_width=True)

        st.info("""
💡 **Understanding GP Deviations:**
- **Zero Unwanted Deviation ($d_1^- = 0, d_2^+ = 0, d_3^+ = 0$) is the PERFECT outcome!** It means Goal Programming successfully satisfied all your target constraints without falling short on production or overshooting chemical budgets.
- **$d_1^-$ (Production Shortfall):** We penalize falling short of target production. If $d_1^- = 0$, production target was met or exceeded.
- **$d_2^+$ & $d_3^+$ (Chemical Overshoot):** We penalize exceeding fertilizer/pesticide limits. If $d_2^+ = 0, d_3^+ = 0$, chemical limits were respected.
- **$d_1^+$ (Exceeding Production Target):** Over-producing beyond the goal is GOOD in agriculture, so $d_1^+$ is not penalized in the objective function ($Z_{GP}$).
        """)

        # ── Binding Constraints Analysis ────────────────────────────────────
        st.markdown("### 🔗 Which Constraints Were Binding? (LP Sensitivity)")
        binding = []
        if abs(lp_land_used - max_land) < 1: binding.append("Land (fully exhausted)")
        if abs(lp_fert_used - max_fert) < max_fert * 0.01: binding.append("Fertilizer (near limit)")
        if abs(lp_pest_used - max_pest) < max_pest * 0.01: binding.append("Pesticide (near limit)")
        if binding:
            st.warning(f"**Binding constraints:** {', '.join(binding)}. "
                        "These constraints are stopping LP from producing even more. "
                        "Increase these limits to allow higher production.")
        else:
            st.success("No single constraint is fully binding — the problem is balanced.")

        # ── Summary Table ──────────────────────────────────────────────────
        st.markdown("### 📋 Side-by-Side Summary Table")
        summary_df = pd.DataFrame({
            'Metric': ['Total Production (tons)', 'Land Used (ha)', 'Fertilizer Used (kg)', 'Pesticide Used (kg)',
                       'Crops with Allocation > 0'],
            'Historical (Dataset)': [f"{rec_prod:,.0f}", f"{rec_land:,.0f}", f"{rec_fert:,.0f}", f"{rec_pest:,.0f}", f"{len(selected_crops)}"],
            'Linear Programming': [f"{lp_total_prod:,.0f}", f"{lp_land_used:,.0f}", f"{lp_fert_used:,.0f}", f"{lp_pest_used:,.0f}",
                                    f"{sum(1 for v in lp_results.values() if v > 1)}"],
            'Goal Programming': [f"{gp_total_prod:,.0f}", f"{gp_land_used:,.0f}", f"{gp_fert_used:,.0f}", f"{gp_pest_used:,.0f}",
                                   f"{sum(1 for v in gp_results.values() if v > 1)}"],
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        # ── Final Interpretation ────────────────────────────────────────────
        st.markdown("### 📝 Analysis & Interpretation")
        best_lp_crop = max(selected_crops, key=lambda c: lp_results[c])
        best_gp_crop = max(selected_crops, key=lambda c: gp_results[c])
        st.markdown(f"""
**Linear Programming (LP):**
LP is a pure optimizer — it found that **{best_lp_crop}** has the highest yield relative to its resource use,
so it allocated most land there to maximize total production of **{lp_total_prod:,.0f} tons**.
This is mathematically optimal but not practically diverse. In real farming, you wouldn't bet everything on one crop.

**Goal Programming (GP):**
GP is a balanced planner. With your targets set to {target_prod:,.0f} tons production, {target_fert:,.0f} kg fertilizer,
and {target_pest:,.0f} kg pesticide, GP found a plan that achieves **{gp_total_prod:,.0f} tons** while staying as close
as possible to all three goals simultaneously. The diversity slider ({diversity_pct}%) ensured that each crop got at least
some land, making the plan realistic for a farmer.

**Key Insight for Final Review:** LP gives you the theoretical maximum. GP gives you the practical optimum that
a real farmer would actually implement — balancing yield, cost, and sustainability.
        """)



# --- 8. Team Contribution ---

elif nav == "8. Team Contribution":
    st.markdown('<p class="section-header">👥 Meet the Team</p>', unsafe_allow_html=True)
    
    st.markdown("""
    | Team Member | GitHub Profile | Core Focus & Responsibilities |
    | :--- | :--- | :--- |
    | **Vignesh V S** | [@VigneshVS2005](https://github.com/VigneshVS2005) | Linear Programming Model, Decision Variables, Objective Functions & LP Solver Code |
    | **Karthick Ruban** | [@Karthickruban](https://github.com/Karthickruban) | Goal Programming Model, Deviation Variables, Goal Weighting & GP Solver Code |
    | **Hariprakash** | [@Hariprakash024](https://github.com/Hariprakash024) | Streamlit UI Development, Plotly Visualizations, System Integration & Dashboard |
    | **Sanjay Senthil** | [@sanjaysenthil17](https://github.com/sanjaysenthil17) | Dataset Acquisition, Data Cleaning, Exploratory Data Analysis & Parameter Calculations |
    """)
    
    st.markdown("---")
    st.markdown("### 🏁 First Review Boundary")
    st.write("We have successfully identified the dataset, cleaned the data, established the research methodology, and formulated both the Linear Programming and Goal Programming approaches mathematically.")
    st.write("In the final review, we will present the fully functional optimization engine integrated directly into this dashboard.")

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
st.markdown('<p class="sub-title">Operations Research: Linear & Goal Programming (Final System Optimization & Review)</p>', unsafe_allow_html=True)
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
            "8. Crop Advisory & Recommendation",
            "9. Team Contribution"
        ],
        icons=[
            "house", "book", "bar-chart-line", "diagram-3", 
            "graph-up", "bullseye", "laptop", "lightbulb", "people"
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
    st.success("📌 **Final Review System:** All steps (A through K) are fully implemented, verified, and operational with interactive LP and GP solvers.")

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
        st.info(f"ℹ️ **State Baseline Chemical Rates ({target_state} — {target_season} {target_year}):** Calculated Fertilizer Rate = **{state_avg_fert_ha:.2f} kg/ha** | Pesticide Rate = **{state_avg_pest_ha:.2f} kg/ha** (constant per hectare across crops for this state-year). Crop Yields (tons/ha) and Total Historical Resource Footprints vary distinctly.")

        param_df = pd.DataFrame({
            'Yield (tons/ha)':         {c: params[c]['Yield']      for c in selected_crops},
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

    # ── STEP 5: LP & GP Strategy Configuration ────────────────────────────
    st.markdown("### 📏 Step 5 — Set Resource Constraints & LP Strategy")
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
    st.markdown("### 🎯 Step 6 — Set Goal Programming Targets & Strategy")
    st.caption("GP balances multiple conflicting goals simultaneously: hitting production target, staying within chemical limits, AND maintaining crop diversity.")
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

    st.markdown("#### ⚖️ Goal Programming Strategy & Solver Engine")
    gp_strategy = st.radio(
        "Select Goal Weighting Strategy & Solver Engine:",
        [
            "🌾 Multi-Goal Cropping Pattern Balancing (Recommended — SciPy HiGHS Engine with Crop Target Shares)",
            "🎯 Global Goals Only (SciPy HiGHS Engine — Production & Chemical Targets)",
            "⚡ Strictly PuLP CBC Solver GP (PuLP Object-Oriented Engine — Preemptive & Weighted Deviations)"
        ],
        index=0,
        help="Multi-Goal mode adds crop-level target share goals. PuLP mode strictly executes the COIN-OR CBC Solver engine!"
    )
    use_multi_crop_goals = "Multi-Goal" in gp_strategy
    use_pulp_solver = "PuLP CBC" in gp_strategy

    with st.expander("📖 Deep Comparison of the 3 Goal Programming Strategies & Solvers"):
        st.markdown("""
        | Strategy / Engine | Core Formulation & Method | Why Use It? | Output Characteristics |
        |---|---|---|---|
        | **🌾 Multi-Goal Cropping Pattern Balancing** | SciPy HiGHS Solver with $N$ Crop Land Share Goals ($x_i + d_{i,c}^- - d_{i,c}^+ = A_i^{\\text{target}}$) | Prevents monoculture; distributes land across **ALL crops** proportional to history. | Balanced, multi-crop realistic farm portfolio. |
        | **🎯 Global Goals Only** | SciPy HiGHS Matrix Solver targeting aggregate Production, Fertilizer, & Pesticide | Focuses strictly on total yield & chemical caps without crop-level share goals. | May concentrate land into 1–2 highly efficient crops. |
        | **⚡ Strictly PuLP CBC Solver** | COIN-OR CBC C++ Branch & Cut Solver via PuLP symbolic objects (`LpProblem`, `lpSum`) | Object-oriented symbolic execution with explicit deviation weights ($w_k \cdot d_k$). | Exact CBC solver pivot solutions with symbolic equation inspection. |
        """)

    # Diversity slider
    st.markdown("#### 🌈 Additional Crop Diversity Floor (Minimum % per crop)")
    diversity_pct = st.slider(
        "Minimum guaranteed land allocation per crop (%)",
        min_value=0, max_value=25, value=2, step=1,
        help="Sets a hard minimum land bound for every selected crop."
    )

    # ── RUN ───────────────────────────────────────────────────────────────
    if st.button("🚀 Run Operations Research Solvers", use_container_width=True, type="primary"):
        from scipy.optimize import linprog

        n = len(selected_crops)
        yields = np.array([params[c]['Yield']      for c in selected_crops])
        ferts  = np.array([params[c]['Fertilizer'] for c in selected_crops])
        pests  = np.array([params[c]['Pesticide']  for c in selected_crops])
        hist_areas = np.array([params[c]['Area_hist'] for c in selected_crops])
        sum_hist_area = hist_areas.sum()

        # Calculate target land allocation per crop based on historical shares
        if sum_hist_area > 0:
            target_crop_areas = max_land * (hist_areas / sum_hist_area)
        else:
            target_crop_areas = np.full(n, max_land / n)

        # ── LINEAR PROGRAMMING ────────────────────────────────────────────
        min_alloc = (diversity_pct / 100.0) * max_land / n

        # Standard LP Tonnage Objective (Maximize Total Production)
        lp_c = -yields

        lp_A      = np.vstack([np.ones(n), ferts, pests])
        lp_b      = [max_land, max_fert, max_pest]
        lp_bounds = [(min_alloc, None)] * n

        lp_res = linprog(lp_c, A_ub=lp_A, b_ub=lp_b, bounds=lp_bounds, method='highs')

        lp_alloc       = lp_res.x if lp_res.success else np.zeros(n)
        lp_status_text = "Optimal ✅" if lp_res.success else "Infeasible ❌"
        lp_results     = {c: float(lp_alloc[i]) for i, c in enumerate(selected_crops)}
        lp_total_prod  = float(yields @ lp_alloc)
        lp_fert_used   = float(ferts @ lp_alloc)
        lp_pest_used   = float(pests @ lp_alloc)
        lp_land_used   = float(lp_alloc.sum())

        # ── GOAL PROGRAMMING ──────────────────────────────────────────────
        if use_pulp_solver:
            pulp_exec_success = False
            try:
                import pulp
                prob = pulp.LpProblem("PuLP_Goal_Programming", pulp.LpMinimize)
                
                lb_val = float(min_alloc) if min_alloc is not None else 0.0
                x_vars = {c: pulp.LpVariable(name=f"x_{i}", lowBound=lb_val, upBound=None, cat=pulp.LpContinuous) for i, c in enumerate(selected_crops)}
                
                d1_minus = pulp.LpVariable(name="d1_minus", lowBound=0.0, upBound=None, cat=pulp.LpContinuous)
                d1_plus  = pulp.LpVariable(name="d1_plus", lowBound=0.0, upBound=None, cat=pulp.LpContinuous)
                d2_minus = pulp.LpVariable(name="d2_minus", lowBound=0.0, upBound=None, cat=pulp.LpContinuous)
                d2_plus  = pulp.LpVariable(name="d2_plus", lowBound=0.0, upBound=None, cat=pulp.LpContinuous)
                d3_minus = pulp.LpVariable(name="d3_minus", lowBound=0.0, upBound=None, cat=pulp.LpContinuous)
                d3_plus  = pulp.LpVariable(name="d3_plus", lowBound=0.0, upBound=None, cat=pulp.LpContinuous)
                
                prob += pulp.lpSum([x_vars[c] for c in selected_crops]) <= float(max_land), "Land_Limit"
                prob += pulp.lpSum([float(params[c]['Yield']) * x_vars[c] for c in selected_crops]) + d1_minus - d1_plus == float(target_prod), "Prod_Goal"
                prob += pulp.lpSum([float(params[c]['Fertilizer']) * x_vars[c] for c in selected_crops]) + d2_minus - d2_plus == float(target_fert), "Fert_Goal"
                prob += pulp.lpSum([float(params[c]['Pesticide']) * x_vars[c] for c in selected_crops]) + d3_minus - d3_plus == float(target_pest), "Pest_Goal"
                
                w1 = 10.0 / max(float(target_prod), 1.0)
                w2 = 10.0 / max(float(target_fert), 1.0)
                w3 = 10.0 / max(float(target_pest), 1.0)
                prob += w1 * d1_minus + w2 * d2_plus + w3 * d3_plus, "Total_Deviation"
                
                try:
                    solver = pulp.PULP_CBC_CMD(msg=0)
                    prob.solve(solver)
                except Exception:
                    prob.solve()
                
                gp_status_text = f"PuLP CBC {pulp.LpStatus[prob.status]} ✅" if prob.status == 1 else f"PuLP CBC {pulp.LpStatus[prob.status]} ⚠️"
                gp_alloc = np.array([float(pulp.value(x_vars[c])) if pulp.value(x_vars[c]) is not None else 0.0 for c in selected_crops])
                
                d1m = float(pulp.value(d1_minus)) if pulp.value(d1_minus) is not None else 0.0
                d1p = float(pulp.value(d1_plus))  if pulp.value(d1_plus) is not None else 0.0
                d2m = float(pulp.value(d2_minus)) if pulp.value(d2_minus) is not None else 0.0
                d2p = float(pulp.value(d2_plus))  if pulp.value(d2_plus) is not None else 0.0
                d3m = float(pulp.value(d3_minus)) if pulp.value(d3_minus) is not None else 0.0
                d3p = float(pulp.value(d3_plus))  if pulp.value(d3_plus) is not None else 0.0

                pulp_exec_success = True
            except Exception as ex:
                import traceback
                st.error("⚠️ PuLP CBC Solver Execution Traceback Details:")
                st.code(f"Error Type: {type(ex).__name__}\nDetails: {str(ex)}\n\nTraceback:\n{traceback.format_exc()}")
                st.info("ℹ️ Executing PuLP-equivalent formulation via SciPy HiGHS Solver for 100% stability.")
                use_pulp_solver = False

        if not use_pulp_solver:
            if use_multi_crop_goals:
                # Multi-Goal GP: Total Production + Total Fert + Total Pest + N Crop Land Goals
                nv = n + 6 + 2 * n
                gp_c = np.zeros(nv)
                
                gp_c[n]   = 10.0 / max(target_prod, 1.0)   # d1- : under-achieve production
                gp_c[n+3] = 10.0 / max(target_fert, 1.0)   # d2+ : over-shoot fertilizer
                gp_c[n+5] = 10.0 / max(target_pest, 1.0)   # d3+ : over-shoot pesticide

                for i in range(n):
                    w_c = 1.0 / max(target_crop_areas[i], 1.0)
                    gp_c[n + 6 + 2*i]     = w_c   # d_{i,c}-
                    gp_c[n + 6 + 2*i + 1] = w_c   # d_{i,c}+

                gp_A_ub = np.zeros((1, nv)); gp_A_ub[0, :n] = 1
                gp_b_ub = [max_land]

                gp_A_eq = np.zeros((3 + n, nv))
                gp_A_eq[0, :n] = yields; gp_A_eq[0, n]   =  1; gp_A_eq[0, n+1] = -1  # prod goal
                gp_A_eq[1, :n] = ferts;  gp_A_eq[1, n+2] =  1; gp_A_eq[1, n+3] = -1  # fert goal
                gp_A_eq[2, :n] = pests;  gp_A_eq[2, n+4] =  1; gp_A_eq[2, n+5] = -1  # pest goal

                for i in range(n):
                    gp_A_eq[3 + i, i]               = 1
                    gp_A_eq[3 + i, n + 6 + 2*i]     = 1   # d_{i,c}-
                    gp_A_eq[3 + i, n + 6 + 2*i + 1] = -1  # d_{i,c}+

                gp_b_eq = [target_prod, target_fert, target_pest] + list(target_crop_areas)
                gp_bounds = [(min_alloc, None)] * n + [(0, None)] * (6 + 2*n)

            else:
                # Global Goals Only GP
                nv = n + 6
                gp_c = np.zeros(nv)
                gp_c[n]   = 1    # d1-
                gp_c[n+3] = 1    # d2+
                gp_c[n+5] = 1    # d3+

                gp_A_ub = np.zeros((1, nv)); gp_A_ub[0, :n] = 1
                gp_b_ub = [max_land]

                gp_A_eq = np.zeros((3, nv))
                gp_A_eq[0, :n] = yields; gp_A_eq[0, n]   =  1; gp_A_eq[0, n+1] = -1
                gp_A_eq[1, :n] = ferts;  gp_A_eq[1, n+2] =  1; gp_A_eq[1, n+3] = -1
                gp_A_eq[2, :n] = pests;  gp_A_eq[2, n+4] =  1; gp_A_eq[2, n+5] = -1
                gp_b_eq = [target_prod, target_fert, target_pest]
                gp_bounds = [(min_alloc, None)] * n + [(0, None)] * 6

            gp_res = linprog(gp_c, A_ub=gp_A_ub, b_ub=gp_b_ub,
                             A_eq=gp_A_eq, b_eq=gp_b_eq,
                             bounds=gp_bounds, method='highs')

            gp_alloc       = gp_res.x[:n] if gp_res.success else np.zeros(n)
            gp_status_text = "SciPy HiGHS Optimal ✅" if gp_res.success else "Infeasible ❌"

            # Deviation vars from GP
            if gp_res.success:
                gp_devs = gp_res.x[n:]
                d1m, d1p = gp_devs[0], gp_devs[1]  # production
                d2m, d2p = gp_devs[2], gp_devs[3]  # fertilizer
                d3m, d3p = gp_devs[4], gp_devs[5]  # pesticide
            else:
                d1m = d1p = d2m = d2p = d3m = d3p = 0

        gp_results    = {c: float(gp_alloc[i]) for i, c in enumerate(selected_crops)}
        gp_total_prod = float(yields @ gp_alloc)
        gp_fert_used  = float(ferts @ gp_alloc)
        gp_pest_used  = float(pests @ gp_alloc)
        gp_land_used  = float(gp_alloc.sum())

        # ── RESULTS ───────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("## 🏆 Optimization Results")

        # Status banner
        b1, b2 = st.columns(2)
        b1.success(f"**LP:** {lp_status_text} | Max Production: **{lp_total_prod:,.2f} tons**")
        b2.info(f"**GP:** {gp_status_text} | Balanced Production: **{gp_total_prod:,.2f} tons**")

        # ── Land Allocation Chart ──────────────────────────────────────────
        st.markdown("### 📊 Land Allocation Comparison")
        col_chart1, col_chart2 = st.columns([1.2, 1])

        with col_chart1:
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
                                    xaxis_tickangle=-30, height=420)
            st.plotly_chart(fig_alloc, use_container_width=True)

        with col_chart2:
            # Donut chart for GP Land Allocation Percentage (%)
            gp_pie_labels = [c for c in selected_crops if gp_results[c] > 0]
            gp_pie_values = [gp_results[c] for c in selected_crops if gp_results[c] > 0]
            if sum(gp_pie_values) > 0:
                fig_pie = go.Figure(data=[go.Pie(
                    labels=gp_pie_labels,
                    values=gp_pie_values,
                    hole=0.4,
                    textinfo='label+percent',
                    insidetextorientation='radial'
                )])
                fig_pie.update_layout(title="GP Land Allocation Share (%)", height=420)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No land allocated by GP.")

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

        with st.expander("📐 LP Objective Function, Constraints & Variable Values — Expanded", expanded=True):
            lp_obj_terms = " + ".join([f"({params[c]['Yield']:.2f} × x_{i+1}[{c}])" for i, c in enumerate(selected_crops)])
            st.markdown(f"""
**Objective Function (Maximize Production):**
$$Z_{{LP}} = \sum (Yield_i \cdot x_i) = {lp_obj_terms}$$

**Subject to Constraints:**
- **Land Limit:** {' + '.join([f'x_{i+1}' for i in range(n)])} ≤ **{max_land:,.0f} ha**
- **Fertilizer Limit:** {' + '.join([f'({params[c]["Fertilizer"]:.1f} × x_{i+1})' for i,c in enumerate(selected_crops)])} ≤ **{max_fert:,.0f} kg**
- **Pesticide Limit:** {' + '.join([f'({params[c]["Pesticide"]:.2f} × x_{i+1})' for i,c in enumerate(selected_crops)])} ≤ **{max_pest:,.0f} kg**
- **Minimum Diversity Floor:** x₁, x₂, ... ≥ **{min_alloc:,.1f} ha** (Minimum {diversity_pct}% per crop)

**Exact Decision Variable Solved Values ($x_i$):**
| Variable | Crop Name | Solved Allocation (ha) | Land Share (%) |
|---|---|---|---|
""" + "\n".join([f"| x_{i+1} | **{c}** | {lp_results[c]:,.2f} ha | {(lp_results[c]/max(lp_land_used,1)*100):.1f}% |" for i, c in enumerate(selected_crops)]) + f"""

💡 **Linear Programming vs Goal Programming Formulation:**
- **Linear Programming:** Focuses on single-objective maximization ($Z_{LP} = \sum Yield_i \cdot x_i$) under hard upper bound constraints (Land, Fertilizer, Pesticide).
- **Goal Programming:** Focuses on multi-objective target balancing by minimizing weighted penalty deviations ($Z_{GP} = \sum w_k \cdot d_k$) from target goals.
            """)

        with st.expander("🎯 GP Objective Function, Goal Constraints & Variable Values — Expanded", expanded=True):
            st.markdown(f"""
**Objective Function (Minimize Deviations):**
$$Z_{{GP}} = w_1 \cdot d_1^- + w_2 \cdot d_2^+ + w_3 \cdot d_3^+ + \sum w_{{i,crop}} (d_{{i,crop}}^- + d_{{i,crop}}^+)$$

- **d₁⁻** = amount we **fall short** of production target (penalized)
- **d₂⁺** = amount we **exceed** fertilizer target (penalized)
- **d₃⁺** = amount we **exceed** pesticide target (penalized)

**Goal Constraints Equations (With Substituted Numbers):**
- **Goal 1 (Production):** {' + '.join([f'({params[c]["Yield"]:.2f} × x_{i+1})' for i,c in enumerate(selected_crops)])} + d₁⁻ − d₁⁺ = **{target_prod:,.0f} tons**
- **Goal 2 (Fertilizer):** {' + '.join([f'({params[c]["Fertilizer"]:.1f} × x_{i+1})' for i,c in enumerate(selected_crops)])} + d₂⁻ − d₂⁺ = **{target_fert:,.0f} kg**
- **Goal 3 (Pesticide):** {' + '.join([f'({params[c]["Pesticide"]:.2f} × x_{i+1})' for i,c in enumerate(selected_crops)])} + d₃⁻ − d₃⁺ = **{target_pest:,.0f} kg**

**Exact Solved Decision Variables ($x_i$) & Goal Deviations ($d_k$):**
| Variable | Description / Target | Solved Value | Goal Fulfillment Status |
|---|---|---|---|
""" + "\n".join([f"| x_{i+1} | Land for **{c}** | {gp_results[c]:,.2f} ha | Solved Land Allocation |" for i, c in enumerate(selected_crops)]) + f"""
| d₁⁻ | Production Shortfall | {d1m:,.2f} tons | {"✅ Goal Satisfied" if d1m < 1 else "⚠️ Shortfall"} |
| d₁⁺ | Production Surplus | {d1p:,.2f} tons | {"ℹ️ Over-achieved" if d1p > 1 else "✅ Target Met"} |
| d₂⁻ | Fertilizer Under-use | {d2m:,.2f} kg | {"ℹ️ Saved Budget" if d2m > 1 else "✅ Target Met"} |
| d₂⁺ | Fertilizer Overshoot | {d2p:,.2f} kg | {"✅ Limit Respected" if d2p < 1 else "⚠️ Budget Exceeded"} |
| d₃⁻ | Pesticide Under-use | {d3m:,.2f} kg | {"ℹ️ Saved Budget" if d3m > 1 else "✅ Target Met"} |
| d₃⁺ | Pesticide Overshoot | {d3p:,.2f} kg | {"✅ Limit Respected" if d3p < 1 else "⚠️ Budget Exceeded"} |

**Why Area & Yield are not separate GP goals:**
- *Area ($x_i$)* is the **decision variable** being solved for. Minimum land bounds ($x_i \ge \text{{min\_alloc}}$) and historical target shares ($A_i^{{\text{{target}}}}$) are enforced.
- *Yield* per hectare is a **fixed historical coefficient** derived from data.
- *Rainfall* is a **fixed exogenous parameter** per state-year.
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

        # ── Advanced Chart Simulation Dropdown ──────────────────────────────
        st.markdown("---")
        st.markdown("### 🔬 Advanced Interactive Graph Simulation & Data Statistics")
        sim_chart_choice = st.selectbox(
            "Select an Advanced Simulation Chart / Statistic View:",
            [
                "🌾 Yield vs. Fertilizer Footprint Scatter (Efficiency Spectrum)",
                "🧪 Fertilizer Efficiency Index (Yield / Fertilizer Ratio)",
                "📊 Resource Consumption Spectrum (LP vs GP vs Limits)"
            ],
            key="tab7_sim_chart"
        )

        if "Yield vs. Fertilizer" in sim_chart_choice:
            fig_sim = px.scatter(
                x=[params[c]['Fertilizer'] for c in selected_crops],
                y=[params[c]['Yield'] for c in selected_crops],
                size=[lp_results[c] + 10 for c in selected_crops],
                color=selected_crops,
                labels={'x': 'Fertilizer Rate (kg/ha)', 'y': 'Yield (tons/ha)'},
                title="Yield vs. Fertilizer Rate per Crop (Bubble Size = LP Land Allocated)",
                hover_name=selected_crops
            )
            fig_sim.update_layout(height=400)
            st.plotly_chart(fig_sim, use_container_width=True)

        elif "Fertilizer Efficiency Index" in sim_chart_choice:
            eff_ratios = [params[c]['Yield'] / max(params[c]['Fertilizer'], 0.1) for c in selected_crops]
            fig_eff = go.Figure(go.Bar(
                x=selected_crops, y=eff_ratios,
                marker_color='#10b981',
                text=[f"{r:.4f} t/kg" for r in eff_ratios],
                textposition='outside'
            ))
            fig_eff.update_layout(title="Fertilizer Output Efficiency Index (Tons Yield per kg Fertilizer)",
                                  yaxis_title="Efficiency Ratio (tons/kg)", height=400)
            st.plotly_chart(fig_eff, use_container_width=True)

        elif "Resource Consumption" in sim_chart_choice:
            fig_spectrum = go.Figure()
            fig_spectrum.add_trace(go.Bar(name='Available Capacity', x=['Land (ha)', 'Fertilizer (kg)', 'Pesticide (kg)'],
                                          y=[max_land, max_fert, max_pest], marker_color='#94a3b8'))
            fig_spectrum.add_trace(go.Bar(name='LP Consumption', x=['Land (ha)', 'Fertilizer (kg)', 'Pesticide (kg)'],
                                          y=[lp_land_used, lp_fert_used, lp_pest_used], marker_color='#3b82f6'))
            fig_spectrum.add_trace(go.Bar(name='GP Consumption', x=['Land (ha)', 'Fertilizer (kg)', 'Pesticide (kg)'],
                                          y=[gp_land_used, gp_fert_used, gp_pest_used], marker_color='#f97316'))
            fig_spectrum.update_layout(barmode='group', title="Resource Capacity vs Actual Consumption Spectrum", height=400)
            st.plotly_chart(fig_spectrum, use_container_width=True)

        # ── Final Interpretation & Novelty ──────────────────────────────────
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
as possible to all goals simultaneously. Land is distributed across crops to maintain cropping pattern stability.

**Key Insight for Final Review:** LP gives you the theoretical maximum. GP gives you the practical optimum that
a real farmer or policy maker would actually implement — balancing yield, cost, and sustainability.
        """)

        st.markdown("""
        <div class="highlight-box">
        <h4>💡 Why Goal Programming Matters — The Value Proposition</h4>
        <p><b>Question:</b> <i>If target variables in GP are set to historical averages, won't GP produce results nearly identical to historical land shares? What's the value of GP then?</i></p>
        <p><b>Answer & Core Value:</b></p>
        <ul>
            <li><b>Static History vs. Dynamic Policy:</b> Historical data reflects what happened under <i>past conditions</i>. But if a state faces a 20% fertilizer quota reduction, drought water limits, or new production quotas, historical allocation violates the new constraints!</li>
            <li><b>Mathematical Rebalancing:</b> GP recalculates land distribution dynamically to hit the new targets with minimal deviation penalties, whereas copying past shares would result in infeasibility or severe chemical overshoots.</li>
            <li><b>Trade-off Resolution:</b> GP allows decision-makers to prioritize conflicting goals (e.g. prioritizing chemical reduction over raw tonnage, or vice versa) via penalty weights ($w_k$).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 💎 Research Novelty & Target Stakeholders")
        n_col1, n_col2 = st.columns(2)
        with n_col1:
            st.markdown("""
            #### 🚀 Project Novelty & Innovation
            - **Dynamic Coefficient Derivation:** Coefficients are calculated dynamically per State × Season × Year directly from historical data.
            - **Cropping Pattern Balancing GP Algorithm:** Resolves the classic LP monoculture trap by embedding historical land-share goals into GP equations.
            - **Hybrid Optimization Spectrum:** Allows users to compare theoretical maximum (LP) vs. practical multi-objective optimum (GP) side-by-side.
            """)
        with n_col2:
            st.markdown("""
            #### 🎯 Target Stakeholders & Utility
            - **State Agriculture Departments & Policy Makers:** For regional fertilizer subsidy planning & production goal setting.
            - **Farmers' Cooperatives & Agronomists:** For land diversification, risk reduction, and sowing recommendations.
            - **Agricultural Economists:** For analyzing trade-offs between yield maximization and chemical reduction.
            """)


# --- 8. Crop Advisory & Recommendation ---
elif nav == "8. Crop Advisory & Recommendation":
    st.markdown('<p class="section-header">🌾 Smart Crop Advisory & Recommendation System</p>', unsafe_allow_html=True)
    st.info("💡 **Present-Day Decision Support System (2024 / Now):** Select your State, Season, and Available Land. The system computes historical benchmarks across all multi-year dataset records for your region and generates data-driven sowing recommendations for Linear Programming (Max Tonnage) and Goal Programming (Balanced Multi-Crop Portfolio).")

    try:
        df = pd.read_csv("crop_yield.csv")
        df['Season'] = df['Season'].str.strip()
        df['State']  = df['State'].str.strip()
        df['Crop']   = df['Crop'].str.strip()
    except FileNotFoundError:
        st.error("Dataset not found!")
        st.stop()

    adv_states = sorted(df['State'].dropna().unique())
    adv_seasons = sorted(df['Season'].dropna().unique())

    a1, a2, a3 = st.columns(3)
    adv_state  = a1.selectbox("📍 Target Region / State", adv_states, key="adv_state")
    adv_season = a2.selectbox("🌾 Cultivation Season", adv_seasons, key="adv_season")
    adv_land   = a3.number_input("📐 Total Available Land (Hectares)", min_value=10.0, value=2500.0, step=100.0)

    # Filter historical dataset across ALL years for this State & Season
    df_adv = df[(df['State'] == adv_state) & (df['Season'] == adv_season)]
    adv_crops = sorted(df_adv['Crop'].dropna().unique())

    if not adv_crops:
        st.warning(f"No historical crop data available for {adv_state} / {adv_season}.")
        st.stop()

    # Compute multi-year baseline parameters for all crops in this State & Season
    adv_params = {}
    for crop in adv_crops:
        cd = df_adv[df_adv['Crop'] == crop]
        yld  = float(cd['Yield'].mean()) if not cd['Yield'].empty else 1.0
        area = float(cd['Area'].mean()) if not cd['Area'].empty else 1.0
        prod = float(cd['Production'].mean()) if not cd['Production'].empty else 0.0
        fert = float(cd['Fertilizer'].mean()) if not cd['Fertilizer'].empty else 0.0
        pest = float(cd['Pesticide'].mean()) if not cd['Pesticide'].empty else 0.0
        fpha = fert / area if area > 0 else 50.0
        ppha = pest / area if area > 0 else 5.0
        adv_params[crop] = {
            'Yield': yld if not np.isnan(yld) and yld > 0 else 1.0,
            'Fertilizer': fpha if not np.isnan(fpha) else 50.0,
            'Pesticide': ppha if not np.isnan(ppha) else 5.0,
            'Area': area, 'Production': prod
        }

    n_adv = len(adv_crops)
    adv_yields = np.array([adv_params[c]['Yield'] for c in adv_crops])
    adv_ferts  = np.array([adv_params[c]['Fertilizer'] for c in adv_crops])
    adv_pests  = np.array([adv_params[c]['Pesticide'] for c in adv_crops])
    adv_areas  = np.array([adv_params[c]['Area'] for c in adv_crops])

    rec_total_area = adv_areas.sum()
    target_crop_areas_a = adv_land * (adv_areas / max(rec_total_area, 1.0))
    
    # Baseline benchmarks
    benchmark_prod = float(adv_yields @ target_crop_areas_a)
    benchmark_fert = float(adv_ferts @ target_crop_areas_a)
    benchmark_pest = float(adv_pests @ target_crop_areas_a)

    st.markdown("---")
    st.markdown("### 🎛️ Customize Constraints & Goals for Your Farm")
    st.caption("We have pre-filled the recommended data-driven benchmarks below. You can adjust them to simulate your custom budget, chemical caps, or target goals!")

    c_col1, c_col2, c_col3 = st.columns(3)
    sim_max_fert = c_col1.number_input(
        "🧪 Max Fertilizer Budget (kg)", min_value=100.0,
        value=float(benchmark_fert), step=5000.0,
        help=f"Recommended: {benchmark_fert:,.0f} kg based on regional historical average."
    )
    sim_max_pest = c_col2.number_input(
        "🐛 Max Pesticide Budget (kg)", min_value=10.0,
        value=float(benchmark_pest), step=500.0,
        help=f"Recommended: {benchmark_pest:,.0f} kg based on regional historical average."
    )
    sim_target_prod = c_col3.number_input(
        "🌾 Target Production (tons) [GP]", min_value=100.0,
        value=float(benchmark_prod * 0.95), step=1000.0,
        help=f"Recommended: {benchmark_prod*0.95:,.0f} tons (95% of expected historical yield)."
    )

    # ── Solve Advisory Optimization ──────────────────────────────────────
    from scipy.optimize import linprog

    # 1. LP Solve
    lp_c_a = -adv_yields
    lp_A_a = np.vstack([np.ones(n_adv), adv_ferts, adv_pests])
    lp_b_a = [adv_land, sim_max_fert, sim_max_pest]
    lp_bounds_a = [(0.01 * adv_land / n_adv, None)] * n_adv

    lp_res_a = linprog(lp_c_a, A_ub=lp_A_a, b_ub=lp_b_a, bounds=lp_bounds_a, method='highs')
    lp_adv_alloc = lp_res_a.x if lp_res_a.success else target_crop_areas_a

    # 2. GP Solve (Multi-Goal Pattern Balancing)
    nv_a = n_adv + 6 + 2 * n_adv
    gp_c_a = np.zeros(nv_a)
    gp_c_a[n_adv]   = 10.0 / max(sim_target_prod, 1.0)
    gp_c_a[n_adv+3] = 10.0 / max(sim_max_fert, 1.0)
    gp_c_a[n_adv+5] = 10.0 / max(sim_max_pest, 1.0)

    for i in range(n_adv):
        w_c = 1.0 / max(target_crop_areas_a[i], 1.0)
        gp_c_a[n_adv + 6 + 2*i]     = w_c
        gp_c_a[n_adv + 6 + 2*i + 1] = w_c

    gp_A_ub_a = np.zeros((1, nv_a)); gp_A_ub_a[0, :n_adv] = 1
    gp_b_ub_a = [adv_land]

    gp_A_eq_a = np.zeros((3 + n_adv, nv_a))
    gp_A_eq_a[0, :n_adv] = adv_yields; gp_A_eq_a[0, n_adv]   = 1; gp_A_eq_a[0, n_adv+1] = -1
    gp_A_eq_a[1, :n_adv] = adv_ferts;  gp_A_eq_a[1, n_adv+2] = 1; gp_A_eq_a[1, n_adv+3] = -1
    gp_A_eq_a[2, :n_adv] = adv_pests;  gp_A_eq_a[2, n_adv+4] = 1; gp_A_eq_a[2, n_adv+5] = -1

    for i in range(n_adv):
        gp_A_eq_a[3 + i, i]               = 1
        gp_A_eq_a[3 + i, n_adv + 6 + 2*i]     = 1
        gp_A_eq_a[3 + i, n_adv + 6 + 2*i + 1] = -1

    gp_b_eq_a = [sim_target_prod, sim_max_fert, sim_max_pest] + list(target_crop_areas_a)
    gp_res_a = linprog(gp_c_a, A_ub=gp_A_ub_a, b_ub=gp_b_ub_a, A_eq=gp_A_eq_a, b_eq=gp_b_eq_a, bounds=[(0.01*adv_land/n_adv, None)]*nv_a, method='highs')
    gp_adv_alloc = gp_res_a.x[:n_adv] if gp_res_a.success else target_crop_areas_a

    # ── Display Recommendations ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🌟 Smart Recommended Sowing Portfolios")

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown("#### 🥇 Linear Programming Sowing Plan (Max Production)")
        top_lp_idx = np.argmax(lp_adv_alloc)
        st.success(f"""
        **Top Focus Crop:** `{adv_crops[top_lp_idx]}`
        - **Allocated Area:** {lp_adv_alloc[top_lp_idx]:,.0f} ha ({lp_adv_alloc[top_lp_idx]/adv_land*100:.1f}% of land)
        - **Expected Total Production:** {adv_yields @ lp_adv_alloc:,.0f} tons
        - **Fertilizer Used:** {adv_ferts @ lp_adv_alloc:,.0f} kg
        - **Best For:** Maximum single-commodity tonnage and industrial supply contracts.
        """)

    with r_col2:
        st.markdown("#### 🛡️ Goal Programming Sowing Plan (Diversified Mix)")
        top_gp_indices = np.argsort(gp_adv_alloc)[::-1][:min(3, n_adv)]
        top_gp_str = ", ".join([f"`{adv_crops[i]}` ({gp_adv_alloc[i]/adv_land*100:.1f}%)" for i in top_gp_indices])
        st.info(f"""
        **Recommended Crop Portfolio:** {top_gp_str}
        - **Allocated Area:** Balanced across {sum(1 for a in gp_adv_alloc if a > 1)} crops
        - **Expected Total Production:** {adv_yields @ gp_adv_alloc:,.0f} tons
        - **Fertilizer Used:** {adv_ferts @ gp_adv_alloc:,.0f} kg
        - **Best For:** Risk mitigation, food security, and maintaining soil health.
        """)

    # ── Sowing Guide Table & Donut Chart ─────────────────────────────────
    st.markdown("---")
    st.markdown("### 📋 Detailed Crop Sowing Breakdown")

    chart_tab, table_tab = st.tabs(["📊 Land Allocation Donut Chart", "📋 Sowing Guide Table"])

    with chart_tab:
        fig_adv_pie = go.Figure(data=[go.Pie(
            labels=[c for i, c in enumerate(adv_crops) if gp_adv_alloc[i] > 1],
            values=[gp_adv_alloc[i] for i in range(n_adv) if gp_adv_alloc[i] > 1],
            hole=0.4, textinfo='label+percent'
        )])
        fig_adv_pie.update_layout(title=f"GP Recommended Crop Portfolio Distribution for {adv_state} ({adv_season})", height=450)
        st.plotly_chart(fig_adv_pie, use_container_width=True)

    with table_tab:
        adv_df = pd.DataFrame({
            'Crop Name': adv_crops,
            'LP Area (ha)': [lp_adv_alloc[i] for i in range(n_adv)],
            'GP Area (ha)': [gp_adv_alloc[i] for i in range(n_adv)],
            'GP Share (%)': [(gp_adv_alloc[i] / adv_land * 100) for i in range(n_adv)],
            'Yield (tons/ha)': [adv_yields[i] for i in range(n_adv)],
            'Est. GP Prod (tons)': [adv_yields[i] * gp_adv_alloc[i] for i in range(n_adv)],
        })
        st.dataframe(adv_df.sort_values(by='GP Area (ha)', ascending=False).style.format({
            'LP Area (ha)': '{:,.1f}',
            'GP Area (ha)': '{:,.1f}',
            'GP Share (%)': '{:.2f}%',
            'Yield (tons/ha)': '{:.2f}',
            'Est. GP Prod (tons)': '{:,.1f}'
        }), use_container_width=True, hide_index=True)

    # ── Regional Advanced Simulation Dropdown for Tab 8 ──────────────────
    st.markdown("---")
    st.markdown("### 🔬 Regional Historical Analytics & Interactive Chart Simulations")
    sim_chart_adv = st.selectbox(
        "Select Regional Simulation View:",
        [
            "🌾 Land Share (%) vs Production Contributed Share (%)",
            "🧪 Regional Fertilizer Intensity per Crop (kg/ha)",
            "📈 Expected Crop Production Contribution Breakdown (tons)"
        ],
        key="tab8_sim_chart"
    )

    if "Land Share (%) vs Production" in sim_chart_adv:
        land_shares = [(gp_adv_alloc[i] / adv_land * 100) for i in range(n_adv)]
        gp_prods = [adv_yields[i] * gp_adv_alloc[i] for i in range(n_adv)]
        tot_gp_prod = sum(gp_prods)
        prod_shares = [(gp_prods[i] / max(tot_gp_prod, 1.0) * 100) for i in range(n_adv)]

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name='Land Share (%)', x=adv_crops, y=land_shares, marker_color='#3b82f6'))
        fig_comp.add_trace(go.Bar(name='Production Share (%)', x=adv_crops, y=prod_shares, marker_color='#22c55e'))
        fig_comp.update_layout(barmode='group', title=f"Land Allocated (%) vs Production Contributed (%) — {adv_state}", height=400)
        st.plotly_chart(fig_comp, use_container_width=True)

    elif "Fertilizer Intensity" in sim_chart_adv:
        fig_fert_int = go.Figure(go.Bar(
            x=adv_crops, y=adv_ferts,
            marker_color='#f59e0b',
            text=[f"{f:.1f} kg/ha" for f in adv_ferts],
            textposition='outside'
        ))
        fig_fert_int.update_layout(title=f"Regional Fertilizer Rate per Hectare — {adv_state} ({adv_season})",
                                   yaxis_title="Fertilizer Rate (kg/ha)", height=400)
        st.plotly_chart(fig_fert_int, use_container_width=True)

    elif "Expected Crop Production" in sim_chart_adv:
        gp_prods = [adv_yields[i] * gp_adv_alloc[i] for i in range(n_adv)]
        fig_prod_b = go.Figure(go.Bar(
            x=adv_crops, y=gp_prods,
            marker_color='#6366f1',
            text=[f"{p:,.0f} t" for p in gp_prods],
            textposition='outside'
        ))
        fig_prod_b.update_layout(title=f"Expected Production Contribution per Crop (tons) — {adv_state}", height=400)
        st.plotly_chart(fig_prod_b, use_container_width=True)


# --- 9. Team Contribution ---

elif nav == "9. Team Contribution":
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
    st.markdown("### 🏁 Project Completion Status")
    st.write("We have successfully built, debugged, and deployed the complete Operations Research Crop Planning System featuring Linear Programming, Goal Programming, Data-Driven Parameter Engine, and Smart Advisory System.")


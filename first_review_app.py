import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

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

# --- 7. Proposed Final Dashboard ---
elif nav == "7. Final Dashboard":
    st.markdown('<p class="section-header">Proposed Final System Architecture</p>', unsafe_allow_html=True)
    st.info("⚙️ **Note:** This tab is a conceptual mockup. The actual LP and GP engines will be wired up here for the Final Review.")
    
    st.markdown("### 🎛️ Optimization Control Panel")
    c1, c2, c3 = st.columns(3)
    c1.selectbox("Target State", ["Andhra Pradesh", "Karnataka", "Tamil Nadu", "Maharashtra"])
    c2.selectbox("Season", ["Kharif", "Rabi", "Whole Year"])
    c3.multiselect("Crops to Consider", ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane"], default=["Rice", "Wheat", "Maize"])
    
    st.markdown("#### 📏 Resource Constraints")
    rc1, rc2, rc3 = st.columns(3)
    rc1.slider("Available Land (Hectares)", 1000, 50000, 10000)
    rc2.slider("Max Fertilizer (kg)", 10000, 1000000, 500000)
    rc3.slider("Max Pesticide (kg)", 1000, 50000, 20000)
    
    st.button("🚀 Run Optimization Engine (Final Review)", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Expected Output Dashboard (Mockup)")
    
    out1, out2 = st.columns(2)
    with out1:
        # Mock LP vs GP Bar chart
        fig = go.Figure(data=[
            go.Bar(name='LP Allocation (ha)', x=['Rice', 'Wheat', 'Maize'], y=[7000, 3000, 0]),
            go.Bar(name='GP Allocation (ha)', x=['Rice', 'Wheat', 'Maize'], y=[4000, 3500, 2500])
        ])
        fig.update_layout(barmode='group', title="Land Allocation Recommendation")
        st.plotly_chart(fig, use_container_width=True)
    with out2:
        # Mock resource usage
        fig2 = go.Figure(data=[
            go.Bar(name='Used', x=['Land', 'Fertilizer', 'Pesticide'], y=[100, 98, 40]),
            go.Bar(name='Remaining', x=['Land', 'Fertilizer', 'Pesticide'], y=[0, 2, 60])
        ])
        fig2.update_layout(barmode='stack', title="Resource Utilization (%)")
        st.plotly_chart(fig2, use_container_width=True)

# --- 8. Team Contribution ---
elif nav == "8. Team Contribution":
    st.markdown('<p class="section-header">Team Responsibilities</p>', unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.columns(4)
    t1.success("**Sanjay**\n\nDataset Acquisition\n\nData Cleaning\n\nExploratory Data Analysis\n\nParameter Calculations")
    t2.info("**Vignesh**\n\nLinear Programming Model\n\nDecision Variables\n\nObjective Functions\n\nLP Solver Code")
    t3.warning("**Ruban**\n\nGoal Programming Model\n\nDeviation Variables\n\nGoal Weighting\n\nGP Solver Code")
    t4.error("**Hari**\n\nStreamlit UI Development\n\nPlotly Visualizations\n\nSystem Integration\n\nDashboard Finalization")
    
    st.markdown("---")
    st.markdown("### 🏁 First Review Boundary")
    st.write("We have successfully identified the dataset, cleaned the data, established the research methodology, and formulated both the Linear Programming and Goal Programming approaches mathematically.")
    st.write("In the final review, we will present the fully functional optimization engine integrated directly into this dashboard.")

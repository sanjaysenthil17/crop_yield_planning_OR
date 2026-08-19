import streamlit as st
import pandas as pd
import numpy as np

# Page Config
st.set_page_config(page_title="First Review: Crop Planning OR", layout="wide")

st.title("Optimal Agricultural Crop Planning")
st.subheader("Using Linear Programming and Goal Programming (First Review Demo)")

st.markdown("---")

# Sidebar for Navigation
st.sidebar.title("Navigation")
nav = st.sidebar.radio("Go to", [
    "1. Introduction & Problem", 
    "2. Dataset & EDA", 
    "3. Methodology & OR Concept",
    "4. Proposed Final System (Mockup)",
    "5. Team Contribution"
])

# 1. Introduction
if nav == "1. Introduction & Problem":
    st.header("Project Introduction")
    st.write("""
    Agricultural crop planning is the process of deciding which crops to plant and how much land to allocate to each. 
    In India, farmers have limited resources to work with:
    - **Land:** A fixed amount of cultivable area.
    - **Fertilizer & Pesticide:** Limited quantities or budgets.
    - **Water:** Dependent on rainfall and irrigation.
    
    Different crops have varying yield rates and resource requirements. Our project aims to use **Operations Research** 
    to help decide how available land can be allocated among selected crops to obtain good expected production while respecting resource limitations.
    """)
    
    st.header("Problem Statement")
    st.info("""
    **"Given historical crop and resource data, how can available land be allocated among selected crops 
    to obtain good expected production while respecting resource limitations?"**
    """)
    st.write("""
    Later in the final project, we will use:
    - **Linear Programming (LP):** For maximizing expected total production.
    - **Goal Programming (GP):** For finding a balanced solution when we have multiple competing goals.
    """)
    
    st.header("Project Significance")
    st.write("""
    - Better utilization of limited agricultural resources
    - Data-driven crop planning
    - Understanding crop yield and production patterns
    - Helping compare different crop planning scenarios
    - Demonstrating how Operations Research can be applied to a real-world agricultural problem
    """)

# 2. Dataset & EDA
elif nav == "2. Dataset & EDA":
    st.header("Dataset Section")
    st.write("We are using the 'Agricultural Crop Yield in Indian States Dataset' (1997–2020).")
    
    try:
        df = pd.read_csv("crop_yield.csv")
        st.success("Dataset loaded successfully!")
        
        st.subheader("Dataset Overview (First 10 Rows)")
        st.dataframe(df.head(10))
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        col3.metric("Unique Crops", df['Crop'].nunique())
        col4.metric("Unique States", df['State'].nunique())
        
        st.subheader("Dataset Explanation")
        st.write("""
        - **Crop:** Name of crop
        - **Crop_Year:** Year of cultivation
        - **Season:** Agricultural season
        - **State:** Indian state
        - **Area:** Cultivated area in hectares
        - **Production:** Production in metric tons
        - **Annual_Rainfall:** Rainfall in millimetres
        - **Fertilizer & Pesticide:** Usage in kilograms
        - **Yield:** Production per unit area
        """)
        
        st.subheader("Exploratory Data Analysis (EDA)")
        
        try:
            import plotly.express as px
            
            c1, c2 = st.columns(2)
            
            with c1:
                # Crop distribution
                crop_counts = df['Crop'].value_counts().reset_index()
                crop_counts.columns = ['Crop', 'Count']
                fig1 = px.pie(crop_counts, values='Count', names='Crop', title="Crop Distribution")
                st.plotly_chart(fig1, use_container_width=True)
                
                # Average Yield by Crop
                yield_data = df.groupby('Crop')['Yield'].mean().reset_index()
                fig3 = px.bar(yield_data, x='Crop', y='Yield', title="Average Yield by Crop (tons/ha)")
                st.plotly_chart(fig3, use_container_width=True)
                
            with c2:
                # State-wise production
                state_prod = df.groupby('State')['Production'].sum().reset_index()
                fig2 = px.bar(state_prod, x='State', y='Production', title="Total Production by State")
                st.plotly_chart(fig2, use_container_width=True)
                
                # Rainfall vs Yield
                fig4 = px.scatter(df, x='Annual_Rainfall', y='Yield', color='Crop', title="Rainfall vs Yield")
                st.plotly_chart(fig4, use_container_width=True)
                
        except ImportError:
            st.warning("Please install Plotly (`pip install plotly`) to view the interactive charts.")
            
    except FileNotFoundError:
        st.error("Dataset 'crop_dataset.csv' not found. Please ensure the file is in the same directory.")
        
    st.header("Research / Planning Questions")
    st.write("""
    **Questions answered through dataset analysis in the FIRST REVIEW:**
    - Which crops have the highest average yield?
    - Which crops have the highest production?
    - How does crop production vary across states and seasons?
    - What is the relationship between rainfall and crop yield?
    
    **Optimization questions that will be addressed in the FINAL PROJECT:**
    - Which crops appear more suitable when land is limited?
    - How can available land eventually be allocated among selected crops?
    - How can we maximize expected production under land, fertilizer and pesticide constraints?
    - How can we balance multiple objectives using Goal Programming?
    """)

# 3. Methodology & OR Concept
elif nav == "3. Methodology & OR Concept":
    st.header("Methodology")
    st.write("""
    1. Dataset Collection
    2. Data Cleaning
    3. Exploratory Data Analysis **<-- (Current First Review Focus)**
    4. Calculate Historical Yield and Resource Parameters
    5. Define Decision Variables
    6. Linear Programming Formulation
    7. Goal Programming Formulation
    8. Compare Solutions
    9. Final Crop Planning Recommendation
    """)
    
    st.header("Operations Research Concept (Our Approach)")
    
    st.subheader("1. Linear Programming (LP) Approach")
    st.write("""
    **Objective:** Maximize total crop production.
    - Let **$x_i$** be the land (in hectares) allocated to crop $i$.
    - Let **$Y_i$** be the expected yield (tons/ha) of crop $i$.
    
    **Maximize:** $Z = \sum (Y_i \cdot x_i)$
    
    **Subject to Constraints:**
    1. **Land Availability:** $\sum x_i \leq \text{Total Land}$
    2. **Fertilizer Limit:** $\sum (F_i \cdot x_i) \leq \text{Max Fertilizer}$
    3. **Pesticide Limit:** $\sum (P_i \cdot x_i) \leq \text{Max Pesticide}$
    4. **Non-negativity:** $x_i \geq 0$
    """)
    
    st.subheader("2. Goal Programming (GP) Approach")
    st.write("""
    In the real world, farmers don't just want to maximize yield at all costs. They have multiple, sometimes conflicting goals:
    - **Goal 1:** Achieve a target production level.
    - **Goal 2:** Minimize excess fertilizer usage (environmental constraint).
    - **Goal 3:** Ensure a minimum quota for a staple crop (e.g., Rice).
    
    **Approach:** 
    Goal Programming introduces deviation variables ($d^+$ for overachievement, $d^-$ for underachievement). 
    Our objective becomes to **Minimize the weighted sum of unwanted deviations** from these goals.
    """)
    
    st.info("💡 In the Final Review, we will run both models side-by-side to show how GP provides a more balanced real-world solution compared to LP's pure maximization.")
    
    st.header("Tools and Technologies")
    st.write("""
    - **Python:** main programming language
    - **Pandas:** dataset loading and cleaning
    - **NumPy:** numerical calculations
    - **PuLP / OR-Tools:** future optimization solver
    - **Streamlit:** UI and dashboard framework
    - **Plotly:** data visualizations
    - **Antigravity:** AI-assisted development
    """)

# 4. Proposed Final System
elif nav == "4. Proposed Final System (Mockup)":
    st.header("Proposed Final System (Future Implementation)")
    st.info("NOTE: This is a mockup of the UI for the Final Review. The optimization engine is not running yet.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("User Inputs (Mock)")
        st.selectbox("Select State", ["Andhra Pradesh", "Karnataka", "Tamil Nadu", "Maharashtra"])
        st.selectbox("Select Season", ["Kharif", "Rabi", "Whole Year"])
        st.multiselect("Select Crops", ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane"], default=["Rice", "Wheat"])
        
        st.number_input("Total Land Available (Hectares)", value=10000)
        st.number_input("Max Fertilizer Available (kg)", value=500000)
        st.number_input("Max Pesticide Available (kg)", value=20000)
        
        st.button("Run Optimization Engine (Coming Soon)", disabled=True)
        
    with col2:
        st.subheader("Expected Final Outputs")
        st.write("""
        Once the Linear Programming and Goal Programming models are implemented, this section will display:
        - **Optimal crop allocation** (how many hectares per crop)
        - **Expected production** (in metric tons)
        - **Land used vs Land available**
        - **Fertilizer and Pesticide utilized**
        - **LP vs Goal Programming comparison charts**
        st.info("📊 Optimization Results (LP vs GP) and comparison charts will be displayed here in the Final Review.")

# 5. Team Contribution
elif nav == "5. Team Contribution":
    st.header("Team Contribution")
    
    st.write("**Sanjay:**")
    st.write("- Dataset, Data preprocessing, Statistics, Charts, Parameter calculations")
    
    st.write("**Vignesh:**")
    st.write("- Linear Programming, Decision variables, Objective function, Constraints, LP solver")
    
    st.write("**Ruban:**")
    st.write("- Goal Programming, Multiple goals, Deviation variables, Priorities/weights, GP results")
    
    st.write("**Hari:**")
    st.write("- UI and integration, Streamlit dashboard, User inputs, Charts, Connecting modules")
    
    st.markdown("---")
    st.header("Final Review Boundary")
    st.success("""
    **First Review Focus:**
    Understanding the problem, dataset, research questions, methodology and planned Operations Research approach.
    
    **Final Review Focus:**
    Implementation of Linear Programming and Goal Programming, optimization results, interpretation, dashboard and final recommendations.
    """)

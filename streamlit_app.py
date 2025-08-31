"""
VenomVerse - Streamlit Frontend Application
AI-Powered Drug Discovery from Venomous Animals
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import stmol
import py3Dmol

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.venomverse_api import VenomVerseAPI
from backend.molecular_visualizer import MolecularVisualizer
from backend.pdf_generator import PDFGenerator

# Page configuration
st.set_page_config(
    page_title="VenomVerse - AI Drug Discovery",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .kichi {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        animation: blink 4s linear infinite;
    }
    @keyframes blink {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0;
    }
}
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 3rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .disease-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4ECDC4;
        margin: 0.5rem 0;
    }
    
    .protein-card {
        background: linear-gradient(135deg, #8f6d3f 0%, #8f6d3f 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API and visualizer
@st.cache_resource
def get_api():
    return VenomVerseAPI()

@st.cache_resource
def get_visualizer():
    return MolecularVisualizer()

@st.cache_resource
def get_pdf_generator():
    return PDFGenerator()

api = get_api()
visualizer = get_visualizer()
pdf_generator = get_pdf_generator()

# Main header
st.markdown('<h1 class = "kichi">This is a demonstration model and is not intended to replicate or replace a production system.</h1>', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">🐍 VenomVerse</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Drug Discovery from Venomous Animals</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔬 Analysis Controls")
    
    # Species input
    species_input = st.text_input(
        "Enter Venomous Species Name:",
        placeholder="e.g., Cobra, Box Jellyfish, Black Mamba",
        help="Enter the name of any venomous animal"
    )
    
    # Species suggestions
    if species_input:
        suggestions = api.get_species_suggestions(species_input)
        if suggestions:
            st.write("💡 **Suggestions:**")
            for suggestion in suggestions:
                if st.button(suggestion, key=f"suggest_{suggestion}"):
                    species_input = suggestion
                    st.rerun()
    
    # Analysis button
    analyze_button = st.button(
        "🧬 Analyze Venom",
        type="primary",
        use_container_width=True,
        disabled=not species_input
    )
    
    st.divider()
    
    # Information section
    st.header("ℹ️ About VenomVerse")
    st.write("""
    **VenomVerse** uses advanced AI to analyze venomous animal compounds and predict their therapeutic potential.
    
    **Features:**
    - 🎯 Disease prediction using OpenAI API
    - 🧬 Synthetic protein generation with OpenAI models
    - 📊 Market analysis and impact assessment
    - 🔬 3D molecular visualization
    - 📄 Patent-ready documentation
    """)

# Main content area
if analyze_button and species_input:
    with st.spinner(f"🔬 Analyzing {species_input} venom..."):
        try:
            # Perform analysis
            results = api.analyze_species(species_input)
            
            # Store results in session state
            st.session_state.analysis_results = results
            st.session_state.analyzed_species = species_input
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.stop()

# Display results if available
if hasattr(st.session_state, 'analysis_results'):
    results = st.session_state.analysis_results
    
    # Success message
    st.markdown(f"""
    <div class="success-message">
        ✅ <strong>Analysis Complete!</strong> Successfully analyzed {results['venom_analysis']['species']} venom and generated therapeutic predictions.
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎯 Top Disease Target",
            results['top_prediction']['disease'].title(),
            f"{results['top_prediction']['confidence_percentage']}% confidence"
        )
    
    with col2:
        st.metric(
            "🧬 Synthetic Protein",
            results['synthetic_protein']['name'],
            f"MW: {results['synthetic_protein']['properties']['molecular_weight']:,} Da"
        )
    
    with col3:
        st.metric(
            "👥 Potential Patients",
            f"{results['market_analysis']['potential_patients_saved']:,}",
            "Global estimate"
        )
    
    with col4:
        st.metric(
            "💰 Market Value",
            f"${results['market_analysis']['ten_year_market_billions']:.1f}B",
            "10-year projection"
        )
    
    # Detailed results tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Disease Predictions", 
        "🧬 Synthetic Protein", 
        "🔬 3D Structure",
        "📊 Market Analysis", 
        "🔬 Research Abstract",
        "📄 Export Results"
    ])
    
    with tab1:
        st.header("🎯 Disease Prediction Results")
        
        # Disease predictions chart
        diseases = results['venom_analysis']['diseases']
        df_diseases = pd.DataFrame([
            {"Disease": disease.title(), "Confidence": score}
            for disease, score in diseases.items()
        ]).sort_values('Confidence', ascending=True)
        
        fig = px.bar(
            df_diseases, 
            x='Confidence', 
            y='Disease',
            orientation='h',
            title="Therapeutic Potential by Disease",
            color='Confidence',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Venom compounds
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🧪 Key Compounds")
            for compound in results['venom_analysis']['compounds']:
                st.markdown(f"• **{compound}**")
        
        with col2:
            st.subheader("⚙️ Mechanism")
            st.write(results['venom_analysis']['mechanism'])
    
    with tab2:
        st.header("🧬 Synthetic Protein Details")
        
        # Protein overview
        protein = results['synthetic_protein']
        st.markdown(f"""
        <div class="protein-card">
            <h3>🧬 {protein['name']}</h3>
            <p><strong>Type:</strong> {protein['properties']['protein_type']}</p>
            <p><strong>Molecular Weight:</strong> {protein['properties']['molecular_weight']:,} Da</p>
            <p><strong>Amino Acids:</strong> {protein['properties']['amino_acid_count']}</p>
            <p><strong>Stability Score:</strong> {protein['properties']['stability_score']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Protein properties table
        st.subheader("📋 Protein Properties")
        props_df = pd.DataFrame([
            {"Property": "Molecular Weight", "Value": f"{protein['properties']['molecular_weight']:,} Da"},
            {"Property": "Amino Acid Count", "Value": protein['properties']['amino_acid_count']},
            {"Property": "Isoelectric Point", "Value": protein['properties']['isoelectric_point']},
            {"Property": "Stability Score", "Value": protein['properties']['stability_score']},
            {"Property": "Solubility", "Value": protein['properties']['solubility']},
            {"Property": "Expression System", "Value": protein['properties']['expression_system']}
        ])
        st.dataframe(props_df, use_container_width=True, hide_index=True)
        
        # Mechanism description
        st.subheader("⚙️ Mechanism of Action")
        st.markdown(protein['mechanism'])
    
    with tab3:
        st.header("🔬 3D Molecular Structure")
        
        # Generate protein sequence and structure
        protein_name = results['synthetic_protein']['name']
        sequence_length = results['synthetic_protein']['properties']['amino_acid_count']
        
        # Generate molecular data
        protein_sequence = visualizer.generate_protein_sequence(sequence_length, "therapeutic")
        structure_analysis = visualizer.generate_structure_analysis(protein_sequence)
        binding_info = visualizer.generate_binding_site_info(protein_sequence, results['top_prediction']['disease'])
        pdb_structure = visualizer.generate_pdb_structure(protein_sequence, protein_name)
        
        # Display sequence
        st.subheader("🧬 Protein Sequence")
        st.code(protein_sequence, language="text")
        
        # 3D Visualization
        st.subheader("🔬 3D Structure Visualization")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            try:
                # Create 3D molecular visualization
                stmol.showmol(pdb_structure, height=400, width=600)
            except Exception as e:
                st.warning("3D visualization temporarily unavailable. Showing structure data instead.")
                st.text_area("PDB Structure Data", pdb_structure, height=300)
        
        with col2:
            st.subheader("📊 Structure Properties")
            
            # Secondary structure pie chart
            sec_struct_data = structure_analysis['secondary_structure']
            fig_struct = px.pie(
                values=list(sec_struct_data.values()),
                names=list(sec_struct_data.keys()),
                title="Secondary Structure"
            )
            fig_struct.update_layout(height=300)
            st.plotly_chart(fig_struct, use_container_width=True)
        
        # Structure analysis details
        st.subheader("🔍 Detailed Structure Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Amino Acid Composition**")
            for aa_type, percentage in structure_analysis['amino_acid_composition'].items():
                st.write(f"• {aa_type.title()}: {percentage}%")
        
        with col2:
            st.write("**Size Distribution**")
            for size, percentage in structure_analysis['size_distribution'].items():
                st.write(f"• {size.title()}: {percentage}%")
        
        with col3:
            st.write("**Predicted Properties**")
            props = structure_analysis['predicted_properties']
            st.write(f"• Hydrophobicity: {props['hydrophobicity']}%")
            st.write(f"• Charge Ratio: {props['charge_ratio']}%")
            st.write(f"• Stability: {props['stability_score']}")
        
        # Binding sites
        st.subheader("🎯 Predicted Binding Sites")
        
        binding_df = pd.DataFrame(binding_info['binding_sites'])
        if not binding_df.empty:
            st.dataframe(binding_df, use_container_width=True, hide_index=True)
            
            st.metric(
                "Overall Binding Score", 
                f"{binding_info['overall_binding_score']:.3f}",
                "High affinity predicted"
            )
    
    with tab4:
        st.header("📊 Market Analysis")
        
        market = results['market_analysis']
        
        # Market metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Patient Impact")
            st.metric("Potential Patients Saved", f"{market['potential_patients_saved']:,}")
            st.metric("Treatment Efficacy", f"{market['treatment_efficacy']}%")
        
        with col2:
            st.subheader("💰 Market Potential")
            st.metric("Annual Market", f"${market['annual_market_millions']:.1f}M")
            st.metric("10-Year Market Value", f"${market['ten_year_market_billions']:.1f}B")
        
        # Market visualization
        market_data = {
            "Year": list(range(1, 11)),
            "Market Value (Millions)": [market['annual_market_millions'] * (1.1 ** i) for i in range(10)]
        }
        market_df = pd.DataFrame(market_data)
        
        fig = px.line(
            market_df, 
            x='Year', 
            y='Market Value (Millions)',
            title="Projected Market Growth (10-Year Forecast)",
            markers=True
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("🔬 Research Abstract")
        st.markdown(results['research_abstract'])
        
        # Disease information
        disease_info = api.get_disease_info(results['top_prediction']['disease'])
        if disease_info:
            st.subheader(f"📋 {results['top_prediction']['disease'].title()} Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Description:** {disease_info['description']}")
                st.write(f"**Survival Rate:** {disease_info['survival_rate']}")
            
            with col2:
                st.write(f"**Current Treatments:** {', '.join(disease_info['current_treatments'])}")
                st.write(f"**Unmet Need:** {disease_info['unmet_need']}")
    
    with tab6:
        st.header("📄 Export Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📄 JSON Report")
            if st.button("📄 Generate JSON Report", type="primary"):
                json_str = json.dumps(results, indent=2)
                st.download_button(
                    label="💾 Download JSON",
                    data=json_str,
                    file_name=f"venomverse_analysis_{results['venom_analysis']['species'].replace(' ', '_')}.json",
                    mime="application/json"
                )
        
        with col2:
            st.subheader("📋 Summary Report")
            if st.button("📋 Generate Summary", type="secondary"):
                summary = f"""
VenomVerse Analysis Summary
==========================

Species: {results['venom_analysis']['species']}
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TOP PREDICTION:
- Disease: {results['top_prediction']['disease'].title()}
- Confidence: {results['top_prediction']['confidence_percentage']}%

SYNTHETIC PROTEIN:
- Name: {results['synthetic_protein']['name']}
- Molecular Weight: {results['synthetic_protein']['properties']['molecular_weight']:,} Da
- Type: {results['synthetic_protein']['properties']['protein_type']}

MARKET IMPACT:
- Potential Patients: {results['market_analysis']['potential_patients_saved']:,}
- 10-Year Market Value: ${results['market_analysis']['ten_year_market_billions']:.1f}B

Generated by VenomVerse AI Platform
                """.strip()
                
                st.download_button(
                    label="💾 Download Summary",
                    data=summary,
                    file_name=f"venomverse_summary_{results['venom_analysis']['species'].replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        
        with col3:
            st.subheader("📑 Patent Document")
            if st.button("📑 Generate Patent PDF", type="primary"):
                try:
                    with st.spinner("Generating patent document..."):
                        pdf_path = pdf_generator.generate_patent_document(results)
                        
                        # Read the PDF file
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf_data = pdf_file.read()
                        
                        st.download_button(
                            label="💾 Download Patent PDF",
                            data=pdf_data,
                            file_name=f"patent_{results['venom_analysis']['species'].replace(' ', '_')}_{results['synthetic_protein']['name']}.pdf",
                            mime="application/pdf"
                        )
                        st.success("Patent document generated successfully!")
                        
                except Exception as e:
                    st.error(f"PDF generation failed: {str(e)}")
                    st.info("Note: PDF generation requires additional system dependencies.")
        
        st.divider()
        
        # Research Abstract PDF
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔬 Research Abstract PDF")
            if st.button("🔬 Generate Research Abstract", type="secondary"):
                try:
                    with st.spinner("Generating research abstract..."):
                        pdf_path = pdf_generator.generate_research_abstract_pdf(results)
                        
                        # Read the PDF file
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf_data = pdf_file.read()
                        
                        st.download_button(
                            label="💾 Download Research PDF",
                            data=pdf_data,
                            file_name=f"research_abstract_{results['venom_analysis']['species'].replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )
                        st.success("Research abstract generated successfully!")
                        
                except Exception as e:
                    st.error(f"PDF generation failed: {str(e)}")
                    st.info("Note: PDF generation requires additional system dependencies.")
        
        with col2:
            st.subheader("📊 Export Statistics")
            st.metric("Analysis Confidence", f"{results['top_prediction']['confidence_percentage']}%")
            st.metric("Market Potential", f"${results['market_analysis']['ten_year_market_billions']:.1f}B")
            st.metric("Patient Impact", f"{results['market_analysis']['potential_patients_saved']:,}")
            
            st.info("""
            **Export Options:**
            - **JSON**: Complete analysis data
            - **Summary**: Key findings overview  
            - **Patent PDF**: Legal document format
            - **Research PDF**: Academic publication format
            """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    🐍 <strong>VenomVerse</strong> - Powered by OpenAI API | 
    Built for NxtWave OpenAI Buildathon| 
    🧬 Transforming Venom into Medicine
</div>
""", unsafe_allow_html=True)


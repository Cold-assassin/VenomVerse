"""
VenomVerse - Main API Service
Integrates venom analysis and protein generation for the VenomVerse platform
"""

from venom_analyzer import VenomAnalyzer
from protein_generator import ProteinGenerator
from typing import Dict, Any
import json

class VenomVerseAPI:
    def __init__(self):
        self.analyzer = VenomAnalyzer()
        self.generator = ProteinGenerator()
    
    def analyze_species(self, species_name: str) -> Dict[str, Any]:
        """
        Complete analysis pipeline for a venomous species
        Returns comprehensive results including diseases, proteins, and market analysis
        """
        
        # Step 1: Analyze venom using simulated Watsonx.ai
        venom_analysis = self.analyzer.analyze_venom(species_name)
        
        # Step 2: Get top disease prediction
        top_disease, confidence_score = self.analyzer.get_top_disease(venom_analysis)
        
        # Step 3: Generate synthetic protein using simulated Granite
        protein_name = self.generator.generate_protein_name(venom_analysis["species"], top_disease)
        protein_properties = self.generator.generate_protein_properties(protein_name)
        
        # Step 4: Generate mechanism description
        mechanism_description = self.generator.generate_mechanism_description(
            protein_name, 
            venom_analysis["species"], 
            top_disease, 
            venom_analysis["compounds"]
        )
        
        # Step 5: Calculate market impact
        market_impact = self.analyzer.estimate_market_impact(top_disease, confidence_score)
        
        # Step 6: Generate research abstract
        research_abstract = self.generator.generate_research_abstract(
            protein_name,
            venom_analysis["species"],
            top_disease,
            confidence_score,
            market_impact
        )
        
        # Compile comprehensive results
        results = {
            "input": {
                "species_name": species_name,
                "analysis_timestamp": "2025-06-27T12:00:00Z"
            },
            "venom_analysis": venom_analysis,
            "top_prediction": {
                "disease": top_disease,
                "confidence_score": confidence_score,
                "confidence_percentage": round(confidence_score * 100, 1)
            },
            "synthetic_protein": {
                "name": protein_name,
                "properties": protein_properties,
                "mechanism": mechanism_description
            },
            "market_analysis": market_impact,
            "research_abstract": research_abstract,
            "success": True
        }
        
        return results
    
    def get_species_suggestions(self, partial_name: str) -> list:
        """Get species suggestions based on partial input"""
        all_species = list(self.analyzer.venom_database.keys())
        suggestions = []
        
        partial_lower = partial_name.lower()
        for species in all_species:
            if partial_lower in species or species.startswith(partial_lower):
                suggestions.append(species.title())
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def get_disease_info(self, disease_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific disease"""
        disease_info = {
            "glioblastoma": {
                "description": "Aggressive brain cancer with poor prognosis",
                "current_treatments": ["Surgery", "Radiation", "Chemotherapy"],
                "survival_rate": "15 months median",
                "unmet_need": "High - limited treatment options"
            },
            "alzheimer's disease": {
                "description": "Progressive neurodegenerative disorder",
                "current_treatments": ["Cholinesterase inhibitors", "NMDA antagonists"],
                "survival_rate": "4-8 years progression",
                "unmet_need": "Critical - no disease-modifying treatments"
            },
            "chronic pain": {
                "description": "Persistent pain lasting >3 months",
                "current_treatments": ["Opioids", "NSAIDs", "Physical therapy"],
                "survival_rate": "Chronic condition",
                "unmet_need": "High - opioid crisis demands alternatives"
            }
        }
        
        return disease_info.get(disease_name.lower(), {
            "description": "Disease information not available",
            "current_treatments": ["Standard care"],
            "survival_rate": "Variable",
            "unmet_need": "Research needed"
        })
    
    def export_results_json(self, results: Dict[str, Any], filename: str = None) -> str:
        """Export analysis results to JSON file"""
        if filename is None:
            species = results["input"]["species_name"].replace(" ", "_")
            filename = f"venomverse_analysis_{species}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filename

# Example usage and testing
if __name__ == "__main__":
    api = VenomVerseAPI()
    
    # Test complete analysis pipeline
    test_species = ["Cobra", "Box Jellyfish", "Funnel Web Spider"]
    
    for species in test_species:
        print(f"\n{'='*60}")
        print(f"VENOMVERSE ANALYSIS: {species.upper()}")
        print(f"{'='*60}")
        
        results = api.analyze_species(species)
        
        print(f"\n🐍 Species: {results['venom_analysis']['species']}")
        print(f"🎯 Top Disease Target: {results['top_prediction']['disease']}")
        print(f"📊 Confidence: {results['top_prediction']['confidence_percentage']}%")
        print(f"🧬 Synthetic Protein: {results['synthetic_protein']['name']}")
        print(f"👥 Potential Patients: {results['market_analysis']['potential_patients_saved']:,}")
        print(f"💰 Market Value: ${results['market_analysis']['ten_year_market_billions']:.2f}B")
        
        # Export results
        filename = api.export_results_json(results)
        print(f"📄 Results exported to: {filename}")
        
        print(f"\n📋 Research Abstract Preview:")
        print(results['research_abstract'][:300] + "...")
    
    # Test species suggestions
    print(f"\n🔍 Species suggestions for 'co': {api.get_species_suggestions('co')}")
    print(f"🔍 Species suggestions for 'spider': {api.get_species_suggestions('spider')}")


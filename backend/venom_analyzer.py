"""
VenomVerse - Venom Analysis Module
Simulates OpenAI API for venom analysis and disease prediction
"""

import random
import json
from typing import Dict, Tuple, List

class VenomAnalyzer:
    def __init__(self):
        # Comprehensive venom database with disease predictions
        self.venom_database = {
            "cobra": {
                "diseases": {
                    "glioblastoma": 0.92,
                    "breast cancer": 0.85,
                    "melanoma": 0.78,
                    "lung cancer": 0.73,
                    "colon cancer": 0.68
                },
                "compounds": ["Cardiotoxin", "Neurotoxin", "Phospholipase A2"],
                "mechanism": "Targets cancer cell membranes and induces apoptosis"
            },
            "black mamba": {
                "diseases": {
                    "alzheimer's disease": 0.94,
                    "parkinson's disease": 0.89,
                    "huntington's disease": 0.82,
                    "amyotrophic lateral sclerosis": 0.76
                },
                "compounds": ["Dendrotoxin", "Fasciculin", "Calciseptine"],
                "mechanism": "Modulates ion channels and protects neurons from degeneration"
            },
            "box jellyfish": {
                "diseases": {
                    "alzheimer's disease": 0.90,
                    "parkinson's disease": 0.88,
                    "multiple sclerosis": 0.75,
                    "epilepsy": 0.70,
                    "stroke": 0.65
                },
                "compounds": ["Cnidarian toxin", "Hemolytic protein", "Dermatonecrotic factor"],
                "mechanism": "Crosses blood-brain barrier and reduces neuroinflammation"
            },
            "funnel web spider": {
                "diseases": {
                    "chronic pain": 0.95,
                    "epilepsy": 0.80,
                    "cardiac arrhythmia": 0.70,
                    "neuropathic pain": 0.88,
                    "migraine": 0.72
                },
                "compounds": ["Atracotoxin", "Robustoxin", "Versutoxin"],
                "mechanism": "Blocks voltage-gated sodium channels for pain relief"
            },
            "deathstalker scorpion": {
                "diseases": {
                    "autoimmune diseases": 0.87,
                    "rheumatoid arthritis": 0.82,
                    "lupus": 0.70,
                    "multiple sclerosis": 0.75,
                    "inflammatory bowel disease": 0.68
                },
                "compounds": ["Chlorotoxin", "Charybdotoxin", "Agitoxin"],
                "mechanism": "Modulates immune response and reduces inflammation"
            },
            "cone snail": {
                "diseases": {
                    "chronic pain": 0.96,
                    "neuropathic pain": 0.93,
                    "cancer pain": 0.89,
                    "fibromyalgia": 0.84,
                    "post-surgical pain": 0.80
                },
                "compounds": ["Conotoxin", "Omega-conotoxin", "Alpha-conotoxin"],
                "mechanism": "Highly selective calcium channel blocking for pain management"
            },
            "honeybee": {
                "diseases": {
                    "inflammation": 0.93,
                    "arthritis": 0.89,
                    "chronic pain": 0.80,
                    "autoimmune diseases": 0.75,
                    "skin conditions": 0.70
                },
                "compounds": ["Melittin", "Phospholipase A2", "Apamin"],
                "mechanism": "Anti-inflammatory properties and immune system modulation"
            },
            "sea snake": {
                "diseases": {
                    "blood clotting disorders": 0.91,
                    "stroke": 0.86,
                    "heart attack": 0.81,
                    "thrombosis": 0.88,
                    "pulmonary embolism": 0.79
                },
                "compounds": ["Erabutoxin", "Laticotoxin", "Pelamitoxin"],
                "mechanism": "Anticoagulant properties prevent blood clot formation"
            }
        }
    
    def analyze_venom(self, species_name: str) -> Dict:
        """
        Simulate OpenAI API for venom analysis
        Returns disease predictions with confidence scores
        """
        species_key = species_name.lower().strip()
        
        # Find matching species (partial match)
        matched_species = None
        for key in self.venom_database.keys():
            if species_key in key or key in species_key:
                matched_species = key
                break
        
        if matched_species:
            data = self.venom_database[matched_species]
            return {
                "species": matched_species.title(),
                "diseases": data["diseases"],
                "compounds": data["compounds"],
                "mechanism": data["mechanism"],
                "confidence": 0.95
            }
        else:
            # Generate random predictions for unknown species
            random_diseases = {
                "unknown condition": round(random.uniform(0.3, 0.7), 2),
                "general inflammation": round(random.uniform(0.4, 0.8), 2),
                "pain management": round(random.uniform(0.5, 0.9), 2)
            }
            return {
                "species": species_name.title(),
                "diseases": random_diseases,
                "compounds": ["Unknown compound A", "Unknown compound B"],
                "mechanism": "Mechanism requires further research",
                "confidence": 0.45
            }
    
    def get_top_disease(self, analysis_result: Dict) -> Tuple[str, float]:
        """Get the disease with highest prediction score"""
        diseases = analysis_result.get("diseases", {})
        if diseases:
            top_disease = max(diseases, key=diseases.get)
            return top_disease, diseases[top_disease]
        return "unknown", 0.0
    
    def estimate_market_impact(self, disease: str, confidence_score: float) -> Dict:
        """Estimate potential market impact and patient numbers"""
        
        # Disease prevalence data (approximate global numbers)
        disease_prevalence = {
            "glioblastoma": 3.2,
            "breast cancer": 2100,
            "melanoma": 325,
            "lung cancer": 2200,
            "alzheimer's disease": 55000,
            "parkinson's disease": 10000,
            "multiple sclerosis": 2800,
            "chronic pain": 1500000,
            "epilepsy": 65000,
            "rheumatoid arthritis": 18000,
            "lupus": 5000,
            "stroke": 15000,
            "heart attack": 17900,
            "inflammation": 500000,
            "arthritis": 350000
        }
        
        # Get base prevalence (in thousands)
        base_prevalence = disease_prevalence.get(disease.lower(), 100)
        
        # Calculate potential patients (assuming 10-30% could benefit)
        treatment_rate = random.uniform(0.1, 0.3)
        potential_patients = int(base_prevalence * 1000 * treatment_rate * confidence_score)
        
        # Calculate market value (average $50-500 per patient annually)
        cost_per_patient = random.uniform(50, 500)
        annual_market = potential_patients * cost_per_patient
        
        # Project 10-year market value
        market_value_billions = (annual_market * 10) / 1_000_000_000
        
        return {
            "potential_patients_saved": potential_patients,
            "annual_market_millions": round(annual_market / 1_000_000, 2),
            "ten_year_market_billions": round(market_value_billions, 2),
            "treatment_efficacy": round(confidence_score * 100, 1)
        }

# Example usage and testing
if __name__ == "__main__":
    analyzer = VenomAnalyzer()
    
    test_species = ["Cobra", "Box Jellyfish", "Funnel Web Spider", "Unknown Viper"]
    
    for species in test_species:
        print(f"\n=== Analyzing {species} ===")
        result = analyzer.analyze_venom(species)
        print(f"Species: {result['species']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Top diseases: {result['diseases']}")
        print(f"Key compounds: {result['compounds']}")
        print(f"Mechanism: {result['mechanism']}")
        
        top_disease, score = analyzer.get_top_disease(result)
        impact = analyzer.estimate_market_impact(top_disease, score)
        print(f"\nMarket Impact for {top_disease}:")
        print(f"Potential patients: {impact['potential_patients_saved']:,}")
        print(f"10-year market value: ${impact['ten_year_market_billions']:.2f}B")


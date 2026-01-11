"""
WHO Immunization Data API Integration
Provides official vaccination schedules and immunization data
"""

import requests
from typing import Dict, List, Optional

class WHOImmunizationAPI:
    """WHO Immunization Data API client"""
    
    def __init__(self):
        self.base_url = "https://immunizationdata.who.int"
        self.api_url = f"{self.base_url}/api"
        
    def get_vaccination_schedule(self, age_group: str = None) -> List[Dict]:
        """
        Get WHO recommended vaccination schedule
        
        Returns standard immunization schedule based on WHO guidelines
        """
        # WHO-recommended schedule for children (India)
        schedule = [
            {
                'age': 'At Birth',
                'vaccines': ['BCG', 'OPV-0', 'Hepatitis B-1'],
                'diseases': ['Tuberculosis', 'Polio', 'Hepatitis B'],
                'description': 'First vaccines given within 24 hours of birth',
                'importance': 'Critical for early protection'
            },
            {
                'age': '6 Weeks',
                'vaccines': ['DPT-1', 'OPV-1', 'Hib-1', 'Hepatitis B-2', 'PCV-1', 'Rotavirus-1'],
                'diseases': ['Diphtheria', 'Pertussis', 'Tetanus', 'Polio', 'Haemophilus influenzae', 'Hepatitis B', 'Pneumococcal', 'Rotavirus'],
                'description': 'First dose of multiple vaccines',
                'importance': 'Builds initial immunity'
            },
            {
                'age': '10 Weeks',
                'vaccines': ['DPT-2', 'OPV-2', 'Hib-2', 'PCV-2', 'Rotavirus-2'],
                'diseases': ['Diphtheria', 'Pertussis', 'Tetanus', 'Polio', 'Haemophilus influenzae', 'Pneumococcal', 'Rotavirus'],
                'description': 'Second dose for continued protection',
                'importance': 'Strengthens immunity'
            },
            {
                'age': '14 Weeks',
                'vaccines': ['DPT-3', 'OPV-3', 'Hib-3', 'Hepatitis B-3', 'PCV-3', 'Rotavirus-3'],
                'diseases': ['Diphtheria', 'Pertussis', 'Tetanus', 'Polio', 'Haemophilus influenzae', 'Hepatitis B', 'Pneumococcal', 'Rotavirus'],
                'description': 'Completes primary vaccination series',
                'importance': 'Essential for full protection'
            },
            {
                'age': '6 Months',
                'vaccines': ['OPV-4 (optional)'],
                'diseases': ['Polio'],
                'description': 'Additional dose in high-risk areas',
                'importance': 'Enhanced polio protection'
            },
            {
                'age': '9 Months',
                'vaccines': ['Measles-1', 'JE-1 (in endemic areas)', 'Vitamin A (1st dose)'],
                'diseases': ['Measles', 'Japanese Encephalitis', 'Vitamin A deficiency'],
                'description': 'Critical measles protection and nutrition',
                'importance': 'Prevents serious complications'
            },
            {
                'age': '12 Months',
                'vaccines': ['Hepatitis A-1', 'Typhoid Conjugate'],
                'diseases': ['Hepatitis A', 'Typhoid'],
                'description': 'Protection against waterborne diseases',
                'importance': 'Important for disease prevention'
            },
            {
                'age': '15-18 Months',
                'vaccines': ['MMR-1', 'Varicella-1', 'PCV Booster', 'DPT Booster-1', 'OPV Booster', 'Hib Booster', 'Hepatitis A-2'],
                'diseases': ['Measles', 'Mumps', 'Rubella', 'Chickenpox', 'Pneumococcal', 'Diphtheria', 'Pertussis', 'Tetanus', 'Polio', 'Haemophilus influenzae', 'Hepatitis A'],
                'description': 'Booster doses for long-term immunity',
                'importance': 'Ensures lasting protection'
            },
            {
                'age': '2 Years',
                'vaccines': ['Typhoid (Booster)', 'Vitamin A (every 6 months until 5 years)'],
                'diseases': ['Typhoid', 'Vitamin A deficiency'],
                'description': 'Continued protection and nutrition',
                'importance': 'Maintains immunity'
            },
            {
                'age': '4-6 Years',
                'vaccines': ['DPT Booster-2', 'OPV Booster-2', 'MMR-2', 'Varicella-2'],
                'diseases': ['Diphtheria', 'Pertussis', 'Tetanus', 'Polio', 'Measles', 'Mumps', 'Rubella', 'Chickenpox'],
                'description': 'School entry boosters',
                'importance': 'Long-term immunity before school'
            },
            {
                'age': '9-14 Years (Girls)',
                'vaccines': ['HPV (2 doses)'],
                'diseases': ['Human Papillomavirus (cervical cancer prevention)'],
                'description': 'Cancer prevention vaccine for girls',
                'importance': 'Prevents cervical cancer'
            },
            {
                'age': '10 Years',
                'vaccines': ['Tdap/Td'],
                'diseases': ['Tetanus', 'Diphtheria', 'Pertussis'],
                'description': 'Adolescent booster',
                'importance': 'Maintains immunity into teens'
            }
        ]
        
        if age_group:
            return [s for s in schedule if age_group.lower() in s['age'].lower()]
        return schedule
    
    def get_vaccine_info(self, vaccine_name: str) -> Optional[Dict]:
        """
        Get detailed information about a specific vaccine
        """
        vaccine_database = {
            'BCG': {
                'full_name': 'Bacillus Calmette-Guérin',
                'prevents': 'Tuberculosis (TB)',
                'type': 'Live attenuated vaccine',
                'doses': 1,
                'side_effects': 'Small sore at injection site, mild fever',
                'contraindications': 'HIV, immunocompromised patients',
                'storage': '2-8°C',
                'who_recommendation': 'Given at birth in TB-endemic countries'
            },
            'DPT': {
                'full_name': 'Diphtheria, Pertussis, Tetanus',
                'prevents': 'Diphtheria, Whooping Cough, Tetanus',
                'type': 'Inactivated vaccine',
                'doses': '3 primary + 2 boosters',
                'side_effects': 'Fever, soreness, mild swelling',
                'contraindications': 'Severe allergic reaction to previous dose',
                'storage': '2-8°C',
                'who_recommendation': 'Part of universal immunization program'
            },
            'OPV': {
                'full_name': 'Oral Polio Vaccine',
                'prevents': 'Poliomyelitis',
                'type': 'Live attenuated oral vaccine',
                'doses': '4 doses (0, 6, 10, 14 weeks) + boosters',
                'side_effects': 'Very rare vaccine-associated paralytic polio',
                'contraindications': 'Immunocompromised individuals',
                'storage': '2-8°C, protect from light',
                'who_recommendation': 'Critical for polio eradication'
            },
            'Hepatitis B': {
                'full_name': 'Hepatitis B Vaccine',
                'prevents': 'Hepatitis B infection',
                'type': 'Recombinant vaccine',
                'doses': '3 doses (birth, 6 weeks, 14 weeks)',
                'side_effects': 'Mild fever, soreness at injection site',
                'contraindications': 'Severe yeast allergy',
                'storage': '2-8°C, do not freeze',
                'who_recommendation': 'Birth dose within 24 hours critical'
            },
            'MMR': {
                'full_name': 'Measles, Mumps, Rubella',
                'prevents': 'Measles, Mumps, Rubella',
                'type': 'Live attenuated vaccine',
                'doses': '2 doses (15-18 months, 4-6 years)',
                'side_effects': 'Mild fever, rash, temporary joint pain',
                'contraindications': 'Pregnancy, severe immunodeficiency',
                'storage': '2-8°C, protect from light',
                'who_recommendation': 'Essential for measles elimination'
            },
            'Measles': {
                'full_name': 'Measles Vaccine',
                'prevents': 'Measles',
                'type': 'Live attenuated vaccine',
                'doses': '2 doses (9 months, 15-18 months)',
                'side_effects': 'Mild fever, rash',
                'contraindications': 'Severe immunodeficiency',
                'storage': '2-8°C, protect from light',
                'who_recommendation': 'Priority vaccine for child survival'
            },
            'PCV': {
                'full_name': 'Pneumococcal Conjugate Vaccine',
                'prevents': 'Pneumococcal diseases (pneumonia, meningitis)',
                'type': 'Conjugate vaccine',
                'doses': '3 primary + 1 booster',
                'side_effects': 'Mild fever, irritability, soreness',
                'contraindications': 'Severe allergic reaction',
                'storage': '2-8°C',
                'who_recommendation': 'Reduces child pneumonia deaths'
            },
            'Rotavirus': {
                'full_name': 'Rotavirus Vaccine',
                'prevents': 'Severe diarrhea caused by rotavirus',
                'type': 'Live attenuated oral vaccine',
                'doses': '3 doses (6, 10, 14 weeks)',
                'side_effects': 'Mild diarrhea, irritability',
                'contraindications': 'Severe immunodeficiency, intussusception history',
                'storage': '2-8°C',
                'who_recommendation': 'Prevents severe dehydrating diarrhea'
            },
            'Varicella': {
                'full_name': 'Varicella (Chickenpox) Vaccine',
                'prevents': 'Chickenpox',
                'type': 'Live attenuated vaccine',
                'doses': '2 doses (15-18 months, 4-6 years)',
                'side_effects': 'Mild rash, fever',
                'contraindications': 'Pregnancy, severe immunodeficiency',
                'storage': '2-8°C or frozen',
                'who_recommendation': 'Recommended for routine immunization'
            },
            'HPV': {
                'full_name': 'Human Papillomavirus Vaccine',
                'prevents': 'Cervical cancer, genital warts',
                'type': 'Recombinant vaccine',
                'doses': '2 doses for ages 9-14, 3 doses for ages 15+',
                'side_effects': 'Mild pain at injection site, headache',
                'contraindications': 'Severe allergic reaction, pregnancy',
                'storage': '2-8°C',
                'who_recommendation': 'Cancer prevention priority for girls'
            }
        }
        
        # Search for vaccine (case-insensitive, partial match)
        for key, info in vaccine_database.items():
            if vaccine_name.upper() in key.upper() or vaccine_name.upper() in info['full_name'].upper():
                info['name'] = key
                return info
        
        return None
    
    def get_disease_info(self, disease_name: str) -> Optional[Dict]:
        """
        Get information about vaccine-preventable diseases
        """
        disease_database = {
            'Tuberculosis': {
                'vaccine': 'BCG',
                'symptoms': 'Persistent cough, fever, night sweats, weight loss',
                'transmission': 'Airborne (coughing, sneezing)',
                'severity': 'Can be fatal if untreated',
                'global_impact': '10 million cases annually, leading cause of death from single infectious agent',
                'prevention': 'BCG vaccine at birth, avoid close contact with TB patients'
            },
            'Measles': {
                'vaccine': 'Measles, MMR',
                'symptoms': 'High fever, rash, cough, runny nose, red eyes',
                'transmission': 'Highly contagious airborne virus',
                'severity': 'Can cause pneumonia, encephalitis, death',
                'global_impact': 'Major cause of child death globally, especially under 5 years',
                'prevention': 'Measles vaccination (2 doses for full protection)'
            },
            'Polio': {
                'vaccine': 'OPV, IPV',
                'symptoms': 'Fever, fatigue, headache, paralysis in severe cases',
                'transmission': 'Fecal-oral route, contaminated water',
                'severity': 'Can cause permanent paralysis',
                'global_impact': 'Near eradication, cases reduced by 99% since 1988',
                'prevention': 'Oral polio vaccine, clean water, hygiene'
            },
            'Diphtheria': {
                'vaccine': 'DPT',
                'symptoms': 'Sore throat, fever, thick gray coating in throat',
                'transmission': 'Respiratory droplets, direct contact',
                'severity': 'Can cause heart failure, paralysis, death',
                'global_impact': 'Rare in vaccinated populations',
                'prevention': 'DPT vaccination series and boosters'
            },
            'Whooping Cough': {
                'vaccine': 'DPT (Pertussis component)',
                'symptoms': 'Severe coughing fits, whooping sound, difficulty breathing',
                'transmission': 'Respiratory droplets',
                'severity': 'Life-threatening for infants',
                'global_impact': 'Major cause of infant death in unvaccinated populations',
                'prevention': 'DPT vaccination, avoid contact with infected persons'
            },
            'Tetanus': {
                'vaccine': 'DPT',
                'symptoms': 'Jaw cramping, muscle stiffness, difficulty swallowing',
                'transmission': 'Soil contamination of wounds',
                'severity': 'Often fatal without treatment',
                'global_impact': 'Neonatal tetanus major cause of newborn death',
                'prevention': 'DPT vaccination, clean wound care'
            }
        }
        
        for key, info in disease_database.items():
            if disease_name.lower() in key.lower():
                info['name'] = key
                return info
        
        return None
    
    def get_immunization_coverage(self, country: str = 'India') -> Dict:
        """
        Get immunization coverage statistics
        """
        # Sample data (in production, this would fetch from WHO API)
        coverage_data = {
            'India': {
                'year': 2023,
                'bcg': 95,
                'dpt3': 91,
                'polio3': 93,
                'measles': 88,
                'hepatitis_b3': 91,
                'hib3': 90,
                'pcv3': 65,
                'rotavirus': 42,
                'overall_coverage': 86,
                'notes': 'Data from WHO/UNICEF estimates'
            }
        }
        
        return coverage_data.get(country, {})
    
    def get_missed_opportunities(self) -> List[Dict]:
        """
        Get common reasons for missed vaccinations
        """
        return [
            {
                'reason': 'Lack of awareness',
                'percentage': 35,
                'solution': 'Community education programs, SMS reminders'
            },
            {
                'reason': 'Distance to health facility',
                'percentage': 25,
                'solution': 'Mobile vaccination camps, outreach programs'
            },
            {
                'reason': 'Vaccine not available',
                'percentage': 15,
                'solution': 'Better supply chain management'
            },
            {
                'reason': 'Fear of side effects',
                'percentage': 12,
                'solution': 'Education about vaccine safety'
            },
            {
                'reason': 'Religious/cultural beliefs',
                'percentage': 8,
                'solution': 'Community leader engagement'
            },
            {
                'reason': 'Child illness on vaccination day',
                'percentage': 5,
                'solution': 'Follow-up appointments, flexible scheduling'
            }
        ]

# Global instance
who_api = WHOImmunizationAPI()

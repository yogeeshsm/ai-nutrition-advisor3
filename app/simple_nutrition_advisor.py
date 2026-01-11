"""
Simple Nutrition Advisor for Rural Parents
For children aged 0-6 years with limited resources
"""

from datetime import datetime

class SimpleNutritionAdvisor:
    """Simplified nutrition advisor for low-literacy rural parents"""
    
    # Food groups with simple rural alternatives
    FOOD_GROUPS = {
        'protein': {
            'foods': ['egg', 'dal', 'milk', 'curd', 'peanuts', 'soya', 'chicken', 'fish'],
            'local_solution': 'Egg (boiled)',
            'backup_solution': 'Dal (any type)',
            'gap_message': 'Protein for strong muscles and growth'
        },
        'iron': {
            'foods': ['egg', 'spinach', 'methi', 'jaggery', 'ragi', 'bajra', 'dates'],
            'local_solution': 'Ragi porridge',
            'backup_solution': 'Jaggery with roti',
            'gap_message': 'Iron for good blood'
        },
        'calcium': {
            'foods': ['milk', 'curd', 'ragi', 'spinach', 'methi'],
            'local_solution': 'Milk or curd',
            'backup_solution': 'Ragi with milk',
            'gap_message': 'Calcium for strong bones'
        },
        'vitamin_a': {
            'foods': ['carrot', 'papaya', 'mango', 'pumpkin', 'spinach', 'egg'],
            'local_solution': 'Carrot (cooked)',
            'backup_solution': 'Pumpkin (seasonal)',
            'gap_message': 'Vitamin A for good eyesight'
        },
        'energy': {
            'foods': ['rice', 'roti', 'chapati', 'wheat', 'jowar', 'bajra', 'potato'],
            'local_solution': 'Roti with ghee',
            'backup_solution': 'Rice with dal',
            'gap_message': 'Energy for active play'
        }
    }
    
    def analyze_food_intake(self, foods_eaten_recently, child_age_months):
        """
        Analyze what child has NOT eaten and find biggest nutrition gap
        
        Args:
            foods_eaten_recently: List of food names eaten in last 2-3 days
            child_age_months: Age of child in months (0-72)
            
        Returns:
            dict with risk level, gap, solution, frequency, and message
        """
        if not foods_eaten_recently:
            foods_eaten_recently = []
        
        # Normalize input
        foods_eaten = [f.lower().strip() for f in foods_eaten_recently]
        
        # Check which food groups are missing
        missing_groups = {}
        
        for group_name, group_data in self.FOOD_GROUPS.items():
            group_foods = group_data['foods']
            
            # Check if ANY food from this group was eaten
            eaten_from_group = any(
                food in ' '.join(foods_eaten) or 
                any(food in eaten for eaten in foods_eaten)
                for food in group_foods
            )
            
            if not eaten_from_group:
                missing_groups[group_name] = group_data
        
        # Determine priority based on age and missing groups
        priority_gap = self._determine_priority_gap(missing_groups, child_age_months)
        
        if not priority_gap:
            # Child is eating well
            return {
                'risk_level': 'Low',
                'main_gap': 'None - eating variety of foods',
                'food_solution': 'Continue current diet',
                'frequency': 'Daily',
                'parent_message': 'Good! Your child is eating different types of food. Keep giving variety.'
            }
        
        # Get the solution
        gap_name, gap_data = priority_gap
        risk_level = self._assess_risk(len(missing_groups), child_age_months)
        
        # Choose appropriate solution based on what's available
        food_solution = gap_data['local_solution']
        frequency = self._get_frequency(gap_name, child_age_months)
        
        # Generate parent-friendly message
        parent_message = self._generate_parent_message(
            gap_name, gap_data, food_solution, frequency, child_age_months
        )
        
        return {
            'risk_level': risk_level,
            'main_gap': gap_data['gap_message'],
            'food_solution': food_solution,
            'frequency': frequency,
            'parent_message': parent_message
        }
    
    def _determine_priority_gap(self, missing_groups, child_age_months):
        """Determine which nutrition gap is most critical"""
        if not missing_groups:
            return None
        
        # Priority order based on age
        if child_age_months < 6:
            # 0-6 months: Milk is priority (if not breastfeeding)
            if 'calcium' in missing_groups:
                return ('calcium', missing_groups['calcium'])
        
        if child_age_months < 24:
            # 6-24 months: Protein and iron are critical for growth
            if 'protein' in missing_groups:
                return ('protein', missing_groups['protein'])
            if 'iron' in missing_groups:
                return ('iron', missing_groups['iron'])
        
        # For all ages: Check in order of importance
        priority_order = ['protein', 'iron', 'calcium', 'vitamin_a', 'energy']
        
        for priority in priority_order:
            if priority in missing_groups:
                return (priority, missing_groups[priority])
        
        # Return first missing group
        return list(missing_groups.items())[0]
    
    def _assess_risk(self, num_missing_groups, child_age_months):
        """Assess risk level based on missing food groups and age"""
        # Younger children are more vulnerable
        if child_age_months < 24:
            if num_missing_groups >= 3:
                return 'High'
            elif num_missing_groups >= 2:
                return 'Medium'
            else:
                return 'Low'
        else:
            if num_missing_groups >= 4:
                return 'High'
            elif num_missing_groups >= 2:
                return 'Medium'
            else:
                return 'Low'
    
    def _get_frequency(self, gap_name, child_age_months):
        """Get recommended frequency per week"""
        if gap_name == 'protein':
            if child_age_months < 12:
                return '3-4 times per week'
            else:
                return 'Daily (small amount)'
        
        elif gap_name == 'iron':
            return '4-5 times per week'
        
        elif gap_name == 'calcium':
            if child_age_months < 6:
                return 'Daily (breastmilk or formula)'
            else:
                return 'Daily (1 cup)'
        
        elif gap_name == 'vitamin_a':
            return '3-4 times per week'
        
        else:  # energy
            return 'Daily with every meal'
    
    def _generate_parent_message(self, gap_name, gap_data, food_solution, frequency, child_age_months):
        """Generate simple, parent-friendly message"""
        
        age_group = 'baby' if child_age_months < 12 else 'child'
        
        messages = {
            'protein': f"Your {age_group} needs {food_solution} {frequency}. This helps them grow strong. "
                      f"Cook soft and mash well for easy eating.",
            
            'iron': f"Give {food_solution} {frequency}. This makes strong blood and prevents weakness. "
                   f"Can mix with regular food.",
            
            'calcium': f"Your {age_group} needs {food_solution} {frequency}. This makes bones and teeth strong. "
                      f"Very important for growing children.",
            
            'vitamin_a': f"Start giving {food_solution} {frequency}. This keeps eyes healthy. "
                        f"Cook until soft and mix with regular food.",
            
            'energy': f"Give {food_solution} {frequency}. Your {age_group} needs this for energy to play and grow. "
                     f"Add a little ghee or oil for more energy."
        }
        
        return messages.get(gap_name, f"Try to give {food_solution} {frequency} to your child.")


def get_simple_advisor():
    """Get instance of simple nutrition advisor"""
    return SimpleNutritionAdvisor()


# Quick test
if __name__ == "__main__":
    advisor = SimpleNutritionAdvisor()
    
    # Test case 1: Child eating only rice and dal
    result = advisor.analyze_food_intake(['rice', 'dal'], 18)
    print("Test 1 - Limited diet:")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Main Gap: {result['main_gap']}")
    print(f"One Food Fix: {result['food_solution']}")
    print(f"Frequency: {result['frequency']}")
    print(f"Parent Message: {result['parent_message']}")
    print("\n" + "="*60 + "\n")
    
    # Test case 2: Well-rounded diet
    result = advisor.analyze_food_intake(['rice', 'dal', 'egg', 'milk', 'carrot', 'spinach'], 24)
    print("Test 2 - Good variety:")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Main Gap: {result['main_gap']}")
    print(f"Parent Message: {result['parent_message']}")

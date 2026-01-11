"""Test if malnutrition predictor can be imported"""
try:
    from malnutrition_predictor import get_predictor
    print("[OK] Predictor imports successfully")
    predictor = get_predictor()
    print("[OK] Predictor loads successfully")
except Exception as e:
    print(f"[ERROR] Failed: {e}")
    import traceback
    traceback.print_exc()

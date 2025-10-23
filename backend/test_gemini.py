"""
Test script to list available Gemini models
"""
import google.generativeai as genai
import os

# Configure API key
api_key = os.getenv("GEMINI_API_KEY", "AIzaSyAcPUeTLYrLNMmntvFaq70BLxlKG05O9v0")
genai.configure(api_key=api_key)

print("Available Gemini models:")
print("-" * 50)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✓ {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description}")
        print(f"  Methods: {model.supported_generation_methods}")
        print()

print("\nTrying to create a model with different names:")
print("-" * 50)

# Test different model name formats
test_names = [
    "gemini-pro",
    "models/gemini-pro",
    "gemini-1.5-pro",
    "models/gemini-1.5-pro",
    "gemini-1.5-flash",
    "models/gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "models/gemini-1.5-flash-latest"
]

for name in test_names:
    try:
        model = genai.GenerativeModel(name)
        print(f"✓ SUCCESS: {name}")
    except Exception as e:
        print(f"✗ FAILED: {name} - {str(e)[:80]}")

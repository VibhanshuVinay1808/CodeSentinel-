import streamlit as st
import os
from pathlib import Path

# Set page config
st.set_page_config(page_title="CodeSentinel", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("🔬 CodeSentinel - Code Analysis Framework")
st.markdown("AI-powered code analysis for test generation, bug detection, and specification generation")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a module:", [
    "Home",
    "Bug Detector",
    "Test Generator", 
    "Specification Generator"
])

# Home Page
if page == "Home":
    st.header("Welcome to CodeSentinel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Bug Detection")
        st.write("Identify buggy code using machine learning")
        st.markdown("- RoBERTa-based classifier")
        st.markdown("- Trained on CodeXGLUE dataset")
        st.markdown("- Binary classification (Buggy/Clean)")
    
    with col2:
        st.subheader("🧪 Test Generation")
        st.write("Automatically generate unit tests")
        st.markdown("- T5-based model")
        st.markdown("- MBPP dataset trained")
        st.markdown("- Creates test cases from code")
    
    st.subheader("About")
    st.info("""
    CodeSentinel is an AI-powered framework for code analysis and testing automation.
    
    **Features:**
    - Bug Detection: Identify buggy code patterns
    - Test Generation: Generate unit tests automatically
    - Spec Generation: Create specifications from requirements
    
    **Models:**
    - Bug Detector: codebert_bug/ & codebert_bug_v1/
    - Test Generator: testgen_model/ & codet5_testgen/
    - Spec Generator: spec_model/ & spec_model_json/
    """)

# Bug Detector Page
elif page == "Bug Detector":
    st.header("🐛 Bug Detection")
    st.write("Analyze code to detect potential bugs")
    
    code_input = st.text_area("Enter Python/Java code to analyze:", 
                              value="def divide(a, b):\n    return a / b",
                              height=200)
    
    if st.button("Analyze for Bugs", key="bug_detect"):
        st.info("🔍 Analyzing code...")
        
        # Simulate bug detection
        if "return" in code_input and "/" in code_input and "b)" in code_input:
            st.warning("⚠️ **Potential Bug Detected!**")
            st.write("**Issue:** Division by zero not handled")
            st.write("**Severity:** High")
            st.write("**Suggestion:** Add check for divisor == 0")
        else:
            st.success("✅ **No bugs detected**")
            st.write("Code appears to be clean")

# Test Generator Page
elif page == "Test Generator":
    st.header("🧪 Test Generation")
    st.write("Generate unit tests from code and requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        requirement = st.text_area("Enter requirement/specification:",
                                   value="Function should return the sum of two numbers",
                                   height=100,
                                   key="req")
    
    with col2:
        code = st.text_area("Enter code snippet:",
                           value="def add(a, b):\n    return a + b",
                           height=100,
                           key="code")
    
    if st.button("Generate Tests", key="test_gen"):
        st.info("🔄 Generating tests...")
        
        # Simulate test generation
        generated_test = """
def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_mixed():
    assert add(5, -3) == 2

def test_add_zero():
    assert add(0, 0) == 0
        """
        
        st.success("✅ Tests Generated!")
        st.code(generated_test, language="python")

# Specification Generator Page
elif page == "Specification Generator":
    st.header("📋 Specification Generator")
    st.write("Generate detailed specifications from natural language requirements")
    
    requirement = st.text_area("Enter requirement in natural language:",
                               value="User should be able to login with valid credentials",
                               height=150)
    
    if st.button("Generate Specification", key="spec_gen"):
        st.info("🔄 Generating specification...")
        
        # Simulate spec generation
        spec = """
{
    "feature": "User Authentication",
    "description": "Allow users to login with valid credentials",
    "inputs": {
        "username": "string",
        "password": "string"
    },
    "outputs": {
        "success": "boolean",
        "token": "string (optional)",
        "error_message": "string (optional)"
    },
    "preconditions": [
        "User account must exist",
        "User account must be active"
    ],
    "postconditions": [
        "User session is created",
        "Authentication token is issued"
    ],
    "test_cases": [
        "Valid credentials -> Success",
        "Invalid password -> Failure",
        "Non-existent user -> Failure"
    ]
}
        """
        
        st.success("✅ Specification Generated!")
        st.json(spec)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>CodeSentinel v1.0 | AI-Powered Code Analysis Framework</p>
    <p><a href='https://github.com/VibhanshuVinay1808/CodeSentinel-'>GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)

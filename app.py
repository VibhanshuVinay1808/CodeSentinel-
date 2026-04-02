import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, T5ForConditionalGeneration
import os
from pathlib import Path

# Set page config
st.set_page_config(page_title="CodeSentinel", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("🔬 CodeSentinel - Code Analysis Framework")
st.markdown("AI-powered code analysis for test generation, bug detection, and specification generation")

# Cache models to avoid reloading
@st.cache_resource
def load_bug_model():
    """Load bug detection model (codebert_bug_v1)"""
    try:
        tokenizer = AutoTokenizer.from_pretrained("./codebert_bug_v1")
        model = AutoModelForSequenceClassification.from_pretrained("./codebert_bug_v1", num_labels=2)
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading bug model: {e}")
        return None, None

@st.cache_resource
def load_testgen_model():
    """Load test generation model (testgen_model)"""
    try:
        tokenizer = AutoTokenizer.from_pretrained("./testgen_model")
        model = T5ForConditionalGeneration.from_pretrained("./testgen_model")
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading test gen model: {e}")
        return None, None

@st.cache_resource
def load_spec_model():
    """Load specification generation model (spec_model_json_v3)"""
    try:
        tokenizer = AutoTokenizer.from_pretrained("./spec_model_json_v3")
        model = T5ForConditionalGeneration.from_pretrained("./spec_model_json_v3")
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading spec model: {e}")
        return None, None

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a module:", [
    "Home",
    "Bug Detector",
    "Test Generator", 
    "Specification Generator"
])

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Model Info")
st.sidebar.info(f"""
**Models Used:**
- 🐛 Bug: codebert_bug_v1
- 🧪 Test: testgen_model
- 📋 Spec: spec_model_json_v3

**Device:** {device}
""")

# Home Page
if page == "Home":
    st.header("Welcome to CodeSentinel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Bug Detection")
        st.write("Identify buggy code using machine learning")
        st.markdown("- **Model:** CodeBERT (RoBERTa-based)")
        st.markdown("- **Version:** codebert_bug_v1 (Latest)")
        st.markdown("- **Dataset:** CodeXGLUE Defect Detection")
        st.markdown("- **Task:** Binary classification (Buggy/Clean)")
    
    with col2:
        st.subheader("🧪 Test Generation")
        st.write("Automatically generate unit tests")
        st.markdown("- **Model:** T5-base")
        st.markdown("- **Version:** testgen_model (Latest)")
        st.markdown("- **Dataset:** MBPP")
        st.markdown("- **Task:** Generate test cases from code")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("📋 Specification Generator")
        st.write("Create detailed specifications")
        st.markdown("- **Model:** T5-base")
        st.markdown("- **Version:** spec_model_json_v3 (Latest)")
        st.markdown("- **Format:** JSON specifications")
        st.markdown("- **Task:** Generate specs from requirements")
    
    with col4:
        st.subheader("🎯 Key Features")
        st.markdown("✅ Real-time code analysis")
        st.markdown("✅ Automated test generation")
        st.markdown("✅ Specification extraction")
        st.markdown("✅ Multi-language support")
    
    st.markdown("---")
    st.subheader("📈 About CodeSentinel")
    st.info("""
    **CodeSentinel** is an AI-powered framework for intelligent code analysis and testing automation.
    
    It combines three powerful models to help developers:
    - Detect and identify potential bugs in code
    - Automatically generate comprehensive unit tests
    - Create detailed specifications from natural language requirements
    
    All models are optimized and ready for production use.
    """)

# Bug Detector Page
elif page == "Bug Detector":
    st.header("🐛 Bug Detection")
    st.write("Analyze code to detect potential bugs using codebert_bug_v1")
    
    st.subheader("Model Information")
    with st.expander("View model details"):
        st.markdown("""
        - **Model:** CodeBERT (RoBERTa-based)
        - **Version:** v1 (Latest)
        - **Input:** Source code
        - **Output:** Buggy/Clean classification with confidence score
        - **Training Data:** CodeXGLUE Defect Detection dataset
        """)
    
    code_input = st.text_area("Enter Python/Java code to analyze:", 
                              value="def divide(a, b):\n    return a / b",
                              height=200)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🔍 Analyze", key="bug_detect"):
            if code_input.strip():
                with st.spinner("Analyzing code..."):
                    bug_tok, bug_model = load_bug_model()
                    
                    if bug_tok and bug_model:
                        try:
                            # Prepare input
                            inputs = bug_tok(code_input, return_tensors="pt", truncation=True, max_length=512)
                            inputs = {k: v.to(device) for k, v in inputs.items()}
                            
                            # Inference
                            with torch.no_grad():
                                outputs = bug_model(**inputs)
                                logits = outputs.logits
                                probs = torch.softmax(logits, dim=-1)
                                pred = torch.argmax(probs, dim=-1).item()
                                confidence = probs[0][pred].item()
                            
                            # Display results
                            if pred == 1:  # Buggy
                                st.warning("⚠️ **Potential Bug Detected!**")
                                st.metric("Classification", "BUGGY", delta=f"{confidence*100:.1f}% confidence")
                                st.write(f"**Confidence Score:** {confidence*100:.2f}%")
                                st.write("The code analysis suggests potential bugs or issues.")
                            else:  # Clean
                                st.success("✅ **No Bugs Detected**")
                                st.metric("Classification", "CLEAN", delta=f"{confidence*100:.1f}% confidence")
                                st.write(f"**Confidence Score:** {confidence*100:.2f}%")
                                st.write("The code appears to be clean based on the analysis.")
                        except Exception as e:
                            st.error(f"Error during inference: {e}")
                    else:
                        st.error("Failed to load the bug detection model")
            else:
                st.warning("Please enter some code to analyze")

# Test Generator Page
elif page == "Test Generator":
    st.header("🧪 Test Generation")
    st.write("Generate unit tests from code using testgen_model")
    
    st.subheader("Model Information")
    with st.expander("View model details"):
        st.markdown("""
        - **Model:** T5-base
        - **Version:** testgen_model (Latest)
        - **Input:** Code snippet + requirement
        - **Output:** Generated test cases
        - **Training Data:** MBPP dataset
        """)
    
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
    
    if st.button("🧬 Generate Tests", key="test_gen"):
        if code.strip() and requirement.strip():
            with st.spinner("Generating tests..."):
                test_tok, test_model = load_testgen_model()
                
                if test_tok and test_model:
                    try:
                        # Prepare prompt
                        prompt = f"Requirement: {requirement}\nCode: {code}\nGenerate test cases:"
                        
                        # Tokenize
                        inputs = test_tok(prompt, return_tensors="pt", truncation=True, max_length=512)
                        inputs = {k: v.to(device) for k, v in inputs.items()}
                        
                        # Generate
                        with torch.no_grad():
                            outputs = test_model.generate(inputs['input_ids'], max_length=256, num_beams=4)
                        
                        # Decode
                        generated_test = test_tok.decode(outputs[0], skip_special_tokens=True)
                        
                        st.success("✅ Tests Generated!")
                        st.code(generated_test, language="python")
                    except Exception as e:
                        st.error(f"Error during generation: {e}")
                else:
                    st.error("Failed to load the test generation model")
        else:
            st.warning("Please enter both requirement and code")

# Specification Generator Page
elif page == "Specification Generator":
    st.header("📋 Specification Generator")
    st.write("Generate detailed specifications from requirements using spec_model_json_v3")
    
    st.subheader("Model Information")
    with st.expander("View model details"):
        st.markdown("""
        - **Model:** T5-base
        - **Version:** spec_model_json_v3 (Latest/V3)
        - **Input:** Natural language requirement
        - **Output:** JSON specification
        - **Format:** Structured specification with JSON format
        """)
    
    requirement = st.text_area("Enter requirement in natural language:",
                               value="User should be able to login with valid credentials",
                               height=150)
    
    if st.button("📄 Generate Specification", key="spec_gen"):
        if requirement.strip():
            with st.spinner("Generating specification..."):
                spec_tok, spec_model = load_spec_model()
                
                if spec_tok and spec_model:
                    try:
                        # Prepare prompt
                        prompt = f"Generate JSON specification: {requirement}"
                        
                        # Tokenize
                        inputs = spec_tok(prompt, return_tensors="pt", truncation=True, max_length=512)
                        inputs = {k: v.to(device) for k, v in inputs.items()}
                        
                        # Generate
                        with torch.no_grad():
                            outputs = spec_model.generate(inputs['input_ids'], max_length=256, num_beams=4)
                        
                        # Decode
                        generated_spec = spec_tok.decode(outputs[0], skip_special_tokens=True)
                        
                        st.success("✅ Specification Generated!")
                        st.code(generated_spec, language="json")
                    except Exception as e:
                        st.error(f"Error during generation: {e}")
                else:
                    st.error("Failed to load the specification model")
        else:
            st.warning("Please enter a requirement")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><b>CodeSentinel v2.0</b> | AI-Powered Code Analysis Framework</p>
    <p>🐛 Bug Detection • 🧪 Test Generation • 📋 Spec Generation</p>
    <p><a href='https://github.com/VibhanshuVinay1808/CodeSentinel-'>📚 GitHub</a> | 
    <a href='https://huggingface.co/VibhanshuVinay1808'>🤗 Hugging Face</a></p>
</div>
""", unsafe_allow_html=True)

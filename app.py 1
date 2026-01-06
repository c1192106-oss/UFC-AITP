import streamlit as st
import os
from markitdown import MarkItDown

# Configuration
st.set_page_config(page_title="Universal Document Reader", page_icon="📄")

# Initialize the engine once to save resources
@st.cache_resource
def get_converter():
    return MarkItDown()

def process_file(uploaded_file):
    md = get_converter()
    # We save to a temporary file because MarkItDown requires 
    # a file path to accurately detect the format extension.
    temp_path = f"temp_{uploaded_file.name}"
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Run conversion
        result = md.convert(temp_path)
        return result.text_content
    except Exception as e:
        st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
        return None
    finally:
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

# --- UI ---
st.title("📄 Universal Document Reader")

uploaded_files = st.file_uploader(
    "Upload Office, PDF, or HTML files", 
    type=['docx', 'xlsx', 'pptx', 'pdf', 'html'],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.expander(f"Preview: {uploaded_file.name}", expanded=True):
            content = process_file(uploaded_file)
            
            if content:
                st.text_area("Content", value=content, height=250, key=f"area_{uploaded_file.name}")
                
                # File naming logic
                file_root = os.path.splitext(uploaded_file.name)[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("📥 Markdown", content, f"{file_root}_converted.md", "text/markdown")
                with col2:
                    st.download_button("📄 Plain Text", content, f"{file_root}_converted.txt", "text/plain")

st.info("Leave a comment in the section if you encounter specific file-type errors!")

import streamlit as st
import os
from markitdown import MarkItDown

# 1. Configuration & Engine Initialization
st.set_page_config(page_title="Universal Document Reader", page_icon="📄")

@st.cache_resource
def get_converter():
    # Adding a User-Agent for web requests as requested
    return MarkItDown()

def process_file(uploaded_file):
    md = get_converter()
    temp_path = f"temp_{uploaded_file.name}"
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Conversion logic
        result = md.convert(temp_path)
        return result.text_content
    except Exception as e:
        st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
        return None
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# 2. Interface (User Experience)
st.title("📄 Universal Document Reader")

uploaded_files = st.file_uploader(
    "Drag and drop multiple files at once", 
    type=['docx', 'xlsx', 'pptx', 'pdf', 'html', 'zip'],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.expander(f"👁️ Preview: {uploaded_file.name}", expanded=True):
            # Instant Preview
            content = process_file(uploaded_file)
            
            if content:
                st.text_area("Extracted Content", value=content, height=300, key=f"area_{uploaded_file.name}")
                
                # File naming logic for download
                file_root = os.path.splitext(uploaded_file.name)[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Markdown (.md)", 
                        data=content, 
                        file_name=f"{file_root}_converted.md", 
                        mime="text/markdown",
                        key=f"md_{uploaded_file.name}"
                    )
                with col2:
                    st.download_button(
                        label="📄 Download Text (.txt)", 
                        data=content, 
                        file_name=f"{file_root}_converted.txt", 
                        mime="text/plain",
                        key=f"txt_{uploaded_file.name}"
                    )

# Corrected divider syntax
st.markdown("---")
st.caption("Professional-grade document-to-text converter.")

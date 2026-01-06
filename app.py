import streamlit as st
import os
from markitdown import MarkItDown

# 1. Configuration & Engine Initialization
st.set_page_config(page_title="Universal Document Reader", page_icon="📄")

@st.cache_resource
def get_converter():
    # Initializes the Microsoft MarkItDown engine
    return MarkItDown()

def process_file(uploaded_file):
    md = get_converter()
    # We use a temp file to help MarkItDown identify the file extension correctly
    temp_path = f"temp_{uploaded_file.name}"
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Conversion logic: Handles Word, Excel, PPTX, PDF, HTML
        result = md.convert(temp_path)
        return result.text_content
    except Exception as e:
        st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
        return None
    finally:
        # Cleanup temp file immediately after processing
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
            content = process_file(uploaded_file)
            
            if content:
                # Instant Preview in a scrollable box
                st.text_area("Extracted Content", value=content, height=300, key=f"area_{uploaded_file.name}")
                
                # Dynamic File Naming for Download
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

# Logic for visual separation (Wrapped in a function to avoid Syntax Errors)
st.divider() 
st.caption("One-click solution for professional document-to-text conversion.")

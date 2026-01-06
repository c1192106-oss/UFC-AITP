import streamlit as st
import os
from markitdown import MarkItDown
from io import BytesIO

# Configuration for stability & UX
st.set_page_config(page_title="Universal Document Reader", page_icon="📄")
USER_AGENT = "UniversalDocReader/1.0"

def save_and_convert(uploaded_file):
    """Temporary saves file to process via MarkItDown and returns content."""
    md_converter = MarkItDown()
    
    # markitdown typically works best with file paths or specific stream types
    # We create a temp file to ensure the 'engine' can read it reliably
    temp_filename = f"temp_{uploaded_file.name}"
    try:
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Conversion attempt
        result = md_converter.convert(temp_filename)
        return result.text_content
    except Exception as e:
        st.warning(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
        return None
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

# --- UI Interface ---
st.title("📄 Universal Document Reader")
st.markdown("Convert Office docs, PDFs, and HTML into clean Markdown instantly.")

# Upload Area
uploaded_files = st.file_uploader(
    "Drag and drop files here", 
    type=['docx', 'xlsx', 'pptx', 'pdf', 'html', 'zip'],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.expander(f"👁️ Preview: {uploaded_file.name}", expanded=True):
            with st.spinner(f"Processing {uploaded_file.name}..."):
                content = save_and_convert(uploaded_file)
            
            if content:
                # Instant Preview Box
                st.text_area(
                    label="Extracted Text",
                    value=content,
                    height=300,
                    key=f"text_{uploaded_file.name}"
                )
                
                # Download Options
                base_name = os.path.splitext(uploaded_file.name)[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download .md",
                        data=content,
                        file_name=f"{base_name}_converted.md",
                        mime="text/markdown",
                        key=f"md_{uploaded_file.name}"
                    )
                with col2:
                    st.download_button(
                        label="📄 Download .txt",
                        data=content,
                        file_name=f"{base_name}_converted.txt",
                        mime="text/plain",
                        key=f"txt_{uploaded_file.name}"
                    )

---
st.caption("Powered by Microsoft MarkItDown & Streamlit")

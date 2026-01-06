import streamlit as st
import os
import zipfile
from io import BytesIO
from markitdown import MarkItDown

# 1. Page Config & Setup
st.set_page_config(page_title="Pro Doc Converter", page_icon="🚀", layout="wide")

@st.cache_resource
def get_converter():
    return MarkItDown()

def format_size(bytes_size):
    return round(bytes_size / (1024 * 1024), 2)

def get_reading_time(text):
    words = len(text.split())
    minutes = round(words / 200) # Average reading speed
    return 1 if minutes == 0 else minutes

# 2. Main Interface
st.title("🚀 Pro Document Intelligence & Converter")
st.markdown("---")

uploaded_files = st.file_uploader(
    "Upload multiple documents for instant conversion", 
    type=['docx', 'xlsx', 'pptx', 'pdf', 'html', 'zip'],
    accept_multiple_files=True
)

# Global list to store processed files for the Batch Zip feature
all_converted_docs = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.expander(f"📦 Processing: {uploaded_file.name}", expanded=True):
            
            # Processing Logic
            converter = get_converter()
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                result = converter.convert(temp_path)
                content = result.text_content
                all_converted_docs.append({"name": uploaded_file.name, "content": content})
                
                # Layout Columns
                col_left, col_right = st.columns([2, 1])
                
                with col_left:
                    tab1, tab2 = st.tabs(["📄 Markdown Preview", "📊 Analysis"])
                    with tab1:
                        st.text_area("Content", value=content, height=350, key=f"txt_{uploaded_file.name}")
                    
                    with tab2:
                        # File Size Table
                        original_size = uploaded_file.size
                        converted_size = len(content.encode('utf-8'))
                        reduction = 100 * (1 - (converted_size / original_size))
                        
                        st.table({
                            "Metric": ["Original Size", "Converted Size", "Reduction"],
                            "Value": [f"{format_size(original_size)} MB", f"{format_size(converted_size)} MB", f"{round(reduction, 1)}%"]
                        })
                        
                with col_right:
                    st.metric("Reading Time", f"{get_reading_time(content)} min")
                    
                    file_root = os.path.splitext(uploaded_file.name)[0]
                    st.download_button("📥 Download .md", content, f"{file_root}.md", key=f"btn_md_{uploaded_file.name}")
                    st.download_button("📄 Download .txt", content, f"{file_root}.txt", key=f"btn_txt_{uploaded_file.name}")

            except Exception as e:
                st.error(f"⚠️ Error: {uploaded_file.name} is corrupted or unsupported.")
            finally:

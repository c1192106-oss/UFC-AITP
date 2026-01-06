import streamlit as st
import os
from markitdown import MarkItDown

# 1. Configuration & Engine Initialization
st.set_page_config(page_title="Universal Document Reader", page_icon="📄")

@st.cache_resource
def get_converter():
    return MarkItDown()

def format_size(bytes_size):
    """Converts bytes to a human-readable MB format."""
    return round(bytes_size / (1024 * 1024), 2)

def process_file(uploaded_file):
    md = get_converter()
    temp_path = f"temp_{uploaded_file.name}"
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
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
        with st.expander(f"👁️ {uploaded_file.name}", expanded=True):
            content = process_file(uploaded_file)
            
            if content:
                # Create Tabs
                tab1, tab2 = st.tabs(["📄 Preview & Download", "📊 File Size Comparison"])
                
                with tab1:
                    st.text_area("Extracted Content", value=content, height=300, key=f"area_{uploaded_file.name}")
                    file_root = os.path.splitext(uploaded_file.name)[0]
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.download_button("📥 Download .md", content, f"{file_root}.md", "text/markdown", key=f"md_{uploaded_file.name}")
                    with c2:
                        st.download_button("📄 Download .txt", content, f"{file_root}.txt", "text/plain", key=f"txt_{uploaded_file.name}")

                with tab2:
                    # Calculations
                    original_size = uploaded_file.size
                    converted_size = len(content.encode('utf-8'))
                    reduction = 100 * (1 - (converted_size / original_size))
                    
                    # Size Table
                    st.table({
                        "Version": ["Original File", "Converted Text"],
                        "Size (MB)": [f"{format_size(original_size)} MB", f"{format_size(converted_size)} MB"]
                    })
                    
                    st.success(f"✅ Text version is **{round(reduction, 1)}% smaller**.")

st.divider()
st.caption("Leave a comment in the section if you need help adding more file types!")

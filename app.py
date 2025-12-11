import streamlit as st
import pdfplumber
from io import BytesIO
import re
import json
from collections import Counter

# Page configuration
st.set_page_config(
    page_title="PDF Text Extractor",
    page_icon="📄",
    layout="wide"
)

# Title and description
st.title("Rebecca's PDF Text Extractor")
st.markdown("Upload a PDF file to extract text for FREE!! \n ONLY works on PDFs that contain actual digital text.")

# Initialize session state
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'total_pages' not in st.session_state:
    st.session_state.total_pages = 0

# Sidebar for options
with st.sidebar:
    st.header("Extraction Options")
    
    add_page_separator = st.checkbox("Add page separator lines", value=True)
    show_statistics = st.checkbox("Show simple text statistics", value=False)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Upload PDF")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Only PDF files are supported"
    )
    
    if uploaded_file is not None:
        st.success(f"File uploaded: **{uploaded_file.name}**")
        
        # Read PDF to get total pages
        try:
            with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
                total_pages = len(pdf.pages)
                st.session_state.total_pages = total_pages
                st.info(f"Total pages in PDF: **{total_pages}**")
        except Exception as e:
            st.error(f"❌ Error reading PDF: {str(e)}")
            st.stop()
        
        # Page range selector
        st.subheader("Page Range Selection")
        
        if st.session_state.total_pages > 0:
            if st.session_state.total_pages == 1:
                st.info("Single-page PDF detected. Page 1 will be extracted.")
                start_page = end_page = 1
                button_label = "🔍 Extract Text"
            else:
                page_range = st.slider(
                    "Select page range to extract",
                    min_value=1,
                    max_value=st.session_state.total_pages,
                    value=(1, st.session_state.total_pages),
                    help=f"Select pages 1 to {st.session_state.total_pages}"
                )
                start_page, end_page = page_range
                button_label = "🔍 Extract Text"
                
                # Validate page range
                if start_page > end_page:
                    st.error("❌ Invalid page range: Start page must be less than or equal to end page")
                    st.stop()
            
            # Extract button
            if st.button(button_label, type="primary", use_container_width=True):
                with st.spinner("Extracting text from PDF..."):
                    try:
                        # Reset file pointer
                        uploaded_file.seek(0)
                        
                        extracted_pages = []
                        pages_with_no_text = []
                        
                        with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
                            for page_num in range(start_page - 1, end_page):  # pdfplumber uses 0-based indexing
                                if page_num < len(pdf.pages):
                                    page = pdf.pages[page_num]
                                    page_text = page.extract_text()
                                    
                                    if page_text is None or page_text.strip() == "":
                                        pages_with_no_text.append(page_num + 1)
                                        continue
                                    
                                    if add_page_separator:
                                        extracted_pages.append(f"\n{'='*60}\nPage {page_num + 1}\n{'='*60}\n\n{page_text}")
                                    else:
                                        extracted_pages.append(page_text)
                        
                        # Combine all extracted text
                        full_text = "\n".join(extracted_pages)
                        
                        # Check if any text was extracted
                        if not full_text.strip():
                            st.warning("⚠️ This PDF appears to contain no extractable text (possibly scanned).")
                            st.session_state.extracted_text = ""
                        else:
                            st.session_state.extracted_text = full_text
                            
                            # Show warnings for pages with no text
                            if pages_with_no_text:
                                st.warning(f"⚠️ Pages with no extractable text: {', '.join(map(str, pages_with_no_text))}")
                            
                            st.success(f"Successfully extracted text from pages {start_page} to {end_page}!")
                    
                    except Exception as e:
                        st.error(f"❌ Error during extraction: {str(e)}")
                        st.session_state.extracted_text = ""
        else:
            st.error("❌ Could not determine PDF page count")

with col2:
    st.header("Extracted Text Preview")
    
    if st.session_state.extracted_text:
        # Text preview (first 5000 characters)
        preview_text = st.session_state.extracted_text[:5000]
        if len(st.session_state.extracted_text) > 5000:
            preview_text += "\n\n... (text truncated for preview)"
        
        st.text_area(
            "Preview (select and copy enabled)",
            value=preview_text,
            height=400,
            help="Select any portion to copy. Preview is limited to the first 5000 characters."
        )
        
        # Download button
        st.download_button(
            label="💾 Download TXT",
            data=st.session_state.extracted_text.encode("utf-8"),
            file_name="extracted_text.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )

        # Copy full text to clipboard (client-side)
        copy_text = json.dumps(st.session_state.extracted_text)
        st.components.v1.html(
            f"""
            <div style="display:flex;justify-content:flex-start;gap:8px;margin:8px 0;">
              <button id="copy-all-btn" style="padding:8px 12px;border:none;border-radius:4px;background:#0f8bff;color:white;cursor:pointer;">
                📋 Copy all extracted text
              </button>
              <span id="copy-status" style="font-size:14px;color:#444;"></span>
            </div>
            <script>
              const data = {copy_text};
              const btn = document.getElementById("copy-all-btn");
              const status = document.getElementById("copy-status");
              btn.onclick = async () => {{
                try {{
                  await navigator.clipboard.writeText(data);
                  status.textContent = "Copied!";
                  setTimeout(() => status.textContent = "", 2000);
                }} catch (err) {{
                  status.textContent = "Copy failed";
                  console.error(err);
                }}
              }};
            </script>
            """,
            height=60
        )
        
        # Statistics section
        if show_statistics:
            st.subheader("📊 Text Statistics")
            
            full_text = st.session_state.extracted_text
            
            # Basic statistics
            char_count = len(full_text)
            word_count = len(re.findall(r'\b\w+\b', full_text))
            
            # Count pages (based on separator if enabled, or estimate)
            if add_page_separator:
                page_count = full_text.count("Page ")
            else:
                # Estimate: count newlines and divide by average lines per page (rough estimate)
                page_count = max(1, full_text.count('\n') // 50)
            
            # Display basic stats
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("Character Count", f"{char_count:,}")
            with stat_col2:
                st.metric("Word Count", f"{word_count:,}")
            with stat_col3:
                st.metric("Page Count", page_count)
            
            # Word frequency analysis
            st.subheader("Top 10 Most Frequent Words")
            
            # Simple stopwords list
            stopwords = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
                'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had',
                'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
                'can', 'this', 'that', 'these', 'those', 'i', 'you','yours','yourself','himself','herself','itself','themselves', 'he', 'she', 'it', 'we', 'they',
                'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
                'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
                'own', 'same', 'so', 'than', 'too', 'very', 'just', 'now'
            }
            
            # Extract words and count frequency
            words = re.findall(r'\b[a-zA-Z]{3,}\b', full_text.lower())
            filtered_words = [w for w in words if w not in stopwords]
            word_freq = Counter(filtered_words)
            top_words = word_freq.most_common(10)
            
            if top_words:
                # Display as a table
                import pandas as pd
                df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No words found after filtering stopwords.")
    else:
        st.info("👈 Upload a PDF file and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("**PDF Text Extractor** - Built with Streamlit and pdfplumber")


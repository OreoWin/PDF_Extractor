# PDF Text Extractor - Streamlit Web App

A fully functional Streamlit web application for extracting text from PDF files using pdfplumber. No OCR required!

## Features

- 📤 **PDF File Upload** - Upload PDF files with validation
- 📑 **Page Range Selection** - Extract text from specific page ranges using an interactive slider
- ⚙️ **Customizable Options** - Add page separators and enable text statistics
- 📋 **Text Preview** - Preview extracted text (first 5000 characters)
- 💾 **Download Functionality** - Download extracted text as a .txt file
- 📊 **Text Statistics** - Optional word count, character count, page count, and top 10 word frequency analysis
- ⚠️ **Error Handling** - Comprehensive error messages and warnings

## Installation

1. **Install Python** (if not already installed)
   - Python 3.8 or higher is required

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Access the app**
   - The app will automatically open in your default web browser
   - If it doesn't, navigate to: `http://localhost:8501`

## Usage Instructions

1. **Upload PDF**
   - Click "Browse files" or drag and drop a PDF file
   - Only `.pdf` files are accepted

2. **Select Options** (in the sidebar)
   - Check "Add page separator lines" to add separators between pages
   - Check "Show simple text statistics" to display text analytics

3. **Select Page Range**
   - Use the slider to select which pages to extract (default: all pages)

4. **Extract Text**
   - Click the "Extract Text" button
   - Wait for the extraction to complete

5. **Preview & Download**
   - View the preview of extracted text (first 5000 characters)
   - Click "Download TXT" to save the full extracted text

## Features Explained

### Page Range Selection
- Dynamic slider that adjusts based on the total number of pages in the PDF
- Select any range from page 1 to the last page

### Page Separators
- When enabled, adds clear separators between pages in the extracted text
- Format: `============================================================ Page X ============================================================`

### Text Statistics
When enabled, displays:
- **Character Count**: Total number of characters in extracted text
- **Word Count**: Total number of words
- **Page Count**: Number of pages extracted
- **Top 10 Word Frequency**: Most common words (excluding common stopwords)

### Error Handling
The app handles various error scenarios:
- No file uploaded
- Invalid file type (non-PDF)
- Invalid page range
- Empty extraction results
- Pages with no extractable text

## Requirements

- Python 3.8+
- streamlit >= 1.28.0
- pdfplumber >= 0.10.0
- pandas >= 2.0.0

## Notes

- This app uses **pdfplumber** which extracts text from PDFs that contain text layers
- **Scanned PDFs** (image-based) will not work as they require OCR
- If a PDF appears to have no extractable text, a warning will be displayed
- Pages with no text are skipped with a warning message

## Troubleshooting

**App won't start:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

**PDF extraction fails:**
- Ensure the PDF contains text (not just images)
- Try a different PDF file to verify the app is working
- Check the error message for specific details

**Port already in use:**
- Streamlit uses port 8501 by default
- If occupied, use: `streamlit run app.py --server.port 8502`

## License

This project is open source and available for use.


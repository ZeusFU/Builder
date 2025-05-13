import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import io

st.set_page_config(page_title="Bulk OCR Text Extractor", layout="wide")

st.title("📸 Bulk OCR Text Extractor")
st.markdown("""
Upload up to 110 snapshot images and extract text from each using Tesseract OCR.
""")

uploaded_files = st.file_uploader(
    label="Upload snapshot images",
    type=["png", "jpg", "jpeg", "bmp", "tiff"],
    accept_multiple_files=True
)

if uploaded_files:
    results = []
    for img_file in uploaded_files:
        img = Image.open(img_file)
        text = pytesseract.image_to_string(img)
        results.append({"filename": img_file.name, "text": text})
        
    df = pd.DataFrame(results)
    
    st.subheader("Extracted Text Preview")
    st.dataframe(df, use_container_width=True)
    
    # Allow download as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="ocr_results.csv",
        mime="text/csv"
    )
else:
    st.info("Upload snapshot images (up to 110) to get started.")

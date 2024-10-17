# Import necessary libraries
import streamlit as st
import PyPDF2
from googletrans import Translator
from transformers import pipeline

# Initialize Google Translator and Transformers Summarizer
translator = Translator()
summarizer = pipeline("summarization")

def read_pdf(file):
    """Reads a PDF file and returns its text content."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def translate_text(text, target_language='mr'):
    """Translates text to the target language (Marathi in this case)."""
    translated = translator.translate(text, dest=target_language)
    return translated.text

def summarize_text(text):
    """Summarizes the text using the Transformers summarization pipeline."""
    if len(text) < 50:  # Adjust this threshold based on input size
        return "Text too short to summarize."
    
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Streamlit UI
def main():
    st.title("PDF Translator and Summarizer")

    # File uploader in Streamlit
    uploaded_file = st.file_uploader("Please upload a PDF file", type="pdf")

    if uploaded_file is not None:
        # Read and extract text from the PDF file
        pdf_text = read_pdf(uploaded_file)
        st.subheader("Original Text:")
        st.text(pdf_text)

        # Translate the text to Marathi
        translated_text = translate_text(pdf_text, target_language='mr')
        st.subheader("Translated Text (Marathi):")
        st.text(translated_text)

        # Summarize the original text
        summary = summarize_text(pdf_text)
        st.subheader("Summary (English):")
        st.text(summary)

        # Translate the summary to Marathi
        translated_summary = translate_text(summary, target_language='mr')
        st.subheader("Summary in Marathi:")
        st.text(translated_summary)

# Run the main function in Streamlit
if __name__ == "__main__":
    main()

from PyPDFForm import PdfWrapper
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from datetime import datetime, timedelta, date
import os
from PIL import Image
import numpy as np

# get info (form fillout)
name = st.text_input("Legal name")
birthday = st.date_input(
    "Birthday",
    value=(datetime.now() - timedelta(days=18*365+1)),
    format="DD/MM/YYYY",
    min_value=date(1950, 1, 1),
    max_value=(datetime.now() - timedelta(days=18*365))
)
email = st.text_input("Email")
phone_num = st.text_input("Phone number")

telegram_checkbox = st.checkbox("Telegram")
whatsapp_checkbox = st.checkbox("WhatsApp")
signal_checkbox = st.checkbox("Signal")
other_toggle = st.toggle("Other messenger")

if other_toggle:
    other_text = st.text_input("Messenger")
else:
    other_text = ""

newsletter_checkbox = st.checkbox("Receive Sicut Dico Newsletter?")

date = st.date_input("Applicable date", value=datetime.now(), format="DD/MM/YYYY")

# Create two columns for the canvas
col1, col2 = st.columns([3, 1])

with col1:
    canvas = st_canvas(
        stroke_width=2,
        update_streamlit=True,
        height=150,
        drawing_mode="freedraw",
        key="canvas",
    )

button = st.button(label="All done?")

if button:
    try:
        form_data = {
            "Full legal name": name,
            "Birth date": birthday.strftime("%m/%d/%Y"),
            "Contact Email and phone 1": phone_num,
            "Contact Email and phone 2": email,
            "Telegram": "/Yes" if telegram_checkbox else "/Off",
            "WhatsApp": "/Yes" if whatsapp_checkbox else "/Off",
            "Signal": "/Yes" if signal_checkbox else "/Off",
            "Other": "/Yes" if other_toggle else "/Off",
            "other preferred messenger": other_text,
            "newsletter": "/Yes" if newsletter_checkbox else "/Off",
            "Date": date.strftime("%m/%d/%Y"),
        }
        
        # Create PDF wrapper and fill initial data
        pdf = PdfWrapper("Release Agreement Form - Model _ 18+.pdf")
        
        # Handle signature
        if canvas is not None and canvas.image_data is not None:
            if np.any(canvas.image_data):
                # Create temporary file for signature
                temp_sig_path = "temp_signature.png"
                signature_image = Image.fromarray((canvas.image_data * 255).astype(np.uint8))
                signature_image.save(temp_sig_path)
                
                # Add signature to form data using file path
                form_data["signature_es_:signatureblock"] = signature_image

        # Fill the form
        filled_pdf = pdf.fill(form_data)

        # Create a safe filename
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '.', '_')).rstrip()
        new_filename = f"Release_Agreement_Form_-_Model_{safe_name}_{date.strftime('%Y-%m-%d')}_18+.pdf"

        # Save and offer download
        with open(new_filename, "wb") as output_stream:
            output_stream.write(filled_pdf.read())

        with open(new_filename, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name=new_filename,
                mime="application/pdf"
            )

        # Clean up temporary files
        if os.path.exists(temp_sig_path):
            os.remove(temp_sig_path)
        os.remove(new_filename)
        
    except Exception as e:
        st.error(f"An error occurred while processing the form: {str(e)}")

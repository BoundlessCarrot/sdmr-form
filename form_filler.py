from PyPDFForm import PdfWrapper
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from datetime import datetime, timedelta, date
import os
import io
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
    other_text = st.text_input("Mesenger")
else:
    other_text = ""

newsletter_checkbox = st.checkbox("Receive Sicut Dico Newsletter?")

date = st.date_input("Applicable date", value=datetime.now(), format="DD/MM/YYYY")

canvas = st_canvas(
    stroke_width=2,
    update_streamlit=False,
    height=150,
    drawing_mode="freedraw",
    key="canvas",
)

button = st.button(label="All done?")

if button:
    # update pdf with info

    signature_bytes = None
    if canvas is not None and canvas.image_data is not None:
        # Check if there's any drawing
        if np.any(canvas.image_data):
            # Convert numpy array to PIL Image
            signature_image = Image.fromarray((canvas.image_data * 255).astype(np.uint8))
            
            # Convert PIL Image to bytes
            signature_buffer = io.BytesIO()
            signature_image.save(signature_buffer, format='PNG')
            signature_bytes = signature_buffer.getvalue()        
    
    form_data = {
        "Full legal name": name,
        "Birth date": birthday.strftime("%m/%d/%Y"),
        "Contact Email and phone 1": phone_num,
        "Contact Email and phone 2": email,
        "Telegram": telegram_checkbox,
        "WhatsApp": whatsapp_checkbox,
        "Signal": signal_checkbox,
        "Other": other_toggle,
        "other preferred messenger": other_text,
        "newsletter": newsletter_checkbox,
        "Date": date.strftime("%m/%d/%Y"),
    }
    
    # Only add signature if it exists
    if signature_bytes:
        form_data["signature_es_:signatureblock"] = signature_bytes

    filler = PdfWrapper("Release Agreement Form - Model _ 18+.pdf").fill(form_data)
    
    # Create a safe filename
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '.', '_')).rstrip()
    new_filename = f"Release_Agreement_Form_-_Model_{safe_name}_{date.strftime('%Y-%m-%d')}_18+.pdf"

    # Ensure the file is created in the current working directory
    new_filepath = os.path.join(os.getcwd(), new_filename)

    with open(new_filepath, "wb+") as output_stream:
        output_stream.write(filler.read())

    # Use the file path for the download button
    with open(new_filepath, "rb") as file:
        st.download_button(
            label="Download PDF",
            data=file,
            file_name=new_filename,
            mime="application/pdf"
        )

    # Optionally, remove the file after offering download
    os.remove(new_filepath)

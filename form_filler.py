from pypdf import PdfReader, PdfWriter
import streamlit as st
from streamlit_drawable_canvas import st_canvas 

# get info (form fillout)
name = st.text_input("Legal name")
birthday = st.date_input("Birthday")
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

date = st.date_input("Applicable date", "today")

signature = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=2,
    stroke_color=0x000000,
    background_color=0xEEEEEE,
    background_image=None,
    update_streamlit=False,
    height=150,
    drawing_mode="freedraw",
    point_display_radius=0,
    key="canvas",
)

# update pdf with info
reader = PdfReader("Release Agreement Form - Model _ 18+.pdf")
writer = PdfWriter()

fields = reader.get_fields()
writer.append(reader)

new_filename = f"Release Agreement Form - Model {name}/{date} 18+.pdf"

writer.update_page_form_field_values(
    writer.pages[0],
    {
        "Full legal name": name,
        "Birth date": birthday,
        "Contact Email and phone 1": email,
        "Contact Email and phone 2": phone_num,
    },
    auto_regenerate=False
)

# NOTE: do we need to write after each page?

writer.update_page_form_field_values(
    writer.pages[1],
    {
        "Telegram": telegram_checkbox,
        "WhatsApp": whatsapp_checkbox,
        "Signal": signal_checkbox,
        "Other": other_toggle,
        "other preferred messenger": other_text,
        "newsletter": newsletter_checkbox,
        "Date": date,
        "signature_es_:signatureblock": signature 
    },
    auto_regenerate=False
)

# NOTE: maybe add custom filename with date and persons name here
with open(new_filename, "wb") as output_stream:
    writer.write(output_stream)

st.download_button("Download PDF", new_filename)

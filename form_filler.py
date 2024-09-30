from pypdf import PdfReader, PdfWriter
import streamlit as st
# from streamlit_drawable_canvas import st_canvas
from datetime import datetime, timedelta, date

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

# signature = st_canvas(
#     fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
#     stroke_width=2,
#     stroke_color=0x000,
#     background_color=0xEEE,
#     background_image=None,
#     update_streamlit=False,
#     height=150,
#     drawing_mode="freedraw",
#     point_display_radius=0,
#     key="canvas",
# )

button = st.button(label="All done?")

if button:
    # update pdf with info
    reader = PdfReader("Release Agreement Form - Model _ 18+.pdf")
    writer = PdfWriter()

    writer.append(reader)

    writer.update_page_form_field_values(
        writer.pages[0],
        {
            "Full legal name": name,
            "Birth date": birthday.strftime("%m/%d/%Y"),
            "Contact Email and phone 1": phone_num,
            "Contact Email and phone 2": email,
        },
        auto_regenerate=False
    )

    # NOTE: do we need to write after each page?

    writer.update_page_form_field_values(
        writer.pages[1],
        {
            "Telegram": "/Yes" if telegram_checkbox else "/Off",
            "WhatsApp": "/Yes" if whatsapp_checkbox else "/Off",
            "Signal": "/Yes" if signal_checkbox else "/Off",
            "Other": "/Yes" if other_toggle else "/Off",
            "other preferred messenger": other_text,
            "newsletter": "/Yes" if newsletter_checkbox else "/Off",
            "Date": date.strftime("%m/%d/%Y"),
        },
        auto_regenerate=False
    )

    new_filename = f"Release Agreement Form - Model {name}/{date} 18+.pdf"

    with open(new_filename, "wb") as output_stream:
        writer.write(output_stream)

    st.download_button("Download PDF", new_filename)

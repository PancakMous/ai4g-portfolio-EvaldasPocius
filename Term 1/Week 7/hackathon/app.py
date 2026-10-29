import streamlit as st
from PIL import Image, ImageDraw
from inference_sdk import InferenceHTTPClient

MODEL_ID = "hakis-workspace-y3j23/hackathon-civ4a-1-rfdetr-small-t1"

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=st.secrets["ROBOFLOW_API_KEY"],
)

st.title("StreetScan")
st.write("Upload a photo and the model will detect ... (fill in what you detect)")

conf = st.slider("Minimum confidence", 0.1, 0.9, 0.4)
file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])

if file:
    img = Image.open(file).convert("RGB")
    with st.spinner("Detecting..."):
        result = client.infer(img, model_id=MODEL_ID)
    draw = ImageDraw.Draw(img)
    found = [p for p in result["predictions"] if p["confidence"] >= conf]
    for p in found:
        x, y, w, h = p["x"], p["y"], p["width"], p["height"]  # x,y = box center
        draw.rectangle([x - w/2, y - h/2, x + w/2, y + h/2], outline="lime", width=4)
        draw.text((x - w/2, y - h/2 - 12), f'{p["class"]} {p["confidence"]:.0%}', fill="lime")
    st.image(img, use_container_width=True)
    st.write(f"{len(found)} detection(s)")

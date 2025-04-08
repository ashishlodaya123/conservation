import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="Monument Conservation Analyzer", layout="centered")
st.title("🏛️ Monument Conservation Detector (Enhanced Heuristic-Based)")

uploaded_file = st.file_uploader("Upload a monument image", type=["jpg", "jpeg", "png"])

def analyze_monument(img_cv):
    # Convert to grayscale and HSV
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

    # 1. Edge Detection (cracks, sharp structures)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size

    # 2. Brightness Check
    brightness = np.mean(gray) / 255.0  # 0 to 1 scale

    # 3. Texture Analysis using Laplacian variance (blur = less texture)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # 4. Color Saturation
    saturation = np.mean(hsv[:, :, 1]) / 255.0

    # Heuristic Rule
    if edge_density > 0.07 or brightness < 0.45 or laplacian_var < 100 or saturation < 0.3:
        decision = "Conservation Needed"
    else:
        decision = "No Conservation Needed"

    return decision, {
        "Edge Density": edge_density,
        "Brightness": brightness,
        "Texture (Laplacian Variance)": laplacian_var,
        "Color Saturation": saturation
    }

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Monument", use_container_width=True)

    image_np = np.array(image)
    img_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    with st.spinner("Analyzing the monument..."):
        decision, metrics = analyze_monument(img_cv)

        st.markdown(f"### 🔍 Result: **{decision}**")
        st.markdown("---")
        st.subheader("📊 Analysis Metrics:")
        st.markdown(f"- 🧱 **Edge Density**: `{metrics['Edge Density']:.3f}`")
        st.markdown(f"- 💡 **Brightness**: `{metrics['Brightness']:.3f}`")
        st.markdown(f"- 🌀 **Texture Variance**: `{metrics['Texture (Laplacian Variance)']:.2f}`")
        st.markdown(f"- 🎨 **Color Saturation**: `{metrics['Color Saturation']:.3f}`")

        if decision == "Conservation Needed":
            st.warning("⚠️ This monument may show signs of wear and might require conservation.")
        else:
            st.success("✅ The monument appears to be in good condition.")

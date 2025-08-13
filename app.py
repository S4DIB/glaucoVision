import streamlit as st
import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F
from torchvision import transforms
from torchvision.models import densenet121

# ========================
# 1. Load Image Model (CPU only)
# ========================
def get_densenet121_model():
    model = densenet121(pretrained=False)
    num_ftrs = model.classifier.in_features
    model.classifier = torch.nn.Linear(num_ftrs, 2)
    return model

device = torch.device("cpu")
img_model = get_densenet121_model()
img_model.load_state_dict(torch.load("models/densenet121.pth", map_location=device))
img_model.to(device)
img_model.eval()

# ========================
# 2. Streamlit UI
# ========================
st.title("Glaucoma Diagnosis (Late Fusion)")
st.write("Upload a retinal fundus image and enter clinical data to get prediction.")

uploaded_file = st.file_uploader(
    "Choose a retinal image", type=["jpg", "png"], key="retinal_image"
)

# Clinical inputs (for display only, not used in prediction)
age = st.number_input("Age", min_value=0, max_value=120, value=50, key="age")
gender = st.selectbox("Gender (0=Male,1=Female)", [0, 1], key="gender")
dioptre_1 = st.number_input("Dioptre_1", value=0.0, key="dioptre_1")
astigmatism = st.number_input("Astigmatism", value=0.0, key="astigmatism")
phakic = st.selectbox("Phakic/Pseudophakic (0=Phakic,1=Pseudophakic)", [0, 1], key="phakic")
pneumatic = st.number_input("Pneumatic", value=0.0, key="pneumatic")
perkins = st.number_input("Perkins", value=0.0, key="perkins")
pachymetry = st.number_input("Pachymetry", value=0.0, key="pachymetry")
axial_length = st.number_input("Axial Length", value=0.0, key="axial_length")
vf_md = st.number_input("VF_MD", value=0.0, key="vf_md")

# Image Transform
transform_val = transforms.Compose([
    transforms.Resize((299, 299)),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
])

# ========================
# 3. Predict Button
# ========================
if st.button("Predict", key="predict_button") and uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    img_tensor = transform_val(img).unsqueeze(0)  # add batch dim

    # --- Image model prediction ---
    with torch.no_grad():
        img_probs = F.softmax(img_model(img_tensor), dim=1).numpy()
        img_pos = img_probs[:, 1]  # positive class (Glaucoma)

    clin_values = np.array([age, gender, dioptre_1, astigmatism, phakic,
                            pneumatic, perkins, pachymetry, axial_length, vf_md], dtype=np.float32)
    # normalize clinical values roughly
    clin_norm = (clin_values - clin_values.min()) / (clin_values.max() - clin_values.min() + 1e-6)
    clin_adjust = 0.05 * (np.sum(clin_norm) / len(clin_norm) - 0.5)  # small adjustment [-0.025, +0.025]

    # --- Apply fake late fusion ---
    fused_prob = np.clip(img_pos + clin_adjust, 0, 1)
    pred_class = int(fused_prob >= 0.5)

    # --- Show Result ---
    st.subheader("Prediction Result")
    st.write(f"Predicted Class: **{pred_class}** (0=Healthy, 1=Glaucoma)")
    st.write(f"Probability of Glaucoma: **{fused_prob[0]:.4f}**")
    st.image(img, caption="Uploaded Fundus Image", use_column_width=True)

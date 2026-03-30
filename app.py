import streamlit as st
from PIL import Image
from snake_ai_system import final_prediction
import geocoder
import requests
import pandas as pd

# -------------------------------
# 🔹 CONFIG
# -------------------------------

GEOAPIFY_API_KEY = "df7b0449981e4a9d87c1533025dc9313"
st.set_page_config(page_title="Snake AI System", layout="wide")

# -------------------------------
# 🔹 PREMIUM CSS
# -------------------------------

st.markdown("""
<style>
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(0,255,200,0.2);
    animation: fadeUp 1s;
}
.title {
    font-size: 40px;
    font-weight: bold;
    color: #00FFC6;
}
@keyframes fadeUp {
    from {opacity:0; transform:translateY(20px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🔹 FUNCTIONS
# -------------------------------

def get_user_location():
    try:
        g = geocoder.ip('me')
        if g.ok:
            return g.latlng, g.city
    except:
        pass
    return (None, None), None


def get_nearby_hospitals(lat, lon):
    url = f"https://api.geoapify.com/v2/places?categories=healthcare.hospital&filter=circle:{lon},{lat},5000&limit=10&apiKey={GEOAPIFY_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        hospitals = []

        for place in data.get("features", []):
            props = place["properties"]

            name = props.get("name")
            if not name:
                continue

            address = props.get("formatted", "Address not available")
            h_lat = props.get("lat")
            h_lon = props.get("lon")

            link = f"https://www.google.com/maps?q={h_lat},{h_lon}"

            hospitals.append({
                "name": name,
                "address": address,
                "lat": h_lat,
                "lon": h_lon,
                "link": link
            })

            if len(hospitals) == 5:
                break

        return hospitals

    except:
        return []

# -------------------------------
# 🔹 ADVANCED FIRST AID LOGIC
# -------------------------------

def get_first_aid_by_type(snake_type):

    s = snake_type.lower()

    # 🧠 NEUROTOXIC (Cobra, Krait)
    if "cobra" in s or "krait" in s:
        return [
            "Keep the victim completely calm and restrict movement",
            "Immobilize the affected limb using splints",
            "Keep limb at heart level (not above)",
            "Remove tight clothing, rings, and accessories",
            "DO NOT cut, suck, or apply ice",
            "Continuously monitor breathing (risk of paralysis)",
            "Keep airway clear and be ready for CPR",
            "Do not give food, alcohol, or caffeine",
            "Transport immediately to nearest hospital"
        ]

    # 🩸 HEMOTOXIC (Viper)
    elif "viper" in s:
        return [
            "Keep patient calm and minimize movement",
            "Immobilize the bitten limb below heart level",
            "Clean wound gently with water",
            "DO NOT apply tourniquet or pressure band",
            "Watch for swelling, bleeding, bruising",
            "Avoid massaging or touching wound",
            "Monitor for internal bleeding symptoms",
            "Transport immediately to hospital",
            "Keep patient hydrated but still"
        ]

    # ✅ NON-VENOMOUS
    elif "non venomous" in s:
        return [
            "Clean the wound with antiseptic solution",
            "Apply a sterile bandage",
            "Keep the wound dry and clean",
            "Monitor for infection (redness, swelling)",
            "Take tetanus vaccination if needed",
            "Rest and observe for any unusual symptoms"
        ]

    # ⚠️ UNKNOWN
    else:
        return [
            "Keep the patient calm and still",
            "Immobilize the affected limb",
            "Avoid cutting, sucking, or applying ice",
            "Remove tight accessories",
            "Seek immediate medical help"
        ]

# -------------------------------
# 🔹 HEADER
# -------------------------------

st.markdown('<div class="title">🐍 Snake Detection & Advisory System</div>', unsafe_allow_html=True)
st.markdown("### Smart Detection • First Aid • Hospital Locator")

# -------------------------------
# 🔹 INPUT
# -------------------------------

st.markdown('<div class="glass">', unsafe_allow_html=True)

snake_name = st.text_input("Snake name (optional)")
snake_image_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

snake_image = None

if snake_image_file:
    snake_image = Image.open(snake_image_file)
    st.image(snake_image, use_column_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 🔹 SYMPTOMS
# -------------------------------

st.markdown('<div class="glass">', unsafe_allow_html=True)

pain = st.slider("Pain Level", 0, 10)
swelling = st.slider("Swelling", 0, 10)
bleeding = st.checkbox("Bleeding")
nausea = st.checkbox("Nausea")
paralysis = st.checkbox("Paralysis")
vision = st.checkbox("Vision Problem")
breathing = st.checkbox("Breathing Difficulty")
tissue = st.checkbox("Tissue Damage")

st.markdown('</div>', unsafe_allow_html=True)

symptoms = [
    pain, swelling,
    int(bleeding), int(nausea),
    int(paralysis), int(vision),
    int(breathing), int(tissue)
]

# -------------------------------
# 🔹 PREDICTION
# -------------------------------

if st.button("🔍 Analyze Snake"):

    with st.spinner("Analyzing..."):
        snake_type = final_prediction(
            snake_name=snake_name,
            snake_image=snake_image,
            symptoms=symptoms
        )

    st.success(f"🧠 Detected Snake: {snake_type}")

    # -------------------------------
    # 🔹 DETAILED FIRST AID
    # -------------------------------

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("🩺 First Aid (Based on Snake Type)")

    advice = get_first_aid_by_type(snake_type)

    for step in advice:
        st.markdown(f"✅ {step}")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------
    # 🔹 CONDITIONAL HOSPITAL
    # -------------------------------

    if snake_type.lower() == "non venomous":
        st.success("✅ No need of hospitals. You are safe.")

    else:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("🏥 Nearby Hospitals")

        (lat, lon), city = get_user_location()

        if lat and lon:
            st.info(f"📍 Location: {city}")

            hospitals = get_nearby_hospitals(lat, lon)

            if hospitals:
                map_data = pd.DataFrame(
                    [{"lat": lat, "lon": lon}] +
                    [{"lat": h["lat"], "lon": h["lon"]} for h in hospitals]
                )

                st.map(map_data)

                for h in hospitals:
                    st.markdown(f"""
                    <div class="glass">
                        <h4>🏥 {h['name']}</h4>
                        <p>{h['address']}</p>
                        <a href="{h['link']}" target="_blank">Open in Maps</a>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.warning("No hospitals found")

        else:
            st.error("Location not detected")

        st.markdown('</div>', unsafe_allow_html=True)
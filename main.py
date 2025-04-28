import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from streamlit_mic_recorder import mic_recorder

from image import get_gemini_response
from utils.voice import speak_response
from utils.translate import translate_text
from utils.chat_storage import save_chat, load_chat

st.set_page_config(page_title="AI Fitness Coach 💪", layout="centered")
st.title("🏋️ AI Fitness Coach")

# Sidebar Settings
st.sidebar.title("⚙️ Fitness Settings")
task_type = st.sidebar.selectbox("Choose Fitness Goal", [
    "💪 Training Advice",
    "🍗 Protein-Rich Diet",
    "💡 Muscle Group Exercises",
    "🎯 Dream Physique Strategy",
    "🥗 Balanced Diet Tips",
    "🕒 Workout Schedule",
    "🧠 Custom Question"
])

translate_option = st.sidebar.checkbox("🌍 Translate Output (Hindi)")
voice_option = st.sidebar.checkbox("🔊 Read Out Loud")
canvas_mode = st.sidebar.checkbox("🎨 Enable Drawing on Image (Form Check)")

# Show diet preference only if diet-related task
diet_type = None
if task_type in ["🍗 Protein-Rich Diet", "🥗 Balanced Diet Tips"]:
    diet_type = st.sidebar.radio("🍽️ Choose Diet Preference", ["Vegetarian", "Non-Vegetarian"])

# BMI Calculator with Ideal Weight Range
st.sidebar.markdown("---")
st.sidebar.subheader("📏 BMI & Ideal Weight Checker")

height_cm = st.sidebar.number_input("Enter your height (cm):", min_value=100, max_value=250, value=170)
weight_kg = st.sidebar.number_input("Enter your weight (kg):", min_value=30, max_value=250, value=70)

if st.sidebar.button("🧮 Calculate BMI"):
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)

    if bmi < 18.5:
        status = "Underweight 😕"
    elif 18.5 <= bmi < 25:
        status = "Normal weight 🙂"
    elif 25 <= bmi < 30:
        status = "Overweight 😐"
    else:
        status = "Obese 😟"

    min_ideal_weight = round(18.5 * (height_m ** 2), 1)
    max_ideal_weight = round(24.9 * (height_m ** 2), 1)

    st.sidebar.success(f"🧠 BMI: {bmi} ({status})")
    st.sidebar.info(f"✅ Ideal Weight Range: {min_ideal_weight}kg – {max_ideal_weight}kg")

# Input and image upload
user_input = st.text_input("💬 Ask your fitness question (optional):")

uploaded_file = st.file_uploader("📁 Upload an image (form or physique check)", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if canvas_mode:
        st.subheader("🖌️ Draw on the Image")
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=3,
            stroke_color="#000000",
            background_image=image,
            update_streamlit=True,
            height=400,
            drawing_mode="freedraw",
            key="canvas"
        )

# Prompt builder based on task and diet preference
if task_type == "🍗 Protein-Rich Diet":
    prompt = "What foods should I eat to reach 150g of protein daily?"
    if diet_type:
        prompt += f" I prefer a {diet_type.lower()} diet."
elif task_type == "🥗 Balanced Diet Tips":
    prompt = "Provide a high-protein, low-carb diet plan on a budget."
    if diet_type:
        prompt += f" Make sure it is a {diet_type.lower()} diet."
elif task_type == "💪 Training Advice":
    prompt = "Suggest a weekly training plan for building muscle and burning fat."
elif task_type == "💡 Muscle Group Exercises":
    prompt = "List the best exercises to build my chest and shoulders."
elif task_type == "🎯 Dream Physique Strategy":
    prompt = "How can I achieve a lean, muscular physique like a fitness model?"
elif task_type == "🕒 Workout Schedule":
    prompt = "Create a 5-day workout split with strength and cardio mix."
elif task_type == "🧠 Custom Question":
    prompt = user_input
else:
    prompt = ""

# Append user input if it's not a custom question
if task_type != "🧠 Custom Question" and user_input:
    prompt += " " + user_input

# Submit button
if st.button("🚀 Get Fitness Guidance"):
    if image or user_input:
        with st.spinner("Processing with Gemini..."):
            response = get_gemini_response(prompt, image)

            if translate_option:
                response = translate_text(response)

            if voice_option:
                audio_path = speak_response(response)
                st.audio(audio_path, format="audio/mp3")

            st.subheader("💡 AI Fitness Response")
            st.write(response)
            save_chat(prompt, response)
    else:
        st.warning("⚠️ Please upload an image or enter a question.")

# Show Chat History
if st.checkbox("📜 Show Past Questions"):
    history = load_chat()
    for idx, chat in enumerate(history[::-1]):
        st.markdown(f"**🏋️‍♂️ Q{idx+1}:** {chat['question']}")
        st.markdown(f"**💬 A{idx+1}:** {chat['response']}")

# Microphone input
st.subheader("🎙️ Voice Input (Optional)")
audio_text = mic_recorder(start_prompt="▶️ Speak", stop_prompt="⏹️ Stop", just_once=True)

if audio_text:
    st.write("🗣️ You said:", audio_text)
    user_input = audio_text
else:
    user_input = st.text_input("💬 Or type your question:")

# Download chat history
if st.button("📥 Download Your Fitness Q&A"):
    history = load_chat()
    content = "\n\n".join([f"Q: {c['question']}\nA: {c['response']}"] for c in history)
    st.download_button("⬇️ Save as .txt", content, file_name="fitness_chat_history.txt")

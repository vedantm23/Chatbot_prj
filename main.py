import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from image import get_gemini_response
from utils.voice import speak_response
from utils.translate import translate_text
from utils.chat_storage import save_chat, load_chat

st.set_page_config(page_title="Gemini AI Chatbot", layout="centered")
st.title("🖼️ Gemini Advanced Image Chatbot")

# Sidebar Settings
st.sidebar.title("⚙️ Settings")
task_type = st.sidebar.selectbox("Choose Task", [
    "Describe Image",
    "Detect Objects",
    "Creative Story",
    "Custom Prompt"
])

translate_option = st.sidebar.checkbox("🌍 Translate Output (Hindi)")
voice_option = st.sidebar.checkbox("🔊 Read Out Loud")
canvas_mode = st.sidebar.checkbox("🎨 Enable Drawing on Image")

# Input and image upload
user_input = st.text_input("Input your question (optional):")

uploaded_file = st.file_uploader("📁 Upload an image", type=["jpg", "jpeg", "png"])
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

# Task-based prompt builder
prompt_map = {
    "Describe Image": "Give a detailed description of the image.",
    "Detect Objects": "List all identifiable objects in this image.",
    "Creative Story": "Generate a creative short story based on this image.",
    "Custom Prompt": user_input
}
prompt = prompt_map[task_type]
if task_type != "Custom Prompt" and user_input:
    prompt += " " + user_input

# Submit button
if st.button("🚀 Generate Response"):
    if image:
        with st.spinner("Processing with Gemini..."):
            response = get_gemini_response(prompt, image)

            if translate_option:
                response = translate_text(response)

            if voice_option:
                audio_path = speak_response(response)
                st.audio(audio_path, format="audio/mp3")

            st.subheader("🧠 Gemini's Response")
            st.write(response)
            save_chat(prompt, response)
    else:
        st.warning("⚠️ Please upload an image first.")

# Show Chat History
if st.checkbox("📝 Show Chat History"):
    history = load_chat()
    for idx, chat in enumerate(history[::-1]):
        st.markdown(f"**🗨️ Q{idx+1}:** {chat['question']}")
        st.markdown(f"**💬 A{idx+1}:** {chat['response']}")

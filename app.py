import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pyperclip
import os
import base64

# Page setup
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 AI Language Translation Tool")

st.write(
    "Translate text and hear the translated speech."
)

# Languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Russian": "ru",
    "Arabic": "ar"
}

# Input text
text = st.text_area(
    "Enter Text",
    placeholder="Type here...",
    height=150
)

# Source language
source_language = st.selectbox(
    "Select Source Language",
    list(languages.keys())
)

# Target language
target_language = st.selectbox(
    "Select Target Language",
    list(languages.keys()),
    index=1
)

# Translate button
if st.button("Translate"):

    if not text.strip():

        st.warning(
            "Please enter some text."
        )

    elif source_language == target_language:

        st.warning(
            "Source and target language cannot be same."
        )

    else:

        try:

            translated = GoogleTranslator(
                source=languages[source_language],
                target=languages[target_language]
            ).translate(text)

            audio_file = "translated_audio.mp3"

            tts = gTTS(
                text=translated,
                lang=languages[target_language]
            )

            tts.save(audio_file)

            audio_bytes = open(
                audio_file,
                "rb"
            ).read()

            audio_base64 = base64.b64encode(
                audio_bytes
            ).decode()

            st.success(
                "Translation Completed ✅"
            )

            col1, col2 = st.columns(
                [6,1]
            )

            with col1:

                st.text_area(
                    "Translated Text",
                    translated,
                    height=150
                )

            with col2:

                speaker_html = f"""
                <audio id="player">
                    <source
                    src="data:audio/mp3;base64,{audio_base64}"
                    type="audio/mp3">
                </audio>

                <button
                onclick="
                document.getElementById(
                'player'
                ).play()"
                style="
                font-size:28px;
                border:none;
                background:none;
                cursor:pointer;
                margin-top:35px;">
                🔊
                </button>
                """

                st.components.v1.html(
                    speaker_html,
                    height=80
                )

            if st.button(
                "Copy Translation"
            ):

                pyperclip.copy(
                    translated
                )

                st.success(
                    "Copied Successfully ✅"
                )

            st.download_button(
                "Download Translation",
                translated,
                "translated_text.txt"
            )

            st.download_button(
                "Download Audio",
                audio_bytes,
                "translation_audio.mp3"
            )

            os.remove(
                audio_file
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

st.markdown("---")
st.caption(
    "Created for CodeAlpha AI Internship"
)
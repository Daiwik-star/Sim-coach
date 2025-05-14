import streamlit as st
import pandas as pd
import pyttsx3

st.set_page_config(page_title="Sim Racing Coach Dashboard", layout="wide")
st.title("🏎️ Sim Racing Coach - Driver61 Style")

st.sidebar.header("📂 Upload Lap Files")
ref_file = st.sidebar.file_uploader("Upload Reference Lap CSV", type=["csv"])
user_file = st.sidebar.file_uploader("Upload User Lap CSV", type=["csv"])

if ref_file and user_file:
    ref_df = pd.read_csv(ref_file)
    user_df = pd.read_csv(user_file)

    merged_df = pd.merge(user_df, ref_df, on="corner_name", suffixes=("_user", "_ref"))

    feedback = []
    for _, row in merged_df.iterrows():
        corner = row['corner_name']
        advice = []

        brake_diff = row['brake_user'] - row['brake_ref']
        throttle_diff = row['throttle_user'] - row['throttle_ref']
        speed_diff = row['speed_user'] - row['speed_ref']

        if brake_diff < -0.1:
            advice.append(f"Brake later at {corner}.")
        elif brake_diff > 0.1:
            advice.append(f"Brake earlier at {corner}.")

        if throttle_diff < -0.1:
            advice.append(f"Apply throttle sooner at {corner}.")
        elif throttle_diff > 0.1:
            advice.append(f"Smoothen throttle at {corner}.")

        if speed_diff < -5:
            advice.append(f"You're too slow through {corner}.")
        elif speed_diff > 5:
            advice.append(f"Good speed through {corner}.")

        feedback.append({"corner": corner, "feedback": " ".join(advice)})

    feedback_df = pd.DataFrame(feedback)

    st.subheader("📊 Coaching Feedback Summary")
    st.dataframe(feedback_df)

    st.subheader("🎙️ Audio Coach Feedback")
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    voices = engine.getProperty('voices')
    british_voice = next((v for v in voices if "english" in v.name.lower()), None)
    if british_voice:
        engine.setProperty('voice', british_voice.id)

    for row in feedback:
        st.markdown(f"**{row['corner']}**: {row['feedback']}")
        if st.button(f"🔊 Play feedback for {row['corner']}"):
            engine.say(row['feedback'])
            engine.runAndWait()

    st.subheader("📈 Speed, Brake & Throttle Comparison")
    st.line_chart(merged_df[['speed_user', 'speed_ref']].rename(columns={'speed_user': 'User Speed', 'speed_ref': 'Ref Speed'}))
    st.line_chart(merged_df[['brake_user', 'brake_ref']].rename(columns={'brake_user': 'User Brake', 'brake_ref': 'Ref Brake'}))
    st.line_chart(merged_df[['throttle_user', 'throttle_ref']].rename(columns={'throttle_user': 'User Throttle', 'throttle_ref': 'Ref Throttle'}))
else:
    st.info("👈 Upload your lap files in the sidebar to begin analysis.")

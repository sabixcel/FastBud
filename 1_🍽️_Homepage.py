import streamlit as st
from styles import get_background_style
import time

st.set_page_config(
    page_title="FastBud",
    page_icon="🍽️",
)

# Load background style
img_url = "https://images.unsplash.com/photo-1552089123-2d26226fc2b7?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
# Apply sidebar background style
st.markdown(get_background_style(img_url), unsafe_allow_html=True)

st.title("FastBud😎")
st.sidebar.header("Select an option from above.")

with st.container():
    if "name_input" not in st.session_state or "age_input" not in st.session_state or "gender_input" not in st.session_state or "weight_input" not in st.session_state or "height_input" not in st.session_state or "data" not in st.session_state or "activity_level" not in st.session_state:
        st.session_state["name_input"] = ""
        st.session_state["age_input"] = ""
        st.session_state["gender_input"] = "Male"
        st.session_state["weight_input"] = 60
        st.session_state["height_input"] = 165
        st.session_state["data"] = False
        st.session_state["activity_level"] = "Sedentary"

    name_input = st.text_input("Hello. What's your name?", st.session_state["name_input"])

    age, gender, activity = st.columns(3)
    with age:
        age_input = st.text_input("What's your age?", st.session_state["age_input"])
    gender_options = ["Male", "Female", "Others"]
    with gender:
        gender_input = st.selectbox("Select your gender:", gender_options)
    activity_options = ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"]
    with activity:
        activity_level = st.selectbox("What's your daily activity level?", activity_options)
        # Put on notifications
        if st.button("ℹ️ Info"):
            if activity_level == activity_options[0]:
                st.toast('Sedentary: If you get minimal or no exercise.', icon='🐒')
                time.sleep(6)
            elif activity_level == activity_options[1]:
                st.toast('Lightly active: If you exercise lightly one to three days a week.', icon='🤸')
                time.sleep(6)
            elif activity_level == activity_options[2]:
                st.toast('Moderately active: If you exercise moderately three to five days a week.', icon='🏋️‍♂️')
                time.sleep(6)
            elif activity_level == activity_options[3]:
                st.toast('Very active: If you engage in hard exercise six to seven days a week.', icon='💪')
                time.sleep(6)
            elif activity_level == activity_options[4]:
                st.toast('Extra active: If you engage in very hard exercise six to seven days a week or have a physical job.', icon='🦸‍♂️')
                time.sleep(6)

    weight, height = st.columns(2)
    with weight:
        weight_input = st.slider("Weight (kg)", min_value=0, max_value=150, value=st.session_state.get("weight_input", 70))
    with height:
        height_input = st.slider("Height (cm)", min_value=0, max_value=210, value=st.session_state.get("height_input", 170))

    submit = st.button("Submit")
    if submit:
        error_messages = []

        try:
            # Validate name input
            if not name_input:
                error_messages.append("Please enter your name.")
                
            # Validate age input
            age_input = int(age_input)
            if not 0 <= age_input <= 100:
                error_messages.append("Please enter a valid age (between 0 and 100).")

            # Validate gender input
            if gender_input not in gender_options:
                error_messages.append("Please select a valid gender.")

            # No need for validation on weight and height sliders as they have limits set

        except ValueError: 
            error_messages.append("Please enter valid numeric values.")

        if not error_messages: 
            st.session_state["data"] = True
            st.session_state["name_input"] = name_input
            st.session_state["age_input"] = age_input
            st.session_state["gender_input"] = gender_input
            st.session_state["weight_input"] = weight_input
            st.session_state["height_input"] = height_input
            st.session_state["activity_level"] = activity_level
            st.write("Nice to meet you, ", name_input, "!😊")
        else:
            for error in error_messages:
                st.error(error)

with st.container():
    st.header("About")
    st.markdown(
        "With the help of this application, you will be able to follow your fasting program, manually adding the fasting periods or just pressing the start fasting button! More updates to come, stay close!"
    )
 
import streamlit as st
import hydralit_components as hc
from styles import get_background_style
import time
from datetime import datetime
import streamlit.components.v1 as components
from calc_calories import calculate_calories_burned_with_activity, calculate_calories_needed, calculate_bmi

theme_good = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}

st.set_page_config(
    page_title="Fast",
    page_icon="🕒",
)

# Load background style
img_url = "https://images.unsplash.com/photo-1560487765-67095b892dd1?q=80&w=1925&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
# Apply sidebar background style
st.markdown(get_background_style(img_url), unsafe_allow_html=True)

st.title("Fast")

calories_burned_resting, calories_burned_active = calculate_calories_needed(
    st.session_state["age_input"],
    st.session_state["gender_input"],
    st.session_state["weight_input"],
    st.session_state["height_input"],
    st.session_state["activity_level"]
)
status, bmi = calculate_bmi(st.session_state["weight_input"],
    st.session_state["height_input"])

cc = st.columns(3)
##### Info card #####
if st.session_state["data"]:
    with cc[2]:
        hc.info_card(title="{}, here is your profile:".format(st.session_state["name_input"]), content =
            "Age: {} years,\n"
            "Gender: {},\n"
            "Weight: {} kg,\n"
            "Height: {} cm,\n"
            "Activity_level: {}".format(
                st.session_state["age_input"],
                st.session_state["gender_input"],
                st.session_state["weight_input"],
                st.session_state["height_input"],
                st.session_state["activity_level"],
            ),
            title_text_size = "15px",
            content_text_size = "15px",
            icon_size = "30px",
        )
        # hc.info_card(title="BMR - Basal Metabolic Rate:", content =
        #     "{} kCal".format(
        #         calories_burned_resting,
        #     ),
        #     title_text_size = "15px",
        #     content_text_size = "15px",
        #     icon_size = "30px",
        # )
        # hc.info_card(title="TDEE - Total Daily Energy Expenditure:", content =
        #     "{} kCal".format(
        #         calories_burned_active,
        #     ),
        #     title_text_size = "15px",
        #     content_text_size = "15px",
        #     icon_size = "30px",
        # )
        # hc.info_card(title="BMI - Body mass index:", content =
        #     "{} - {} kg/m2".format(
        #         status,
        #         bmi,
        #     ),
        #     title_text_size = "15px",
        #     content_text_size = "15px",
        #     icon_size = "30px",
        # )
        if st.button("⚖️ BMR - Basal Metabolic Rate: {} kCal".format(calories_burned_resting)):
            st.toast('You burn calories even when resting through basic life-sustaining functions like breathing, circulation, nutrient processing, and cell production. This is known as basal metabolic rate (BMR).', icon='⚖️')
            time.sleep(10)
        if st.button("⚖️ TDEE - Total Daily Energy Expenditure: {} kCal".format(calories_burned_active)):
            st.toast('Your total daily energy expenditure (TDEE) is the number of calories you burn throughout a 24-hour period. These calories come from the work your body does to keep you alive, including your brain functions, breathing, digestion, and so on as well as all your physical activities.', icon='⚖️')
            time.sleep(10)
        if st.button("⚖️ BMI - Body mass index: {} - {} kg/m2".format(status, bmi)):
            st.toast('Body mass index (BMI) is a person’s weight in kilograms divided by the square of height in meters. BMI is an inexpensive and easy screening method for weight category—underweight, healthy weight, overweight, and obesity.', icon='⚖️')
            time.sleep(10)
else:
    with cc[2]:
        st.write("No input data for now.")

##### Start and stop fasting #####
# with cc[0]:
#     container_2 = st.empty()
#     button_A = container_2.button('Start Fasting')
#     if button_A:
#         container_2.empty()
#         button_B = container_2.button('Stop Fasting')

# Function to draw the circular border with text inside
def draw_circle_with_text(fill_percentage, time_format):
    diameter = 150
    radius = diameter / 2
    border_width = 10
    border_color = 'white'
    fill_color = 'orange'
    circumference = 2 * 3.1415 * radius
    filled_length = circumference * fill_percentage

    svg_code = (
        f'<svg width="{diameter}" height="{diameter}">'
        f'<circle cx="{radius}" cy="{radius}" r="{radius - border_width / 2}" '
        f'stroke="{border_color}" stroke-width="{border_width}" fill="{fill_color}" />'
        f'<circle cx="{radius}" cy="{radius}" r="{radius - border_width / 2}" '
        f'stroke="green" stroke-width="{border_width}" fill="transparent" '
        f'stroke-dasharray="{filled_length} {circumference}" '
        f'style="transform: rotate(-90deg); transform-origin: 50% 50%;" />'
        f'<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" '
        f'font-size="16" fill="black">⏳{time_format}</text>'
        f'</svg>'
    )

    st.write(svg_code, unsafe_allow_html=True)

# Initialize session state
if 'is_fasting' not in st.session_state:
    st.session_state.is_fasting = False
    st.session_state.start_time = 0

# Buttons for starting and stopping fasting
with cc[0]:
    button_start = st.button('Start Fasting')

    if button_start:
        st.session_state.is_fasting = True
        st.session_state.start_time = time.time()
        st.session_state.start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    button_stop = st.button('Stop Fasting')

    if button_stop:
        st.session_state.is_fasting = False
        st.session_state.start_time = 0  # Reset the start time
        st.session_state.stop_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Initialize entry list
if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = []

# Display circular border and elapsed time when fasting is ongoing
with cc[1]:
    while st.session_state.is_fasting:
        elapsed_time = int(time.time() - st.session_state.start_time)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the time string for final display
        if hours > 0:
            time_fasted = f"{hours} hours, {minutes} minutes, {seconds} seconds"
        elif minutes > 0:
            time_fasted = f"{minutes} minutes, {seconds} seconds"
        else:
            time_fasted = f"{seconds} seconds"
        st.session_state.hours = hours
        st.session_state.time_fasted = time_fasted

        time_format = f"{hours:02}:{minutes:02}:{seconds:02}"
        draw_circle_with_text(elapsed_time / (60 * 60), time_format)  # Fill percentage based on elapsed time
        time.sleep(1)  # Update every 1 second
        st.rerun()  # Rerun the script to update the UI 

    if button_stop:
        #st.write(f"Start Date and Time: {st.session_state.start_date}")
        #st.write(f"Stop Date and Time: {st.session_state.stop_date}")
        st.write(f"⏰Time fasted: {st.session_state.time_fasted}") 
        calories_burned = calculate_calories_burned_with_activity(st.session_state["age_input"], st.session_state["gender_input"], st.session_state["weight_input"], st.session_state["height_input"], st.session_state.hours, st.session_state["activity_level"])
        st.session_state.calories_burned = calories_burned
        st.write(f"🔥Calories burned: {calories_burned} kcal")

        # Save entry to the journal
        entry = {
            "start_date": st.session_state.start_date,
            "stop_date": st.session_state.stop_date,
            "time_fasted": st.session_state.time_fasted,
            "calories_burned": st.session_state.calories_burned
        }
        st.session_state.journal_entries.append(entry)
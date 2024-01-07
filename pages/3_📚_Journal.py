import streamlit as st
from styles import get_background_style
from streamlit_modal import Modal
from datetime import datetime, timedelta
import time
import hydralit_components as hc
from calc_calories import calculate_calories_burned_with_activity, calculate_calories_needed

st.set_page_config(
    page_title="Journal",
    page_icon="📚",
)

# Load background style
img_url = "https://images.unsplash.com/photo-1550534791-2677533605ab?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
# Apply sidebar background style
st.markdown(get_background_style(img_url), unsafe_allow_html=True)

st.title("Journal")

import streamlit as st
from streamlit_modal import Modal

import streamlit.components.v1 as components

delete_modal = Modal(
    "Are you sure?", 
    key="delete-modal",
    padding=20,    # default value
    max_width=300,  # default value
)

edit_modal = Modal(
    "Edit your entry", 
    key="edit-modal",
    padding=20,    # default value
    max_width=500,  # default value
)

# Insert containers separated into tabs:
tab1, tab2, tab3 = st.tabs(["Entries", "Fasts", "Stats"])

# Retrieve from st.session_state
if 'journal_entries' in st.session_state:
    journal_entries = st.session_state.journal_entries
else:
    journal_entries = []


with tab1:
    st.write("Add a new entry below 😀")
    with st.form("new_entry_form"):
        start_date_column, start_time_column = st.columns(2)
        with start_date_column:
            new_start_date = st.date_input("Start Date:")
        with start_time_column:
            new_start_time = st.time_input("Start Time:")
        stop_date_column, stop_time_column = st.columns(2)
        with stop_date_column:
            new_stop_date = st.date_input("End Date:")
        with stop_time_column:
            new_stop_time = st.time_input("End Time:")

        # Calculate the elapsed time
        elapsed_time = datetime.combine(new_stop_date, new_stop_time) - datetime.combine(new_start_date, new_start_time)
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the time string for final display
        if hours > 0:
            time_fasted = f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
        elif minutes > 0:
            time_fasted = f"{int(minutes)} minutes, {int(seconds)} seconds"
        else:
            time_fasted = f"{int(seconds)} seconds"

        # Calculate calories burned
        calories_burned = calculate_calories_burned_with_activity(
            st.session_state["age_input"], st.session_state["gender_input"],
            st.session_state["weight_input"], st.session_state["height_input"],
            elapsed_time.total_seconds() / 3600,  # Convert elapsed time to hours
            st.session_state["activity_level"]
        )

        # Create a new entry
        new_entry = {
            'start_date': datetime.combine(new_start_date, new_start_time),
            'stop_date': datetime.combine(new_stop_date, new_stop_time),
            'time_fasted': time_fasted,
            'calories_burned': calories_burned
        }

        # Add a button to confirm the edit
        submit_button = st.form_submit_button("Add Entry")

    # The logic associated with adding the entry should be outside the st.form block
    if submit_button:
        # Append the new entry to the journal_entries list
        journal_entries.append(new_entry)

        # Update the session state
        st.session_state.journal_entries = journal_entries

        # Display success message
        success_message = st.success("Entry added successfully.")
        time.sleep(3)
        # Clear the success message
        success_message.empty()


with tab2 or tab3:
    selected_period = st.sidebar.selectbox("📅Select Period", ["Current Month", "Current Year", "Last 30 Days", "Last 365 Days", "Custom Range"])

    # Filter entries based on the selected period
    filtered_entries = []
    today = datetime.now().date()

    if selected_period == "Current Month":
        current_month_start = today.replace(day=1)
        for entry in journal_entries:
            if current_month_start <= entry['start_date'].date() <= today:
                filtered_entries.append(entry)

    elif selected_period == "Current Year":
        current_year_start = today.replace(month=1, day=1)
        for entry in journal_entries:
            if current_year_start <= entry['start_date'].date() <= today:
                filtered_entries.append(entry)

    elif selected_period == "Last 30 Days":
        last_30_days_start = today - timedelta(days=30)
        for entry in journal_entries:
            if last_30_days_start <= entry['start_date'].date() <= today:
                filtered_entries.append(entry)

    elif selected_period == "Last 365 Days":
        last_365_days_start = today - timedelta(days=365)
        for entry in journal_entries:
            if last_365_days_start <= entry['start_date'].date() <= today:
                filtered_entries.append(entry)

    elif selected_period == "Custom Range":
        # Allow the user to input custom start and stop dates
        custom_start_date = st.sidebar.date_input("Custom Start Date:")
        custom_stop_date = st.sidebar.date_input("Custom Stop Date:")

        # Filter entries based on the custom range
        for entry in journal_entries:
            if custom_start_date <= entry['start_date'].date() <= custom_stop_date:
                filtered_entries.append(entry)

    journal_entries = filtered_entries


with tab2:
    for idx, entry in enumerate(journal_entries):
        # Check if current_start_date is already a datetime object
        if not isinstance(entry['start_date'], datetime):
            # Convert the start_date string to a datetime object
            entry['start_date'] = datetime.strptime(entry['start_date'], "%Y-%m-%d %H:%M:%S")

        # Similarly, check for current_stop_date
        if not isinstance(entry['stop_date'], datetime):
            entry['stop_date'] = datetime.strptime(entry['stop_date'], "%Y-%m-%d %H:%M:%S")

        # Rest of the code remains the same
        start_day_month = entry['start_date'].strftime("%d %B")
        start_hour_min = entry['start_date'].strftime("%H:%M")
        stop_day_month = entry['stop_date'].strftime("%d %B")
        stop_hour_min = entry['stop_date'].strftime("%H:%M")

        st.write(f"📅 {start_day_month}, {start_hour_min} → {stop_day_month}, {stop_hour_min}")
        st.write(f"⏰ Time fasted: {entry['time_fasted']}")
        st.write(f"🔥 Calories burned: {entry['calories_burned']} kcal")

        # Use columns to organize buttons on the same row
        edit_column, delete_column = st.columns([.1,1])

        # Add an "Edit" button to edit the entry
        with edit_column:
            edit_button = st.button('✏️', key=f"edit_button_{idx}")
        with delete_column:
            delete_button = st.button('🗑️', key=f"delete_button_{idx}")

        if edit_button:
            edit_modal.open()
        if edit_modal.is_open():
            with edit_modal.container():
                if not isinstance(entry['start_date'], datetime):
                    # Convert the start_date string to a datetime object
                    current_start_date = datetime.strptime(entry['start_date'], "%Y-%m-%d %H:%M:%S")
                else:
                    current_start_date = entry['start_date']
                #current_start_date = datetime.strptime(entry['start_date'], "%Y-%m-%d %H:%M:%S")
                start_date_column, start_time_column = st.columns(2)
                with start_date_column:
                    new_start_date = st.date_input("Edit Start Date:", value=current_start_date.date(), key=f"edit_start_date_{idx}")
                with start_time_column:
                    new_start_time = st.time_input("Edit Start Time:", value=current_start_date.time(), key=f"edit_start_time_{idx}")

                #current_stop_date = datetime.strptime(entry['stop_date'], "%Y-%m-%d %H:%M:%S")
                if not isinstance(entry['stop_date'], datetime):
                    # Convert the start_date string to a datetime object
                    current_stop_date = datetime.strptime(entry['stop_date'], "%Y-%m-%d %H:%M:%S")
                else:
                    current_stop_date = entry['stop_date']
                stop_date_column, stop_time_column = st.columns(2)
                with stop_date_column:
                    new_stop_date = st.date_input("Edit Stop Date:", value=current_stop_date.date(), key=f"edit_stop_date_{idx}")
                with stop_time_column:
                    new_stop_time = st.time_input("Edit Stop Time:", value=current_stop_date.time(), key=f"edit_stop_time_{idx}")

                # Add a button to confirm the edit
                confirm_edit = st.button("Confirm Edit", key=f"confirm_edit_button_{idx}")
                
                if confirm_edit:
                    # Update the entry only when the "Confirm Edit" button is pressed
                    new_start_datetime = datetime.combine(new_start_date, new_start_time)
                    new_stop_datetime = datetime.combine(new_stop_date, new_stop_time)
                    
                    # Calculate the elapsed time
                    elapsed_time = new_stop_datetime - new_start_datetime
                    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
                    minutes, seconds = divmod(remainder, 60)

                    # Format the time string for final display
                    if hours > 0:
                        time_fasted = f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
                    elif minutes > 0:
                        time_fasted = f"{int(minutes)} minutes, {int(seconds)} seconds"
                    else:
                        time_fasted = f"{int(seconds)} seconds"
                    
                    # Calculate calories burned
                    calories_burned = calculate_calories_burned_with_activity(
                        st.session_state["age_input"], st.session_state["gender_input"],
                        st.session_state["weight_input"], st.session_state["height_input"],
                        elapsed_time.total_seconds() / 3600,  # Convert elapsed time to hours
                        st.session_state["activity_level"]
                    )
                    
                    # Update entry with new values
                    entry['start_date'] = new_start_datetime
                    entry['stop_date'] = new_stop_datetime
                    entry['time_fasted'] = time_fasted
                    entry['calories_burned'] = calories_burned
                    
                    # Update UI
                    st.write("Entry edited successfully.")
                    edit_modal.close()

        if delete_button:
                delete_modal.open()

        if delete_modal.is_open():  
            with delete_modal.container():
                # Add buttons for confirmation and cancel
                confirm_delete = st.button("✓", key=f"confirm_delete_button_{idx}")

                if confirm_delete:
                    # Handle deletion
                    journal_entries.pop(idx)
                    st.session_state.journal_entries = journal_entries
                    # Update UI
                    st.write("Entry deleted successfully.")
                    delete_modal.close()
        
        st.write("---")  # Add a separator between entries


total_time_fasted_seconds = 0
total_calories_burned = 0
longest_fasting_duration = timedelta(0)
with tab3:
    for entry in journal_entries:
        elapsed_time = entry['stop_date'] - entry['start_date']
        total_time_fasted_seconds += elapsed_time.total_seconds()

        # Calculate total calories burned
        if entry['calories_burned'] == '0.00':
            entry['calories_burned'] = 0
        try:
            calories_burned = float(entry['calories_burned'])
            total_calories_burned += int(calories_burned)
        except ValueError:
            print(f"Skipping entry with invalid 'calories_burned' value: {entry['calories_burned']}")

        # Find the longest fasting duration
        if elapsed_time > longest_fasting_duration:
            longest_fasting_duration = elapsed_time
    
    longest_fasting_duration = longest_fasting_duration.total_seconds()
    longest_fasting_hours = int(longest_fasting_duration // 3600)
    longest_fasting_minutes = int((longest_fasting_duration % 3600) // 60)
    longest_fasting_seconds = int(longest_fasting_duration % 60)
    
    # Convert total_time_fasted_seconds to hours, minutes, and seconds
    total_hours, remainder = divmod(total_time_fasted_seconds, 3600)
    total_minutes, total_seconds = divmod(remainder, 60)

    cc = st.columns(3)
    with cc[0]:
        hc.info_card(title="⏳Total time fasted", content =
            "{} hours, {} minutes, {} seconds".format(
                int(total_hours),
                int(total_minutes),
                int(total_seconds)
            ),
            title_text_size = "15px",
            content_text_size = "15px",
            icon_size = "30px",
        )
        hc.info_card(title="🔥Total calories burned", content =
            "{} kCal".format(
                total_calories_burned
            ),
            title_text_size = "15px",
            content_text_size = "15px",
            icon_size = "30px",
        )
        hc.info_card(title="🚀Longest fasting duration", content =
            "{} hours, {} minutes, {} seconds".format(
                longest_fasting_hours,
                longest_fasting_minutes,
                longest_fasting_seconds
            ),
            title_text_size = "15px",
            content_text_size = "15px",
            icon_size = "30px",
        )
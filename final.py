import csv
import gradio as gr
import re
from datetime import datetime

event_file = "events.csv"
pending_event_file = "pending_events.csv"
user_file = "registrations.csv"

ADMIN_ID = "admin"
ADMIN_PASSWORD = "123"

def submit_event(event_name, date, time, venue, organizer_name, organizer_phone, organizer_email):
    if not event_name:
        return "Enter the event name!"
    if not date:
        return "Enter the date!"
    if not time:
        return "Enter the time!"
    if not venue:
        return "Enter venue!"
    if not organizer_name:
        return "Enter organizer name!"
    if not organizer_phone:
        return "Enter organizer phone number!"
    if not organizer_email:
        return "Enter organizer email!"
    
    date_pattern = r"^\d{2}-\d{2}-\d{4}$"
    if not re.match(date_pattern, date):
        return "Invalid date format! Use DD-MM-YYYY."
    
    try:
        event_date = datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        return "Invalid date! Ensure it is a real date."

    today = datetime.today()
    if event_date < today:
        return "Event date must be today or in the future!"
    
    time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    if not re.match(time_pattern, time):
        return "Invalid time format! Use HH:MM (24-hour format)."
    
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, organizer_email):
        return "Invalid email format! Please enter a valid email (e.g., example@mail.com)."
    
    if not organizer_phone.isdigit() or not (10 <= len(organizer_phone) <= 15):
        return "Invalid phone number! Enter only digits (10-15 digits allowed)."
    
    with open(pending_event_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([event_name, date, time, venue, organizer_name, organizer_phone, organizer_email])
    return "Event submitted for approval!"

def view_events():
    try:
        with open(event_file, 'r') as file:
            reader = csv.reader(file)
            events = list(reader)
        return events if events else [["No events available."]]
    except FileNotFoundError:
        return [["No events available."]]
    
def approve_selected_events(selected_indices):
    try:
        with open(pending_event_file, 'r') as file:
            reader = list(csv.reader(file))
        
        approved_events = [reader[i] for i in selected_indices if 0 <= i < len(reader)]
        remaining_events = [row for i, row in enumerate(reader) if i not in selected_indices]
        
        with open(event_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(approved_events)
        
        with open(pending_event_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(remaining_events)
        
        return "Selected events approved and added successfully!"
    except FileNotFoundError:
        return "No pending events."

def view_pending_events():
    try:
        with open(pending_event_file, 'r') as file:
            reader = csv.reader(file)
            events = [[i] + row for i, row in enumerate(reader)]  
        return events if events else [["No pending events."]]
    except FileNotFoundError:
        return [["No pending events."]]

def register_user(name, email, phone, event_name):
    if not name:
        return "Enter your name!"
    if not email:
        return "Enter your email!"
    if not phone:
        return "Enter your phone number!"
    if not event_name:
        return "Enter the event name!"
    
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        return "Invalid email format! Please enter a valid email (e.g., example@mail.com)."
    
    if not phone.isdigit() or not (10 <= len(phone) <= 15):
        return "Invalid phone number! Enter only digits (10-15 digits allowed)."
    
    try:
        with open(event_file, 'r') as file:
            reader = csv.reader(file)
            events = [row[0] for row in reader] 
        
        if event_name not in events:
            return "Event does not exist! Please enter a valid event."
    except FileNotFoundError:
        return "No events available for registration."

    # Proceed with registration if event exists
    with open(user_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, phone, event_name])
    
    return "Registered successfully!"


def view_registrations():
    try:
        with open(user_file, 'r') as file:
            reader = csv.reader(file)
            registrations = [row for row in reader]  
        return registrations if registrations else [["No registrations found."]]
    except FileNotFoundError:
        return [["No registrations found."]]

def main():
    with gr.Blocks() as demo:
        gr.Markdown("# Event Management System")

        # role selection and admin credentials
        with gr.Row():
            role = gr.Radio(["User", "Admin"], label="Select Role", value="User" )

        # admin login section
        admin_id = gr.Textbox( label="Admin ID", visible=False)
        admin_password = gr.Textbox(label="Admin Password", type="password", visible=False)
        login_button = gr.Button("Login")
        login_status = gr.Textbox(label="Login Status", interactive=False)

        user_dashboard = gr.Column(visible=False)
        admin_dashboard = gr.Column(visible=False)

        role.change(
            lambda role: (gr.update(visible=role == "Admin"), gr.update(visible=role == "Admin")),
            inputs=role,
            outputs=[admin_id, admin_password]
        )

        # Admin dashboard
        with admin_dashboard:
            gr.Markdown("## Admin Dashboard")

            with gr.Tab("Submit Event"):
                event_name = gr.Textbox(label="Event Name")
                event_date = gr.Textbox(label="Event Date (DD-MM-YYYY)")
                event_time = gr.Textbox(label="Event Time (HH:MM)")
                event_venue = gr.Textbox(label="Event Venue")
                organizer_name = gr.Textbox(label="Organizer Name")
                organizer_phone = gr.Textbox(label="Organizer Phone Number")
                organizer_email = gr.Textbox(label="Organizer Email")
                submit_output = gr.Textbox(label="Submission Status")
                submit_button = gr.Button("Submit")
        
                submit_button.click(submit_event, inputs=[event_name, event_date, event_time, event_venue, organizer_name, organizer_phone, organizer_email], outputs=submit_output)

            with gr.Tab("View Events"):
                events_output = gr.Dataframe(headers=["Event Name", "Date" , "Time", "Venue", "Organizer Name", "Organizer Phone", "Organizer Email"], label="Events")
                events_refresh_button = gr.Button("Refresh")
                events_refresh_button.click(view_events, inputs=None, outputs=events_output)

            with gr.Tab("Pending Events"):
                gr.Markdown("### Pending Events List")
                pending_events = gr.Dataframe(headers=["Event No.", "Event Name", "Date" , "Time", "Venue", "Organizer Name", "Organizer Phone", "Organizer Email"], label="Pending Events")
                
                gr.Markdown("### Select Events to Approve")
                selected_events = gr.CheckboxGroup(choices=[], label="Select events to approve")
                approve_button = gr.Button("Approve Selected Events")
                
                def update_pending_events():
                    events = view_pending_events()
                    choices = [str(i) for i in range(len(events))] if events and events[0][0] != "No pending events." else []
                    return events, gr.update(choices=choices)
                
                pending_refresh_button = gr.Button("Refresh Pending Events")
                pending_refresh_button.click(update_pending_events, inputs=None, outputs=[pending_events, selected_events])
                
                def approve_and_refresh(selected):
                    result = approve_selected_events([int(i) for i in selected])
                    updated_events, updated_choices = update_pending_events()
                    return result, updated_events, updated_choices, gr.update(value=[])
                
                approve_button.click(approve_and_refresh, inputs=selected_events, outputs=[submit_output, pending_events, selected_events, selected_events])

            with gr.Tab("View Registrations"):
                registrations_output = gr.Dataframe(headers=["Name", "Email", "Phone", "Event Name"], label="Registrations")
                registrations_refresh_button = gr.Button("Refresh")
                registrations_refresh_button.click(view_registrations, inputs=None, outputs=registrations_output)


        # User dashboard
        with user_dashboard:
            gr.Markdown("## User Dashboard")
            with gr.Tab("Submit Event"):
                event_name = gr.Textbox(label="Event Name")
                event_date = gr.Textbox(label="Event Date (DD-MM-YYYY)")
                event_time = gr.Textbox(label="Event Time (HH:MM)")
                event_venue = gr.Textbox(label="Event Venue")
                organizer_name = gr.Textbox(label="Organizer Name")
                organizer_phone = gr.Textbox(label="Organizer Phone Number")
                organizer_email = gr.Textbox(label="Organizer Email")
                submit_output = gr.Textbox(label="Submission Status")
                submit_button = gr.Button("Submit")
        
                submit_button.click(submit_event, inputs=[event_name, event_date, event_time, event_venue, organizer_name, organizer_phone, organizer_email], outputs=submit_output)

            with gr.Tab("View Events"):
                events_output = gr.Dataframe(headers=["Event Name", "Date","Time", "Venue", "Organizer Name", "Organizer Phone", "Organizer Email"], label="Events")
                events_refresh_button = gr.Button("Refresh")
                events_refresh_button.click(view_events, inputs=None, outputs=events_output)

            with gr.Tab("Register for Event"):
                user_name = gr.Textbox(label="Your Name")
                user_email = gr.Textbox(label="Your Email")
                user_phone = gr.Textbox(label="Your Phone Number")
                register_event_name = gr.Textbox(label="Event Name")
                register_output = gr.Textbox(label="Registration Status")
                register_button = gr.Button("Register")

                # Bind Enter key to the register button
                user_name.submit(register_user, inputs=[user_name, user_email, user_phone, register_event_name], outputs=register_output)
                user_email.submit(register_user, inputs=[user_name, user_email, user_phone, register_event_name], outputs=register_output)
                user_phone.submit(register_user, inputs=[user_name, user_email, user_phone, register_event_name], outputs=register_output)
                register_event_name.submit(register_user, inputs=[user_name, user_email, user_phone, register_event_name], outputs=register_output)
                register_button.click(register_user, inputs=[user_name, user_email, user_phone, register_event_name], outputs=register_output)


        # Login function
        def login(role, admin_id, admin_password):
            if role == "Admin":
                if admin_id == ADMIN_ID and admin_password == ADMIN_PASSWORD:
                    return "Admin Login Successful!", gr.update(visible=False), gr.update(visible=True)
                return "Invalid Admin Credentials!", gr.update(visible=False), gr.update(visible=False)
            else:
                return "User Panel", gr.update(visible=True), gr.update(visible=False)

        # Bind Enter key to the login button
        admin_password.submit(login, inputs=[role, admin_id, admin_password], outputs=[login_status, user_dashboard, admin_dashboard])
        login_button.click(login, inputs=[role, admin_id, admin_password], outputs=[login_status, user_dashboard, admin_dashboard])

    demo.launch()

if __name__ == "__main__":
    main()
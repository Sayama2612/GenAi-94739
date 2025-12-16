import streamlit as st

with st.form("reg_form"):
    st.header("Registration Form")
    first_name = st.text_input(key="fname", label="First Name")
    last_name = st.text_input(key="lname",label="Last Name")
    age = st.slider("Age", 10, 100, 25, 1)
    addr = st.text_area("Address")
    submit_btn = st.form_submit_button("Submit")
    
    if submit_btn:
        
        error_msg = ""
        is_error = False
        if not first_name:
            is_error = True
            error_msg += "First Name is required. "
            
        if not last_name:
            is_error = True
            error_msg += "Last Name is required. "
            
        if not addr:
            is_error = True
            error_msg += "Address is required. "   
            
        if is_error:
            st.error(error_msg)
            
        else:
            message = f"Successfully Registered: {st.session_state['fname']} {st.session_state['lname']} . Age is: {age}. Living at: {addr}"
            st.success(message)             
    
    
    
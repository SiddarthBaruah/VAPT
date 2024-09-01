import streamlit as st
import requests
import json

st.title('Network Scan App')

# Input fields
ip_address = st.text_input('IP Address', '10.24.9.31')
scan_type = st.selectbox('Scan Type', ['nmap', 'nikto'])
command_options = st.text_input('Command Options', '-sV')


def format_nmap_output(output_raw):
    '''
    This funciton would format the output nicely
    ars:
        output_raw
    '''
    lines = output_raw.split('\n')
    formatted_lines = []
    for line in lines:
        if line.startswith('PORT'):
            formatted_lines.append(f'**{line}**')
        elif line.startswith('Service Info'):
            formatted_lines.append(f'**{line}**')
        else:
            formatted_lines.append(line)
    return '\n'.join(formatted_lines)


# Button to trigger the scan
if st.button('Run Scan'):
    # Prepare the payload
    payload = {
        'ip_address': ip_address,
        'scan_type': scan_type,
        'command_options': command_options
    }

    # Send the request to the API
    response = requests.post('http://127.0.0.1:3000/scan', headers={
                             'Content-Type': 'application/json'}, data=json.dumps(payload))

    # Display the output
    if response.status_code == 200:
        st.subheader('Scan Output')
        output = response.json().get('output')
        if scan_type == 'nmap':
            formatted_output = format_nmap_output(output)
            st.text(formatted_output)
        else:
            st.text(output)
    else:
        st.error('Error: ' + response.json().get('error'))

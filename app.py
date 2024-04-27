import streamlit as st
from scripts import *

# Set the configuration of the Streamlit page with a title and an icon
st.set_page_config(
    page_title='Summarizer App',
    page_icon='🤖'
)

# Display a subheader on the page
st.subheader('🤖 Summarizer App 🤖')

# Initialize a list to hold chunks of text from the uploaded file
chunks = []

# Main entry point of the script
if __name__ == "__main__":
    import os
    with st.sidebar: # Create a sidebar for the Streamlit app
        # Create a file uploader widget allowing txt files
        uploaded_file = st. file_uploader('Upload a file:', type= ['txt'])
        # Create a button for the user to add data after selecting a file
        add_data = st.button('Add Data')

        # Check if a file is uploaded and the 'Add Data' button is clicked
        if uploaded_file and add_data: # if the user browsed a file
            with st.spinner('Reading and chunking file ...'):  # Show a loading spinner
                
                # Writing the file from RAM to the current directory on disk
                bytes_data = uploaded_file.read()
                file_name = os.path.join('./', uploaded_file.name) # Determine the file path where the file will be saved

                # Write the file's bytes data to a new file on disk
                with open(file_name, 'wb') as f:
                    f.write(bytes_data)

                data = extract_text(file_name) # Extract text from the file using a extract_text function from scripts
                chunks = chunk_text(data) # Divide the text into chunks using chunk_text function from scripts

                # Show a success message once the file is uploaded and processed
                st.success('File uploaded, well chunked!')
    
    # Check if there are any chunks of text to process
    if len(chunks) > 0:

        with st.spinner('Generating summary, please wait...'): # Show a loading spinner
            answer = asyncio.run(main(chunks)) # Generate a summary with the main function

        # Display the generated summary and key points to the user
        st.markdown("**The summary and key points of the provided text is:**\n")
        st.write(str(answer))

         # Customize the style of the download button using HTML and CSS
        st.markdown("""
    <style>
    div.stDownloadButton > button {
        background-color: #fffdd0; 
        color: black;
        padding: 10px 24px;
        border-radius: 8px;
        border: 2px solid #e7e7e7;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
        
        # Download button allowing the user to download the generated summary
        st.download_button('📥  Download the summary', str(answer), file_name='summary.txt')


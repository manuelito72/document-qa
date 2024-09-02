import streamlit as st
from anthropic import Anthropic

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – Claude will answer! "
    "To use this app, you need to provide an Anthropic API key, which you can get from the Anthropic website. "
)

# Ask user for their Anthropic API key via `st.text_input`.
anthropic_api_key = st.text_input("Anthropic API Key", type="password")

if not anthropic_api_key:
    st.info("Please add your Anthropic API key to continue.", icon="🗝️")
else:
    # Create an Anthropic client.
    client = Anthropic(api_key=anthropic_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        
        # Use the Messages API to interact with Claude
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": f"Here's a document: {document}\n\n---\n\n{question}"}
            ]
        )

        # Display the response
        st.write(message.content[0].text)

import streamlit as st
import os
from router_selection import Router
import pandas as pd

from dotenv import load_dotenv
##to load credentials
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

st.title("🔀 LLM Model Router 🧠")
st.markdown("#### Your AI-Powered Model Gateway. Choses between Llama3 70B, Gemini Flash, GPT-3.5-Turbo, GPT-4o")

## Add a markdown table of model costs
# Sample data (replace with your DataFrame)
df = pd.DataFrame({
    "Model-Name": ["Groq - LLama3 70B", "Gemini Flash", "GPT-3.5-turbo", "GPT-4o"],
    "Input-Cost per MM tokens": ['Free', '$0.35', '$0.50', '$5'],
    "Output-Cost per MM tokens": ['Free', '$0.70', '$1.50', '$15']
})

# Convert DataFrame to markdown table
markdown_table = df.to_markdown(index=False, numalign="left", stralign="left")

# Display table
st.markdown(markdown_table)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

##Initialize the Agents:
router_agent = Router(cost_threshold=0.11593)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your question here."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    ## Get response
    model_response, model_type = router_agent.generate(st.session_state.messages)
    st.markdown(f"**:green[{model_type}]** is responding...")
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(model_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": model_response})

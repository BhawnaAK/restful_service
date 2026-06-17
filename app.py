import streamlit as st
from langgraph_workflow import graph

st.set_page_config(
    page_title="HR Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("HR Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectordb" not in st.session_state:
    st.session_state.vectordb = True


if st.session_state.vectordb:
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input(
        "Ask a question about the PDF..."
    )

    if user_query:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_query
            }
        )

        with st.chat_message("user"):
            st.markdown(user_query)


        with st.spinner("Generating response..."):
            state = graph.invoke({
                "user_input": user_query
            })
            answer = state.get("final_output", "")
            docs = state.get("rag_docs", [])

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

else:
    st.info("Upload a PDF to start chatting.")
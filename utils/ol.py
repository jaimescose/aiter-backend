from typing import List

from phi.assistant import Assistant
from phi.document import Document
from phi.document.reader.pdf import PDFReader
from phi.document.reader.website import WebsiteReader
from phi.utils.log import logger

from assistant import get_groq_assistant  # type: ignore

def query_llm(query):
    # Get LLM model
    llm_model = "llama3-70b-8192"
    # Get Embeddings model
    embeddings_model = "nomic-embed-text"

    # Get the assistant
    rag_assistant: Assistant
    rag_assistant = get_groq_assistant(llm_model=llm_model, embeddings_model=embeddings_model)

    # Create assistant run (i.e. log to database)
    try:
        new_run = rag_assistant.create_run()
    except Exception:
        print("Could not create assistant, is the database running?")
        return

    # Load existing messages
    assistant_chat_history = rag_assistant.memory.get_chat_history()
    if len(assistant_chat_history) > 0:
        logger.debug("Loading chat history")
        messages = assistant_chat_history
    else:
        logger.debug("No chat history found")
        messages = []

    # Prompt for user input
    messages.append({"role": "user", "content": query})

    # If last message is from a user, generate a new response
    last_message = messages[-1]
    if last_message.get("role") == "user":
        question = last_message["content"]
        response = ""
        for delta in rag_assistant.run(question):
            response += delta  # type: ignore
        messages.append({"role": "assistant", "content": response})
    
    return response


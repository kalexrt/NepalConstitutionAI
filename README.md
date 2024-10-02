# Nepal Constitution AI 

**Nepal Constitution AI** is a Retrieval-Augmented Generation (RAG) chatbot built using the Langchain framework. The bot is designed to assist users in querying and understanding the Constitution of Nepal by leveraging a powerful combination of retrieval-based search and generative AI.

## Features

- **Constitution Querying**: Users can ask specific questions about the Constitution of Nepal, and the bot retrieves relevant sections to provide accurate responses.
- **Contextual Understanding**: The bot uses retrieval-augmented generation to fetch relevant constitutional articles and generate responses in a clear, understandable manner.

## Technology Stack

- **Langchain**: Core framework to manage the retrieval and generation processes.
- **Pinecone/FAISS**: Used as a vector database for efficient document retrieval.
- **OpenAI/LLMs**: For generating coherent and context-aware responses.
- **Custom Dataset**: Includes all articles of the Constitution of Nepal for comprehensive query results.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-link>
   cd nepal-constitution-ai
   ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables:

    - Add your API keys to a .env file.

## Methods to Run the Application
### 1. Running the API only
```bash
fastapi run app.py
```
### 2. Running the Application
```bash
streamlit run streamlit_app.py
```
## Evaluate
The Chatbot is evaluated based on three primary criteria:
1. **Context Precision**: Measures how accurately the chatbot understands and  maintains the context of the conversation.
2. **Faithfulness**: Evaluates whether the chatbot's responses are truthful and consistent with the source information or data.
3. **Answer Relevancy**: Determines the degree to which the responses are relevant and meaningful to the user's queries.

To initiate the evaluation, run the following command:
```bash
python eval.py
```
## Usage

Once the application is running, users can interact with Nepal Constitution AI through a chat interface. Simply type in your questions about the constitution, and the bot will provide relevant articles along with explanations.

## Example Queries
    "What are the fundamental rights mentioned in the Constitution of Nepal?"
    "How is the president of Nepal elected?"
    "What does the Constitution say about federalism?"
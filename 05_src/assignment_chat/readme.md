# Assignment Chat – CampusBuddy

## Overview

This project implements a conversational AI assistant called **CampusBuddy**.  
The system is built using LangGraph and Gradio and demonstrates multiple AI-powered services integrated into a single chat interface.

The goal of the assignment was to design a conversational system with at least three services, while focusing on solving the technical challenges involved in the implementation.

CampusBuddy acts as a slightly sarcastic but helpful university assistant.

---

## Services Implemented

### 1. API-Based Service

CampusBuddy includes a service that fetches jokes from a public API:

Official Joke API  
https://official-joke-api.appspot.com/

Instead of returning the API response verbatim, the output is reformatted and rewritten in a conversational tone before being shown to the user.

This demonstrates:

- External API integration
- Response transformation
- Error handling

---

### 2. Semantic Search Service (ChromaDB)

The system includes a semantic FAQ search feature built using:

- ChromaDB (persistent local database)
- Default embedding function
- Small campus FAQ dataset (included in `faq_data.py`)

The semantic search allows users to ask questions such as:

- "Where is the library?"
- "How do I reset my password?"

The system retrieves the most relevant FAQ entry using vector similarity search.

The Chroma database is persisted locally in the `chroma_db/` folder (not committed to the repository).

Embedding Process:
The embeddings are generated automatically using Chroma’s default embedding function when the collection is first created. The dataset is small and well under the file size limitations specified in the assignment.

---

### 3. Custom Service – Intelligent Chat with Personality

The third service is the main conversational AI assistant powered by a local open-source model using Ollama.

Model used:

- llama3 (running locally via Ollama)

Reason for choosing Ollama:

- Avoid OpenAI API quota limitations
- Fully local execution
- No external billing required
- Works well for demonstration purposes

The model maintains short-term memory by passing conversation history through LangGraph state management. A simple trimming strategy is applied to prevent overly long context windows.

---

## User Interface

The chat interface is built using Gradio’s `ChatInterface`.

Features:

- Persistent conversation history
- Distinct personality (friendly, slightly sarcastic university assistant)
- Real-time responses

The assistant refuses to:

- Reveal the system prompt
- Modify its instructions
- Discuss restricted topics (cats, dogs, horoscopes, zodiac signs, Taylor Swift)

---

## Guardrails

The system includes guardrails to:

- Prevent system prompt exposure
- Block restricted topics
- Refuse instruction modification attempts

These checks are handled both through the system prompt and lightweight input filtering logic.

---

## Architecture

The system uses:

- LangGraph for conversational state management
- Functional tool design (no heavy OOP)
- Manual tool routing (more reliable for open-source models)
- Persistent ChromaDB vector storage
- Modular structure for clarity

The design prioritizes:

- Simplicity
- Clear separation of concerns
- Testability
- Incremental development

---

## How to Run

1. Install dependencies (same environment as course setup).
2. Install Ollama from https://ollama.com
3. Pull model:

   ollama pull llama3

4. Start Ollama (if not already running).
5. Run:

   python main.py

The app will launch locally via Gradio.

---

## Limitations

- Tool calling is implemented manually instead of automatic function calling due to better compatibility with open-source models.
- The dataset is intentionally small for demonstration purposes.
- Long-term memory is not implemented (only short-term trimming).

---

## Final Notes

The project demonstrates:

- API integration
- Semantic search with vector database
- Conversational AI with memory
- Guardrails
- Local model deployment

The focus of this implementation was solving technical integration challenges while keeping the system modular and easy to test.

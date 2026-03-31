# Architecture

The system is a two-tier application with a Django REST backend and a React frontend. Documents are ingested and embedded into a local Chroma vector store. Chat requests are processed via a RAG pipeline that retrieves relevant chunks and generates answers.

## Backend
- Django apps: authentication, chatbot (RAG), documents (ingestion), admin_dashboard, users
- REST API endpoints for auth, chat, and document management
- Vector store path configurable via environment variables

## Frontend
- React (Vite) app with chat components and admin pages
- Uses a simple API client for requests

## Data Flow
1. Documents uploaded in the Documents module
2. Text split and embedded
3. Stored in Chroma
4. Chat requests use retriever and response generator

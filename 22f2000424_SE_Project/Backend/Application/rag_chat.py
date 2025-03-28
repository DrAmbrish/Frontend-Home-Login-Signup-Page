from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from .model import db, User, IssueQuery, ChatbotHistory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db")

# Load embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Load vector store
doc_db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embeddings
)

# Initialize chat model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.2,
    max_tokens=150,
    top_p=0.9
)

# System Prompt
SYSTEM_PROMPT = """You are a helpful educational guide. Your role is to:
1. Provide a brief, thoughtful hint based on the context (1 sentence only).
2. Direct students to relevant course materials from provided references.
3. Never give complete answers but encourage self-learning.
4. Be warm and supportive while maintaining academic rigor.
5. If it's a programming-related query, try fetching documentation or relevant examples.

Format response like:
Hint: [One sentence hint relevant to the question]
Example Code: [Python code snippet if applicable]
Resource Guide: Check [Subject] Week [Number] for more details.
"""

class ChatbotAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            jwt_claims = get_jwt()
            user_id = jwt_claims.get("id")
            user = User.query.get(user_id)
            data = request.get_json()
            query = data.get("query", "").strip()

            if not query:
                return jsonify({"error": "Query cannot be empty"}), 400
            
            # Save query in database
            new_query = IssueQuery(details=query, user_id=user_id)
            db.session.add(new_query)
            db.session.commit()

            # Retrieve relevant documents
            relevant_docs = doc_db.similarity_search(query, k=3)

            # Create context from retrieved documents
            context = "Retrieved Resources:\n"
            doc_references = []  # Store document references

            for i, doc in enumerate(relevant_docs, 1):
                metadata = doc.metadata
                doc_references.append({
                    'subject': metadata.get('subject', 'N/A'),
                    'week': metadata.get('week', 'N/A'),
                    'doc_type': metadata.get('doc_type', 'N/A')
                })
                context += f"\nReference {i}:\n"
                context += f"Subject: {metadata.get('subject', 'N/A')}\n"
                context += f"Week: {metadata.get('week', 'N/A')}\n"
                context += f"Document Type: {metadata.get('doc_type', 'N/A')}\n"
                context += f"Content: {doc.page_content.strip()}\n"

            # Prepare messages for the chatbot
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=f"""Context: {context}
                \nStudent Question: {query}
                Provide the answer only if there is enough information provided in the context, otherwise provide the message that the user's input is not answerable.
                Remember: Provide only a hint and resource guidance based on the provided context.""")
            ]

            # Generate response
            response = llm.invoke(messages)

            # Store chat history in the database
            chat_entry = ChatbotHistory(user_id=user_id, query=query, response=response.content)
            db.session.add(chat_entry)
            db.session.commit()

            return jsonify({
                "query": query,
                "response": response.content,
                "references": doc_references
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500
## Tovo – One Agent, All Conversations: A multimodal WhatsApp AI agent that processes text, speech, and images.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) 
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green) 
![LangGraph](https://img.shields.io/badge/LangGraph-Powered-orange)  ![LangChain](https://img.shields.io/badge/LangChain-Integrated-green)  ![WhatsApp](https://img.shields.io/badge/Platform-WhatsApp-lightgrey)
![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue)


Tovo is a **multimodal WhatsApp AI Agent** that processes **text, speech, and images** in one unified experience.  
It is designed to be **context-aware, memory-driven, and adaptive**, handling conversations just like a human would.  

---

## 🌟 Features  

- 💬 **Text Conversations** – Engage in natural, human-like dialogue.  
- 🎙 **Speech-to-Text (STT)** – Understands voice messages.  
- 🔊 **Text-to-Speech (TTS)** – Responds with lifelike audio.  
- 🖼️ **Image-to-Text (ITT)** – Interprets and explains images.  
- 🖌️ **Text-to-Image (TTI)** – Generates creative images from text prompts. 
- 🖼 **Image Understanding** – Analyzes and describes images with contextual meaning.  
- 🧠 **Memory-Aware Agent**  
  - **Qdrant Vector Store** → Long-term semantic recall.  
  - **SQLite Short-Term Memory** → Recent conversational context.  
  - **Conversation Summary** → Keeps a compact summary so full message history does not need to be loaded.
- 🔄 **Adaptive Workflow** – Automatically routes input to text, audio, or image workflows.  

---

## 🛠️ Tech Stack
- **Backend**: FastAPI  
- **LLM Orchestration**: LangChain , LangGraph  
- **Memory**: Qdrant (long-term), SQLite (short-term)  
- **Models**: LLM, TTS, ITT ( Groq ) , ElevenLabs TTS, Together Ai TTI

---

## 🏗️ Architecture  

Tovo is built with a modular, graph-based workflow:  

- **LangGraph** → State management, branching, and workflow orchestration.  
- **LangChain** → LLM reasoning, context injection, and memory management.  
- **Qdrant Vector Store** → Stores embeddings for semantic memory.  
- **SQLite (AsyncSqliteSaver)** → Tracks session-specific short-term memory.  
- **WhatsApp Cloud API** → Interface for receiving and sending multimodal messages.  
- **STT/TTS Models** → Converts between speech and text.  
- **ITT/TTI Models** → Converts between Image and text. 

---

## 📊 Workflow Diagram  

Here’s the workflow representation of **Tovo Agent**:  

![Workflow](test/output.png)   

---

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/bisVo159/Tovo.git
cd Tovo
```

### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 3️⃣ Setup Environment Variables
```
Create a .env file and configure:

WHATSAPP_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token

ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_voice_id
TOGETHER_API_KEY=your_together_api_key

GROQ_API_KEY=your_groq_api_key
QDRANT_API_KEY=your_qdrant_api_key
```

### 4️⃣ Run the Agent
```
uvicorn src\interfaces\whatsapp\webhook_endpoint:app --reload
```

---

## 👨‍💻 Author

**Anik Biswas**  
📍 Kolkata, India  
🚀 Building backend, generative AI, and AIML applications.


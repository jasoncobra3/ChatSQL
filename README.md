# 🦜 ChatSQL – Talk to Your Databases with AI

An AI-powered SQL chatbot built with **LangChain**, **GROQ LLMs**, and **Streamlit**.  
ChatSQL lets you **query relational databases in plain English** and get intelligent, conversational responses.  

It supports both a preloaded **SQLite database (`student.db`)** and custom **MySQL connections**.  

---

## 🚀 Features

- 💬 Chat with your database using **natural language**  
- 🛢️ Supports both **SQLite** (default) and **MySQL**  
- 🔗 Powered by **LangChain SQL Agent** and **SQLDatabaseToolkit**  
- ⚡ Uses **GROQ LLM (Gemma2-9b-it)** for accurate query generation  
- 🎛️ Interactive **Streamlit UI** with message history  
- 🧠 Auto-translates queries into **SQL statements** behind the scenes  
- 📊 Example database (`student.db`) preloaded with `STUDENT` table  

---

## 🧰 Tech Stack

- Python  
- Streamlit  
- LangChain  
- GROQ LLM (`gemma2-9b-it`)  
- SQLite / MySQL  
- SQLAlchemy  

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jasoncobra3/ChatSQL.git
   cd ChatSQL


2. **Create Virtual Environment**
   ```bash
    python -m venv venv
   
3. **Activate the Virtual Environment**
   ```bash
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    venv/bin/activate

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

---
## 🔐 Setup
1. **Create a `.env` file in root folder with**
   ```env
    GROQ_API_KEY=your_groq_api_key_here
   ```
   
2. **SQLite Database (Default)**
    Run `sqlite.py` to create `student.db` with sample records.
   ```bash
   python sqlite.py
   ```
  This creates a `STUDENT` table with sample entries:
  ```bash
  Name    | Subject       | Grade | Marks
--------|---------------|-------|------
Krish   | Data Science  | A     | 90
John    | Data Science  | B     | 100
Mukesh  | Data Science  | A     | 86
Jacob   | DEVOPS        | A     | 50
Dipesh  | DEVOPS        | A     | 35
```

3. **MySQL Connection, In the Streamlit sidebar, provide**:
- Host
- User
- Password
- Database name

---

##  🚀Run the App
   **Run the Script in Terminal**
   ```bash
     streamlit run app.py
   ```

---

## 📁 Project Structure
```

├── app.py          # Main Streamlit app
├── sqlite.py       # Script to generate sample SQLite DB
├── student.db      # SQLite DB file (created by sqlite.py)
├── requirements.txt
└── README.md
```

---

##  🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork this repo and submit a pull request

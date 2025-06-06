import streamlit as st 
from pathlib import Path
import os  # Added for environment variables
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits import SQLDatabaseToolkit  # Updated import
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
import sqlite3

st.set_page_config(page_title="Langchain: Chat With SQL DB", page_icon="🦜")
st.title("🦜 Langchain: Chat with SQL DB")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = ["Use SQLite3 Database:-Student.db", "Connect to your MySQL Database"]

selected_opt = st.sidebar.radio(
    label="Choose the DB which you want to chat",
    options=radio_opt
)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database")
else:
    db_uri = LOCALDB
    
# Updated API key handling with environment variable fallback
api_key = st.sidebar.text_input(
    label="Groq API key",
    type="password"
) or os.getenv("GROQ_API_KEY")

if not db_uri:
    st.info("Please enter the database information and uri")
    
if not api_key:
    st.error("Please add the GROQ API key either in the sidebar or as GROQ_API_KEY environment variable")
    st.stop()  # Stop execution if no API key is provided

# LLM Model
try:
    llm = ChatGroq(
        api_key=api_key,
        model_name="gemma2-9b-it",
        streaming=True
    )
except Exception as e:
    st.error(f"Failed to initialize Groq client: {str(e)}")
    st.stop()

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide All MySQL Connection Details")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)
    
# Toolkit
toolkit = SQLDatabaseToolkit(llm=llm, db=db)

agent = create_sql_agent(
    toolkit=toolkit,
    llm=llm,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
)

if "messages" not in st.session_state or st.sidebar.button("Clear Message History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        try:
            response = agent.run(user_query, callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": f"Sorry, I encountered an error: {str(e)}"})

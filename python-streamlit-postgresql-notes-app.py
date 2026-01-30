'''
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

-- db.py

from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASSWORD = "turtlecode"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)



-- app.py

import streamlit as st
import pandas as pd
from sqlalchemy import text
from db import engine

st.set_page_config(page_title="Notes App", page_icon="📝")

st.title("📝 Streamlit + PostgreSQL Notes App")

# ----------------------
# Add a new note
# ----------------------
st.subheader("Add New Note")

title = st.text_input("Title")
content = st.text_area("Content")

if st.button("Save"):
    if title:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO notes (title, content) VALUES (:title, :content)"
                ),
                {"title": title, "content": content},
            )
        st.success("Note saved successfully 🎉")
    else:
        st.warning("Title cannot be empty!")

# ----------------------
# List notes
# ----------------------
st.subheader("📚 Saved Notes")

query = """
SELECT id, title, content, created_at
FROM notes
ORDER BY created_at DESC
"""

df = pd.read_sql(query, engine)

st.dataframe(df, use_container_width=True)

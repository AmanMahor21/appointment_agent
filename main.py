from dotenv import load_dotenv
from fastapi import FastAPI
import os
from app.db.sqlite import create_db
from app.route import register_routes
# from app.nodes.user_info import extract_user_info

load_dotenv()
app = FastAPI()

register_routes(app)
create_db()
# extract_user_info()


@app.get("/try")
def read_root():
    return {"Hello": "langraph"}

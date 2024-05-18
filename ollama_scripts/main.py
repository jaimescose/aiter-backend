from fastapi import FastAPI
from utils import query_llm

app = FastAPI()

@app.get("/process")
def process():
    query = "How can I do to improve my VO2Max?"
    result = query_llm(query)
    return {"result": result}
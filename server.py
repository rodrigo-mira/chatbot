from fastapi import FastAPI
from langserve import add_routes
from dotenv import load_dotenv
from chatbot import qa_chain

load_dotenv()

app = FastAPI(
  title="Chatbot Promotior",
  version="1.0",
  description="Un chatbot para la prueba de promptior",
)

add_routes(app, qa_chain, playground_type="default")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
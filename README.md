# healthatlas-ai

# add src/ to Python path so the chiron module is discoverable
export PYTHONPATH=./src

# start FastAPI in dev mode
uvicorn chiron.main:app --reload --host 0.0.0.0 --port 8000

# open http://127.0.0.1:8000/docs for Swagger
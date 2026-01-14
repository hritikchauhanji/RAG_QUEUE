from fastapi import FastAPI, Query
from queues.worker import process_queue
from client.rq_client import queue
app = FastAPI()

@app.get("/")
def root():
    return {"status": "Server is up and running"}

@app.post("/chat")
def chat(
    query: str = Query(..., description="The user query to process")
    ):
      job = queue.enqueue(process_queue, query)
      
      return {"status": "Queued", "job_id": job.id}
  
  
@app.get("/get-status")
def get_result(job_id: str = Query(..., description="job id")):
      job = queue.fetch_job(job_id=job_id)
      resault = job.return_value()
      
      return {"status": "Completed", "result": resault}
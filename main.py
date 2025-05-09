import json
import uvicorn

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage

from graph.graph import graph


app = FastAPI()

@app.get("/chat/stream")
async def stream(query: str, thread_id: str = "1"):
    config = {"configurable": {"thread_id": thread_id}}

    async def event_stream():
        try:
            async for chunk in graph.astream(
                input={"messages": [HumanMessage(content=query)]},
                config=config,
                stream_mode=["custom"],
            ):
                yield f"data: {json.dumps({'text': chunk[1]})}\n\n"
        except Exception as e:
            print(f"========== {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import asyncio
from fastapi import FastAPI, Request
from aio_pika.abc import AbstractIncomingMessage
import json
import uvicorn

from threading import Thread
from config import config
from backend.Consumer import Consumer
from backend.Producer import Producer


app = FastAPI()

success = {'status': 200}
failure = {'failure': 400, 'message': 'bad request'}

global_response_variable = None
def service_response(message: AbstractIncomingMessage):
    print(message)
    global global_response_variable
    global_response_variable = json.loads(message.body)


@app.post('/register')
async def register(request: Request):
    service = json.loads(await request.body())['service']
    await Producer(service=f'{service}-in'
            ).send(message=request.body())

    await Consumer(service=f'{service}-out'
        ).listen(callback=service_response)

    global success
    global failure
    global global_response_variable 
    if global_response_variable != None:
        success['body'] = global_response_variable
        return success
    return failure



def run():
    uvicorn.run(
        app='main:app', 
        host=config.HOST, 
        port=config.PORT,
        workers=1,
        reload=True)

if __name__ == '__main__':
    run()

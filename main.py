from socket import timeout
from fastapi import FastAPI
import uvicorn

from config import config
from core.backend.ConnectionManager import ConnectionManager
from core.schema.Generic import GeneticModel

app = FastAPI()

@app.on_event('startup')
async def startup():
    await ConnectionManager.start(
        services=config.ALLOWED_TOPICS, 
        server=config.RABBITMQ_SERVER,
        suffixes=['in', 'out'])
    
@app.on_event('shutdown')
async def startup():
    await ConnectionManager.stop()

@app.post('/register')
async def register(genetic: GeneticModel):
    await ConnectionManager.send(f'{genetic.service}-in', genetic.user)
    respond = await ConnectionManager.receive(f'{genetic.service}-out', timeout=genetic.timeout)
    return respond


def run():
    uvicorn.run(app='main:app', host=config.HOST, port=config.PORT, workers=1, reload=True)

if __name__ == '__main__':
    run()

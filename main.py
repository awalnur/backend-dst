import threading
from time import sleep

from src.app import app
import uvicorn

from config.cache import get_redis

app = app()


# router = APIRouter(pre)
@app.get(f"/api/v1/healthcheck", status_code=200)
async def healthcheck():
    return {"message": "Ok"}

def get_trx(refno: str):
    print({"message": refno})
    if refno == '1':
        print('del')


def worker(cache=get_redis()):
    # if cache is None:
    #     return None

    # status = cache.getex('referenceNo')
    # print(status)
    while True:
        status = cache.keys('referenceNo*')
        # print(status)
        if status is not None:
            # break
            for trx in status:
                refno = cache.getex(trx)
                get_trx(refno)
        else:
            break
        sleep(5)

if __name__ == "__main__":
    # worker()
    # t = threading.Thread(target=worker)
    # t.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

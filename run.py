from fastapi import FastAPI

from rankwar.view import rw_report

app = FastAPI(title='BEreportapi文档')

app.include_router(rw_report, prefix='/rw/report', tags=['RW相关api'])

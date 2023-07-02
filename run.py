from fastapi import FastAPI

from rank_war.api import rw_report

app = FastAPI(title='BEreportapi文档')

app.include_router(rw_report, prefix='/rw/report', tags=['RW相关api'])

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router
from heyhome import heyhome_router
from tuya import tuya_router

app = FastAPI(
    swagger_ui_parameters={"persistAuthorization": True} # 인증 유지 활성화
    )

@app.on_event("startup")
async def startup():
    print("Application is starting")

@app.on_event("shutdown")
async def shutdown():
    print("Application is shutting down")

origins = [
    "http://127.0.0.1:5173",  # Svelte
    "http://localhost:3000",  # React
    "http://localhost:8000",  # Fastapi
]

# origins = [
#     "http://eplab.hanyang.ac.kr:5173",  # Svelte
#     "http://eplab.hanyang.ac.kr:3000",  # React
#     "http://eplab.hanyang.ac.kr:8000",  # Fastapi
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.include_router(heyhome_router.router)
app.include_router(tuya_router.router)
app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"))


@app.get("/")
def index():
    return FileResponse("../frontend/dist/index.html")

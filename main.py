from http.client import HTTPException

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

app = FastAPI(title="Dashboard API", version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return{"message": "API do Dashboard rodando com sucesso!"}

@app.get("/api/kpis")
def get_kpis(db: Session = Depends(get_db)):
    try:
        total_vendas = db.execute(text("SELECT COUNT(*) FROM vendas")).scalar()
        receita_total = db.execute(text("SELECT SUM(valor) FROM vendas")).scalar() or 0.0
        ticket_medio = db.execute(text("SELECT AVG(valor) FROM vendas")).scalar() or 0.0

        return{
            "total_vendas": total_vendas,
            "receita_total": float(receita_total),
            "ticket_medio": round(float(ticket_medio), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/grafico-categorias")
def get_grafico_categorias(db: Session = Depends(get_db)):
    try:
         query = text("""
              SELECT categoria, SUM(valor) as total_receita
              FROM vendas
              GROUP BY categoria
              ORDER BY total_receita DESC:
         """)
         result = db.execute(query).fetchall()

         categorias = [row[0] for row in result]
         receitas = [float(row[1]) for row in result]

         return{
             "labels": categorias,
             "data": receitas
         }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
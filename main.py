from http.client import HTTPException

from fastapi import Depends, FastAPI, Query
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

# 1. Rota para os Gráficos: Agrupa receita por categoria
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

         # Mapeando os resultados para listas separadas
         categorias = [row[0] for row in result]
         receitas = [float(row[1]) for row in result]

         return{
             "labels": categorias,
             "data": receitas
         }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#2. Rota para a Tabela: Suporta paginação (limit/skip) e filtro por categoria
@app.get("/api/tabela-vendas")
def get_tabela_vendas(
    categoria: str | None = Query(default=None, description="Filtrar por categoria"),
    limit: int = Query(default=5, ge=1, le=50, description="Itens por página"),
    skip: int = Query(default=0, ge=0, description="Itens a pula"),
    db: Session = Depends(get_db)
):

    try:
        if categoria:
            query = text("""
                SELECT id, cliente, categoria, valor, data_venda
                FROM vendas
                WHERE categoria  = :cat
                ORDER BY data_venda DESC 
                LIMIT :limit OFFSET :skip;
                """)
            result = db.execute(query,{"cat": categoria,"limit": limit, "skip": skip }).fetchall()
        else:
            query = text("""
                SELECT id, cliente, categoria, valor, data_venda
                FROM vendas
                ORDER BY data_venda DESC 
                LIMIT :limit OFFSET :skip;
                """)
            result = db.execute(query, {"limit": limit, "skip": skip}).fetchall()

        vendas_lista = []
        for row in result:
            vendas_lista.append({
                "id": row[0],
                "cliente": row[1],
                "categoria": row[2],
                "valor": float(row[3]),
                "data_venda": str(row[4])
            })

            return {"vendas": vendas_lista}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

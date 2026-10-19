from fastapi import FastAPI, Depends, HTTPException, Query
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
    return {"message": "API rodando"}

@app.get("/api/kpis")
def get_kpis(db: Session = Depends(get_db)):
    try:
        total_vendas = db.execute(text("SELECT COUNT(*) FROM vendas;")).scalar()
        receita_total = db.execute(text("SELECT SUM(valor) FROM vendas;")).scalar() or 0.0
        ticket_medio = db.execute(text("SELECT AVG(valor) FROM vendas;")).scalar() or 0.0

        return {
            "total_vendas": int(total_vendas or 0),
            "receita_total": float(receita_total),
            "ticket_medio": round(float(ticket_medio), 2)
        }
    except Exception as e:
        print(f"Erro em kpis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/grafico-categorias")
def get_grafico_categorias(db: Session = Depends(get_db)):
    try:
        query = text("SELECT categoria, SUM(valor) as total FROM vendas GROUP BY categoria ORDER BY total DESC;")
        result = db.execute(query).fetchall()
        
        categorias = [row[0] for row in result]
        receitas = [float(row[1]) for row in result]

        return {
            "labels": categorias,
            "data": receitas
        }
    except Exception as e:
        print(f"Erro em grafico: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tabela-vendas")
def get_tabela_vendas(
    categoria: str | None = Query(default=None),
    limit: int = Query(default=5, ge=1, le=50),
    skip: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    try:
        if categoria:
            query = text("SELECT id, cliente, categoria, valor, data_vendas FROM vendas WHERE categoria = :cat ORDER BY data_vendas DESC LIMIT :limit OFFSET :skip;")
            result = db.execute(query, {"cat": categoria, "limit": limit, "skip": skip}).fetchall()
        else:
            query = text("SELECT id, cliente, categoria, valor, data_vendas FROM vendas ORDER BY data_vendas DESC LIMIT :limit OFFSET :skip;")
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
        print(f"Erro em tabela: {e}")
        raise HTTPException(status_code=500, detail=str(e))
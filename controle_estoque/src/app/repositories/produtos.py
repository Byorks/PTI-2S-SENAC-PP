import csv
from pathlib import Path
from ..models.produto import Produto
from ..utils.arquivos import arquivo_vazio
from ..config import DATA_DIR
import uuid

CAMPOS = ["codigo", "nome", "preco", "quantidade"]
# CSV_FILE = Path("src/data/produtos.csv")
CSV_FILE = DATA_DIR / "produtos.csv"


class ProdutoRepository:
    # Métodos dentro de classe, métodos de instancia
    def __init__(self):
        self._verificar_arquivo()

    # Métodos privados iniciam a com _, mas se trata de uma convenção não temos como encapsular realmente
    def _verificar_arquivo(self):
        if not CSV_FILE.exists():
            # Cria pasta data se nào existir
            CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
            with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)  # Cria escritor CSV
                # Seria possível assim: nova_lista = ["id", *CAMPOS] com uso de args
                writer.writerow(CAMPOS)

    # A seta é pra mostrar o tipo que vai ser retornado
    # Type hint
    def _ler_todos(self) -> list[dict]:
        if not CSV_FILE.exists():
            return []
        with CSV_FILE.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
        
    def _salvar_todos(self, produtos: list[dict]):
        # with -> 
        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", *CAMPOS])
            writer.writeheader()
            writer.writerows(produtos)

    def adicionar(self, produto: Produto, ) -> None:
        produtos = self._ler_todos()
        if any(p["codigo"] == produto.codigo for p in produtos):
            raise ValueError( f"Código {produto.codigo} já existe!")
        
        print(produtos)
        produtos.append({
            "id": str(produto.id),
            "codigo": produto.codigo,
            "nome": produto.nome,
            "preco": str(produto.preco),
            "quantidade": str(produto.quantidade) 
        })
        
        print(produtos)
        self._salvar_todos(produtos)
        
    def listar_todos(self) -> list[Produto]:
        dados = self._ler_todos()
        return [
            Produto(
                id=uuid.UUID(p["id"]),
                codigo=p["codigo"],
                nome=p["nome"],
                preco=float(p["preco"]),
                quantidade=int(p["quantidade"])
            ) 
            for p in dados
        ]
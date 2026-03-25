from __future__ import annotations

from collections.abc import Iterable

from ..models.produto import Produto
from .produtos import ProdutoRepository
from .protocols import ProdutoRepositoryProtocol


class ProdutoInMemoryRepository:
    def __init__(self, *, loader: ProdutoRepositoryProtocol | None = None):
        self._produtos: list[Produto] = []
        self._por_codigo: dict[str, Produto] = {}

        if loader is None:
            loader = ProdutoRepository()

        self._carregar(loader.listar_todos())

    def _carregar(self, produtos: Iterable[Produto]) -> None:
        for produto in produtos:
            if produto.codigo in self._por_codigo:
                raise ValueError(
                    f"Conflito ao carregar dados: código {produto.codigo} duplicado."
                )
            self._por_codigo[produto.codigo] = produto
            self._produtos.append(produto)

    def adicionar(self, produto: Produto) -> None:
        if produto.codigo in self._por_codigo:
            raise ValueError(f"Código {produto.codigo} já existe!")

        self._por_codigo[produto.codigo] = produto
        self._produtos.append(produto)

    def listar_todos(self) -> list[Produto]:
        return list(self._produtos)

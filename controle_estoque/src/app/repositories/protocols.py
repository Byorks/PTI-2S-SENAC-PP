from __future__ import annotations

from typing import Protocol

from ..models.produto import Produto


class ProdutoRepositoryProtocol(Protocol):
    def adicionar(self, produto: Produto) -> None:
        ...

    def listar_todos(self) -> list[Produto]:
        ...

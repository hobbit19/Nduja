from typing import Iterator
from typing import Any
from typing import Optional
from typing import Dict


def draw(G: Graph, **kwargs: Any) -> Any: ...
def graphviz_draw(G: Graph, **kwargs: Any) -> Any: ...

class PropertyMap:
    def __init__(self, pmap: Any, g: Any, key_type: Any) -> None: ...
    def __getitem__(self, item: Any) -> Any: ...
    def __iter__(self) -> Any: ...

class Vertex:
    def __getitem__(self, item: Any): ...
    def __iter__(self) -> Iterator[Any]: ...
    def all_edges(self) -> Iterator[Edge]: ...
    def all_neighbors(self) -> Iterator[Vertex]: ...
    def in_degree(self, weight: Optional[Any]) -> int: ...
    def out_degree(self, weight: Optional[Any]) -> int: ...
    def in_neighbors(self) -> Iterator[Vertex]: ...
    def is_valid(self) -> bool: ...
    def out_neighbors(self) -> Iterator[Vertex]: ...

class Edge:
    def __getitem__(self, item: Any): ...
    def __iter__(self) -> Iterator[Any]: ...
    def source(self) -> Vertex: ...
    def target(self) -> Vertex: ...
    def is_valid(self) -> bool: ...

class Graph:
    def __init__(self, g:Optional[Graph] = None,
                 directed:bool = True,
                 prune:bool = False,
                 vorder:Optional[PropertyMap] = None) -> None: ...

    def edge(self, u: Vertex, v: Vertex) -> Optional[Edge]: ...
    def new_vertex_property(self, t: str) -> PropertyMap: ...
    def new_edge_property(self, t: str) -> PropertyMap: ...
    def add_vertex(self, **kwargs: Any) -> Vertex: ...
    def add_edge(self, u: Vertex, v: Vertex,
                 **kwargs: Dict[Any, Any]) -> Edge: ...
    def copy(self): ...

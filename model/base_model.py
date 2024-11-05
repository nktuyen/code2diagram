class BaseModel:
    def __init__(self, name: str = '', parent = None) -> None:
        self._name: str = name
        self._parent: BaseModel = parent
        self._children: list = []
    
    def __str__(self):
        return self._name
    
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, val: str):
        self._name = val
    
    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, val) -> None:
        self.parent = val
    
    @property
    def children(self) -> list:
        return self._children
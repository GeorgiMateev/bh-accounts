import abc
from typing import Optional, List
from accounts.domain import model

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item:model.Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: str) ->Optional[model.Entity]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[model.Entity]:
        raise NotImplementedError

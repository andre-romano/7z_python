import logging
from threading import RLock

# Configuração do logger
logger = logging.getLogger(__name__)


class SafeList:
    def __init__(self, listObj: list | None = None):
        """Inicializa uma lista compartilhada com bloqueio para segurança em threads."""
        self._list = listObj or []
        self._lock = RLock()

    def append(self, value):
        """Adiciona um item à lista de maneira segura."""
        with self._lock:
            self._list.append(value)

    def extend(self, values):
        """Adiciona múltiplos itens à lista de maneira segura."""
        with self._lock:
            self._list.extend(values)

    def insert(self, index, value):
        """Insere um item na posição especificada de maneira segura."""
        with self._lock:
            self._list.insert(index, value)

    def pop(self, index=-1):
        """Remove e retorna um item da lista de maneira segura."""
        with self._lock:
            return self._list.pop(index)

    def remove(self, value):
        """Remove um item da lista de maneira segura."""
        with self._lock:
            self._list.remove(value)

    def clear(self):
        """Esvazia a lista de maneira segura."""
        with self._lock:
            self._list.clear()

    def index(self, value, start=0, end=None):
        """Retorna o índice do primeiro item correspondente de maneira segura."""
        with self._lock:
            return self._list.index(value, start, end if end is not None else len(self._list))

    def count(self, value):
        """Conta o número de ocorrências de um item na lista."""
        with self._lock:
            return self._list.count(value)

    def sort(self, **kwargs):
        """Ordena a lista de maneira segura."""
        with self._lock:
            self._list.sort(**kwargs)

    def reverse(self):
        """Inverte a ordem da lista de maneira segura."""
        with self._lock:
            self._list.reverse()

    def copy(self):
        """Retorna uma cópia segura da lista."""
        with self._lock:
            return SafeList(self._list.copy())

    def toList(self):
        """Retorna uma cópia da lista interna como uma lista normal."""
        with self._lock:
            return self._list.copy()

    def __getitem__(self, index):
        """Obtém um item da lista de maneira segura."""
        with self._lock:
            return self._list[index]

    def __setitem__(self, index, value):
        """Define um valor na posição específica de maneira segura."""
        with self._lock:
            self._list[index] = value

    def __delitem__(self, index):
        """Remove um item pelo índice de maneira segura."""
        with self._lock:
            del self._list[index]

    def __contains__(self, value):
        """Verifica se um item está na lista de maneira segura."""
        with self._lock:
            return value in self._list

    def __len__(self):
        """Retorna o tamanho da lista de maneira segura."""
        with self._lock:
            return len(self._list)

    def __iter__(self):
        """Make SafeList iterable by returning a thread-safe iterator."""
        with self._lock:
            return iter(self._list.copy())

    def __repr__(self):
        """Retorna uma representação da lista de maneira segura."""
        with self._lock:
            return repr(self._list)

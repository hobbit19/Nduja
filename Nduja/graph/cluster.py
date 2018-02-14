from typing import Iterable
from typing import Set
from typing import Any

from dao.wallet import Wallet

from graph.BitcoinTransactionRetriever import BtcTransactionRetriever


class Cluster:
    """Class that represents the Wallet that are belonging (or are supposed to
    belong) to a person, i.e., addresses that are inputs of the same transaction
    """

    def __init__(self,
                 addresses: Iterable[Wallet],
                 inferred_addresses: Iterable[Wallet] = []) -> None:
        self._original_addresses = set(addresses)
        self._inferred_addresses = set(inferred_addresses)
        for w in self._original_addresses:
            self._inferred_addresses.add(w)

    @property
    def original_addresses(self) -> Set[Wallet]:
        return self._original_addresses

    @property
    def inferred_addresses(self) -> Set[Wallet]:
        return self._inferred_addresses

    def add_inferred_address(self, address: Wallet):
        self._inferred_addresses.add(address)

    def merge_original_list(self, other: 'Cluster'):
        self.original_addresses.update(other.original_addresses)

    def merge(self, other: 'Cluster') -> 'Cluster':
        originals = self.original_address.union(other.original_address)
        inferred = self.inferred_addresses.union(other.inferred_addresses)
        return Cluster(originals, inferred)

    def __hash__(self):
        return hash(frozenset(self._inferred_addresses))

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and \
               self._inferred_addresses == other.inferred_addresses

    def __str__(self) -> str:
        return str(list(self._original_addresses)) + "\n" + \
               str(list(self._inferred_addresses))

    def intersect(self, other: 'Cluster') -> bool:
        return self.inferred_addresses.intersection(other.inferred_addresses)

    def fill_cluster(self, black_list=[]):
        btc_transaction_retriever = BtcTransactionRetriever()

        stack = set([])
        tmp_black_list = []
        for saddr in self.inferred_addresses:
            stack.add(saddr)

        while len(stack) > 0:
            elem = stack.pop()
            self.add_inferred_address(elem)
            tmp_black_list.append(elem)
            a, b, siblings = btc_transaction_retriever. \
                get_input_output_addresses(elem.address)
            for s in siblings:
                w = Wallet(s, "BTC", "", 1, True)
                if w not in black_list and w not in tmp_black_list:
                    stack.add(w)
"""
Trie (prefix tree) data structure used for autocomplete.

Expected public API:
- class Trie
  - insert(word: str, freq: float)
  - remove(word: str) -> bool
  - contains(word: str) -> bool
  - complete(prefix: str, k: int) -> list[str]
  - stats() -> tuple[int, int, int]
  - items() -> list[tuple[str, float]]

Complexity notes:
- insert/remove/contains: O(L) where L = length of word
- complete(prefix, k): roughly O(M + N log K)
"""

import heapq


class TrieNode:
    """Node of a Trie structure."""
    __slots__ = ("children", "is_word", "freq")

    def __init__(self):
        self.children = {}
        self.is_word = False
        self.freq = 0.0


class Trie:
    def __init__(self):
        """Initialize an empty Trie."""
        self.root = TrieNode()
        self._total_words = 0
        self._total_nodes = 1  # count root

    # --------------------------- internal helpers ---------------------------

    def _trace(self, text):
        """Traverse the Trie along text; return (node, path) if found."""
        node = self.root
        path = [(node, '')]
        for ch in text:
            if ch not in node.children:
                return None, []
            node = node.children[ch]
            path.append((node, ch))
        return node, path

    # ----------------------------- core methods -----------------------------

    def insert(self, word, freq):
        """
        Insert or update a word with its frequency.
        Complexity: O(L)
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self._total_nodes += 1
            node = node.children[ch]

        if not node.is_word:
            node.is_word = True
            self._total_words += 1

        node.freq = freq

    def remove(self, word):
        """
        Remove a word from the Trie if it exists.
        Returns True if removed, False if not found.
        Complexity: O(L)
        """
        node, path = self._trace(word)
        if not node or not node.is_word:
            return False

        node.is_word = False
        node.freq = 0.0
        self._total_words -= 1

        # prune unnecessary nodes from bottom up
        for i in range(len(path) - 1, 0, -1):
            parent, ch = path[i - 1]
            child, _ = path[i]
            if not child.children and not child.is_word:
                if ch in parent.children:
                    del parent.children[ch]
                    self._total_nodes -= 1
            else:
                break
        return True

    def contains(self, word):
        """Return True if exact word exists. Complexity: O(L)."""
        node, _ = self._trace(word)
        return node is not None and node.is_word

    def complete(self, prefix, k):
        """
        Return up to k words that start with prefix,
        ranked by frequency (desc) and then alphabetically.
        Complexity: O(M + N log K)
        """
        node, _ = self._trace(prefix)
        if not node:
            return []

        heap = []  # (freq, word)

        def dfs(cur_node, built):
            if cur_node.is_word:
                item = (cur_node.freq, built)
                if len(heap) < k:
                    heapq.heappush(heap, item)
                else:
                    heapq.heappushpop(heap, item)

            for ch in sorted(cur_node.children.keys()):
                dfs(cur_node.children[ch], built + ch)

        dfs(node, prefix)

        # sort by descending freq, ascending word
        result = sorted(heap, key=lambda x: (-x[0], x[1]))
        return [word for _, word in result]

    def stats(self):
        """
        Return (num_words, height, num_nodes).
        Complexity: O(T) to compute height.
        """
        def height(node):
            if not node.children:
                return 0
            return 1 + max(height(child) for child in node.children.values())

        return (self._total_words, height(self.root), self._total_nodes)

    def items(self):
        """
        Return list of all (word, freq) pairs stored in the Trie.
        Complexity: O(T)
        """
        pairs = []

        def gather(node, prefix):
            if node.is_word:
                pairs.append((prefix, node.freq))
            for ch, nxt in node.children.items():
                gather(nxt, prefix + ch)

        gather(self.root, "")
        return pairs

from typing import List


class Chunker:
    def __init__(self, chunk_size: int = 800, overlap: int = 150):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        i = 0
        n = len(text)
        while i < n:
            end = min(i + self.chunk_size, n)
            chunks.append(text[i:end])
            if end == n:
                break
            i = end - self.overlap
            if i < 0:
                i = 0
        return chunks
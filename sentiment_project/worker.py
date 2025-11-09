# worker.py
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import List
from sentiment import classify




class ParallelSentiment:
def __init__(self, max_workers: int = 4):
self.max_workers = max_workers
self.lock = Lock()
self.results = [] # lista segura por Lock


def _process_chunk(self, comments_chunk: List[str]):
local = []
for c in comments_chunk:
label = classify(c)
local.append((c, label))
# sincronizamos escritura en shared state
with self.lock:
self.results.extend(local)
return len(local)


def run(self, comments: List[str], chunk_size: int = 10):
# dividir en chunks sencillos
chunks = [comments[i:i+chunk_size] for i in range(0, len(comments), chunk_size)]
with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
futures = [ex.submit(self._process_chunk, ch) for ch in chunks]
for f in as_completed(futures):
_ = f.result()
return self.results




if __name__ == "__main__":
# ejemplo de uso
sample = [
"Me encanta este producto, es excelente",
"Muy malo, llegó defectuoso",
"No está mal, hace su función",
]
ps = ParallelSentiment(max_workers=3)
res = ps.run(sample, chunk_size=1)
for r in res:
print(r)

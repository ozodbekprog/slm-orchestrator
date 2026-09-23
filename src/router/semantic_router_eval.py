#!/usr/bin/env python3
"""SLM Orkestrator — SEMANTIC ROUTER (o'qitishsiz) o'rnatish va baholash.

Ikki konfiguratsiya taqqoslanadi:
  A) Sof semantic: 5 route (math|code|uz|chat|image) — multilingual embedding
  B) Gibrid: uz-detektor (tez evristika) + 4 route semantic (qolganlar)

Metrikalar: accuracy, per-class F1, confusion matrix, latency (ms/query).

Ishlatish:
    .venv/bin/python router/semantic_router_eval.py
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

CLASSES = ["math", "code", "uz", "chat", "image"]
ENCODER = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EVAL_FILE = Path("data/router_eval.jsonl")
LOG = Path("logs/inference/semantic_router_results.json")

# ----------------------------------------------------------- utterances
UTTERANCES: dict[str, list[str]] = {
    "math": [
        "solve for x", "what is 25 times 4", "calculate the derivative of x squared",
        "find the integral from 0 to 1", "what percentage of 80 is 20",
        "area of a circle with radius 5", "probability of rolling a six",
        "simplify the fraction", "compute the sum of the first n numbers",
        "convert kilometers to miles", "solve the quadratic equation",
        "least common multiple", "average speed of the train",
        "how many combinations of items", "what is 15 percent off",
        "prove that the sum is divisible", "matrix determinant calculation",
        "solve the equation 3x plus 7 equals 22", "what is the integral of sine",
        "compute the determinant of the matrix", "how many prime numbers below 100",
        "the sum of angles in a triangle", "convert 5 feet to meters",
        "what is the tangent of 45 degrees", "compound interest calculation",
        "find the roots of the polynomial", "standard deviation of the dataset",
        "logarithm base 2 of 64", "greatest common divisor of two numbers",
        "volume of a sphere radius 3", "what is 7 factorial",
        "solve the system of linear equations", "percentage increase from 40 to 50",
        "find the limit as x approaches zero", "arithmetic sequence sum",
        "what is 2 to the power of 10", "median of the numbers list",
    ],
    "code": [
        "write a python function", "debug my code", "fix this error",
        "explain this code snippet", "sql query to find duplicates",
        "how do i parse json", "write a unit test", "docker build fails",
        "git merge versus rebase", "optimize this slow loop",
        "regex for email validation", "http request example", "typeerror none type",
        "indexerror list index out of range", "segmentation fault core dumped",
        "compile error in c++", "dependency injection", "api endpoint with fastapi",
        "database migration", "async await example", "refactor this class",
        "code review feedback", "algorithm complexity big o", "binary search implementation",
        "python script to resize images with opencv", "read image metadata in code",
        "convert image format programmatically", "pdf to text extraction script",
        "web scraping with beautifulsoup", "flask route returns 500 error",
        "how to use a virtual environment", "pip install fails with permission error",
        "merge conflicts in git", "kubernetes pod crashloopbackoff",
        "sql join three tables", "redis cache implementation", "rabbitmq message queue",
        "write a bash loop over files", "yaml parsing in python",
        "upload file to s3 with boto3", "jwt authentication middleware",
        "websocket server example", "pytest fixture example",
        "linting setup with ruff", "type hints for a function",
        "dataclass versus namedtuple", "memory leak profiling",
    ],
    "chat": [
        "hello how are you", "tell me a joke", "thanks that was helpful",
        "what is your favorite color", "i feel tired today", "recommend a good book",
        "let's talk about music", "good morning", "what should i have for dinner",
        "congratulations on the release", "good night see you tomorrow",
        "what do you think about coffee", "i watched a great movie",
        "tell me a fun fact", "how was your day", "i am bored",
        "motivational quote please", "do you have hobbies", "what makes you happy",
        "how is the weather today", "i had a long day at work", "what should i watch tonight",
        "my favorite season is autumn", "do you prefer cats or dogs",
        "i just moved to a new city", "any tips for better sleep", "what is a good breakfast",
        "i am learning to cook", "tell me about your favorite food",
        "how do i make new friends", "i want to start jogging", "what movie should i watch",
        "i love rainy days", "board games night with friends", "i planted tomatoes today",
        "do you play chess", "what is a good podcast", "i am redecorating my room",
        "coffee or tea in the morning", "i finished a puzzle", "planning a weekend trip",
        "my phone battery drains fast", "looking for a new hobby", "how to stay focused",
        "i adopted a kitten", "best way to learn guitar", "what should i cook for guests",
        "i enjoy long walks", "favorite childhood memory", "how to be more productive",
        "i want to write a diary",
        "say hello in one sentence", "say hi", "say hello to me", "greet me briefly",
        "write a short greeting", "introduce yourself", "say welcome", "wish me good luck",
        "tell me something nice", "cheer me up", "say good morning", "say good night",
    ],
    "image": [
        "draw a cat", "generate an image of a dragon", "create a logo for my shop",
        "what is in this picture", "remove the background from this photo",
        "upscale this image", "colorize this old photograph",
        "turn this sketch into a realistic render", "describe this image",
        "make it look like an anime scene", "extract text from this screenshot",
        "a watercolor painting of mountains", "pixel art sprite of a knight",
        "concept art of a sci-fi city", "blend these two photos",
        "retouch this portrait", "replace the sky in this photo",
        "generate a poster design", "make a minimalist wallpaper",
        "generate a landscape with mountains and a river", "portrait of a queen in renaissance style",
        "create three logo variations", "remove the person from this photo",
        "change the background to a beach", "make a sticker pack from my pet photo",
        "enhance the colors of this photo", "denoise this grainy image",
        "comic book style illustration", "turn this photo into a pencil sketch",
        "generate icons for a mobile app", "matte painting of a fantasy castle",
        "product mockup on a white background", "restore this old damaged photo",
        "seamless pattern of tropical leaves", "character design sheet for a game",
        "isometric room illustration", "create a banner for my channel",
        "fix the perspective of this building photo", "anime portrait of a girl with blue hair",
        "aerial view of a coastline at sunset",
    ],
    "uz": [
        "salom, qalaysiz", "menga o'zbek tilida yozib ber", "O'zbekistonning poytaxti qayerda",
        "matematik masalani yechib ber", "bu kodda xato bormi", "tarjima qilib ber",
        "qanday qilib buni qilaman", "menga rasm chizib ber", "ertaga ob-havo qanday",
        "kitob tavsiya qiling", "rahmat, juda foydali bo'ldi", "kechirasiz, tushunmadim",
        "o'zbek tilida gaplashamiz", "shu gapni inglizchaga o'gir", "menga maslahat bering",
        "nega bunday bo'lyapti", "qancha vaqt ketadi", "qayerdan topa olaman",
        "ertaga uchrashuv bor", "ishlarim yaxshi", "yordamingiz uchun rahmat",
        "bir savolim bor edi", "buni qanday hal qilaman", "o'zbek adabiyoti haqida gapirib bering",
        "assalomu alaykum, yaxshimisiz", "menga yordam bering", "buni qanday qilish mumkin",
        "kechagi kun qanday o'tdi", "ertaga nima qilamiz", "menga maslahat kerak",
        "o'qishga tayyorlanyapman", "ishdan charchadim", "bugun havo juda issiq",
        "menga kitob tavsiya qiling", "oila haqida gaplashaylik", "pulni qanday tejash mumkin",
        "yangi telefon olishni o'ylayapman", "sog'liq uchun nima foydali",
        "sayohatga chiqmoqchiman", "o'zbek taomlari haqida aytib bering",
        "buxoro shahri haqida ma'lumot", "ingliz tilini qanday o'rganaman",
        "ertalabki mashqlar foydalimi", "ish topish uchun maslahat",
        "kompyuterim sekin ishlayapti", "internet tezligini qanday oshiraman",
        "rasmni qanday tahrirlayman", "kod yozishni o'rganmoqchiman",
        "matematikadan yordam kerak", "misolni yechib bera olasizmi",
        "tarjima qilib bering iltimos", "xat yozishga yordam bering",
        "rejam haqida o'ylayapman", "bugun nima yangilik bor",
    ],
}

UZ_WORDS = {
    "va", "bilan", "uchun", "qanday", "nima", "nima?", "menga", "kerak", "bo'ladi",
    "bo'ldi", "shunday", "juda", "yaxshi", "nega", "qayerda", "qachon", "qancha",
    "kim", "men", "sen", "biz", "ular", "rahmat", "salom", "xayr", "iltimos",
    "bor", "yo'q", "kerakmi", "qilib", "bering", "beringiz", "qiling", "qilaman",
    "yozib", "chizib", "yechib", "tarjima", "tushunmadim", "gaplashamiz", "o'zbek",
    "o'zbekcha", "o'zbekiston", "haqida", "hali", "endi", "yana", "hammasi", "ishlarim",
}
UZ_SUFFIX = re.compile(r"\w+(lar|ning|ga|ka|da|dan|ni|im|ing|miz|siz|miz)\b", re.I)


def uz_score(text: str) -> int:
    t = text.lower()
    score = 0
    if re.search(r"[oʻo'gʻg']", t):
        score += 1
    words = set(re.findall(r"[a-zʻ'’]+", t))
    score += len(words & UZ_WORDS)
    if UZ_SUFFIX.search(t):
        score += 1
    return score


def load_eval() -> tuple[list[str], np.ndarray]:
    texts, labels = [], []
    with EVAL_FILE.open(encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            texts.append(d["text"])
            labels.append(CLASSES.index(d["label"]))
    return texts, np.array(labels)


def best_route(q_emb: np.ndarray, route_embs: dict[str, np.ndarray]) -> tuple[str, float]:
    best, best_score = "chat", -1.0
    for route, embs in route_embs.items():
        sim = float(np.max(q_emb @ embs.T))
        if sim > best_score:
            best, best_score = route, sim
    return best, best_score


def main() -> None:
    print(f"Encoder yuklanmoqda: {ENCODER}")
    model = SentenceTransformer(ENCODER)
    texts, labels = load_eval()
    print(f"Eval: {len(texts)} namuna")

    route_embs = {r: model.encode(u, normalize_embeddings=True, convert_to_numpy=True,
                                  show_progress_bar=False)
                  for r, u in UTTERANCES.items()}

    for cfg in ["A_pure", "B_hybrid"]:
        routes = CLASSES if cfg == "A_pure" else ["math", "code", "chat", "image"]
        preds, lat = [], []
        for text in texts:
            t0 = time.perf_counter()
            if cfg == "B_hybrid" and uz_score(text) >= 2:
                pred = "uz"
            else:
                emb = model.encode([text], normalize_embeddings=True,
                                   convert_to_numpy=True, show_progress_bar=False)[0]
                pred, _ = best_route(emb, {r: route_embs[r] for r in routes})
            lat.append((time.perf_counter() - t0) * 1000)
            preds.append(CLASSES.index(pred))

        preds_a = np.array(preds)
        acc = accuracy_score(labels, preds_a)
        f1m = f1_score(labels, preds_a, average="macro")
        f1p = f1_score(labels, preds_a, average=None)
        cm = confusion_matrix(labels, preds_a).tolist()
        med = float(np.median(lat))

        print(f"\n=== Konfiguratsiya {cfg} ===")
        print(f"accuracy : {acc:.4f}")
        print(f"f1_macro : {f1m:.4f}")
        print(f"latency  : {med:.1f} ms/query (median)")
        print("per-class F1: " + "  ".join(f"{c}={v:.3f}" for c, v in zip(CLASSES, f1p)))
        if cfg == "A_pure":
            print("confusion matrix (satr=haqiqiy, ustun=pred):")
            print("        " + " ".join(f"{c:>6s}" for c in CLASSES))
            for c, row in zip(CLASSES, cm):
                print(f"{c:>7s} " + " ".join(f"{v:>6d}" for v in row))

        if cfg == "A_pure":
            res_a = dict(accuracy=acc, f1_macro=f1m, latency_ms=med,
                         f1_per_class=dict(zip(CLASSES, f1p.tolist())), confusion=cm)
        else:
            res_b = dict(accuracy=acc, f1_macro=f1m, latency_ms=med,
                         f1_per_class=dict(zip(CLASSES, f1p.tolist())))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps({"A_pure": res_a, "B_hybrid": res_b}, indent=1))
    print(f"\nNatijalar: {LOG}")


if __name__ == "__main__":
    sys.exit(main())

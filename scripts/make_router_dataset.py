#!/usr/bin/env python3
"""SLM Orkestrator — BOSQICH 2: router dataset (10k, 5 sinf) generatori.

Sinflar: math | code | uz | chat | image
Har sinf: 2000 namuna (train 1600 / eval 400), jami 10 000.

Parallel: multiprocessing Pool(--workers). Mashinada 12 thread bor —
10-12 worker optimal; 20 worker oversubscribe qiladi (foyda yo'q).

Ishlatish:
    .venv/bin/python scripts/make_router_dataset.py --workers 10
"""
from __future__ import annotations

import argparse
import json
import random
import re
from multiprocessing import Pool
from pathlib import Path

CLASSES = ["math", "code", "uz", "chat", "image"]
PER_CLASS = 2000
UZ_SOURCE = Path("../uz-llm-lab/data/uzbek-instruct.jsonl")

PREFIX = ["", "", "", "Please ", "Can you ", "I need to ", "Help me ", "Quick question: ",
          "Hey, ", "Could you please "]

# ---------------------------------------------------------------- math
MATH_TEMPLATES = [
    "What is {a} * {b}?", "Calculate {a} + {b} - {c}.", "How much is {a} divided by {b}?",
    "{a}% of {b} equals what?", "Solve for x: {a}x + {b} = {c}.",
    "What is the square root of {a2}?", "If a train travels {a} km in {b} hours, what is its speed?",
    "A shirt costs {a} dollars after a {b}% discount. What was the original price?",
    "Find the area of a circle with radius {b}.",
    "Simplify the fraction {a}/{b}.", "What is {a} factorial divided by {b} factorial?",
    "Convert {a} kilometers to miles.", "Solve the quadratic equation x^2 - {a}x + {b} = 0.",
    "What is the sum of the first {b} natural numbers?",
    "Three plus five times two equals what?", "What is twenty percent of eighty?",
    "If x = {a} and y = {b}, what is x^2 - y^2?",
    "A rectangle is {a} by {b}. What is its perimeter?",
    "What is the derivative of x^{b} + {a}x?", "Find the mean of {a}, {b}, and {c}.",
    "How many combinations of {b} items from {a} items are there?",
    "What is {a} mod {b}?", "Solve: |x - {a}| = {b}.",
    "A car depreciates {b}% per year. What is its value after 3 years if it cost {a}?",
    "What is the least common multiple of {a} and {b}?",
    "Compute the integral of {a}x^2 dx from 0 to {b}.",
    "If {a} workers build a wall in {b} days, how long for {c} workers?",
]

# ---------------------------------------------------------------- code
CODE_FORMS = [
    "Write a {lang} function to {task}.",
    "How do I {task} in {lang}?",
    "My {lang} code fails when I try to {task}. Any fix?",
    "Show me an example of how to {task} with {lang}.",
    "What is the best way to {task} in {lang}?",
    "Help me debug my {lang} snippet that should {task}.",
    "Explain step by step how to {task} in {lang}.",
]
CODE_TASKS = [
    "reverse a string", "read a CSV file", "parse JSON", "sort a list of dicts",
    "make an HTTP request", "connect to PostgreSQL", "write a unit test", "handle exceptions",
    "upload a file", "send an email", "cache API responses", "rate-limit an endpoint",
    "run a background task", "merge two dataframes", "find duplicates in a list",
    "implement binary search", "validate an email address", "generate a random password",
    "convert timestamps", "use environment variables", "paginate results",
    "write to a log file", "clean temporary files", "schedule a cron job", "profile slow code",
    "resize an image", "handle timeouts", "implement retry logic", "deduplicate records",
    "stream large files", "build a CLI tool", "implement a queue", "read environment config",
    "handle file uploads", "write a Dockerfile", "set up CI for my project",
]
CODE_MISC = [
    "What's the difference between a list and a tuple in Python?",
    "Explain async/await with a simple example.",
    "What is the time complexity of quicksort?",
    "Explain the difference between git merge and git rebase.",
    "Why does my React component re-render infinitely?",
    "How do I use environment variables in a Python project?",
    "What happens when you add two strings in JavaScript?",
    "Explain database normalization with an example.",
    "What is a race condition and how do I avoid it?",
    "How do I handle CORS errors in an Express server?",
    "What is the difference between TCP and UDP?",
    "Explain pointers in C in simple terms.",
    "How does garbage collection work in Go?",
    "What is a deadlock and how can I prevent it?",
    "Explain the CAP theorem.",
]
CODE_ERRORS = [
    "IndexError: list index out of range", "KeyError: 'user_id'",
    "TypeError: cannot unpack non-iterable NoneType", "ImportError: No module named 'requests'",
    "SyntaxError: invalid syntax", "ValueError: could not convert string to float",
    "AttributeError: 'NoneType' object has no attribute 'split'",
    "NullPointerException in my Java code", "Segmentation fault (core dumped)",
    "ModuleNotFoundError: No module named 'numpy'", "UnicodeDecodeError: 'utf-8' codec can't decode",
    "CORS policy: No 'Access-Control-Allow-Origin' header",
    "Cannot read properties of undefined (reading 'map')",
    "EADDRINUSE: address already in use :::3000", "docker: no space left on device",
]
CODE_SNIPPETS = [
    "for (int i = 0; i < n; i++) sum += arr[i];",
    "def f(x): return x[::-1]",
    "SELECT * FROM users WHERE age > 30;",
    "const result = items.filter(i => i.active).map(i => i.id);",
    "if err != nil { return fmt.Errorf(\"load: %w\", err) }",
    "public static void main(String[] args) { }",
    "with open('data.csv') as f: rows = list(csv.reader(f))",
    "await fetch(url, { method: 'POST', body: JSON.stringify(payload) })",
    "return [x for x in nums if x % 2 == 0]",
    "git reset --hard HEAD~1",
    "docker run -p 8080:80 -v $(pwd):/app nginx",
    "CREATE INDEX idx_email ON users(email);",
    "try: risky() except ValueError as e: log(e)",
    "let sum = nums.reduce((a, b) => a + b, 0);",
    "chmod +x deploy.sh && ./deploy.sh",
]

# ---------------------------------------------------------------- image
IMG_ACTS = ["Draw", "Generate an image of", "Create artwork of", "Make a picture of",
            "Illustrate", "Render", "Design a poster of", "Paint"]
IMG_STYLES = ["photorealistic", "in watercolor", "in pixel art", "as an oil painting",
              "as a 3D render", "in anime style", "as a minimalist poster",
              "as a vintage photograph", "in isometric style", "in low-poly style",
              "as concept art", "in cyberpunk style"]
IMG_SUBJECTS = [
    "a cat wearing a spacesuit", "a cyberpunk city at night with neon lights",
    "an old fisherman on a boat", "a mountain lake at sunrise", "a futuristic electric motorcycle",
    "a knight with a glowing sword", "a cozy cabin in a snowy forest", "a dragon over Samarkand",
    "a robot drinking coffee", "a floating island with waterfalls", "a steampunk clock tower",
    "a wolf howling at the moon", "a desert planet with two suns", "a library inside a giant tree",
    "a samurai standing in the rain", "a hot air balloon race above the clouds",
    "a fox reading a book", "an astronaut planting a flag on Mars", "a lighthouse in a storm",
    "a market street in old Bukhara", "a glass butterfly on a flower",
    "a subway station in 2100", "a phoenix rising from ashes", "a ship sailing into a nebula",
    "a chessboard in a surreal landscape", "a lion made of constellation lines",
    "a tiny house on a giant turtle", "a garden of glowing mushrooms",
    "a vintage car on a coastal road", "a snow leopard on a cliff",
]
IMG_EDITS = [
    "Remove the background from this photo.", "Upscale this image to 4K.",
    "What's in this picture?", "Describe everything you see in the attached image.",
    "Colorize this black and white photograph.", "Retouch this portrait: smooth the skin and fix the lighting.",
    "Replace the sky in this photo with a dramatic sunset.", "Extract the text from this screenshot.",
    "What breed is the dog in this photo?", "Remove the watermark from this image.",
    "Blend these two photos into one.", "Turn this sketch into a realistic render.",
    "Make this picture look like a Studio Ghibli scene.", "Fix the red eyes in this photo.",
    "Crop this image to a square.", "Identify the object in this image.",
    "Is this photo real or AI generated?", "Sharpen this blurry photo.",
    "Add snow to this landscape.", "Remove the person in the background.",
]

# ---------------------------------------------------------------- chat
CHAT_OPENERS = ["Hi", "Hello", "Hey", "Good morning", "Good afternoon", "Good evening",
                "Yo", "Hi there"]
CHAT_FOLLOW = ["how are you?", "how's it going?", "what's up?", "how was your day?",
               "long time no see!", "how are things?", "hope you're doing well",
               "anything new?", "what are you up to?", "how do you feel today?",
               "nice to meet you", "good to see you"]
CHAT_FEEL = ["I'm feeling tired today", "I had a great day", "I'm a bit stressed",
             "I'm excited about the weekend", "I'm bored", "I can't sleep",
             "I'm happy right now", "work was exhausting", "I miss my friends",
             "I just finished a big project", "I'm hungry", "I need a break",
             "I'm learning something new", "I feel motivated", "today was tough",
             "I'm looking forward to vacation", "I'm nervous about tomorrow",
             "I feel calm this evening", "I'm proud of myself", "I'm curious about many things"]
CHAT_FEEL_FRAMES = ["{f}.", "{f}, what should I do?", "Honestly, {f}.",
                    "{f} — any advice?", "Anyway, {f}."]
CHAT_PREF_FORMS = ["What's your favorite {x}?", "Do you like {x}?", "What do you think about {x}?",
                   "Recommend a good {x}."]
CHAT_PREF_THINGS = ["color", "movie", "book", "song", "season", "city", "food", "hobby",
                    "programming language", "way to relax", "coffee blend", "board game",
                    "podcast", "documentary", "recipe", "weekend activity", "sport",
                    "travel destination", "science topic", "historical era"]
CHAT_TOPICS = ["music", "space", "history", "cooking", "sports", "movies", "travel",
               "photography", "animals", "technology", "art", "nature", "books",
               "science", "coffee", "chess", "gardening", "astronomy", "philosophy", "design"]
CHAT_MISC = [
    "Thanks, that was really helpful.", "Tell me a fun fact.", "Tell me a short joke.",
    "Give me a motivational quote.", "Who are you?", "Let's just talk. Tell me something interesting.",
    "I watched a great movie last night.", "What's the best way to relax after work?",
    "Do you have any hobbies?", "Good night, see you tomorrow!", "Congratulations on the new release!",
    "Sorry, I didn't catch that. Can you repeat?", "What should I have for dinner?",
    "What's the weather usually like in October?", "I'm planning a small trip.",
    "Do you believe in luck?", "What makes you happy?", "Tell me about your day.",
    "I bought a new plant today.", "My cat is sleeping on my keyboard.",
]
CHAT_SUFFIX = ["", "", "", "", " Thanks!", " :)", " Have a nice day.", " Anyway, talk later.",
               " No rush.", " What do you think?"]
CHAT_STATEMENTS = [
    "cats are better than dogs", "remote work is more productive", "AI will replace most jobs",
    "coffee is healthier than tea", "money can buy happiness", "learning languages is easy",
    "movies are better than books", "winter is the best season", "breakfast is the most important meal",
    "social media does more harm than good", "everyone should learn to code",
    "space exploration is worth the cost", "cities are better than villages",
    "cooking at home saves money", "music helps you focus", "exercising in the morning is best",
    "artificial intelligence is dangerous", "students should learn handwriting",
    "pets make people happier", "traveling alone is fun", "technology makes us lonely",
    "reading fiction improves empathy", "video games are good for the brain",
    "people work better at night", "schools should teach personal finance",
]
CHAT_STORY = [
    "a brave little robot", "a lost cat", "a magical library", "a dragon who loves tea",
    "a detective in the rain", "a time traveler's mistake", "a lighthouse keeper",
    "a fox and a star", "a talking mountain", "a boy who could fly",
    "the last tree on Earth", "a musician in space", "a ghost who helps people",
    "a gardener of clouds", "two friends on a train", "a wish that went wrong",
    "a city under the sea", "the world's smallest elephant", "a book that writes itself",
    "an island that disappears", "a clockmaker's secret", "a bridge between two worlds",
]


def fill(template: str, rng: random.Random) -> str:
    a, b, c = rng.randint(2, 97), rng.randint(2, 89), rng.randint(2, 49)
    a2 = rng.choice([4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
    lang = rng.choice(["Python", "JavaScript", "C++", "Go", "Rust", "Java", "SQL"])
    task = rng.choice(CODE_TASKS)
    return template.format(a=a, b=b, c=c, a2=a2, lang=lang, task=task)


def class_texts(cls: str, rng: random.Random) -> list[str]:
    out: list[str] = []
    if cls == "math":
        out = [fill(t, rng) for t in MATH_TEMPLATES]
        while len(out) < PER_CLASS * 3:
            out.append(fill(rng.choice(MATH_TEMPLATES), rng))
    elif cls == "code":
        langs = ["Python", "JavaScript", "C++", "Go", "Rust", "Java", "SQL"]
        for form in CODE_FORMS:
            for task in CODE_TASKS:
                for lang in langs:
                    out.append(form.format(lang=lang, task=task))
        for e in CODE_ERRORS:
            out.append(f"My code throws {e}. How do I fix it?")
            out.append(f"Getting this error: {e}")
            out.append(f"How do I resolve this: {e}?")
        for snip in CODE_SNIPPETS:
            for lang in langs:
                out.append(f"Explain what this {lang} line does: {snip}")
                out.append(f"What does this {lang} code do? {snip}")
        out.extend(CODE_MISC)
    elif cls == "image":
        for act in IMG_ACTS:
            for style in IMG_STYLES:
                for subj in IMG_SUBJECTS[:12]:
                    out.append(f"{act} {subj} {style}.")
        out.extend(IMG_EDITS)
        while len(out) < PER_CLASS * 3:
            act, style = rng.choice(IMG_ACTS), rng.choice(IMG_STYLES)
            subj = rng.choice(IMG_SUBJECTS)
            out.append(f"{act} {subj} {style}.")
    elif cls == "chat":
        base: list[str] = []
        for op in CHAT_OPENERS:
            for fl in CHAT_FOLLOW:
                base.append(f"{op}, {fl}")
        for f in CHAT_FEEL:
            for fr in CHAT_FEEL_FRAMES:
                base.append(fr.format(f=f))
        for x in CHAT_PREF_THINGS:
            for form in CHAT_PREF_FORMS:
                base.append(form.format(x=x))
        for t in CHAT_TOPICS:
            base.append(f"Let's talk about {t}.")
            base.append(f"Can we chat about {t}?")
            base.append(f"I've been thinking about {t} lately.")
        for st in CHAT_STATEMENTS:
            for form in ["Do you think {s}?", "Is it true that {s}?", "What's your take: {s}?"]:
                base.append(form.format(s=st))
        for thing in CHAT_STORY:
            base.append(f"Tell me a story about {thing}.")
            base.append(f"Tell me a short story about {thing}.")
        base.extend(CHAT_MISC)
        out = [t + s for s in CHAT_SUFFIX for t in base]
    elif cls == "uz":
        return load_uz(rng, PER_CLASS * 2)
    return out


def load_uz(rng: random.Random, n: int) -> list[str]:
    if not UZ_SOURCE.exists():
        raise FileNotFoundError(f"UZ manba topilmadi: {UZ_SOURCE}")
    pool: list[str] = []
    with UZ_SOURCE.open(encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                msgs = obj.get("messages", [])
                text = next((m["content"] for m in msgs if m.get("role") == "user"),
                            msgs[0]["content"] if msgs else "")
            except Exception:
                continue
            text = re.sub(r"\s+", " ", str(text)).strip()
            if 15 <= len(text) <= 400:
                pool.append(text)
    rng.shuffle(pool)
    uniq, seen = [], set()
    for t in pool:
        if t.lower() in seen:
            continue
        seen.add(t.lower())
        uniq.append(t)
        if len(uniq) >= n:
            break
    return uniq


def gen_worker(args: tuple[str, int]) -> tuple[str, list[str]]:
    cls, seed = args
    rng = random.Random(seed)
    texts = class_texts(cls, rng)
    seen: set[str] = set()
    uniq: list[str] = []
    for t in texts:
        key = t.lower()
        if key in seen:
            continue
        seen.add(key)
        uniq.append(t)
    return cls, uniq[:PER_CLASS]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--out-dir", default="data")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    print(f"Dataset generatsiyasi boshlandi (workers={args.workers}, "
          f"har sinf {PER_CLASS})...")
    tasks = [(cls, args.seed + i) for i, cls in enumerate(CLASSES)]
    with Pool(args.workers) as pool:
        results = pool.map(gen_worker, tasks)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    train, evals, stats = [], [], []
    for cls, texts in results:
        rng.shuffle(texts)
        cut = int(PER_CLASS * 0.8)
        for t in texts[:cut]:
            train.append({"text": t, "label": cls, "label_id": CLASSES.index(cls)})
        for t in texts[cut:]:
            evals.append({"text": t, "label": cls, "label_id": CLASSES.index(cls)})
        stats.append((cls, len(texts), cut, len(texts) - cut,
                      sum(len(t) for t in texts) / max(len(texts), 1)))

    rng.shuffle(train)
    rng.shuffle(evals)
    for path, rows in [("router_train.jsonl", train), ("router_eval.jsonl", evals)]:
        with (out_dir / path).open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (out_dir / "label_map.json").write_text(
        json.dumps({c: i for i, c in enumerate(CLASSES)}, indent=1), encoding="utf-8")

    print(f"\n{'sinf':8s} {'jami':>6s} {'train':>6s} {'eval':>6s} {'o`rt.uzunlik':>12s}")
    print("-" * 46)
    for cls, total, tr, ev, avglen in stats:
        print(f"{cls:8s} {total:>6d} {tr:>6d} {ev:>6d} {avglen:>12.0f}")
    print("-" * 46)
    print(f"{'JAMI':8s} {len(train) + len(evals):>6d} {len(train):>6d} {len(evals):>6d}")
    print(f"\nFayllar: {out_dir}/router_train.jsonl, {out_dir}/router_eval.jsonl")


if __name__ == "__main__":
    main()

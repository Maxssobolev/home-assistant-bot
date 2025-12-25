import json
import re
from faker import Faker


fake = Faker("en_US")


ANCHOR_TERMS = [
    # персонажи
    "Darth Vader",
    "Luke Skywalker",
    "Leia Organa",
    "Emperor Palpatine",
    "Obi-Wan Kenobi",
    "Yoda",
    "Han Solo",
    "Chewbacca",
    "R2-D2",
    "C-3PO",

    # технологии и объекты
    "Death Star",
    "Millennium Falcon",
    "Lightsaber",
    "Kyber crystal",

    # организации и понятия
    "The Force",
    "Jedi",
    "Sith",
    "Galactic Empire",
    "Rebel Alliance",
    "Stormtrooper",

    # планеты и события
    "Tatooine",
    "Coruscant",
    "Naboo",
    "Hoth",
    "Endor",
    "Clone Wars",
    "Order 66",
    "Star Destroyer",
    "X-wing",
    "TIE fighter",
]


FIXED_REPLACEMENTS = {
    "The Force": "Synth Flux",
    "Jedi": "Aster Monks",
    "Sith": "Obsidian Order",
    "Lightsaber": "Photon Blade",
    "Kyber crystal": "Prism Core",
    "Galactic Empire": "Helion Dominion",
    "Rebel Alliance": "Nordic Freefront",
    "Stormtrooper": "Ashline Trooper",
    "Death Star": "Void Spindle",
    "Star Destroyer": "Graviton Dreadship",
}


def is_code_like(term: str) -> bool:
    return bool(re.fullmatch(r"[A-Z0-9\-]{2,}", term))


def make_name(term: str) -> str:
    # Роботы и коды оставляем в стиле "ID-формата", но меняем набор символов
    if is_code_like(term) or term in {"R2-D2", "C-3PO"}:
        prefix = fake.random_uppercase_letter() + fake.random_uppercase_letter()
        return f"{prefix}-{fake.random_int(10, 99)}-{fake.random_uppercase_letter()}{fake.random_int(0,9)}"

    # Планеты и объекты: одно слово, "инопланетное"
    if " " not in term and term[0].isupper():
        base = fake.word().capitalize()
        tail = fake.random_uppercase_letter() + fake.random_uppercase_letter()
        return f"{base}{tail}"

    # Персонажи: имя + фамилия
    if any(ch.isalpha() for ch in term) and term[0].isupper():
        return fake.name()

    return fake.word().capitalize()


def build_map() -> dict[str, str]:
    terms_map: dict[str, str] = {}

    for term in ANCHOR_TERMS:
        if term in FIXED_REPLACEMENTS:
            terms_map[term] = FIXED_REPLACEMENTS[term]
        else:
            terms_map[term] = make_name(term)

    # Дополнительно: "Star Wars" как фраза, чтобы убрать явные следы
    terms_map["Star Wars"] = "Ion Sagas"

    return terms_map


def main():
    terms_map = build_map()

    # Проверка на дубликаты значений
    inv = {}
    for k, v in terms_map.items():
        if v in inv:
            raise SystemExit(f"Коллизия: '{k}' и '{inv[v]}' оба заменены на '{v}'")
        inv[v] = k

    out_path = "terms_map.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(terms_map, f, ensure_ascii=False, indent=2)

    print(f"Готово: {out_path} ({len(terms_map)} замен).")


if __name__ == "__main__":
    main()

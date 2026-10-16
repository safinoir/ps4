# Look up anime details using Anime News Network's encyclopedia API.
import time
import textwrap
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from xml.etree import ElementTree as ET


API_URL = "https://cdn.animenewsnetwork.com/encyclopedia/api.xml"


def load_anime(anime_id):
    # ANN returns XML rather than JSON.
    with urlopen(f"{API_URL}?anime={anime_id}", timeout=20) as response:
        root = ET.parse(response).getroot()
    anime = root.find("anime")
    if anime is None:
        raise ValueError("No anime found for that ID.")
    return anime


def get_info(anime, field):
    # Collect matching fields, since an anime can have several genres or themes.
    values = ["".join(item.itertext()).strip()
              for item in anime.findall("info") if item.get("type") == field]
    return ", ".join(value for value in values if value) or "Unavailable"


def show_anime(anime, choice):
    print(f"\n{anime.get('name', 'Unknown title')}")
    if choice in ("1", "3"):
        print(f"Format: {anime.get('type', 'Unavailable')}")
        print(f"Episodes: {get_info(anime, 'Number of episodes')}")
        print(f"Release dates: {get_info(anime, 'Vintage')}")
        print(f"Genres: {get_info(anime, 'Genres')}")
        print(f"Themes: {get_info(anime, 'Themes')}")
        ratings = anime.find("ratings")
        if ratings is not None and ratings.get("weighted_score"):
            score = float(ratings.get("weighted_score"))
            print(f"User rating: {score:.2f}/10 ({ratings.get('nb_votes', '?')} votes)")
    if choice in ("2", "3"):
        print("\nPlot summary:")
        print(textwrap.fill(get_info(anime, "Plot Summary"), width=80))

    print("\nSource: Anime News Network")
    print(f"https://www.animenewsnetwork.com/encyclopedia/anime.php?id={anime.get('id')}")


def main():
    print("Anime lookup (Anime News Network)")
    print("Use the ID from an ANN anime page's URL. Example: 4658 = Jinki:Extend.")
    # Reuse results and space requests to avoid repeatedly fetching the same data.
    cache = {}
    last_request = 0
    try:
        while True:
            answer = input("\nAnime ID (Enter for 4658, or quit): ").strip()
            if answer.lower() in ("quit", "exit"):
                break
            answer = answer or "4658"
            if not answer.isascii() or not answer.isdigit() or int(answer) < 1:
                print("Please enter a positive numeric anime ID.")
                continue
            anime_id = int(answer)

            choice = input("Show 1) overview, 2) plot, 3) both [3]: ").strip() or "3"
            while choice not in ("1", "2", "3"):
                choice = input("Please choose 1, 2, or 3: ").strip()

            try:
                if anime_id not in cache:
                    time.sleep(max(0, 1 - (time.monotonic() - last_request)))
                    last_request = time.monotonic()
                    print("Loading...")
                    cache[anime_id] = load_anime(anime_id)
                show_anime(cache[anime_id], choice)
            except HTTPError as error:
                print(f"ANN returned HTTP {error.code}. Please try again later.")
            except (URLError, TimeoutError):
                print("Could not reach Anime News Network. Please try again.")
            except ET.ParseError:
                print("ANN returned an unexpected response. Please try again later.")
            except ValueError as error:
                print(error)
    except (KeyboardInterrupt, EOFError):
        print()
    print("Goodbye!")


if __name__ == "__main__":
    main()

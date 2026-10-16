"""Show a small anime leaderboard using the free Jikan API."""

import json
import threading
import tkinter as tk
from collections import Counter
from tkinter import messagebox, ttk
from urllib.error import URLError
from urllib.request import urlopen


API_URL = "https://api.jikan.moe/v4/top/anime?limit=15"


def load_anime():
	"""Download the current top anime list from Jikan."""
	with urlopen(API_URL, timeout=20) as response:
		result = json.load(response)
	return result["data"]


def show_anime(anime_list):
	"""Put the anime list and a few quick statistics in the window."""
	for row in table.get_children():
		table.delete(row)

	genres = Counter()
	scores = []
	total_members = 0

	for anime in anime_list:
		anime_genres = [genre["name"] for genre in anime.get("genres", [])]
		genres.update(anime_genres)
		score = anime.get("score")
		if score is not None:
			scores.append(score)
		total_members += anime.get("members") or 0

		table.insert(
			"",
			"end",
			values=(
				anime.get("rank", "-"),
				anime.get("title_english") or anime.get("title", "Unknown"),
				f"{score:.2f}" if score is not None else "N/A",
				f"{(anime.get('members') or 0):,}",
				", ".join(anime_genres[:3]) or "-",
			),
		)

	average_score = sum(scores) / len(scores) if scores else 0
	popular_genre = genres.most_common(1)[0][0] if genres else "N/A"
	summary.config(
		text=(
			f"Showing {len(anime_list)} titles    "
			f"Average score: {average_score:.2f}/10    "
			f"Combined members: {total_members:,}    "
			f"Most common genre: {popular_genre}"
		)
	)
	status.config(text="Updated from Jikan")


def refresh():
	"""Fetch data in the background so the window stays responsive."""
	refresh_button.config(state="disabled")
	status.config(text="Loading anime rankings...")

	def fetch():
		try:
			anime_list = load_anime()
			window.after(0, lambda: show_anime(anime_list))
		except (URLError, TimeoutError, json.JSONDecodeError, KeyError, TypeError) as error:
			window.after(0, lambda error=error: show_error(error))

	def show_error(error):
		status.config(text="Could not load anime rankings")
		messagebox.showerror(
			"Jikan request failed",
			f"Check your internet connection and try again.\n\n{error}",
		)

	threading.Thread(target=fetch, daemon=True).start()
	window.after(100, enable_refresh)


def enable_refresh():
	"""Re-enable refresh after the request completes or fails."""
	if status.cget("text") != "Loading anime rankings...":
		refresh_button.config(state="normal")
	else:
		window.after(100, enable_refresh)


# Build the window and its leaderboard.
window = tk.Tk()
window.title("Anime Top 15 | Jikan")
window.geometry("900x500")
window.minsize(650, 350)

heading = ttk.Frame(window, padding=(18, 16, 18, 8))
heading.pack(fill="x")
ttk.Label(heading, text="Anime Top 15", font=("TkDefaultFont", 18, "bold")).pack(
	side="left"
)
refresh_button = ttk.Button(heading, text="Refresh", command=refresh)
refresh_button.pack(side="right")

summary = ttk.Label(window, text="", padding=(18, 4, 18, 12))
summary.pack(fill="x")

columns = ("rank", "title", "score", "members", "genres")
table = ttk.Treeview(window, columns=columns, show="headings")
for column, label, width in (
	("rank", "Rank", 55),
	("title", "Anime", 300),
	("score", "Score", 75),
	("members", "Members", 110),
	("genres", "Genres", 230),
):
	table.heading(column, text=label)
	table.column(
		column,
		width=width,
		anchor="w" if column in ("title", "genres") else "center",
	)

scrollbar = ttk.Scrollbar(window, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
table.pack(side="left", fill="both", expand=True, padx=(18, 0), pady=4)
scrollbar.pack(side="right", fill="y", padx=(0, 18), pady=4)

status = ttk.Label(window, text="Ready", anchor="w", padding=(18, 10))
status.pack(side="bottom", fill="x")

# Load the leaderboard as soon as the app opens.
refresh()
window.mainloop()

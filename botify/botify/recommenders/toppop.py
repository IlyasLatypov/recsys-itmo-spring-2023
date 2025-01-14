import random
from typing import List

from .sticky_artist import StickyArtist
from .random import Random
from .recommender import Recommender


class TopPop(Recommender):
    def __init__(self, tracks_redis, artists_redis, catalog, top_tracks: List[int]):
        self.random = StickyArtist(tracks_redis, artists_redis, catalog)
        self.top_tracks = top_tracks

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        if self.top_tracks:
            shuffled = list(self.top_tracks)
            random.shuffle(shuffled)
            return shuffled[0]

        return self.random.recommend_next(user, prev_track, prev_track_time)

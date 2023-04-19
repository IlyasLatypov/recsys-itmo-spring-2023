from .random import Random
from.indexed import Indexed
from .sticky_artist import StickyArtist
from .recommender import Recommender
import random


class MyRecommender(Recommender):
    """
    Recommend tracks closest to the previous one.
    Fall back to the random recommender if no
    recommendations found for the track.
    """

    def __init__(self, tracks_redis, artists_redis, recommendations_redis, catalog):
        self.tracks_redis = tracks_redis
        self.recommendations_redis = recommendations_redis
        self.artists_redis = artists_redis
        # self.fallback = StickyArtist(tracks_redis, artists_redis, catalog)
        self.fallback = Indexed(tracks_redis, artists_redis, recommendations_redis, catalog)
        self.catalog = catalog

    # TODO Seminar 5 step 1: Implement contextual recommender based on NN predictions
    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        previous_track = self.tracks_redis.get(prev_track)
        if previous_track is None or prev_track_time <= 0.4:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        previous_track = self.catalog.from_bytes(previous_track)
        recommendations = previous_track.recommendations
        if recommendations is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        shuffled = list(recommendations)
        random.shuffle(shuffled)
        return shuffled[0]

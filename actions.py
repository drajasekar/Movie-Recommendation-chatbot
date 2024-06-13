

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests


class ActionRecommendMovies(Action):
    def name(self) -> Text:
        return "action_recommend_movies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        genre = next(tracker.get_latest_entity_values("genre"), None)

        if not genre:
            response_text = "I'm sorry, I couldn't detect the genre you're looking for."
            dispatcher.utter_message(text=response_text)
            return []

        # Make API request to fetch movie recommendations based on genre
        api_key = 'aea06b0403c2606effa31e9fdb17f495'  # Replace with your TMDb API key

        # Fetch genre ID from TMDb API
        genre_id = self.get_genre_id(genre, api_key)

        if genre_id:
            api_endpoint = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}'
            response = requests.get(api_endpoint)

            if response.status_code == 200:
                movies = response.json().get('results', [])
                if movies:
                    recommended_movies = [movie['title'] for movie in movies]
                    response_text = f"Sure! Here are some {genre} movie recommendations for you: "
                    response_text += ", ".join(recommended_movies)
                else:
                    response_text = "I'm sorry, I couldn't find any recommendations for that genre."
            else:
                response_text = "Oops! Something went wrong while fetching recommendations. Please try again later."
        else:
            response_text = "I'm sorry, I couldn't find that genre in my database."

        dispatcher.utter_message(text=response_text)

        return []

    def get_genre_id(self, genre, api_key):
        genre_endpoint = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}'
        response = requests.get(genre_endpoint)

        if response.status_code == 200:
            genres = response.json().get('genres', [])
            for g in genres:
                if g['name'].lower() == genre.lower():
                    return g['id']
        return None


# class ActionRecommendMovies(Action):
#
#     def name(self) -> Text:
#         return "action_recommend_movies"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         genre = next(tracker.get_latest_entity_values("genre"), None)
#
#         if genre == "action":
#             recommend_movies = ["Inception", "The Dark Knight", "John Wick"]
#         elif genre == "comedy":
#             recommend_movies = ["The Hangover", "Superbad", "XYZ"]
#
#         elif genre == "horror":
#             recommend_movies = ["The Conjuring", "Get Out", "A Quiet Place"]
#         else:
#             recommend_movies = []
#
#         if recommend_movies:
#             response = f"Sure, There are some {genre} movie recommendation for you: " + ", ".join(recommend_movies)
#         else:
#             response = "Iam sorry, I don''t have any recommendations for that genre"
#
#         dispatcher.utter_message(text=response)
#
#         return []




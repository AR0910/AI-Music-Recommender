import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load dataset
data = pd.read_csv(r"C:\Users\Krishika Garg\Desktop\MIT\Sem 6\WEB DEV\project\music_recommender\music_recommender\music\recommender\data.csv")

# Selecting only numerical columns for clustering
X = data.select_dtypes(include=np.number)

# Drop rows with missing values in numerical columns
data = data.dropna(subset=X.columns)

# Fit KMeans with a pipeline to standardize and cluster
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('kmeans', KMeans(n_clusters=20, random_state=42))
])
pipeline.fit(X)

# Assign clusters
data['cluster_label'] = pipeline.named_steps['kmeans'].predict(X)

def get_recommendations(song_name, artist=None, n=5):
    try:
        print(f"Looking for song: {song_name}, Artist: {artist}")

        # Matching song name and artist (exact match)
        if artist:
            song = data[(data['name'] == song_name) & 
                        (data['artists'].str.contains(artist, case=False))]
        else:
            song = data[data['name'] == song_name]

        # Debug: Check if song is found
        if song.empty:
            return [{"error": "Song not found"}]

        # Debug: Print song details
        print(f"Song found: {song.iloc[0]['name']} by {song.iloc[0]['artists']}")

        # Extract the song and cluster it belongs to
        song = song.iloc[0]
        cluster = song['cluster_label']
        features = song[X.columns]

        # Get all songs in the same cluster
        cluster_songs = data[data['cluster_label'] == cluster].copy()

        # Calculate distance from the selected song to others in the same cluster
        cluster_songs['distance'] = cluster_songs[X.columns].apply(
            lambda row: np.linalg.norm(row.values - features.values), axis=1
        )

        # Debug: Check the distances
        print(f"Distances for cluster {cluster}: {cluster_songs[['name', 'distance']].head()}")

        # Exclude the original song from recommendations and sort by distance
        recommendations = cluster_songs[cluster_songs['name'] != song_name].sort_values('distance')[:n]

        # If no recommendations found, return a message
        if recommendations.empty:
            return [{"error": "No recommendations found"}]

        # Return a list of dictionaries with recommended songs' name, artists, and distance
        return recommendations[['name', 'artists', 'distance']].to_dict(orient='records')
    
    except Exception as e:
        return [{"error": str(e)}]

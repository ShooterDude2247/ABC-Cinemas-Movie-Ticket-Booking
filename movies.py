# ABC CINEMAS - Movies Module
# =============================
# Handles movie browsing, details, and admin management

from database import Database

class Movies:
    """
    Movies class for handling movie-related operations.
    """
    
    @staticmethod
    def get_all_movies():
        """
        Get all active movies from database.
        
        Returns:
            list: List of movie dictionaries
        """
        query = """
            SELECT movie_id, title, genre, language, duration, rating, 
                   description, poster_path
            FROM movies
            WHERE status = 'active'
            ORDER BY title
        """
        return Database.execute_query(query, fetch_all=True, dictionary=True)
    
    @staticmethod
    def get_movie_by_id(movie_id):
        """
        Get a specific movie by ID.
        
        Args:
            movie_id (int): Movie ID
        
        Returns:
            dict: Movie details or None
        """
        query = """
            SELECT movie_id, title, genre, language, duration, rating,
                   description, poster_path
            FROM movies
            WHERE movie_id = %s AND status = 'active'
        """
        return Database.execute_query(query, (movie_id,), fetch_one=True, dictionary=True)
    
    @staticmethod
    def search_movies(search_term):
        """
        Search movies by title.
        
        Args:
            search_term (str): Search query
        
        Returns:
            list: List of matching movies
        """
        query = """
            SELECT movie_id, title, genre, language, duration, rating,
                   description, poster_path
            FROM movies
            WHERE status = 'active' AND title LIKE %s
            ORDER BY title
        """
        return Database.execute_query(
            query,
            (f"%{search_term}%",),
            fetch_all=True,
            dictionary=True
        )
    
    @staticmethod
    def filter_movies(genre=None, language=None, rating=None):
        """
        Filter movies by genre, language, or rating.
        
        Args:
            genre (str): Genre filter
            language (str): Language filter
            rating (str): Rating filter
        
        Returns:
            list: Filtered movies
        """
        query = "SELECT movie_id, title, genre, language, duration, rating, description, poster_path FROM movies WHERE status = 'active'"
        params = []
        
        if genre:
            query += " AND genre LIKE %s"
            params.append(f"%{genre}%")
        
        if language:
            query += " AND language = %s"
            params.append(language)
        
        if rating:
            query += " AND rating = %s"
            params.append(rating)
        
        query += " ORDER BY title"
        
        if params:
            return Database.execute_query(query, tuple(params), fetch_all=True, dictionary=True)
        else:
            return Database.execute_query(query, fetch_all=True, dictionary=True)
    
    @staticmethod
    def add_movie(title, genre, language, duration, rating, description, poster_path):
        """
        Add a new movie (Admin function).
        
        Args:
            title (str): Movie title
            genre (str): Genre
            language (str): Language
            duration (int): Duration in minutes
            rating (str): Rating (U, UA, A, S)
            description (str): Description
            poster_path (str): Path to poster image
        
        Returns:
            tuple: (success: bool, movie_id: int or message: str)
        """
        if not title or not genre or not language or not duration or not rating:
            return False, "All fields are required."
        
        try:
            duration = int(duration)
            if duration <= 0:
                return False, "Duration must be greater than 0."
        except ValueError:
            return False, "Duration must be a number."
        
        query = """
            INSERT INTO movies (title, genre, language, duration, rating, description, poster_path, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'active')
        """
        movie_id = Database.insert_data(
            query,
            (title, genre, language, duration, rating, description, poster_path)
        )
        
        if movie_id > 0:
            return True, movie_id
        else:
            return False, "Failed to add movie."
    
    @staticmethod
    def update_movie(movie_id, title, genre, language, duration, rating, description, poster_path):
        """
        Update movie details (Admin function).
        
        Args:
            movie_id (int): Movie ID
            title (str): Movie title
            genre (str): Genre
            language (str): Language
            duration (int): Duration in minutes
            rating (str): Rating
            description (str): Description
            poster_path (str): Poster path
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not title or not genre or not language or not duration or not rating:
            return False, "All fields are required."
        
        try:
            duration = int(duration)
            if duration <= 0:
                return False, "Duration must be greater than 0."
        except ValueError:
            return False, "Duration must be a number."
        
        query = """
            UPDATE movies
            SET title = %s, genre = %s, language = %s, duration = %s,
                rating = %s, description = %s, poster_path = %s
            WHERE movie_id = %s
        """
        rows = Database.update_data(
            query,
            (title, genre, language, duration, rating, description, poster_path, movie_id)
        )
        
        if rows > 0:
            return True, "Movie updated successfully."
        else:
            return False, "Failed to update movie."
    
    @staticmethod
    def delete_movie(movie_id):
        """
        Delete a movie (Admin function).
        
        Args:
            movie_id (int): Movie ID
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Check if movie has any bookings
        query = "SELECT COUNT(*) as count FROM bookings b JOIN shows s ON b.show_id = s.show_id WHERE s.movie_id = %s"
        result = Database.execute_query(query, (movie_id,), fetch_one=True, dictionary=True)
        
        if result and result['count'] > 0:
            return False, "Cannot delete movie with existing bookings."
        
        # Soft delete by marking as inactive
        query = "UPDATE movies SET status = 'inactive' WHERE movie_id = %s"
        rows = Database.update_data(query, (movie_id,))
        
        if rows > 0:
            return True, "Movie deleted successfully."
        else:
            return False, "Failed to delete movie."
    
    @staticmethod
    def get_genres():
        """
        Get all unique genres.
        
        Returns:
            list: List of genres
        """
        query = "SELECT DISTINCT genre FROM movies WHERE status = 'active' ORDER BY genre"
        results = Database.execute_query(query, fetch_all=True, dictionary=True)
        return [r['genre'] for r in results] if results else []
    
    @staticmethod
    def get_languages():
        """
        Get all unique languages.
        
        Returns:
            list: List of languages
        """
        query = "SELECT DISTINCT language FROM movies WHERE status = 'active' ORDER BY language"
        results = Database.execute_query(query, fetch_all=True, dictionary=True)
        return [r['language'] for r in results] if results else []
    
    @staticmethod
    def get_ratings():
        """
        Get all unique ratings.
        
        Returns:
            list: List of ratings
        """
        query = "SELECT DISTINCT rating FROM movies WHERE status = 'active' ORDER BY rating"
        results = Database.execute_query(query, fetch_all=True, dictionary=True)
        return [r['rating'] for r in results] if results else []

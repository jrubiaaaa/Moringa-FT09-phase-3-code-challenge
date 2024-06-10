from database.setup import get_db_connection


class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.name}>"

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError("Author id must be an integer.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Author name must be a string and more than 0 characters.")

    @classmethod
    def create(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return cls(author_id, name)

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """,
            (self.id,),
        )
        magazines = cursor.fetchall()
        conn.close()
        return magazines

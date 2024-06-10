from database.setup import get_db_connection


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.title}>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and 5 <= len(title) <= 50:
            self._title = title

    @classmethod
    def create(cls, author_id, magazine_id, title, content):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (author_id, magazine_id, title, content) VALUES (?, ?, ?, ?)",
            (author_id, magazine_id, title, content),
        )
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return cls(article_id, title, content, author_id, magazine_id)

    def __str__(self):
        return f"Article(ID: {self._id}, Title: {self._title}, Author ID: {self._author_id}, Magazine ID: {self._magazine_id})"

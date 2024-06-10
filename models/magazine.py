from database.setup import get_db_connection


class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.name}>"

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError("Magazine id must be an integer.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and 2 <= len(name) <= 16:
            self._name = name
        else:
            raise ValueError(
                "Name must be a string and berween 2 to 16 characters long."
            )

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if isinstance(category, str) and len(category):
            self._category = category
        else:
            raise ValueError(
                "Category must be a string and longer than 0 characters long."
            )

    @classmethod
    def create(cls, name, category):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category)
        )
        conn.commit()
        magazine_id = cursor.lastrowid
        conn.close()
        return cls(magazine_id, name, category)

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """,
            (self.id,),
        )
        contributors = cursor.fetchall()
        conn.close()
        return contributors

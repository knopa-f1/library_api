from app.db.models import Author
from app.repositories.base_repository import Repository


class AuthorRepository(Repository):
    model = Author

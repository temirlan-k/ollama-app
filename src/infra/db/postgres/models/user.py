import sqlalchemy as sa
import sqlalchemy.orm as so

from infra.db.postgres.models import Base, TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id = so.mapped_column(sa.Integer, primary_key=True, index=True)
    email = so.mapped_column(sa.String, unique=True, index=True, nullable=False)
    hashed_password = so.mapped_column(sa.String, nullable=False)

    requests = so.relationship("Request", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"

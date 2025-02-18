import sqlalchemy as sa
import sqlalchemy.orm as so

from infra.db.postgres.models import Base, TimeStampMixin


class Request(Base, TimeStampMixin):
    __tablename__ = "requests"

    id = so.mapped_column(sa.Integer, primary_key=True, index=True)
    user_id = so.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    input_text = so.mapped_column(sa.String, nullable=False)
    response_text = so.mapped_column(sa.String, nullable=False)

    user = so.relationship("User", back_populates="requests")

    def __repr__(self):
        return f"<Request by {self.user_id}>"

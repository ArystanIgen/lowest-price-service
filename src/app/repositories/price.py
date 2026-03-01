from app.models import PriceModel
from app.repositories.base import BaseRepository
from app.schemas.price import PriceUpdate, PriceCreate


class PriceRepository(
    BaseRepository[PriceModel, PriceCreate, PriceUpdate]
):
    model = PriceModel

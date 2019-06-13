"""
author songjie
"""
from app.modules.helper_config import HelperConfig
from app.services.handle_insomnia_music_service import HandleInsomniaMusicService


class Helper(HelperConfig):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def handle_insomnia_music(self):
        return HandleInsomniaMusicService(self.db, self.init_db)

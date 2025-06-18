from django.conf import settings
from meta.models import ModelMeta


class BaseModelMeta(ModelMeta):
    _metadata_project = {
        "title": settings.PROJECT_NAME,
        "description": settings.PROJECT_DESCRIPTION,
        "locale": "ru_RU",
        "image": settings.STATIC_URL + "img/logo.png",
    }

    def get_meta(self, request=None):
        """
        Retrieve the meta data configuration
        """
        metadata = super().get_meta(request)
        metadata.update({x: y for x, y in self._metadata_project.items() if not metadata.get(x)})
        return metadata

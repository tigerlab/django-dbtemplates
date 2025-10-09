import importlib.metadata

try:
    __version__ = importlib.metadata.version("django-dbtemplates")
except importlib.metadata.PackageNotFoundError:
    # package is not installed
    __version__ = None


default_app_config = 'dbtemplates.apps.DBTemplatesConfig'

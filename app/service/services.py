from libcloud.storage.providers import get_driver
from libcloud.storage.types import Provider
from .config_storage import get_storage_config

class StorageService:
    """
    StorageService encapsulates a single provider's driver and container.
    Once initialized with a provider, it cannot be changed.
    """

    def __init__(self, provider_name):
        self.provider_name = provider_name
        STORAGE_CONFIG = get_storage_config()
        self.config = STORAGE_CONFIG[provider_name]
        provider_type = getattr(Provider, self.config['type'].upper())
        driver_cls = get_driver(provider_type)
        self.driver = driver_cls(
            key=self.config['key'], 
            secret=self.config['secret'], 
            region=self.config.get('region')
        )
        # TODO: Test for all cloud providers. 
        self.container = self.driver.get_container(self.config['bucket'])

    def upload_file(self, file_name, file_data):
        obj = self.driver.upload_object_via_stream(
            iterator=iter([file_data]),
            container=self.container,
            object_name=file_name
        )
        print(f"Filename: {obj.name} successfully uploaded")
        return obj

    def delete_file(self, file_name):
        obj = self.container.get_object(file_name)
        self.driver.delete_object(obj)
        print(f"File successfully deleted")

    def get_file(self, file_name):
        obj = self.container.get_object(file_name)
        stream = self.driver.download_object_as_stream(obj)
        return b"".join(stream) 
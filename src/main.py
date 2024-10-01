print("APP")
from dependency_injection import ServiceCollection

collection = ServiceCollection()

provider = collection.build_service_provider()

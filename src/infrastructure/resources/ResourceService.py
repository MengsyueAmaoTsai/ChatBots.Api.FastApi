import httpx

from .contracts.users import UserDetailsResponse, UserResponse


class ResourceService:
    BASE_ADDRESS = "https://localhost:10000"

    async def list_users(self) -> list[UserResponse]:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{self.BASE_ADDRESS}/api/v1/users")
            response.raise_for_status()
            return [UserResponse(**user) for user in response.json()]

    async def get_user(self, id: str) -> UserDetailsResponse:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{self.BASE_ADDRESS}/api/v1/users/{id}")
            response.raise_for_status()
            return UserDetailsResponse(**response.json())

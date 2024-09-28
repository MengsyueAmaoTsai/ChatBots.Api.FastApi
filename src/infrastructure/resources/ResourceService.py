import httpx

from shared_kernel import Error, ErrorType, ResultT

from .contracts.users import UserDetailsResponse, UserResponse


class ResourceService:
    BASE_ADDRESS = "https://localhost:10000"

    async def get_user(self, id: str) -> ResultT[UserDetailsResponse]:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{self.BASE_ADDRESS}/api/v1/users/{id}")

            if response.status_code >= 400:
                return ResultT[UserDetailsResponse].failure(self._map_response_error(response))

            return ResultT[UserDetailsResponse].success(UserDetailsResponse(**response.json()))

    async def list_users(self) -> ResultT[list[UserResponse]]:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{self.BASE_ADDRESS}/api/v1/users")

            if response.status_code >= 400:
                return ResultT[list[UserResponse]].failure(self._map_response_error(response))

            return ResultT[list[UserResponse]].success([UserResponse(**user) for user in response.json()])

    def _map_response_error(self, response: httpx.Response) -> Error:
        match response.status_code:
            case 400:
                error_type = ErrorType.Validation
            case 401:
                error_type = ErrorType.Unauthorized
            case 403:
                error_type = ErrorType.Forbidden
            case 404:
                error_type = ErrorType.NotFound
            case 409:
                error_type = ErrorType.Conflict
            case 500:
                error_type = ErrorType.Unexpected
            case 503:
                error_type = ErrorType.Unavailable
            case _:
                error_type = ErrorType.Unexpected

        return Error.create(error_type, error_type.name, response.text)

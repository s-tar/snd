import inspect
import json
from typing import Callable
from fastapi.routing import APIRoute
from pydantic.main import ModelMetaclass
from starlette.datastructures import FormData
from starlette.requests import Request
from starlette.responses import Response


class JsonMultipartFormRequest(Request):
    async def form(self) -> bytes:
        if not hasattr(self, "_form_data"):
            endpoint = self.scope["endpoint"]
            signature = inspect.signature(endpoint)
            parameters = signature.parameters
            form_data_dict = {}
            form_data = await super().form()

            for name, value in form_data.items():
                field = parameters.get(name)
                if field and isinstance(field.annotation, ModelMetaclass):
                    form_data_dict[name] = json.loads(value)
                else:
                    form_data_dict[name] = value

            self._form_data = FormData(form_data_dict)

        return self._form_data


class JsonMultipartFormRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = JsonMultipartFormRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

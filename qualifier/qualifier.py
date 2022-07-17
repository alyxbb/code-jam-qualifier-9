import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    scope: typing.Mapping[str, typing.Any]

    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]


class RestaurantManager:
    def __init__(self):


        self.staff = {}

    async def __call__(self, request: Request):
        """Handle a request received.

        This is called for each request received by your application.
        In here is where most of the code for your system should go.

        :param request: request object
            Request object containing information about the sent
            request to your application.
        """
        match request.scope["type"]:
            case "staff.onduty":
                self.staff[request.scope["id"]] = request
            case "staff.offduty":
                self.staff.pop(request.scope["id"])
            case "order":
                staffkeys=list(self.staff.keys())
                found=self.staff[staffkeys[0]]
                full_order= await request.receive()
                await found.send(full_order)
                result=await found.receive()
                await request.send(result)

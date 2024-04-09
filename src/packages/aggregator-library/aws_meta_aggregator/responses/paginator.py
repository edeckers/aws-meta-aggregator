from typing import Any, Callable, Iterator


class Paginator:  # pylint: disable=too-few-public-methods
    __pager: Callable[[str | None], dict[str, Any]]

    def __init__(
        self,
        pager: Callable[[str | None], dict[str, Any]],
        token_key: str = "PaginationToken",
    ) -> None:
        self.__pager = pager
        self.__token_key = token_key

    def page(self) -> Iterator[dict[str, Any]]:
        maybe_token: str | None = None

        while True:
            response = self.__pager(maybe_token)

            yield response

            if (not self.__token_key in response) or (not response[self.__token_key]):
                break

            maybe_token = response[self.__token_key]

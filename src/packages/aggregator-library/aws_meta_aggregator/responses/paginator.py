from abc import ABC, abstractmethod
from typing import Any, Callable, Iterator


class Pageable(ABC):  # pylint: disable=too-few-public-methods
    @abstractmethod
    def __call__(
        self,
        PaginationToken: str,  # pylint: disable=invalid-name
        ResourcesPerPage: int = 100,  # pylint: disable=invalid-name
        IncludeComplianceDetails: bool = False,  # pylint: disable=invalid-name
        ExcludeCompliantResources: bool = False,  # pylint: disable=invalid-name
    ) -> dict[str, Any]:
        pass


class Paginator:  # pylint: disable=too-few-public-methods
    __pager: Callable[[str], dict[str, Any]]

    def __init__(
        self,
        pager: Pageable,
        resources_per_page: int = 100,  # pylint: disable=invalid-name
        include_compliance_details: bool = False,  # pylint: disable=invalid-name
        exclude_compliant_resources: bool = False,  # pylint: disable=invalid-name
    ) -> None:
        self.__pager = lambda token: pager(
            PaginationToken=token,
            ResourcesPerPage=resources_per_page,
            IncludeComplianceDetails=include_compliance_details,
            ExcludeCompliantResources=exclude_compliant_resources,
        )

    def page(self) -> Iterator[dict[str, Any]]:
        token = None

        while True:
            response = self.__pager(
                token or "",
            )

            yield response

            if (not "PaginationToken" in response) or (not response["PaginationToken"]):
                break

            token = response["PaginationToken"]

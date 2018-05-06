from Peekdata.DataGatewayAPI.Model import *

__author__ = 'Vaidotas Senkus'
__email__ = 'vaidas100@gmail.com'


def getTwoDimensionsTwoMetricsFilterAndSorting():

    request = GetDataRequest()

    request.scopeName = "Mortgage-Lending"

    request.dimensions = []
    request.dimensions.append(
        "propertyCityID"
    )
    request.dimensions.append(
        "currency"
    )

    request.metrics = TypedList(type(MetricDto()))
    request.metrics.append(
        MetricDto("loanamount")
    )
    request.metrics.append(
        MetricDto("totalincome")
    )

    request.filters = FilterDto()
    request.filters.singleKeys = TypedList(type(SingleKeyFilterDto()))
    request.filters.singleKeys.append(
        SingleKeyFilterDto(
            "currency",
            Operation.EQUALS,
            ["EUR"]
        )
    )

    request.sortings = SortDto()
    request.sortings.dimensions = TypedList(type(DimensionSortKeyDto()))
    request.sortings.dimensions.append(
        DimensionSortKeyDto("currency", SortDirection.ASC)
    )

    return request


def getTwoMetricsAndTwoFilterFromSpecifiedGraph():

    request = GetDataRequest()

    request.scopeName = "Mortgage-Lending"
    request.graphName = "Origination-MySQL"  # can be "DataWarehouse-HPVertica" or "Servicing-PostgreSQL"

    request.metrics = TypedList(type(MetricDto()))
    request.metrics.append(
        MetricDto("loanamount")
    )
    request.metrics.append(
        MetricDto("waintrate")
    )

    request.filters = FilterDto()
    request.filters.dateRanges = TypedList(type(DateRangeFilterDto()))
    request.filters.dateRanges.append(
        DateRangeFilterDto("closingdate", "2017-01-01", "2017-12-31")
    )
    request.filters.singleKeys = TypedList(type(SingleKeyFilterDto()))
    request.filters.singleKeys.append(
        SingleKeyFilterDto("officerid", Operation.EQUALS, ["1", "2", "3"])
    )

    return request

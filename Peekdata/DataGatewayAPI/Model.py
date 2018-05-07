"""
Model for Peekdata DataGateway API Requests
"""

from enum import Enum
import datetime
import json
import re
import uuid

__author__ = 'Vaidotas Senkus'
__email__ = 'vaidas100@gmail.com'


def serialize_to_json(data):
    """
    method to serialize Python object to JSON
    """
    serialized = json.dumps(
        data,
        cls=ExtendedJsonEncoder,
        indent=4,
        sort_keys=True,
    )
    return serialized


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    json.JSONEncoder extension
    for by default unsupported object types
    """
    def default(self, o):

        if isinstance(o, datetime.datetime):
            return o.replace(microsecond=0).isoformat()

        if isinstance(o, Enum):
            return o.name

        try:
            return o.__dict__
        except:
            pass


def string_to_datetime(string):
    """
    method to convert string to datetime object

    >>> string_to_datetime('19760518T235900+0500').isoformat()
    '1976-05-18T23:59:00+05:00'
    >>> string_to_datetime('19760518T235900Z').isoformat()
    '1976-05-18T23:59:00'
    >>> string_to_datetime('1976-05-18T23:59:00').isoformat()
    '1976-05-18T23:59:00'
    >>> string_to_datetime('19760518T235900').isoformat()
    '1976-05-18T23:59:00'
    >>> string_to_datetime('1976-05-18').isoformat()
    '1976-05-18T00:00:00'
    >>> string_to_datetime('19760518').isoformat()
    '1976-05-18T00:00:00'
    """

    datetime_formats = {
        # datetime example       format
        '19760518T235900+0500':  '%Y%m%dT%H%M%S%z',
        '19760518T235900Z':      '%Y%m%dT%H%M%SZ',
        '1976-05-18T23:59:00':   '%Y-%m-%dT%H:%M:%S',
        '19760518T235900':       '%Y%m%dT%H%M%S',
        '1976-05-18':            '%Y-%m-%d',
        '19760518':              '%Y%m%d',
    }

    m = re.match(r'^(\d{4})-?(\d{2})-?(\d{2})', string)
    if m:
        if int(m.group(1)) in range(1970, datetime.datetime.now().year + 1):
            if int(m.group(2)) in range(1, 13):
                if int(m.group(3)) in range(1, 32):

                    for datetime_format in datetime_formats.values():
                        try:
                            return datetime.datetime.strptime(string, datetime_format)
                        except:
                            pass

    raise ValueError(
        "\n  Unsupported datetime format.\n  Please use:\n    %s"
        % "\n    ".join(datetime_formats.keys())
    )


class TypedList(list):
    """
    Python's list with elements of particular type
    """
    def __init__(self, type):
        super().__init__()
        self.type = type

    def append(self, item):
        if not isinstance(item, self.type):
            raise TypeError('list item is not of type %s' % self.type)
        super(TypedList, self).append(item)


class SortDirection(Enum):
    """
    SortDirection.ASC

    >>> serialize_to_json(SortDirection.DESC)
    '"DESC"'
    """

    ASC, \
    DESC = range(2)

    def __str__(self):
        return self._name_


class FilterDataType(Enum):
    """
    FilterDataType.NUMBER

    >>> serialize_to_json(FilterDataType.NUMBER)
    '"NUMBER"'
    """

    NUMBER, \
    DATE, \
    STRING = range(3)

    def __str__(self):
        return self._name_


class Operation(Enum):
    """
    Operation.EQUALS

    >>> serialize_to_json(Operation.EQUALS)
    '"EQUALS"'
    """

    EQUALS, \
    NOT_EQUALS, \
    STARTS_WITH, \
    NOT_STARTS_WITH, \
    ALL_IS_LESS, \
    ALL_IS_MORE, \
    AT_LEAST_ONE_IS_LESS, \
    AT_LEAST_ONE_IS_MORE = range(8)

    def __str__(self):
        return self._name_


class DateRangeFilterDto:
    """
    DateRangeFilterDto()
    DateRangeFilterDto(String from, String to)
    DateRangeFilterDto(String key, String from, String to)

    >>> DateRangeFilterDto('19760518', '19760519').datetime_from
    datetime.datetime(1976, 5, 18, 0, 0)
    >>> DateRangeFilterDto('19760518', '19760519').datetime_to
    datetime.datetime(1976, 5, 19, 0, 0)
    >>> DateRangeFilterDto('key', '19760518', '19760519').key
    'key'
    >>> DateRangeFilterDto('key', '19760518', '19760519').datetime_from
    datetime.datetime(1976, 5, 18, 0, 0)
    >>> DateRangeFilterDto('key', '19760518', '19760519').datetime_to
    datetime.datetime(1976, 5, 19, 0, 0)
    """

    key = ''
    datetime_from = ''
    datetime_to = ''

    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 2:
            self.datetime_from = string_to_datetime(args[0])
            self.datetime_to   = string_to_datetime(args[1])
        elif len(args) == 3:
            self.key =   args[0]
            self.datetime_from = string_to_datetime(args[1])
            self.datetime_to   = string_to_datetime(args[2])
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))


class DimensionSortKeyDto:
    """
    DimensionSortKeyDto()
    DimensionSortKeyDto(String dimension)
    DimensionSortKeyDto(String dimension, SortDirection direction)

    >>> DimensionSortKeyDto('dimension').dimension
    'dimension'
    >>> DimensionSortKeyDto('dimension', SortDirection.DESC).direction
    <SortDirection.DESC: 1>
    """

    dimension = ''
    direction = SortDirection.ASC

    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 1:
            self.dimension = args[0]
        elif len(args) == 2:
            self.dimension = args[0]
            self.direction = args[1]
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))


class MetricDto:
    """
    MetricDto()
    MetricDto(String metric)
    .AddParameter(String name, String value)

    >>> m = MetricDto('abc'); m.metric
    'abc'
    >>> m = MetricDto(); m.AddParameter('a', 'b'); m.parameters
    {'a': 'b'}
    """

    metric = ''
    parameters = {}

    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 1:
            self.metric = args[0]
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))

    def AddParameter(self, name: str, value: str):
        self.parameters[name] = value


class MetricSortKeyDto:
    """
    MetricSortKeyDto()
    MetricSortKeyDto(MetricDto metric, SortDirection direction)

    >>> MetricSortKeyDto(MetricDto('abc'), SortDirection.DESC).metric.metric
    'abc'
    >>> MetricSortKeyDto(MetricDto('abc'), SortDirection.DESC).direction
    <SortDirection.DESC: 1>
    """

    metric = MetricDto()
    direction = SortDirection.ASC

    def __init__(self, metric=MetricDto(), direction=SortDirection.ASC):
        self.metric = metric
        self.direction = direction


class SortDto:
    """
    SortDto()
    """
    dimensions = TypedList(type(DimensionSortKeyDto()))
    metric = MetricSortKeyDto()


class SimpleFilterDto:
    """
    SimpleFilterDto()
    """
    key = ''
    isMetric = False
    values = []

    def __init__(self):
        self.type = FilterDataType()


class SingleKeyFilterDto:
    """
    SingleKeyFilterDto()
    SingleKeyFilterDto(String key, Operation operation, String[] values)

    >>> SingleKeyFilterDto().operation
    <Operation.EQUALS: 0>
    >>> SingleKeyFilterDto('key', Operation.EQUALS, ['a', 'b']).values
    ['a', 'b']
    """
    def __init__(self, *args):
        if len(args) == 0:
            self.key = ''
            self.operation = Operation.EQUALS
            self.values = []
        elif len(args) == 3:
            self.key       = args[0]
            self.operation = args[1]
            self.values    = args[2]
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))


class FilterDto:
    """
    FilterDto()

    >>> f = FilterDto(); f.dateRanges.append(DateRangeFilterDto('19760518','19760519')); f.dateRanges[0].datetime_to
    datetime.datetime(1976, 5, 19, 0, 0)
    """

    dateRanges = TypedList(type(DateRangeFilterDto()))
    singleKeys = TypedList(type(SingleKeyFilterDto()))


class ReportDataDto:
    """
    ReportDataDto()
    """
    columnHeaders = []
    rows = []


class GetDataRequest:
    """
    GetDataRequest()
    GetDataRequest(String requestID, Map<String, String> consumerInfo)
    .getRequestID()
    .setRequestID(String value)
    """
    requestID = ''
    consumerInfo = {}
    scopeName = ''
    graphName = ''
    dimensions = []
    metrics = TypedList(type(MetricDto()))
    filters = FilterDto()
    sortings = SortDto()

    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 2:
            self.requestID    = args[0]
            self.consumerInfo = args[1]
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))

    def getRequestID(self):
        if self.requestID == '':
            self.requestID = str(uuid.uuid1())
        return self.requestID

    def setRequestID(self, value: str):
        self.requestID = value


class GetDataResponse:
    """
    GetDataResponse(String requestID)
    GetDataResponse(String requestID, ReportDataDto reportData, int totalRows)
    """
    requestID = ''
    reportData = ReportDataDto()
    totalRows = 0

    def __init__(self, *args):
        if len(args) == 1:
            self.requestID = args[0]
        elif len(args) == 3:
            self.requestID =  args[0]
            self.reportData = args[1]
            self.totalRows =  args[2]
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))

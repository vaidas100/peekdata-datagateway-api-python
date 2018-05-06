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
        cls=serialize_to_json_encoder,
        indent=4,
        sort_keys=True,
    )
    serialized = serialized.replace('"from_":', '"from":')
    return serialized


class serialize_to_json_encoder(json.JSONEncoder):
    """
    json.JSONEncoder extension for
    unsupported object types
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

    >>> string_to_datetime('1976-05-18T23:59:00').isoformat()
    '1976-05-18T23:59:00'
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
        # datetime example           format
        '1976-05-18T23:59:00+05:00': '%Y-%m-%dT%H:%M:%S',
        '19760518T235900+0500':      '%Y%m%dT%H%M%S%z',
        '19760518T235900Z':          '%Y%m%dT%H%M%SZ',
        '1976-05-18T23:59:00':       '%Y-%m-%dT%H:%M:%S',
        '19760518T235900':           '%Y%m%dT%H%M%S',
        '1976-05-18':                '%Y-%m-%d',
        '19760518':                  '%Y%m%d',
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


# public enum SortDirection {
#     ASC,
#     DESC;
# }
class SortDirection(Enum):
    """
    >>> str(SortDirection.DESC)
    'DESC'
    >>> serialize_to_json(SortDirection.DESC)
    '"DESC"'
    """

    ASC, \
    DESC = range(2)

    def __str__(self):
        return self._name_


# public enum FilterDataType {
#     NUMBER,
#     DATE,
#     STRING
# }
class FilterDataType(Enum):
    """
    >>> str(FilterDataType.NUMBER)
    'NUMBER'
    >>> serialize_to_json(FilterDataType.NUMBER)
    '"NUMBER"'
    """

    NUMBER, \
    DATE, \
    STRING = range(3)

    def __str__(self):
        return self._name_


# public enum Operation {
#     EQUALS,
#     NOT_EQUALS,
#     STARTS_WITH,
#     NOT_STARTS_WITH,
#     ALL_IS_LESS,
#     ALL_IS_MORE,
#     AT_LEAST_ONE_IS_LESS,
#     AT_LEAST_ONE_IS_MORE
# }
class Operation(Enum):
    """
    >>> str(Operation.EQUALS)
    'EQUALS'
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


# public class DateRangeFilterDto {
#     public String key;
#     public String from;
#     public String to;
#
#     public DateRangeFilterDto() {
#     }
#
#     public DateRangeFilterDto(String from, String to) {
#         this.from = from;
#         this.to = to;
#     }
#
#     public DateRangeFilterDto(String key, String from, String to) {
#         this.key = key;
#         this.from = from;
#         this.to = to;
#     }
# }
class DateRangeFilterDto:
    """
    >>> DateRangeFilterDto().key
    ''
    >>> DateRangeFilterDto('19760518', '19760519').from_
    datetime.datetime(1976, 5, 18, 0, 0)
    >>> DateRangeFilterDto('19760518', '19760519').to
    datetime.datetime(1976, 5, 19, 0, 0)
    >>> DateRangeFilterDto('key', '19760518', '19760519').key
    'key'
    >>> DateRangeFilterDto('key', '19760518', '19760519').from_
    datetime.datetime(1976, 5, 18, 0, 0)
    >>> DateRangeFilterDto('key', '19760518', '19760519').to
    datetime.datetime(1976, 5, 19, 0, 0)
    """

    key = ''
    from_ = ''
    to = ''

    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 2:
            self.from_ = string_to_datetime(args[0])
            self.to =    string_to_datetime(args[1])
        elif len(args) == 3:
            self.key =   args[0]
            self.from_ = string_to_datetime(args[1])
            self.to =    string_to_datetime(args[2])
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))


# public class DimensionSortKeyDto {
#     public String dimension;
#     public SortDirection direction = SortDirection.ASC;
#
#     public DimensionSortKeyDto() {
#     }
#
#     public DimensionSortKeyDto(String dimension) {
#         this(dimension, SortDirection.ASC);
#     }
#
#     public DimensionSortKeyDto(String dimension, SortDirection direction) {
#         this.dimension = dimension;
#         this.direction = direction;
#     }
# }
class DimensionSortKeyDto:
    """
    >>> DimensionSortKeyDto().dimension
    ''
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


# public class MetricDto {
#     public String metric;
#     public Map<String, String> parameters = new HashMap<>();
#
#     public MetricDto() {
#     }
#
#     public MetricDto(String metric) {
#         this.metric = metric;
#     }
#
#     public MetricDto AddParameter(String name, String value) {
#         this.parameters.put(name, value);
#         return this;
#     }
# }
class MetricDto:
    """
    >>> m = MetricDto(); m.metric
    ''
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


# public class MetricSortKeyDto {
#
#     public MetricDto metric;
#     public SortDirection direction = SortDirection.ASC;
#
#     public MetricSortKeyDto(MetricDto metric, SortDirection direction) {
#         this.metric = metric;
#         this.direction = direction;
#     }
# }
class MetricSortKeyDto:
    """
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


# public class SortDto {
#     public DimensionSortKeyDto[] dimensions;
#     public MetricSortKeyDto metric;
# }
class SortDto:
    dimensions = TypedList(type(DimensionSortKeyDto()))
    metric = MetricSortKeyDto()


# public class SimpleFilterDto {
#     public String key;
#     public boolean isMetric = false;
#     public String[] values;
#     public FilterDataType type;
# }
class SimpleFilterDto:
    key = ''
    isMetric = False
    values = []
    # TODO
    # type = FilterDataType()


# public class SingleKeyFilterDto {
#     public String key;
#     public Operation operation;
#     public String[] values;
#
#     public SingleKeyFilterDto() {
#     }
#
#     public SingleKeyFilterDto(String key, Operation operation, String[] values) {
#         this.key = key;
#         this.operation = operation;
#         this.values = values;
#     }
# }
class SingleKeyFilterDto:
    """
    >>> SingleKeyFilterDto().operation
    <Operation.EQUALS: 0>
    >>> SingleKeyFilterDto('key', Operation.EQUALS, ['a', 'b']).values
    ['a', 'b']
    """

    key = ''
    # TODO
    # operation = Operation()
    values = []

    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 3:
            self.key = args[0]
            self.operation = args[1]
            self.values = args[2]
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))


# public class FilterDto {
#     public List<DateRangeFilterDto> dateRanges;
#     public List<SingleKeyFilterDto> singleKeys;
#
#     public FilterDto () {
#     }
# }
class FilterDto:
    """
    >>> f = FilterDto(); f.dateRanges.append(DateRangeFilterDto('19760518','19760519')); f.dateRanges[0].to
    datetime.datetime(1976, 5, 19, 0, 0)
    """

    dateRanges = TypedList(type(DateRangeFilterDto()))
    singleKeys = TypedList(type(SingleKeyFilterDto()))


# public class ReportDataDto {
#     public String[] columnHeaders;
#     public List<Object[]> rows;
#
#     public ReportDataDto() {
#     }
# }
class ReportDataDto:
    columnHeaders = []
    rows = []


# public class GetDataRequest {
#     private String requestID;
#     public Map<String, String> consumerInfo;
#     public String scopeName;
#     public String graphName;
#     public String[] dimensions;
#     public MetricDto[] metrics;
#     public FilterDto filters;
#     public SortDto sortings;
#
#     public GetDataRequest() {
#         this.consumerInfo = new HashMap<>();
#     }
#
#     public GetDataRequest(String requestID, Map<String, String> consumerInfo) {
#         this.requestID = requestID;
#         this.consumerInfo = consumerInfo;
#     }
#
#     public String getRequestID() {
#         if (this.requestID == null)
#             this.requestID = UUID.randomUUID().toString();
#         return this.requestID;
#     }
#
#     public void setRequestID(String value) {
#         this.requestID = value;
#     }
# }
class GetDataRequest:
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
            self.requestID = args[0]
            self.consumerInfo = args[1]
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))

    def getRequestID(self):
        if self.requestID == '':
            self.requestID = str(uuid.uuid1())
        return self.requestID

    def setRequestID(self, value: str):
        self.requestID = value


# public class GetDataResponse  {
#
#     public String requestID;
#     public ReportDataDto reportData;
#     public Integer totalRows;
#
#     public GetDataResponse(String requestID) {
#         this.requestID = requestID;
#     }
#
#     public GetDataResponse(String requestID, ReportDataDto reportData, int totalRows) {
#         this.requestID = requestID;
#         this.reportData = reportData;
#         this.totalRows = totalRows;
#     }
# }
class GetDataResponse:
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

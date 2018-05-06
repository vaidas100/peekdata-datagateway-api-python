from enum import Enum
import datetime
import json
import uuid

__author__ = 'Vaidotas Senkus'
__email__ = 'vaidas100@gmail.com'


def serialize_to_json(data):
    serialized = json.dumps(
        data,
        cls=serialize_to_json_encoder,
        indent=4,
        sort_keys=True,
    )
    serialized = serialized.replace('"from_":', '"from":')
    return serialized


class serialize_to_json_encoder(json.JSONEncoder):
    def default(self, o):

        if isinstance(o, datetime.datetime):
            return o.replace(microsecond=0).isoformat()

        if isinstance(o, Enum):
            return o._name_

        try:
            return o.__dict__
        except:
            pass


class TypedList(list):
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
    >>> DateRangeFilterDto('from', 'to').from_
    'from'
    >>> DateRangeFilterDto('from', 'to').to
    'to'
    >>> DateRangeFilterDto('key', 'from', 'to').key
    'key'
    >>> DateRangeFilterDto('key', 'from', 'to').from_
    'from'
    >>> DateRangeFilterDto('key', 'from', 'to').to
    'to'
    """

    key = ''
    from_ = ''
    to = ''

    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 2:
            self.from_ = args[0]
            self.to = args[1]
        elif len(args) == 3:
            self.key = args[0]
            self.from_ = args[1]
            self.to = args[2]
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
    >>> f = FilterDto(); f.dateRanges.append(DateRangeFilterDto('f','t')); f.dateRanges[0].to
    't'
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
            self.requestID = args[0]
            self.reportData = args[1]
            self.totalRows = args[2]
        else:
            raise ValueError("Bad arguments number for {}".format(self.__class__))

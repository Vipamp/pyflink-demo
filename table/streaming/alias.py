from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, CsvTableSource, CsvTableSink, DataTypes
import os


def alias_streaming():
    s_env = StreamExecutionEnvironment.get_execution_environment()
    s_env.set_parallelism(1)
    st_env = StreamTableEnvironment.create(s_env)
    source_file = os.getcwd() + "/../resources/table_orders.csv"
    result_file = os.getcwd() + "/../result/table_alias_streaming.csv"
    if os.path.exists(result_file):
        os.remove(result_file)
    st_env.register_table_source("Orders",
                                 CsvTableSource(source_file,
                                                ["a", "b", "c", "rowtime"],
                                                [DataTypes.STRING(),
                                                 DataTypes.INT(),
                                                 DataTypes.INT(),
                                                 DataTypes.TIMESTAMP()]))
    st_env.register_table_sink("result",
                               CsvTableSink(["a", "b", "c", "rowtime"],
                                            [DataTypes.STRING(),
                                             DataTypes.INT(),
                                             DataTypes.INT(),
                                             DataTypes.TIMESTAMP()],
                                            result_file))
    orders = st_env.scan("Orders")
    result = orders.alias("x, y, z, t").select("x, y, z, t")
    result.insert_into("result")
    st_env.execute("alias streaming")
    # cat table/result/table_alias_streaming.csv
    # a,1,1,2013-01-01 00:14:13.0
    # b,2,2,2013-01-01 00:24:13.0
    # a,3,3,2013-01-01 00:34:13.0
    # a,4,4,2013-01-01 01:14:13.0
    # b,4,5,2013-01-01 01:24:13.0
    # a,5,2,2013-01-01 01:34:13.0


if __name__ == '__main__':
    alias_streaming()

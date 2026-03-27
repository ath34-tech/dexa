from dexa.execution.tools.data_tools import (
    DescribeDataTool, CheckMissingTool, DropMissingTool, FillMissingTool, 
    FilterDataTool, GetSampleTool, CreateColumnTool, DropColumnTool, 
    RenameColumnTool, SortDataTool, GroupByTool, ChangeDataTypeTool
)
from dexa.execution.tools.ml_tools import TrainLinearModelTool
from dexa.execution.tools.viz_tools import PlotHistogramTool

TOOLS = {
    "describe_data": DescribeDataTool(),
    "check_missing": CheckMissingTool(),
    "drop_missing": DropMissingTool(),
    "fill_missing": FillMissingTool(),
    "filter_data": FilterDataTool(),
    "get_sample": GetSampleTool(),
    "create_column": CreateColumnTool(),
    "drop_column": DropColumnTool(),
    "rename_column": RenameColumnTool(),
    "sort_data": SortDataTool(),
    "group_by": GroupByTool(),
    "change_datatype": ChangeDataTypeTool(),
    "train_linear_model": TrainLinearModelTool(),
    "plot_histogram": PlotHistogramTool()
}

# this code is auto generated by the expr_codegen
# https://github.com/wukan1986/expr_codegen
# 此段代码由 expr_codegen 自动生成，欢迎提交 issue 或 pull request
from typing import TypeVar

import polars as pl  # noqa
import polars.selectors as cs  # noqa

# from loguru import logger  # noqa
from polars import DataFrame as _pl_DataFrame
from polars import LazyFrame as _pl_LazyFrame

# ===================================
# 导入优先级，例如：ts_RSI在ta与talib中都出现了，优先使用ta
# 运行时，后导入覆盖前导入，但IDE智能提示是显示先导入的
_ = 0  # 只要之前出现了语句，之后的import位置不参与调整
# from polars_ta.prefix.talib import *  # noqa
from polars_ta.prefix.tdx import *  # noqa
from polars_ta.prefix.ta import *  # noqa
from polars_ta.prefix.wq import *  # noqa
from polars_ta.prefix.cdl import *  # noqa

DataFrame = TypeVar("DataFrame", _pl_LazyFrame, _pl_DataFrame)
# ===================================

_ = ["volume", "北交所", "上海主板", "low", "最大涨幅限制", "科创板", "high", "B", "创业板", "open", "vwap", "深圳主板", "amount", "preClose", "factor2", "A", "CLOSE", "close"]
[volume, 北交所, 上海主板, low, 最大涨幅限制, 科创板, high, B, 创业板, open, vwap, 深圳主板, amount, preClose, factor2, A, CLOSE, close] = [pl.col(i) for i in _]

_ = ["OPEN", "HIGH", "LOW", "VWAP", "high_limit", "low_limit", "MA5", "MA10", "OUT"]
[OPEN, HIGH, LOW, VWAP, high_limit, low_limit, MA5, MA10, OUT] = [pl.col(i) for i in _]

_DATE_ = "time"
_ASSET_ = "stock_code"
_NONE_ = None
_TRUE_ = True
_FALSE_ = False


def unpack(x: pl.Expr, idx: int = 0) -> pl.Expr:
    return x.struct[idx]


CS_SW_L1 = r"^sw_l1_\d+$"


def func_0_cl(df: DataFrame) -> DataFrame:
    # ========================================
    df = df.with_columns(
        vwap=amount / volume,
        OPEN=factor2 * open,
        HIGH=factor2 * high,
        LOW=factor2 * low,
        CLOSE=close * factor2,
        最大涨幅限制=if_else(北交所, 0.3, 0) + if_else(上海主板 | 深圳主板, 0.1, 0) + if_else(创业板 | 科创板, 0.2, 0),
    )
    # ========================================
    df = df.with_columns(
        VWAP=factor2 * vwap,
        high_limit=preClose * (最大涨幅限制 + 1),
        low_limit=-preClose * (最大涨幅限制 - 1),
    )
    return df


def func_1_ts__stock_code(df: DataFrame) -> DataFrame:
    # ========================================
    df = df.with_columns(
        MA5=(ts_mean(CLOSE, 5)).over(CLOSE.is_not_null(), _ASSET_, order_by=_DATE_),
        MA10=(ts_mean(CLOSE, 10)).over(CLOSE.is_not_null(), _ASSET_, order_by=_DATE_),
        A=(ts_returns(CLOSE, 5)).over(CLOSE.is_not_null(), _ASSET_, order_by=_DATE_),
    )
    return df


def func_2_cs__time(df: DataFrame) -> DataFrame:
    # ========================================
    df = df.with_columns(
        B=(cs_rank(-A, _FALSE_)).over(_DATE_),
    )
    return df


def func_3_cl(df: DataFrame) -> DataFrame:
    # ========================================
    df = df.with_columns(
        OUT=B <= 5,
    )
    return df


"""
#========================================func_0_cl
vwap = amount/volume #
OPEN = factor2*open #
HIGH = factor2*high #
LOW = factor2*low #
CLOSE = close*factor2 #
最大涨幅限制 = if_else(北交所, 0.3, 0) + if_else(上海主板 | 深圳主板, 0.1, 0) + if_else(创业板 | 科创板, 0.2, 0) #
#========================================func_0_cl
VWAP = factor2*vwap #
high_limit = preClose*(最大涨幅限制 + 1) #
low_limit = -preClose*(最大涨幅限制 - 1) #
#========================================func_1_ts__stock_code
MA5 = ts_mean(CLOSE, 5) #
MA10 = ts_mean(CLOSE, 10) #
A = ts_returns(CLOSE, 5) #
#========================================func_2_cs__time
B = cs_rank(-A, _FALSE_) #
#========================================func_3_cl
OUT = B <= 5 #
"""

"""
vwap = amount/volume #
VWAP = factor2*vwap #
OPEN = factor2*open #
HIGH = factor2*high #
LOW = factor2*low #
CLOSE = close*factor2 #
最大涨幅限制 = if_else(北交所, 0.3, 0) + if_else(上海主板 | 深圳主板, 0.1, 0) + if_else(创业板 | 科创板, 0.2, 0) #
high_limit = preClose*(最大涨幅限制 + 1) #
low_limit = preClose*(1 - 最大涨幅限制) #
MA5 = ts_mean(CLOSE, 5) #
MA10 = ts_mean(CLOSE, 10) #
A = ts_returns(CLOSE, 5) #
B = cs_rank(-A, _FALSE_) #
OUT = B <= 5 #
"""


def filter_last(df: DataFrame) -> DataFrame:
    """过滤数据，只取最后一天。实盘时可用于减少计算量
    前一个调用的ts,这里可以直接调用，可以认为已经排序好
        `df = filter_last(df)`
    反之
        `df = filter_last(df.sort(_DATE_))`
    """
    return df.filter(pl.col(_DATE_) >= df.select(pl.last(_DATE_))[0, 0])


def main(df: DataFrame) -> DataFrame:

    df = func_0_cl(df).drop(*[])
    df = func_1_ts__stock_code(df.sort(_ASSET_, _DATE_)).drop(*[])
    df = filter_last(df)
    df = func_2_cs__time(df.sort(_DATE_)).drop(*[])
    df = func_3_cl(df).drop(*[])

    # drop intermediate columns
    # df = df.select(pl.exclude(r'^_x_\d+$'))
    df = df.select(~cs.starts_with("_"))

    # shrink
    df = df.select(cs.all().shrink_dtype())

    return df

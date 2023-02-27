# 对于持仓所有持仓合约按照品种进行压力测试分析
# 先按照单品种计算，再通过greek金额进行加总，此外根据品种的大小对greek进行标准化之后再加总
# 需要一个波动率和标的价格变动组成的表格。
# 先计算隐含波动率，再计算情景
from pyfin.pyfin import OptionType, OptionExerciseType, Option, OptionModel, OptionMeasure
greeks_bs = Option(opt_type=OptionType.CALL, spot0=100, strike=95, mat=3.0 / 12,
                                              vol=0.20, riskless_rate=0.10, exer_type=OptionExerciseType.EUROPEAN).run_model(model=OptionModel.BLACK_SCHOLES)
greeks_bt = Option(opt_type=OptionType.CALL, spot0=100, strike=95, mat=3.0 / 12,
                                              vol=0.20, riskless_rate=0.10).run_model(model=OptionModel.BINOMIAL_TREE)
greeks_mc = Option(opt_type=OptionType.CALL, spot0=100, strike=95, mat=3.0 / 12,
                                             vol=0.20, riskless_rate=0.10, yield_=0.05, exer_type=OptionExerciseType.EUROPEAN) \
                                .run_model(model=OptionModel.MONTE_CARLO, random_seed=12345)


def extreme_scenarios(spot_price,vol0):
    """
    利用计算出的隐含波动率以及标的物收盘价，分析极端情况。
    :param spot_price:
    :param vol0:
    :return:
    """
    number_list = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
    spot_price_list = [(1 + i/100) * 5000 for i in number_list]
    vol0_list = [()]
# 对于持仓所有持仓合约按照品种进行压力测试分析
# 先按照单品种计算，再通过greek金额进行加总，此外根据品种的大小对greek进行标准化之后再加总
# 需要一个波动率和标的价格变动组成的表格。
# 先计算隐含波动率，再计算情景
from pyfin.pyfin import OptionType, OptionExerciseType, Option, OptionModel, OptionMeasure
import pandas as pd

# greeks_bs = Option(opt_type=OptionType.CALL, spot0=100, strike=95, mat=3.0 / 12,
#                                               vol=0.20, riskless_rate=0.10, exer_type=OptionExerciseType.EUROPEAN).run_model(model=OptionModel.BLACK_SCHOLES)
# greeks_bt = Option(opt_type=OptionType.CALL, spot0=100, strike=95, mat=3.0 / 12,
#                                               vol=0.20, riskless_rate=0.10).run_model(model=OptionModel.BINOMIAL_TREE)
# greeks_mc = Option(opt_type=OptionType.CALL, spot0=100, strike=95, mat=3.0 / 12,
#                                              vol=0.20, riskless_rate=0.10, yield_=0.05, exer_type=OptionExerciseType.EUROPEAN) \
#                                 .run_model(model=OptionModel.MONTE_CARLO, random_seed=12345)

class greeks_scenarios():
    """
    对希腊值进行情景分析
    """
# todo:需要将spot_price和vol0的参数直接在类的inti里面设置好，后面函数就不再需要带入参数
    def __init__(self):
        self.spot_price_list = None # 现货价格序列
        self.vol0_list = None # 波动率序列
        self.number_list_price = range(-5, 6, 1)
        self.number_list_vol = range(-10, 11, 3)
        self.delta_scenarios = None
        self.gamma_scenarios = None

    def extreme_scenarios(self,spot_price,vol0):
        """
        利用计算出的隐含波动率以及标的物收盘价，分析极端情况。
        :param spot_price:
        :param vol0:
        :return:
        """
        self.spot_price_list = [(1 + i/100) * spot_price for i in self.number_list_price]
        self.vol0_list = [(i/100 + vol0) for i in self.number_list_vol]
        price_vol_scenarios = [(price,vol) for price in self.spot_price_list for vol in self.vol0_list]
        return price_vol_scenarios


    def delta_s(self):
        self.delta_scenarios = pd.DataFrame(data=None,index=self.vol0_list,columns=self.spot_price_list)
        for i in self.extreme_scenarios(5000,0.2):
            delta = Option(opt_type=OptionType.CALL, spot0=i[0], strike=4900, mat=3.0 / 12,
                                                       vol=i[1], riskless_rate=0.10, exer_type=OptionExerciseType.EUROPEAN).run_model(model=OptionModel.BLACK_SCHOLES)[OptionMeasure.DELTA]
            self.delta_scenarios.loc[i[0],i[1]] = delta
        return self.delta_scenarios


    def gamma_s(self):
        self.gamma_scenarios = pd.DataFrame(data=None,index=self.vol0_list,columns=self.spot_price_list)
        for i in self.extreme_scenarios(5000,0.2):
            gamma = Option(opt_type=OptionType.CALL, spot0=i[0], strike=4900, mat=3.0 / 12,
                                                       vol=i[1], riskless_rate=0.10, exer_type=OptionExerciseType.EUROPEAN).run_model(model=OptionModel.BLACK_SCHOLES)[OptionMeasure.GAMMA]
            self.gamma_scenarios.loc[i[0],i[1]] = gamma
        return self.gamma_scenarios
# todo gamma_s的计算结果有点问题，需要检查

option_s = greeks_scenarios()
option_s.delta_s()
option_s.gamma_s()
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
    def __init__(self,spot_price = 5000,vol0 = 0.2,t = 20):
        self.spot_price_list = None # 现货价格序列
        self.vol0_list = None # 波动率序列
        self.number_list_price = range(-5, 6, 1)
        self.number_list_vol = range(-10, 11, 3)
        self.delta_scenarios = None
        self.gamma_scenarios = None
        self.vega_scenarios = None
        self.theta_scenarios = None
        self.spot_price = spot_price # 标的价格
        self.vol0 = vol0 # 初始隐含波动率
        self.t = t  # 到期日

    def extreme_scenarios(self,**kwargs):
        """
        利用计算出的隐含波动率以及标的物收盘价，分析极端情况。
        :param spot_price:
        :param vol0:
        :return:
        """
        self.spot_price_list = [(1 + i/100) * self.spot_price for i in self.number_list_price]
        self.vol0_list = [(i/100 + self.vol0) for i in self.number_list_vol]
        price_vol_scenarios = [(price,vol) for price in self.spot_price_list for vol in self.vol0_list]
        return price_vol_scenarios


    def delta_s(self,**kwargs):
        self.delta_scenarios = pd.DataFrame(data=None,index=self.vol0_list,columns=self.spot_price_list)
        for i in self.extreme_scenarios(**kwargs):
            delta = Option(opt_type=OptionType.CALL, spot0=i[0], strike=4900, mat=self.t,
                                                       vol=i[1], riskless_rate=0.10, exer_type=OptionExerciseType.EUROPEAN).run_model(model=OptionModel.BLACK_SCHOLES)[OptionMeasure.DELTA]
            self.delta_scenarios.loc[i[0],i[1]] = delta
        return self.delta_scenarios


    def gamma_s(self,**kwargs):
        self.gamma_scenarios = pd.DataFrame(data=None,index=self.vol0_list,columns=self.spot_price_list)
        for i in self.extreme_scenarios(**kwargs):
            gamma = Option(opt_type=OptionType.CALL, spot0=i[0], strike=4900, mat=3.0 / 12,
                                                       vol=i[1], riskless_rate=0.10, exer_type=OptionExerciseType.EUROPEAN).run_model(model=OptionModel.BLACK_SCHOLES)[OptionMeasure.GAMMA]
            self.gamma_scenarios.loc[i[0],i[1]] = gamma
        return self.gamma_scenarios

    def vega_s(self,**kwargs):
        self.vega_scenarios = pd.DataFrame(data=None,index=self.vol0_list,columns=self.spot_price_list)
        for i in self.extreme_scenarios(**kwargs):
            vega = Option(opt_type=OptionType.CALL, spot0=i[0], strike=4900, mat=3.0 / 12,
                                                       vol=i[1], riskless_rate=0.10, exer_type=OptionExerciseType.EUROPEAN).run_model(model=OptionModel.BLACK_SCHOLES)[OptionMeasure.VEGA]
            self.vega_scenarios.loc[i[0],i[1]] = vega
        return self.vega_scenarios
    
    def theta_s(self,**kwargs):
        self.theta_scenarios = pd.DataFrame(data=None,index=self.vol0_list,columns=self.spot_price_list)
        for i in self.extreme_scenarios(**kwargs):
            theta = Option(opt_type=OptionType.CALL, spot0=i[0], strike=4900, mat=3.0 / 12,
                                                       vol=i[1], riskless_rate=0.10, exer_type=OptionExerciseType.EUROPEAN).run_model(model=OptionModel.BLACK_SCHOLES)[OptionMeasure.THETA]
            self.theta_scenarios.loc[i[0],i[1]] = theta
        return self.theta_scenarios
    # def run(self,greek = OptionMeasure.GAMMA,**kwargs):
    #     if greek == OptionMeasure.GAMMA:
    #         result = self.gamma_s(**kwargs)
    #     if greek == OptionMeasure.DELTA:
    #         result = self.delta_s(**kwargs)


option_s = greeks_scenarios(5000,0.2).delta_s()
# todo 函数的参数需要完善，原来option函数中的参数都需要在现在的压力测试的函数里面
# todo 根据文华导出的期权持仓，根据栏目获取期权类型、到期时间、执行价等参数带入
# 对于多张期权合约的greek的计算只需要相乘即可，但是对于不同执行价和期权，但是相同标的的期权，只需要分别计算然后相加即可，不同执行价合约波动率不同的解决办法
# 可以是将风险矩阵的列名换成波动率变动的幅度即可。
# 不同标的的期权计算出的风险矩阵的处理方法是将index换成价格变动的百分比，列名换成波动率变动的百分比

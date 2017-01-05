
"""
>>> class.__dict__ : class의 attr, method 다 봄
>>> func.__code__ : code object 반환
"""

import KSIF as kf
import pandas as pd
import matplotlib.pyplot as plt

# index 가져오기 예제

data = kf.get('C:\\Users\\ysh\\Google 드라이브\\package\\KSIF\\data\\test.csv')

#  Original
data = pd.read_pickle('price_test.pkl')
s1 = kf.Strategy('s1', [kf.algos.RunDaily(),
                        kf.algos.SelectRandomly(),
                        kf.algos.WeighEqually(),
                        kf.algos.Rebalance()])
test = kf.Backtest(s1, data)
res = kf.run(test)
res.save()


# 전략
data = kf.get('KRX:KOSPI', source='google', start='2010-01-01')
s = kf.Strategy('s', [kf.algos.RunMonthly(),
                      kf.algos.SelectRandomly(),
                      kf.algos.WeighEqually(),
                      kf.algos.run_always(kf.algos.RebalanceOverTime(n=3)),
                      kf.algos.LossCut()])
test = kf.Backtest(s, data)
res = kf.run(test)
res.display()
res.plot()
plt.show()




# Value 전략


def ranking(data: pd.DataFrame, group, key, option='relative'):
    filtered = pd.DataFrame({})
    filtered[key + 'r'] = data.groupby(group)[key].rank(ascending=True)
    out = pd.concat([data, filtered[key + 'r']], axis=1)
    temp = out.groupby(group)
    if option == 'absolute':
        return temp[key + 'r']
    elif option == 'relative':
        return temp[key + 'r'].apply(lambda x: x / len(x))
    else:
        print(" Need ranking Option ! Choose {'relative', 'absolute'}")
        return None


def cleanse(data, selector):
    if selector is not None:
        key_array = []
        for key in selector:
            if key[-1] == 'r':
                key_array.append(key[:-1])
            else:
                key_array.append(key)
        data = data[['DATE','NAME', 'FNSECTCODE', 'FNSECTNAME', 'FIRMCO', 'RETM'] + key_array]
        for key in selector:
            if key[-1] == 'r':
                filtered = data[data[key[:-1]] > 0]
                data[key] = ranking(filtered, group=['DATE', 'FNSECTCODE'], key=key[:-1])
    return data


def value_signal(data):
    main_list = ['MVmr', 'PERr', 'PBRr']
    sub_list = ['ROE4Qr', 'OPR4Qr']
    sector_list = ['FGSC.15','FGSC.20','FGSC.25','FGSC.30','FGSC.35','FGSC.45']
    port = cleanse(data, selector=main_list+sub_list)
    data['in_sector'] = port.FNSECTCODE.isin(sector_list)
    data['in_main'] = (port.MVmr + port.PERr + port.PBRr < 1)
    data['in_sub'] = (port.ROE4Qr + port.OPR4Qr > 1)
    data['values'] = ((data['in_sector'] & data['in_main']) & data['in_sub'])
    return data.pivot_table(values='values', index='DATE', columns='FIRMCO').fillna(False)


data = kf.get('D:\\School works\\Business School\\KSIF3\\program\\SAS\\code 2016Q1(SH)\\python\\input.csv')
data.reset_index(level=0, inplace=True)
#data = pd.read_hdf('input.h5', key='ksif')
data = data[data.DATE > '2010-01-01']
main_list = ['MVmr', 'PERr', 'PBRr']
sub_list = ['ROE4Qr', 'OPR4Qr']
sector_list = ['FGSC.15', 'FGSC.20', 'FGSC.25', 'FGSC.30', 'FGSC.35', 'FGSC.45']
port = cleanse(data, selector=main_list+sub_list)
port['in_sector'] = port.FNSECTCODE.isin(sector_list)
port['in_main'] = (port.MVmr + port.PERr + port.PBRr < 0.5)
port['in_sub'] = (port.ROE4Qr + port.OPR4Qr > 1)
port['value_inv'] = (port['in_sector'] & port['in_main'])& port['in_sub']
port_new = port[port.value_inv]


price = data.pivot_table(values='ADJPRC',
                         index='DATE',
                         columns='FIRMCO')
signal = port.pivot_table(values='value_inv', index='DATE', columns='FIRMCO').fillna(False)
del signal[signal.columns[10]]

#price = price.asfreq('D', method='ffill')
#signal = signal.asfreq('D', method='ffill')

s = kf.Strategy('value', [kf.core.algos.SelectWhere(signal),
                          kf.core.algos.WeighEqually(),
                          kf.core.algos.Rebalance()])

t = kf.Backtest(s, price)
res = kf.run(t)
res.display()
res.plot()
plt.show()

res.stats  # 통계치 저장
res.prices  # 각 전략의 가치 저장
t.weights  # 전략의 weight 저장
t.positions  # 실제로 보유했던 주식수
t.weights.ix[1][t.weights.ix[1]>0]  # 첫번째 기간에 weight가 0 이상인 종목 선택
t.weights[t.weights>0]


# RalanceOverTime

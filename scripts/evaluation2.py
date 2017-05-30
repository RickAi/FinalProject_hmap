import numpy as np


def mase(error, forecast):
    f_sum = 0
    for count in range(1, len(forecast)):
        f_sum += forecast[count] - forecast[count - 1]
    base = f_sum/(len(forecast) - 1)

    sum = 0
    for e in error:
        sum += e/base

    return sum/len(error)

def mae(error):
    sum = 0
    for item in error:
        sum += item
    return sum/len(error)

def rmse(error):
    sum = 0
    for item in error:
        sum += np.mean(item*item)
    return np.sqrt(sum)

if __name__ == '__main__':
    # actual = [6580000, 4700000, 3030000, 5350000, 11600000, 4800000, 9400000, 17000000, 2700000, 2950000]
    # forecast = [6283400, 5038800, 2903900, 5587100, 10800800, 5105200, 8928000, 15021000, 3132700, 2860300]

    actual = [6580000, 4700000, 3030000, 5350000, 11600000, 4800000, 9400000, 17000000, 2700000, 2950000]
    forecast = [5893000, 5125350, 3850000, 4950800, 10580500, 5208300, 8900500, 15690100, 3100300, 3150800]

    print("forecast:" + str(forecast))

    error = []
    for count in range(0, len(actual)):
        error.append(actual[count] - forecast[count])
    print("error:" + str(error))

    percent_error = []
    for count in range(0, len(actual)):
        percent_error.append(error[count]/actual[count] * 100)
    print("percent error:" + str(percent_error))

    MAE = mae(error)
    RMSE = rmse(error)

    print("MAE:" + str(MAE))
    print("RMSE:" + str(RMSE))

    MAPE = mae(percent_error)
    MASE = mase(error, forecast)


    print("MAPE:" + str(MAPE))
    print("MASE:" + str(MASE))
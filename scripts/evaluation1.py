from functools import reduce

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
    error = [687000,-425350,-820000,399200,1019500,-408300,499500,1309900, -400300, -200800]
    percent_error =[104, -90.5, -270, 74.617, 87.887, -85.063, 53.139, 77.053, -148.259, -68.0678]
    forecast=[5893000, 5125350, 3850000, 4950800, 10580500, 5208300, 8900500, 15690100, 3100300, 3150800]

    MAE = mae(error)
    RMSE = rmse(error)

    print("MAE:" + str(MAE))
    print("RMSE:" + str(RMSE))

    MAPE = mae(percent_error)
    MASE = mase(error, forecast)


    print("MAPE:" + str(MAPE))
    print("MASE:" + str(MASE))


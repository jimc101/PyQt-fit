from scipy.stats import gaussian_kde
from numpy import atleast_2d, zeros, newaxis, dot, sum, exp

class SpatialAverage(object):
    def __init__(self, xdata, ydata):
        self.xdata = atleast_2d(xdata)
        self.ydata = ydata
        self.kde = gaussian_kde(xdata)
        self.d, self.n = self.xdata.shape


    def evaluate(self, points):
        points = atleast_2d(points).astype(self.xdata.dtype)
        #norm = self.kde(points)
        d, m = points.shape
        result = zeros((m,), points.dtype)
        norm = zeros((m,), points.dtype)

        # iterate on the internal points
        for i in range(self.n):
            diff = self.xdata[:,i,newaxis] - points
            tdiff = dot(self.kde.inv_cov, diff)
            energy = exp(-sum(diff*tdiff,axis=0)/2.0)
            result += self.ydata[i]*energy
            norm += energy

        result[norm>1e-50] /= norm[norm>1e-50]

        return result

    def __call__(self, new_x):
        return self.evaluate(new_x)


# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 23:04:51 2020

@author: adwait
"""
import numpy as np

#polynomial fitting of data
def polyfitData(xdata, ydata, ax, x_plot, unit,
            eq_pos = [1,0.2], fit_order = 1, fit_show = False): #fit data and plot
    data = zip(xdata, ydata, x_plot)
    data = np.array(sorted(data, key = lambda x: x[0]))
    coeff = np.polyfit(data[:,0],data[:,1], fit_order) #fitting coeffients
    slope = coeff[0]
    p_fit = np.poly1d(coeff)
    y_fit = p_fit(data[:,0])
    y_avg = np.sum(data[:,1])/len(data[:,1])
    r2 = (np.sum((y_fit-y_avg)**2))/(np.sum((data[:,1] - y_avg)**2))
    sign = '' if coeff[1] < 0 else '+'
    eq_id = 'Slope'
    eq_coff = ["$%.1e"%(coeff[i]) + "x^" + str(len(coeff) - i - 1) + "$"\
         if i < len(coeff) - 2 else "%.4fx"%(coeff[i]) for i in range(len(coeff)-1)]
    eq =  "y=" + '+'.join(eq_coff) + "+%.4f"%(coeff[len(coeff)-1]) + "; $R^2$=" + "%.4f"%(r2)  
    eq_clean = eq.replace('+-', '-')
##        x_fit = np.linspace(min(data[:,0]), max(data[:,0]), 100)
    ax.plot(data[:,2], y_fit, color = 'black',
            linewidth=2, linestyle='dashed')
##        print(eq_pos)
    if fit_show == True:
        ax.text(float(eq_pos[0]), float(eq_pos[1]), eq_id + ": " + "%.4f"%(slope) + ' (' + unit + ')',
                ha = 'right', transform=ax.transAxes, color = 'black',
                bbox=dict(facecolor='white', edgecolor = 'black', alpha=0.5))
    print('data fitted', eq_clean)
    return slope
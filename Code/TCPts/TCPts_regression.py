'''
Created on Aug 13, 2013

@author: yfried
'''

from ..parse_to_streams.streams_and_packets import dStream, dPacket
# from ..parse_to_streams.parse_stream_packets import dPacket
from scipy import stats
import sys
from operator import itemgetter
from numpy.lib.polynomial import polyval
from copy import deepcopy
from matplotlib.pyplot import scatter, show

class TCPts_regression:
    '''
    classdocs
    '''
    
    def scatter_plot(self, dStream_obj):
        '''
         return list of scattered points (x,y)
         where
         x - packet wireshark timestamp
         y - packet tcp_timestamp
        '''
        def map_packet_to_scatter(dPacket_obj):
            x,y = float(dPacket_obj.time),dPacket_obj.TCPts 
            if y:
                return float(x),y
            
        ret = [map_packet_to_scatter(pkt) for pkt in dStream_obj.packets]

        return ret

    def __add__(self, other):
        ret = deepcopy(self)
        ret += other
        return ret
    
    def __iadd__(self, other):
        
        try:
            if not (self.flag and other.flag):
                raise Exception('bad arguments')
            
            self.scatter_list.extend(other.scatter_list)
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(self.scatter_list)
            self.slope = slope
            self.intercept = intercept
            self.r_val = r_value
            self.p_val = p_value
            self.std_err = std_err
            
            self.max = max(self.scatter_list,key=itemgetter(1))
            self.min = min(self.scatter_list,key=itemgetter(1))
            
            self.x_grid = [x for x,y in self.scatter_list]
            self.line = polyval([self.slope, self.intercept], self.x_grid)
            
            return self
            
        except Exception as e:
            print 'bad'
            print e
            sys.exit(1)

    
    def __init__(self, dStream_obj):
        '''
        Constructor
        '''
        
        self.scatter_list = self.scatter_plot(dStream_obj)

        
        self.scatter_list = [point for point in self.scatter_list if point]

        if self.scatter_list:
            self.flag = True
            slope, intercept, r_value, p_value, std_err = stats.linregress(self.scatter_list)
            self.slope = slope
            self.intercept = intercept
            self.r_val = r_value
            self.p_val = p_value
            self.std_err = std_err
            
            self.max = max(self.scatter_list,key=itemgetter(1))
            self.min = min(self.scatter_list,key=itemgetter(1))
            
            self.x_grid = [x for x,y in self.scatter_list]
            
            self.line = polyval([self.slope, self.intercept], self.x_grid)
        else:
            self.flag = False
#         print scatter_list, self.max
#         sys.exit()     
     
    def plot_scatter(self, plot_flag=True):
        sct_x=list()
        sct_y=list()
        for x,y in self.scatter_list:
            sct_x.append(x)
            sct_y.append(y)
        if plot_flag:
            scatter(sct_x,sct_y)
            show()
        return sct_x, sct_y
    
    def __str__(self):
        out=''
        out += ('slope: ' + str(self.slope) +
                 ' intercept: ' + str(self.intercept) +
                 ' R: ' + str(self.r_val) +
                 ' P: ' + str(self.p_val) +
                 ' std_err: ' + str(self.std_err)
                 )
        return out
     
     
    
         


from config.model_params import direction, minHighLessLow, mincvHighLessLow_bucket, \
	minTrades, minVolume, num_of_buckets, \
	max_quantity, max_share_price, \
	max_notional_value, bucket_weights
import statistics
from datetime import datetime


class GetTradeInfo(object):

	def __init__(self, tradeDictionary, trades):
		self.trades = trades
		self.tradeDictionary = tradeDictionary

def timeFormat(epochTime):
	formattedTime = datetime.fromtimestamp(int(epochTime/1000)).strftime('%H:%M:%S %m-%d-%Y')

	return formattedTime


class RunGrazingModel(object):
	def runner(self, symbol):
		self.open_position = False
		self.symbol = symbol
		print("*"*40)

		print("Assess Long")
		print("Direction: {} >= {}".format(self.direction_bucket, direction))
		print("HighLessLow: {} > {}".format(self.avg_high_less_low_bucket, minHighLessLow))
		print("CV: {} < {}".format(self.cv_high_less_low_bucket, mincvHighLessLow_bucket))
		print("Trades: {} > {}".format(self.avgTrades, minTrades))
		print("Volume: {} > {}".format(self.avgVolume, minVolume))
		print("*"*40)

		if self.direction_bucket >= direction \
			and self.avg_high_less_low_bucket > minHighLessLow \
			and self.cv_high_less_low_bucket < mincvHighLessLow_bucket \
			and self.avgTrades > minTrades \
			and self.avgVolume > minVolume \
			and self.closePx < max_share_price:
				
				self.open_position = True
				self.side = 'BUY'
				self.quantity = round(min(round(self.tradeSizer,0), max_quantity, max_notional_value/self.closePx),0)
				self.entry_price = round(self.closePx+.075,2)
				self.tradeDictionary = TradeDictionary.setValues(self)
								
				print("\n"+"*"*30+"\n")
		return self

class TradeDictionary(object):
	def setValues(self):
		tradeDictionary = {'symbol': self.symbol,
							'side': self.side,
							'quantity': self.quantity,
							'entry_price': self.entry_price}
		return tradeDictionary

class ConstructTimeSeriesData():
	def __init__(self, candlesticks, symbol):

		self.symbol = symbol
		self.candlesticks = candlesticks
		self.direction_bucket = 0
		self.direction_bucket_list = []
		self.high_less_low_bucket_list = []
		self.avg_high_less_low_bucket = 0
		self.stddev_high_less_low_bucket = 0.0
		self.cv_high_less_low_bucket = 999.9
		self.avgTrades = 0.0
		self.avgVolume = 0
		self.totalTrades = 0
		self.tradeSize = 0
		self.volume = 0

		self.calcModelParams()

	def calcModelParams(self):

			weight_counter = 0

			for candlestick in self.candlesticks:
				
					self.high_less_low_bucket_list.append(candlestick['highPxLessLowPx'])
					self.direction_bucket_list.append(candlestick['direction'] * bucket_weights[weight_counter])
					self.totalTrades += candlestick['totalTrades']
					self.tradeSize += candlestick['medTradeSize']
					self.volume += candlestick['volume']
					weight_counter += 1

			self.closePx = self.candlesticks[-1]['closePx']
			self.avgTrades = round(self.totalTrades / num_of_buckets,0)
			self.tradeSizer = round(self.tradeSize / num_of_buckets,0)
			self.avgVolume = round(self.volume / num_of_buckets,0)
			self.stddev_high_less_low_bucket = statistics.stdev(self.high_less_low_bucket_list)
			self.avg_high_less_low_bucket = round(sum(self.high_less_low_bucket_list) / float(num_of_buckets),2)
			try:
				self.cv_high_less_low_bucket = round(self.stddev_high_less_low_bucket/self.avg_high_less_low_bucket,3)
			except:
				self.cv_high_less_low_bucket = 999.9
			self.direction_bucket = sum(self.direction_bucket_list)




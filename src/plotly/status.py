#!/usr/bin/env python3

import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import numpy as np
import sys, os, itertools, json, datetime

def remove_unstable(df,time):
	timeformat = "%b %d, %Y, %H:%M:%S"
	with open('config.json') as f:
		config = json.load(f)
		time = df[time].astype('datetime64[s]')
		sel = np.ones(len(df), dtype='bool')
		for start, end in config["unstable"]:
			start = datetime.datetime.strptime(start, timeformat)
			end   = datetime.datetime.strptime(end,   timeformat)
			mysel = np.logical_and(time > start, time < end)
			sel = np.logical_and(sel,np.logical_not(mysel))
			# print('Remove',start, end, np.sum(mysel))
		return df[sel]
	raise Exception()

class Sysbench(object):
	def __init__(self, path, time='st_mtime', metric='throughput'):
		super(Sysbench, self).__init__()
		self.path = path
		self.time = time
		self.metric = metric
		self.df = remove_unstable(pd.read_csv(path).sort_values(self.time), time)
		self._X = np.array(self.df[self.time])
		self._Y = np.array(self.df[self.metric])
		self.LABELS = [
			'machine',
			'kernel',
			'engine',
			'client',
			'clients',
			'engine_sched',
			'client_sched',
		]
	def classes(self):
		LABELS = self.LABELS
		df = self.df.astype({l:str for l in LABELS})
		all_values = np.array(df[LABELS], dtype=str)
		all_values = np.unique(all_values,axis=0)
		for values in all_values:
			sel = np.ones(len(df),dtype='bool')
			for i in range(len(LABELS)):
				sel = np.logical_and(sel, df[LABELS[i]] == values[i])
				assert np.sum(sel) != 0
			yield sel, LABELS, values
	def normalize(self):
		for sel,labels,values in self.classes():
			self._Y[sel] = self.df[sel][self.metric] / max(self.df[sel][self.metric])
	def X(self, sel=None):
		if sel is None:
			sel = np.ones(len(self.df), dtype='bool')
		return self._X[sel].astype('datetime64[s]')
	def Y(self, sel=None):
		if sel is None:
			sel = np.ones(len(self.df), dtype='bool')
		return self._Y[sel]

class Batch(Sysbench):
	"""docstring for Batch"""
	def __init__(self, path):
		super(Batch, self).__init__(path, metric='time')
		self.LABELS = [
			'machine',
			'kernel',
			'batch',
			'tasks',
			'scheduler',
		]
	def normalize(self):
		for sel,labels,values in self.classes():
			self._Y[sel] = min(self.df[sel][self.metric]) / self.df[sel][self.metric]

def save(objects, output):
	data = [
		go.Scatter(
    		x = o.X(),
    		y = o.Y(),
    		name = o.path,
		)
		for o in objects
	]
	data += [
		go.Scatter(
    		x = o.X(sel),
    		y = o.Y(sel),
    		#name = '-'.join(values),
    		visible='legendonly'
		)
		for o in objects
		for sel,labels,values in o.classes()
	]
	plot(data, filename=output, auto_open=False)

def main():
	output = sys.argv[0]
	output, _ = os.path.splitext(output)
	output += '.html'
	output = 'i80/status.html'
	objects = [
		Sysbench('sysbench.csv'),
		Batch('batch.csv')
	]
	for o in objects:
		o.normalize()
	save(objects, output)

if __name__ == '__main__':
	main()

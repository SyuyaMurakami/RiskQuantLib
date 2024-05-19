#!/usr/bin/python
# coding = utf-8
import numpy as np
#<import>
#</import>

class vectorization(object):
	def __init__(self, value):
		"""
		Add element to object, and mark it as attribute 'all'.
		"""
		super(vectorization, self).__getattribute__('__dict__')['all'] = value

	def __getattr__(self, item):
		"""
		If attribute does not exist, it will return np.ndarray object and fill it with np.nan value.
		The length of returned array is just the length of self.all.
		"""
		length = len(super(vectorization, self).__getattribute__('all'))
		return np.array([np.nan for _ in range(length)])

	def __getattribute__(self, item):
		"""
		If attribute exists, it will return np.ndarray object whose value is the attribute value of each element.
		If some elements do not have that attribute, the np.nan will be used.
		"""
		allElement = super(vectorization, self).__getattribute__('all')
		return np.array([getattr(i,item,np.nan) for i in allElement])

	def __setattr__(self, key, value):
		"""
		The set-attribute-value action will be replaced as a vectorizationd version. value parameter is iterable, and the
		attribute of first element of self.all will be set as the first element of value parameter, etc.
		"""
		allElement = super(vectorization, self).__getattribute__('all')
		[setattr(i, key, v) for i, v in zip(allElement, value)]

	#<vectorization>
	#</vectorization>
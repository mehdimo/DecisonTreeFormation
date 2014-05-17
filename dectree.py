# Western Michigan University, Computer Science Department
# Mehdi Mohammadi
# February 27, 2014

# This program implements ID3 algorithm in python. The input should be a file
# containing the training data.
# The format of training data is as follows:
#     A. At the first line put the attribute (column) names separated by comma.
#     B. In the consequnce lines, attribue values must come in the order of 
#     attribute names and separated by comma.
#
# The output is a decision tree and its demonstration.

import math

class DecisionTree:
	def read_data(self, filename):
		fid = open(filename,"r")
		data = []
		d = []
		for line in fid.readlines():
			d.append(line.strip())
		for d1 in d:
			data.append(d1.split(","))
		fid.close()
		
		self.featureNames = self.get_features(data)		
		data = data[1:]
		self.classes = self.get_classes(data)		
		data = self.get_pure_data(data)

		return data,self.classes,self.featureNames	
	
	def get_classes(self, data):
		data = data[1:]
		classes = []
		for d in range(len(data)):
			classes.append(data[d][-1])			

		return classes
	
	def get_features(self, data):
		features = data[0]
		features = features[:-1]		
		return features
	
	def get_pure_data(self, dataRows):
		dataRows = dataRows[1:]
		for d in range(len(dataRows)):
			dataRows[d] = dataRows[d][:-1]		
		return dataRows
	
	def zeroList(self, size):
		d = []
		for i in range(size):
			d.append(0)
		return d
	
	def getArgmax(self, arr):
		m = max(arr)		
		ix = arr.index(m)
		return ix
	
	def getDistinctValues(self, dataList):
		distinctValues = []
		for item in dataList:
			if(distinctValues.count(item) == 0):
				distinctValues.append(item)		
		return distinctValues
	
	def getDistinctValuesFromTable(self, dataTable, column):
		distinctValues = []
		for row in dataTable:
			if(distinctValues.count(row[column]) == 0):
				distinctValues.append(row[column])		
		return distinctValues	
	
	def getEntropy(self, p):
		if(p != 0):
			return -p * math.log2(p)
		else:
			return 0
		
	def create_tree(self, trainingData, classes, features, maxlevel = -1, level=0):
		nData = len(trainingData)
		nFeatures = len(features)
		
		try:
			self.featureNames
		except:
			self.featureNames = features
			
		newClasses = self.getDistinctValues(classes)				
		frequency = self.zeroList(len(newClasses))
		totalEntropy = 0		
		index = 0
		for aclass in newClasses:
			frequency[index] = classes.count(aclass)
			prob = float(frequency[index])/nData
			totalEntropy += self.getEntropy(prob)			
			index += 1
				
		default = classes[self.getArgmax(frequency)]		
		if(nData == 0 or nFeatures == 0 or (maxlevel >= 0 and level > maxlevel)):
			return default
		elif classes.count(classes[0]) == nData:
			return classes[0]
		else:
			gain = self.zeroList(nFeatures)			
			for feature in range(nFeatures):
				g = self.getGain(trainingData, classes, feature)
				gain[feature] = totalEntropy - g				
				
			bestFeature = self.getArgmax(gain)
			newTree = {features[bestFeature]:{}}
			
			values = self.getDistinctValuesFromTable(trainingData, bestFeature)				
			for value in values:
				newdata = []
				newClasses = []
				index = 0
				for row in trainingData:
					if row[bestFeature] == value:
						if bestFeature == 0:
							newRow = row[1:]
							newNames = features[1:]
						elif bestFeature == nFeatures:
							newRow = row[:-1]
							newNames = features[:-1]
						else:
							newRow = row[:bestFeature]
							newRow.extend(row[bestFeature + 1:])
							newNames = features[:bestFeature]
							newNames.extend(features[bestFeature+1:])
						newdata.append(newRow)
						newClasses.append(classes[index])
					index += 1
					
				subtree = self.create_tree(newdata, newClasses, newNames, maxlevel, level + 1)
				
				newTree[features[bestFeature]][value] = subtree
			return newTree
						
		
		print(newClasses)
		
	def getGain(self, data, classes, feature):
		gain = 0		
		ndata = len(data)
		
		values = self.getDistinctValuesFromTable(data, feature)		
		featureCounts = self.zeroList(len(values))
		entropy = self.zeroList(len(values))		
		valueIndex = 0
		for value in values:
			dataIndex = 0
			newClasses = []
			for row in data:
				if row[feature] == value:
					featureCounts[valueIndex] += 1
					newClasses.append(classes[dataIndex])
				dataIndex += 1
			
			classValues = self.getDistinctValues(newClasses)
			classCounts = self.zeroList(len(classValues))
			classIndex = 0
			for classValue in classValues:
				for aclass in newClasses:
					if aclass == classValue:
						classCounts[classIndex] +=1
				classIndex += 1
			
			for classIndex in range(len(classValues)):
				pr = float(classCounts[classIndex])/sum(classCounts)
				entropy[valueIndex] += self.getEntropy(pr)				
			
			pn = float(featureCounts[valueIndex])/ndata 
			gain = gain + pn * entropy[valueIndex]			
			
			valueIndex += 1
		return gain		

	def showTree(self, dic, seperator):
		if(type(dic)==dict):
			for item in dic.items():        
				print(seperator, item[0])
				self.showTree(item[1], seperator + " | ")
		else:
			print(seperator + " -> (", dic +")")  	

tree = DecisionTree()
tr_data, clss, attrs = tree.read_data('resturant.dat')

tree1 = tree.create_tree(tr_data, clss, attrs)

tree.showTree(tree1, ' ')

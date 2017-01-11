# Decision Tree using Hunt's algorithm

import csv
import pydot

fileh=open('bank.csv','r')
dataset=list()

reader = csv.reader(fileh, delimiter=',')
i=1
for row in reader:
	if i==1:
		actual_attr=row
		i=0
	else:
		dataset.append(row)

attr=range(len(dataset[0])-1)
cont=[None for i in range(len(dataset)-1)]

def continuous(dataset,attr,d):
	l=d.keys()
	l=[float(i) for i in l]
	l.sort()
	p=list()
	for i in range(len(l)-1):
		p.append((l[i]+l[i+1])/2)
	d1=dict()
	
	for i in p:
		for j in dataset:
			if i not in d1:
				d1[i]={}
				d1[i]['left']={}
				d1[i]['right']={}
			if float(j[attr]) <= i:
				if j[-1] not in d1[i]['left']:
					d1[i]['left'][j[-1]]=1
				else:
					d1[i]['left'][j[-1]]+=1
			else:
				if j[-1] not in d1[i]['right']:
					d1[i]['right'][j[-1]]=1
				else:
					d1[i]['right'][j[-1]]+=1
	gini_list=dict()
	total_each=list()
	gini_dict=dict()
	tot_dict=dict()
	for (k,v) in d1.items():
		tot_dict[k]={}
		gini_dict[k]={}
		for (k1,v1) in v.items():
			val=v1.values()
			tot_val=sum(val)
			tot_dict[k][k1]=tot_val
			t=0
			for i in val:
				try:
					t+=(i/float(tot_val))*(i/float(tot_val))
				except:
					t+=0
			t=1-t
			gini_dict[k][k1]=t
	for (k,v) in gini_dict.items():
		wavg=0
		val=tot_dict[k].values()
		tot_val=sum(val)
		for (k1,v1) in v.items():
			wavg+=(tot_dict[k][k1]/float(tot_val))*v1
		gini_list[wavg]=k

	min_gini=min(gini_list.keys())
	split=gini_list[min_gini]
	
	cont[attr]=split
	return min(gini_list)

# Calculating Gini index
def gini(dataset,attr):
	d=dict()
	for i in dataset:
		if i[attr] not in d:
			d[i[attr]]={}
		if i[-1] not in d[i[attr]]:
			d[i[attr]][i[-1]]=1
		else:
			d[i[attr]][i[-1]]+=1
	if len(d)>4 and cont[attr]==None:
		return continuous(dataset,attr,d)
	gini_list=list()
	total_each=list()
	
	for (k,v) in d.items():
		val=sum(v.values())
		total_each.append(val)
		t=0
		for (k1,v1) in v.items():
			try:
				t+=(v1/float(val))*(v1/float(val))
			except:
				t+=0
		t=1-t
		gini_list.append(t)
	tot=sum(total_each)
	wavg=0
	for i in range(len(gini_list)):
		wavg+=(total_each[i]/float(tot))*gini_list[i]
	return wavg

def chooseBestSplit(dataset,labels):
	gini_list=[]
	for i in labels:
		gini_list.append(gini(dataset,i))
	return labels[gini_list.index(min(gini_list))]


def countLabel(dataset):
	d=dict()
	for i in dataset:
		if i[-1] not in d:
			d[i[-1]]=1
		else:
			d[i[-1]]+=1
	return d

def stoppingCond(dataset,attr):
	d=countLabel(dataset)
	for (k,v) in d.items():
		if v==len(dataset):
			return 1
	if attr==[]:
		return 1
	return 0

def classify(dataset,attr):
	d=countLabel(dataset)
	l=d.values()
	m=max(l)
	for (k,v) in d.items():
		if v==m:
			return k

def TreeGrowth(dataset,attr):
	if dataset==[]:
		return 
	if stoppingCond(dataset,attr):
		label=classify(dataset,attr)
		return label
	else:
		d=dict()
		best=chooseBestSplit(dataset,attr)
		V=list()
		for i in dataset:
			if i[best] not in V:
				V.append(i[best])
		attr.remove(best)
		best1=actual_attr[best]
		d[best1]={}
		
		if cont[best] !=None :
			split=cont[best]
			d[best1][split]={}
			Evl=[]
			Evr=[]
			for i in dataset:
				if float(i[best]) <= split:
					Evl.append(i)
				else:
					Evr.append(i)
			d[best1][split]['left']=TreeGrowth(Evl,attr)
			d[best1][split]['right']=TreeGrowth(Evr,attr)
			return d
		
		for i in range(len(V)):
			Ev=list()
			for j in dataset:
				if j[best]==V[i]:
					Ev.append(j)
			d[best1][V[i]]=TreeGrowth(Ev,attr)
	return d

d=TreeGrowth(dataset,attr)
print d

def makeDecision(d):
	if type(d) is not dict:
		return d
	else:
		a=d.keys()
		attribute=a[0]
		print '\nTell me the value for '+attribute
		inp=raw_input().strip()
		k=d[attribute].keys()
		if type(k[0]) is float:
			if float(inp) <= k[0]:
				d=d[attribute][k[0]]['left']
			else:
				d=d[attribute][k[0]]['right']
			result=makeDecision(d)
			return result
		d=d[attribute][inp]
		result=makeDecision(d)
		return result

def draw(parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)

def visit(node, parent=None):
    for k,v in node.iteritems():
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if isinstance(parent,float):
            	parent=str(parent)
            if isinstance(k,float):
            	k=str(k)
            if parent:
                draw(parent, k)
            visit(v, k)
        else:
			if isinstance(parent,float):
				parent=str(parent)
			if isinstance(k,float):
				k=str(k)
			draw(parent, k)
            # drawing the label using a distinct name
			draw(k, k+'_'+v)

graph = pydot.Dot(graph_type='graph')
visit(d)
graph.write_png('bank.png')

while True:
	print '\nEnter your choice 1 for prediction and 0 to stop'
	ans=input()
	if ans == 0:
		print 'bye'
		break
	result=makeDecision(d)
	print result
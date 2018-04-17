import sys
import subprocess
import re
import os
import platform
import networkx as nx
import json
import matplotlib.pyplot as plt
from graphviz import Digraph
#  1. Merging hierarchy for divide nodes by adding variable names in the nodes     2. reading structure from json
#act_code=[]
#act_string=raw_input()
#l=len(codes)
#for i in range(0,l):
#	act_code.append(int(codes[i]))
#var_string=raw_input()
#var_name=var_string.split(" ");
#var_range=[]
#var_string=raw_input()
#var_codes=[]
#cds=var_string.split(" ");
#l=len(cds)
#for i in range(0,l):
#	var_codes.append(int(cds[i]))
def make_graph(hierarchy, iteration):
	global actions
	global act_back
	iteration=iteration+".gv"
	d=Digraph('G',filename=iteration)
	for item in hierarchy:
		d.node(str(item))
	for item in hierarchy:
		if(hierarchy[item]["typ"]!="Actions"):
			for i in range(0,len(hierarchy[item]["children"])):
				d.edge(str(item),str(hierarchy[item]["children"][i]))
		else:
			for i in range(0,len(hierarchy[item]["value"])):
				d.edge(str(item),str(act_back[str(hierarchy[item]["value"][i])]))
	d.format='pdf'
	d.render()



def merge_hierarchy(hierarchy1 ,hierarchy2, root_task1,root_task2):
	if hierarchy1[root_task1]["typ"]=="Actions":
		hierarchy1[root_task1]["value"]=list(set(hierarchy1[root_task1]["value"]+hierarchy2[root_task2]["value"]))
		return 

	elif((hierarchy1[root_task1]["typ"]=="sequence" and hierarchy2[root_task1]["typ"]=="sequence") or (hierarchy1[root_task1]["typ"]=="root" and hierarchy2[root_task2]["typ"]=="root") ):
		hierarchy1[root_task1]["children"].sort()
		hierarchy2[root_task2]["children"].sort()
		diff=len(hierarchy1[root_task1]["children"])-len(hierarchy2[root_task2]["children"])
		if(diff>0):
			for i in range(0,diff):
				queue=[]
				hierarchy1[str((hierarchy2[root_task2]["children"])[i])+"_1"]=hierarchy2[(hierarchy2[root_task2]["children"])[i]]
				hierarchy1[root_task1]["children"].append(str((hierarchy2[root_task2]["children"])[i])+"_1")
				queue.append(hierarchy2[(hierarchy2[root_task2]["children"])[i]]["children"])
				while(queue):
					new_ele=queue[0]
					hierarchy1[(str(new_ele)+"_1")]=hierarchy2[new_ele]
					queue.append(hierarchy2[new_ele]["children"])
					queue.remove(new_ele)




		for i in range(0,len(hierarchy1[root_task1]["children"])):
			merge_hierarchy(hierarchy1,hierarchy2,hierarchy1[root_task1]["children"][i],hierarchy2[root_task2]["children"][i])
	else:
		hierarchy1[root_task1]["typ"]="divide"
		hierarchy2[root_task2]["typ"]="divide"
		list1=hierarchy1[root_task1]["variables"]
		list2=hierarchy2[root_task2]["variables"]
		for i in range(0,len(list1)):
			flag=0
			mark_j=-1
			for j in range(0,len(list2)):
				if(list1[i]==list2[j]):
					flag=1
					mark_j=j
			if(flag==0):
				queue=[]
				for k in range(0,len(list1)):
					if(list1[i] in hierarchy1[hierarchy1[root_task1]["children"][k]]["variables"]):
						hierarchy2[str(hierarchy1[root_task1]["children"][k])+"_1"]=hierarchy1[hierarchy1[root_task1]["children"][k]]
						queue.append(hierarchy1[hierarchy1[root_task1]["children"][k]]["children"])
						while(queue):
							new_ele=queue[0]
							hierarchy2[(str(new_ele)+"_1")]=hierarchy1[new_ele]
							queue.append(hierarchy1[new_ele]["children"])
							queue.remove(new_ele)
			else:
				for k in range(0,len(list1)):
					jk=hierarchy1[hierarchy1[root_task1]["children"][k]]["variables"]
					if(list1[i] in hierarchy1[hierarchy1[root_task1]["children"][k]]["variables"]):
						for p in range(0,len(list2)):
							if(list2[mark_j] in hierarchy2[hierarchy2[root_task2]["children"][p]]["variables"]):
								merge_hierarchy(hierarchy1,hierarchy2,hierarchy1[root_task1]["children"][k],hierarchy2[root_task2]["children"][p])



		for i in range(0,len(list2)):
			flag=0
			for j in range(0,len(list1)):
				if(list2[i]==list1[j]):
					flag=1
			if(flag==0):
				queue=[]
				for k in range(0,len(list2)):
					if(list2[i]in hierarchy2[hierarchy2][root_task2["children"][k]]["variables"]):
						hierarchy1[str(hierarchy2[root_task2]["children"][k])+"_1"]=hierarchy2[hierarchy2[root_task2]["children"][k]]
						queue.append(hierarchy2[hierarchy2[root_task2]["children"][k]]["children"])
						while(queue):
							new_ele=queue[0]
							hierarchy1[(str(new_ele)+"_1")]=hierarchy2[new_ele]
							queue.append(hierarchy2[new_ele]["children"])
							queue.remove(new_ele)




def make_hierarchy(hierarchy,start_node, end_node, typ_e, parent_task, va):
	global my_edges
	global skeleton
	global task_number
	global actions
	variables=actions
	print start_node 
	print end_node
	if(start_node==end_node):
		return
	make_node={"children":[],"typ":typ_e, "variables":[]}
	make_node["variables"]=va
	this_task=task_number
	hierarchy[this_task]=make_node
	task_number=task_number+1
	nodes=[]
	top=0;
	for edges in skeleton:
		if(edges==start_node):
			nodes.append(edges)
			top=top+1
			nodes.append(skeleton[edges])
			break
	curr_node=nodes[1]
	while(curr_node!=" " and curr_node!=end_node and skeleton[curr_node]!=" "):
		nodes.append(skeleton[curr_node])
		curr_node=skeleton[curr_node]
	count=0
	end_list=[]
	for nod in nodes:
		if(nod!=" "):
			edges=my_edges[nod]
			for dests in edges:
				if(dests["dest"]==end_node):
					count=count+1
					end_list.append(nod);
		
	print count
	if(skeleton[start_node]==end_node):
		count=count-1

	if(count>2 or typ_e=="divide"):
		curr_start=start_node
		ed=my_edges[start_node]
		top=1
		for nod in nodes:
			for j in end_list:
				if(j==nod):
					vc=0
					for e in ed:
						if(e["dest"]==nod):
							var_ch=e["var_codes"]
							for i in range(0,len(var_ch)):
								if(var_ch[i]==1):
									vc=i+1
					make_hierarchy(hierarchy,skeleton[curr_start],nod,"divide",this_task,[vc])
					hierarchy[this_task]["variables"].append(vc)
					task_number=task_number+1
					curr_start=nod



	else:
		path_from={}                          # for marking previous node
		dist_from={}
		hierarchy[this_task]["typ"]="sequence" # for storing distance through that route                        
		for j in range(0,len(nodes)):         #marking all the nodes as maximum
			dist_from[nodes[j]]=len(nodes)+1
		dist_from[start_node]=0
		path_from[start_node]=start_node      # distance from start to start is 0
		for nod in nodes:
			edges=my_edges[nod]               # out edges from every node
			for edge in edges:
				desti=edge["dest"]              # end point for every edge
				if(desti not in nodes or dist_from[desti]>(dist_from[nod]+1)): #checking for minimum distance till now
					dist_from[desti]=dist_from[nod]+1    # updating the distances and the route information
					path_from[desti]=nod
		number_of_iter=dist_from[end_node]
		if(number_of_iter<len(nodes)-1):
			curr_dest=end_node

			for k in range(0,number_of_iter):
				rem=my_edges[path_from[curr_dest]]
				top=0
				vc=0
				for i in rem:
					if(i["dest"]==curr_dest):
						var_ch=my_edges[path_from[curr_dest]][top]["var_codes"]
						for p in range(0,len(var_ch)):
							if(var_ch[p]==1):
								vc=p+1
						del my_edges[path_from[curr_dest]][top]
					else:
						top=top+1
				make_hierarchy(hierarchy,path_from[curr_dest],curr_dest,"sequence" , this_task,[vc]) #needs to add this into hierarchy
				hierarchy[this_task]["variables"].append(vc)
				task_number=task_number+1
				curr_dest=path_from[curr_dest]

		else:

			hierarchy[this_task]["typ"]="sequence"
			hierarchy[this_task]["value"]=[]
			task_number=task_number+1
			ka1=end_node
			ka=ka1.split("_")
			new_node={"children":[],"typ":"Actions", "value": [variables[ka[0]]], "variables" :[] }
			hierarchy[this_task]["children"].append(task_number) # adding primitive actions to higher hierarchy like pickup to pickup function
			hierarchy[task_number]=new_node
			task_number=task_number+1
			nn={"children":[],"typ":"Actions","value":[],"variables" :[]}
			curr_node=skeleton[start_node]
			while(skeleton[curr_node]!=end_node and curr_node!=end_node):
				ka2=curr_node
				ka3=ka2.split("_")
				nn["value"].append(variables[ka3[0]])
				curr_node=skeleton[curr_node]
			nn["value"]=list(set(nn["value"]))
			hierarchy[task_number]=nn
			hierarchy[this_task]["children"].append(task_number)


	hierarchy[parent_task]["children"].append(this_task)

			
data=json.load(open('sample.json'))
hea=data["Header"]
header=hea.split("!")
vi=header[0]
v=vi.split(" ")
c=header[1].split(" ")
actions={}
var={}
act_back={}
num_act=len(v)
for i in range(0,len(v)):
	actions[v[i]]=int(c[i])
	act_back[c[i]]=v[i]
actions["End"]=len(v)
act_back[str(len(v))]="End"
print actions
print act_back

v=header[2].split(" ")
for i in range(0,len(v)):
	var[v[i]]=i+1
n=len(data["CatStructures"])
my_edges={}
ed=data["CatStructures"][0]["Actions"]
sk=data["CatStructures"][0]["Path"]
skeleton={}
for i in range(0,len(sk)-1):
	skeleton[sk[i]]=sk[i+1]
	my_edges[sk[i]]=[]
my_edges["End"]=[]
skeleton["End"]=" "
for i in range(1,len(ed)):
	node=ed[i]["Nodes"]
	nodes=node.split(" ")
	new_ed={}
	#new_ed={"code_for_dest": ,"dest": nodes[1], "var_codes" : [ed[i]]["Codes"], "initial_values":[0],"new_values":[0] }
	new_ed["code_for_dest"]=actions[ed[i]["Direction"]]
	new_ed["dest"]=nodes[1]
	kp1=ed[i]["Codes"]
	kp=kp1.split(",")
	new_ed["var_codes"]=[]
	for j in range(0,len(kp)):
		new_ed["var_codes"].append(int(kp[j]))
	#new_ed["var_codes"]=ed[i]["Codes"]
	new_ed["initial_values"]=[0]
	new_ed["new_values"]=[0]
	my_edges[nodes[0]].append(new_ed)


 # ex-{"North":1, "South":2 }
  # ex- { "Start": [{code_for_dest:3,dest: "East1", var_codes: [0,0,0,0,0,0,0,0,1], initial_values:[0], new_values:[1]},{code_for_dest:3,dest: "East1", var_codes: [1,1,0,0,0,0,0,0,0], initial_values:[0,0], new_values:[1,0]},{code_for_dest:5, dest:"Pickup1", var_codes: [0,0,0,0,0,0,1,0], initial_values:[0], new_values:[1]}, {code_for_dest:6,dest: "Dropoff1", var_codes: [0,0,1,1,0,0,0,0,0], initial_values:[3,0], new_values:[-1,-1]}]}
dest_to_end=[]

hierarchy1={}    # ex-{task_number: {children:[], type:}}
for edge in my_edges:  #finding all the nodes directly connected to end
	dests=my_edges[edge]
	for i in range(0,len(dests)):
		dicti=dests[i]
		if(dicti["dest"]=="End"):
			dest_to_end.append(edge)
task_number=1
make_node={"children":[],"typ":"root","variables":[]}
hierarchy1[0]=make_node
make_hierarchy(hierarchy1,"Start","End","sequence",0,[])
hierarchy2={}
my_edges.clear();
new_ed.clear();
dicti.clear();





for ki in range(1,n):
	hierarchy2.clear();
	ed=data["CatStructures"][ki]["Actions"]
	sk=data["CatStructures"][ki]["Path"]
	skeleton={}
	for i in range(0,len(sk)-1):
		skeleton[sk[i]]=sk[i+1]
		my_edges[sk[i]]=[]
	my_edges["End"]=[]
	skeleton["End"]=" "
	for i in range(1,len(ed)):
		node=ed[i]["Nodes"]
		nodes=node.split(" ")
		new_ed={}
		new_ed["code_for_dest"]=actions[ed[i]["Direction"]]
		new_ed["dest"]=nodes[1]
		kp1=ed[i]["Codes"]
		kp=kp1.split(",")
		new_ed["var_codes"]=[]
		for j in range(0,len(kp)):
			new_ed["var_codes"].append(int(kp[j]))
		new_ed["initial_values"]=[0]
		new_ed["new_values"]=[0]
		my_edges[nodes[0]].append(new_ed)



	dest_to_end=[]  
	for edge in my_edges:  
		dests=my_edges[edge]
		for i in range(0,len(dests)):
			dicti=dests[i]
			if(dicti["dest"]=="End"):
				dest_to_end.append(edge)
	task_number=1
	make_node={"children":[],"typ":"root","variables":[]}
	hierarchy2[0]=make_node
	make_hierarchy(hierarchy2,"Start","End","sequence",0,[])
	merge_hierarchy(hierarchy1,hierarchy2,0,0)
	make_graph(hierarchy1,str(ki))
	










g=nx.Graph()
print actions
print var
node_added=[]
for i in hierarchy1:
	print i
	print hierarchy1[i]
	if(i not in node_added):
		node_added.append(i)
		if(hierarchy1[i]["typ"]=="Actions"):
			g.add_node(str(i))
		else:
			g.add_node(str(i),variables=hierarchy1[i]["variables"])
	chi=hierarchy1[i]["children"]
	for j in range(0,len(chi)):
		if(j not in node_added ):
			node_added.append(j)
			if(hierarchy1[j]["typ"]!="Actions"):
				g.add_node(str(j), variables=hierarchy1[j]["variables"])
			else:
				g.add_node(str(j))
		g.add_edge(str(i),str(j))
	if hierarchy1[i]["typ"]=="Actions":
		for j in range(0,len(hierarchy1[i]["value"])):
			g.add_edge(str(i),act_back[str(hierarchy1[i]["value"][j])])

#node_directory=[{typ:"Max", equation: "", task: 1 },{typ: "Q", equation: ""},{typ:"Action", name:""}]





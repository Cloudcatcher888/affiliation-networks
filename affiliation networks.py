u0=2
cu = 5
cq = 5#越大随机性越强，一般可以和节点规模处于同个数量级
beta = 0.5
ii = 0
size=1000
time = 500
time = int(size/beta)
Tij = 0.1
bb=-1
sizeleft=-size/10
dp=np.ones(size+sizeleft)

xn = 30
yn = 3
pc =float(max(cu,cq))/u0 * 1.2

if __name__ == '__main__':
	#set up B(Q,U)  (t=0)
	for kk in range(yn):
		ss=1#生成G图时每个点度的期望（平均度为ss）  影响相变点的主要因素
		u0 = 2
		q0 = 2
		B0 = np.ones([q0,u0])
		rand = np.random.rand(q0,u0)
		B00 = B0 * pc
		mask= rand > B00
		B0[mask] = 0
		print 'initial B0'
		print B0
		#simplify B0,setup G0
		G0 = np.zeros([q0,q0])
		for i in range(u0):
			sum1 = np.sum(B0[:,i])*(np.sum(B0[:,i])-1)/2
			s=0
			for j in range(q0):
				if B0[j,i]==1:
					for k in range(j+1,q0):
						if B0[k,i]==1:
							#print t,q0,u0,j,k
							G0[j,k]=1
							G0[k,j]=1
							s+=1
							if sum1 == s:
								break
					if sum1 == s:
						break
		#print 'initial G0'
		#print G0
		wb=xlwt.Workbook()
		ws=wb.add_sheet('A')
		#add node
		for t in range(time):
			print 't=',t
			if np.random.rand(1) < beta:
				#add in Q	
				#temp=np.sum(B0, axis=1).tolist()
				#B0 = np.vstack((B0,B0[temp.index(max(temp)),:]))
				
				pc = float(cq)/u0
				temp=np.sum(B0,axis=1)/(np.sum(B0)+0.01)
				rand=np.random.rand(1)
				for i in range(q0):
					if rand < np.sum(temp[:(i+1)]):
						ii=i
						print ii,pc
						break
				rand = np.random.rand(u0)
				mask= rand < (B0[i]*pc)
				#print mask
				B000=copy.deepcopy(B0[i])
				B000[~mask] = 0
				#print B000
				B0 = np.vstack((B0,B000))
				#print G0[i]	
				q0+=1
				G0 = np.vstack((G0,np.zeros(q0-1)))
				G0 = np.column_stack((G0,np.zeros([q0,1])))
				print B0
				for i in range(u0):
					if B0[q0-1,i]==1:
						ps=float(ss)/(sum(sum(B0)))
						#print ps
						for j in range(q0-1):
							if B0[j,i]==1 and np.random.rand(1,1)<ps:
								G0[j,q0-1]=1
								G0[q0-1,j]=1
				#print ii, B0[ii], rand,'\n',temp
				#print 'G0'
				#print G0
			else:
				#add in U
				pc=float(cu)/q0
				temp=np.sum(B0,axis=0)/(np.sum(B0)+0.01)
				rand=np.random.rand(1)
				for i in range(u0):
					if rand < np.sum(temp[:(i+1)]):
						ii=i
						#print ii
						break
				rand=np.random.rand(q0)
				mask=rand<(B0[:,i]*pc)
				B000=copy.deepcopy(B0[:,i])
				B000[~mask] = 0
				
				B0 = np.column_stack((B0,B000))	
				u0+=1
				#print ii, B0[:,ii], rand,'\n',temp
			#	print 'B0'
			#	print B0
			#	print G0
			#BFS
			#output:G0[i][j]
			#color = np.zeros([xn,q0])
		
		
			if t==time-1:
				sm=sum(G0)
				for i in range(sizeleft+size):
					for j in range(q0):
						if sm[j]==i:
							dp[i]+=1
							print i
	
			if t==time+100:
				aa=-1
				for Tij in np.hstack((np.linspace(0,0.05,8),np.linspace(0.053,0.295,80),np.linspace(0.3,1,9))):
					color = np.zeros([xn,q0])
					for iii in range(xn):
						graph1 = Tij*np.ones([q0,q0])	
						graph3 = np.zeros([q0,q0])
						graph=copy.deepcopy(G0)
						#print graph
				
				
						#infection
						rand=np.random.rand(q0,q0)
						mask=rand>=graph1
						graph[mask]=0
						#print 'graph'
						#print graph1
						if iii==2:
							print Tij
							#print graph
		
						#BFS	
				
						color[iii,0]=1
						Q = Queue.Queue()
						Q.put(1)
						while not Q.empty():
							u = Q.get()
							for j in np.hstack((np.arange(0,q0,3),np.arange(1,q0,3),np.arange(2,q0,3))):
								if graph[u,j]!=0:
									if color[iii,j]==0:
										color[iii,j]=1
										Q.put(j)
							color[iii,u] = 2
					aa+=1
						#print Tij,'\t',sum(sum(color))/2/xn
					ws.write(aa,3,Tij)
					ws.write(aa,4,sum(sum(color))/2/xn)
			#print G0
			#i=1
			#graph0=np.zeros([q0,q0])
			#graph2=graph
			#while sum(sum(graph2))!=0:
			#	graph2=graph2*graph
			#	i+=1
			#	if i==q0:
			#		break
			#print graph
			#print i, (graph+np.eye(q0))**i
			#print sum((graph+np.eye(q0))**i)[0]
			#print "wwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
	#yy=np.log10(np.sort(np.sum(G0,axis=0)))
	#xx=np.log10(np.linspace(q0,1,q0))	
	yy=np.log10(dp/yn)
	xx=np.log10(np.arange(0.01,size+sizeleft,1))
	print xx
	print yy
		
	for i in range(size+sizeleft):
		ws.write(i,0,yy[i])
		ws.write(i,1,xx[i])
	wb.save('d.xls')
	
	#f.write(G0)
	#f.seek(0)
	#open('a.txt')
						
		
	
	
	



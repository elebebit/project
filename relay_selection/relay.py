import os 
import random
import csv
import matplotlib.pyplot as plt

	
def user_set(nor,fri):

	global seq1,seq2,usr_ls

	# Establish user dataset
	name_ls1=[]
	for i in range(1,nor+1):
		name_ls1.append('UE'+str(i))

	seq1=tuple(name_ls1)

	name_ls2=[]
	for i in range(1,fri+1):
		name_ls2.append('FR'+str(i))

	seq2=tuple(name_ls2)

	usr_ls=name_ls1+name_ls2

# user success rate
def ssr_set():
	global ssr_dic

	normal_dic=dict.fromkeys(seq1,0.5)
	friend_dic=dict.fromkeys(seq2,0.7)

	ssr_dic=dict(normal_dic,**friend_dic)

	return ssr_dic

# user location
def dis_set():
	global dis_dic

	dis_normal=dict.fromkeys(seq1)
	dis_friend=dict.fromkeys(seq2)

	dis_dic=dict(dis_normal,**dis_friend)

	for key in dis_dic.keys():
		dis_dic[key]=random.uniform(20,80)

	return dis_dic

def select_relay(P,ave_dis):

# Establish distance and success rate dataset
	x=[]
	ys=[]
	yd=[]

	diss=[]
	srs=[]
	rates_social=[]
	rates_dis=[]

	for (value1,value2) in zip(dis_dic.values(),ssr_dic.values()):
		diss.append(value1)
		srs.append(value2)

	for i in range(1,1001):

		# Compute the weights 
		for (dis,sr) in zip(diss,srs):
			# with social
			rate1=P*dis+(1-P)*sr
			rates_social.append(rate1)

			# with distance
			rate2=dis
			rates_dis.append(rate2)

		succs_rate=0
		succd_rate=0

		for j in range(1000):
			# establish a, b, and relay 
			usr_sr=random.uniform(1,20)
			usr_de=random.uniform(80,100)

#--------------------- Select relay with social-----------------------------------
			relays=random.choices(usr_ls,rates_social,k=1)
			nums=usr_ls.index(''.join(relays))
			relays_local=diss[nums]

			# distance from relay to source and destination
			diss_s=relays_local-usr_sr
			diss_d=usr_de-relays_local

			if diss_s >= ave_dis or diss_d >=ave_dis:
				continue
			else:
				succs_rate+=0.001
				if nums <= 9:
					srs[nums]+=0.1
				else:
					srs[nums]+=0.05
			
# ---------------------Select relay with distance---------------------------------
			relayd=random.choices(usr_ls,rates_dis,k=1)
			numd=usr_ls.index(''.join(relayd))
			relayd_local=diss[numd]

			# distance from relay to source and destination
			disd_s=relayd_local-usr_sr
			disd_d=usr_de-relayd_local

			if disd_s >= ave_dis or disd_d >=ave_dis:
				continue
			else:
				succd_rate+=0.001

		rates_social.clear()
		rates_dis.clear()

		x.append(i)
		ys.append(succs_rate)
		yd.append(succd_rate)


	# figure
	plt.figure(figsize=(8,6),dpi=100)
	plt.ylim(0,1)
	plt.plot(x,ys,"b--",linewidth=1)
	plt.plot(x,yd,"r--",linewidth=1)
	plt.xlabel('times')
	plt.ylabel('success rate')
	plt.savefig('ssr.jpg')
	plt.show()


if __name__ == '__main__':
	user_set(nor=70,fri=30)
	ssr_set()
	dis_set()
	select_relay(P=0.4,ave_dis=50)

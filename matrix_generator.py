import numpy as np
import itertools



# print np.array([[0 , 0.6 , 0.3 , 0.9],[0.45 , 0  ,0.75  ,0.5],[0.15,0.9,0,0.1]])            0
# print np.array([[0 , 0.9 , 0.15 , 0.5],[0.75 , 0  ,0.45  ,0.9],[0.3, 0.6, 0, 0.1]])         2
# print np.array([[0 , 0.45 , 0.75 , 0.5],[0.6 , 0  ,0.3  ,0.1], [0.9, 0.15, 0 , 0.9]])       3
# print np.array([[0 , 0.3 , 0.6 , 0.9],[0.15 , 0  ,0.9  ,0.1],[0.45 , 0.75 , 0 ,0.5]])       4
# print np.array([[0 , 0.75 , 0.45 , 0.1],[0.9 , 0  ,0.15  ,0.5],[0.6, 0.3 ,0, 0.9]])         1







def get_relationship_aggregation(per):
    relationship_score=[0,0,0]
    aggregation=[per[2]+per[4],per[0]+per[5],per[1]+per[3]]
    relationship_score[np.argmax(aggregation)]=1

    relationship_score[np.argmin(aggregation)]=-1
    std=np.std(aggregation)

    return relationship_score,std,aggregation,per



print len(list(itertools.permutations([0.15, 0.75, 0.3,0.9,0.6,0.45])))

per_dict={}

for per in list(itertools.permutations([0.15, 0.75, 0.3,0.9,0.6,0.45])):
    if abs(per[0]-per[2])<0.25 and abs(per[1]-per[4])<0.25 and abs(per[3]-per[5])<0.25:
        relationship_score, std, aggregation, per=get_relationship_aggregation(per)
        if str(relationship_score) in per_dict.keys():
            per_dict[str(relationship_score)].append((std, aggregation, per))
        else:
            per_dict[str(relationship_score)]=[(std, aggregation, per)]

for key in per_dict.keys():
    print '-------------------',key,'------------------------\n'
    list=per_dict[key]
    list.sort(key=lambda x: x[0],reverse=True)
    print list

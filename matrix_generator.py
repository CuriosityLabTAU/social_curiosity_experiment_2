import numpy as np
import itertools

#
# 1  2  3  4
# 5  6  7  8
# 9  10 11 12
#
# 0  1  2  3
# 4  0  5  6
# 7  8  0  9
#
# 0  1  2
# 3  0  4
# 5  6  0

def get_relationship_aggregation(per):
    mat= np.array([[0 , per[0] , per[1] , per[2]],[per[3] , 0  ,per[4]  ,per[5]],[per[6],per[7],0,per[8]]])

    if  list((mat.sum(axis=1))).count(np.min((mat.sum(axis=1)))) >1:
        return -1,-1,-1

    if  list(mat.sum(axis=0)[0:3]).count(np.max((mat.sum(axis=0))[0:3])) >1:
        return -1,-1,-1

    relationship_score=[np.argmax((mat.sum(axis=0))[0:3]),np.argmin((mat.sum(axis=1))),np.argmax(mat[:, 3]),np.argmin(mat[:, 3])]

    std=np.std([np.max((mat.sum(axis=0))[0:3]),np.min((mat.sum(axis=0))[0:3])])+ np.std([np.min((mat.sum(axis=1))),np.max((mat.sum(axis=1)))])

    return relationship_score,std,[[0 , per[0] , per[1] , per[2]],[per[3] , 0  ,per[4]  ,per[5]],[per[6],per[7],0,per[8]]]



# print len(list(itertools.permutations([0.15, 0.75, 0.3,0.9,0.6,0.45])))

per_dict={}

for per in list(itertools.permutations([-1, 1, 0,-1, 1, 0,-1, 1, 0])):
    # if abs(per[0]-per[3])< 1.5 and abs(per[1]-per[6])<1.5 and abs(per[4]-per[7])<1.5:
    if len(set([per[2],per[5],per[8]])) ==3:
        if len(set([per[0],per[1],per[2]]))==1 or len(set([per[3],per[4],per[5]]))==1 or len(set([per[6],per[7],per[8]]))==1:
            if len(set([per[0], per[1], per[2]]))==1 and list(set([per[0], per[1], per[2]]))[0]==0:
                continue
            if len(set([per[3], per[4], per[5]])) == 1 and list(set([per[3], per[4], per[5]]))[0] == 0:
                continue
            if len(set([per[6], per[7], per[8]])) == 1 and list(set([per[6], per[7], per[8]]))[0] == 0:
                continue

            relationship_score, std, per=get_relationship_aggregation(per)
            if relationship_score== -1 and  std ==-1 and per == -1:
                continue

            if len(set(relationship_score))<3:
                continue

            if str(relationship_score) in per_dict.keys():
                per_dict[str(relationship_score)].append((std, per))
            else:
                per_dict[str(relationship_score)]=[(std, per)]

for key in per_dict.keys():
    # if '0' not in key or '1' not in key or '2' not in key:
    #     continue

    list=per_dict[key]
    list.sort(key=lambda x: x[0],reverse=True)
    print '-------------------',key,'------------------------'
    print list[0]
    print ''







------------------- [1, 0, 2, 0] ------------
[[0, 0, -1, -1], [-1, 0, 0, 0], [1, 1, 0, 1]]

------------------- [2, 0, 1, 0] ------------
[[0, -1, 0, -1], [1, 0, 1, 1], [-1, 0, 0, 0]]

------------------- [0, 2, 1, 2] ------------
[[0, 0, -1, 0], [1, 0, 1, 1], [0, -1, 0, -1]]

------------------- [0, 1, 2, 1] ------------
[[0, -1, 0, 0], [0, 0, -1, -1], [1, 1, 0, 1]]

------------------- [1, 2, 0, 2] ------------
[[0, 1, 1, 1], [0, 0, -1, 0], [-1, 0, 0, -1]]

------------------- [2, 2, 0, 1] ------------
[[0, 1, 1, 1], [0, 0, 0, -1], [-1, -1, 0, 0]]







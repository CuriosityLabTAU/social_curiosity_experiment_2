import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json


AMT_data=pd.read_csv('qualtrics_data.csv')
#preprocessing:
columns= ['Progress','Duration (in seconds)', 'Finished', 'Q1.2', 'Q1.3', 'Q1.4', 'Q1.5',
                     'Q0_1', 'Q1_1', 'Q2_1', 'Q3_1', 'Q4_1', 'Q5_1', 'Q6_1', 'Q7_1', 'Q8_1', 'Q9_1', 'Q10_1', 'Q11_1', 'Q12_1', 'Q13_1', 'Q14_1', 'Q155_1',
                     'validation_1']

columns_names= ['progress','duration','finished','agree_to_participate','gender','age','degree','0','1','2','3','4','5',
                '6','7','8','9','10','11','12','13','14','15','validation']

# remove_ferst_two_lines:#
AMT_data=AMT_data.drop([0,1])

#columns_names
AMT_data=AMT_data[columns]
AMT_data.columns=columns_names

#to numeric:
final_list= list(set(columns_names).difference(set(['finished'])))
for col in final_list:
    AMT_data[col] = AMT_data[col].astype(float)

#Finished
AMT_data=AMT_data[AMT_data.progress==100]

#agree_to_participate
AMT_data=AMT_data[AMT_data.agree_to_participate==1]

#validation
AMT_data=AMT_data[AMT_data.validation!=21]
AMT_data=AMT_data[AMT_data.duration >180] #more then 3 min

######################################################################################

print AMT_data.describe()

######################################################################################
#take out behavior
take_out_behavior=['2'] # '2' is just for test!
final_behaviors= list(set([str(i) for i in range(16)]).difference(set(take_out_behavior)))

print final_behaviors

# AMT data for analysis:
AMT_data= AMT_data[final_behaviors]
AMT_data = AMT_data.reset_index(drop=True)

#pandas.Index.astype
AMT_data.columns=AMT_data.columns.astype(int)

for col in list(AMT_data):
    AMT_data[col] = AMT_data[col].astype(int)
#sacle:
AMT_data=AMT_data-4
AMT_data=AMT_data.div(3)


#########################################################################################

number_of_bins=5

plt.figure()
hist=AMT_data.hist(bins=number_of_bins,xlabelsize=15,ylabelsize=15)
plt.show()


bins = [-1.1,-0.8,-0.2,0.2,0.8,1]
labels = [-1,-0.5,0,0.5,1]
labels=list(np.around(np.array(labels),3))
shape=AMT_data.count()


print "------------------------AMT_data_bin--------------------------------------------"

for i in list(AMT_data):
    AMT_data[i] = pd.cut(AMT_data[i], bins=bins, labels=labels,include_lowest=True)
print AMT_data


# value counts
print "---------------------------hist_df--------------------------------------"
hist_list=[]
for i in list(AMT_data):
    hist_list.append(AMT_data[i].value_counts())
hist_df=pd.DataFrame(hist_list)
print hist_df

#/ by shape
print "---------------------------hist_prob_df--------------------------------------"
hist_prob_df=hist_df.div(shape,axis=0)
print hist_prob_df

#norem bins prob
print "---------------------------probs--------------------------------------"
probs_df=hist_prob_df.div(hist_prob_df.sum(axis=0),axis=1)
print probs_df


#leave only best n probabilities
n=3
for col in list(probs_df):
    col_best_n_values=sorted(probs_df[col].tolist(),reverse =True)[0:n]

    probs_df.loc[(probs_df[col] < col_best_n_values[-1])] = 0

print probs_df

#normliaze agen
#fix fug with 1


probs_df.to_csv('probs_from_AMT.csv')


#make json for pseudo randomization:



# save
# with open('pseudo_randomization_probs.json', 'w') as outfile:
#     json.dump(pseudo_randomization_dict, outfile)
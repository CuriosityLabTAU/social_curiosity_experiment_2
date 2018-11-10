import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


AMT_data=pd.read_csv('AMT_row_2.csv')
#preprocessing:
columns= ['Duration (in seconds)','Finished','RecordedDate','Q1.2','Q1.3','Q1.4','Q1.5','Q0_11','Q1_11','Q2_11','Q3_11','Q4_11','Q5_11',
          'Q6_11','Q7_11','Q8_11','Q9_11','Q10_11','Q11_11','Q12_11','Q13_11','Q14_11','validation_11']
columns_names= ['duration','finished','date','agree_to_participate','gender','age','degree','0','1','2','3','4','5',
                '6','7','8','9','10','11','12','13','14','validation']

# remove_ferst_two_lines:#
AMT_data=AMT_data.drop([0,1])

#columns_names
AMT_data=AMT_data[columns]
AMT_data.columns=columns_names

#to numeric:
final_list= list(set(columns_names).difference(set(['finished','date','agree_to_participate','gender','degree'])))
for col in final_list:
    AMT_data[col] = AMT_data[col].astype(float)

#Finished
AMT_data=AMT_data[AMT_data.finished=='True']

#agree_to_participate
AMT_data=AMT_data[AMT_data.agree_to_participate=='Agree']

#validation
AMT_data=AMT_data[AMT_data.validation==0]
AMT_data=AMT_data[AMT_data.duration >180] #more then 3 min

######################################################################################
# AMT data for analysis:
AMT_data= AMT_data[[str(i) for i in range(15)]]
AMT_data = AMT_data.reset_index(drop=True)


#pandas.Index.astype
AMT_data.columns=AMT_data.columns.astype(int)

for col in list(AMT_data):
    AMT_data[col] = AMT_data[col].astype(int)
#sacle:
AMT_data=AMT_data.div(100)


#########################################################################################

number_of_bins=9

plt.figure()
hist=AMT_data.hist(bins=number_of_bins,xlabelsize=15,ylabelsize=15)
plt.show()


bins = [i*(1.0/number_of_bins) for i in xrange(number_of_bins+1)]
labels = [(bins[i]+bins[i+1])/2.0 for i in xrange(number_of_bins)]
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

probs_df.to_csv('probs_from_AMT.csv')
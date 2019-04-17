#功能：进行多个预测结果的融合，融合方式为投票
#注意点：
# 1、MERGED_CSV为融合后的结果输出，经过了阈值判断，在模块运行之前切记要清空MERGED_CSV
# 2、MERGED_CSV为融合前的输入，支持1-n的结果融合，当仅仅有一个输入的时候为对输入的结果进行阈值判断处理
import pandas as pd
import os
import time
COMPARE_DIR='./prediction'#将需要输出融合的文件融合到一起
MERGED_CSV='./merged_data'#融合后的输出目录,一定要先清空
THROLD=0.5
def merge_csv():
    if os.path.exists('./merged_data/merged_data_pre.csv'):
        os.remove('./merged_data/merged_data_pre.csv')
        os.remove('./merged_data/merged_data.csv')
    start=time.clock()
    if_first_csv=0
    count =0
    if not os.path.exists(MERGED_CSV):
        os.mkdir(MERGED_CSV)
        if_first_csv=1
    if os.listdir(MERGED_CSV)==[]:
        if_first_csv=1
    for filename in os.listdir(COMPARE_DIR):
        print(filename)
        count+=1
        file_path = os.path.join(COMPARE_DIR, filename)
        compare_data = pd.read_csv(file_path)
        if if_first_csv==1:
            result= pd.DataFrame(compare_data)#将内容拷贝进新的表格,并且需要将数据进行阈值处理
            if_first_csv=0
            for i in range(result.shape[0]):
                if result.iloc[i]['Probability'] < THROLD:
                    result.at[i, 'Probability'] = 0
                else:
                    result.at[i, 'Probability'] = 1
        else:
            for i in range(result.shape[0]):
                line_in_source = result.iloc[i]
                for j in range(compare_data.shape[0]):
                    if line_in_source['Id']==compare_data.iloc[j]['Id']:
                        line_temp = line_in_source['Probability']
                        if compare_data.iloc[j]['Probability'] < THROLD:
                            comp_temp = 0
                        else:
                            comp_temp = 1
                        result.at[i,'Probability']=line_temp+comp_temp
                        break
    result.to_csv(MERGED_CSV + '/merged_data_pre.csv', index=False)  # 完成融合输出
    print(count)
    for i in range(result.shape[0]):
        if result.at[i,'Probability']>=count/2*1.0:
            result.at[i,'Probability']=1
        else:
            result.at[i,'Probability']=0
    result.to_csv(MERGED_CSV+'/merged_data.csv',index=False)#完成融合输出
    print("merged all anwers takes times:{:.2f} s".format(time.clock()-start))
if __name__ == '__main__':
    merge_csv()

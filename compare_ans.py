#一个对比表格进行最后统计的程序
#功能：对比经过结果融合的结果与标签的结果的对比
#注意点：对比的预测结果需要经过merge.csv的预测融合处理
import pandas as pd
import random
import merge_csv as merge
SOURCE_PATH="./source_label/test.csv"#放置已经标记好的数据
COMPARE_PATH="./merged_data/merged_data.csv"#放置融合好的结果
Threshold=0.5

def get_recall():
    true_num_danger=0.0
    prediction_danger=0.0
    compare_data=pd.read_csv(COMPARE_PATH)
    source_data = pd.read_csv(SOURCE_PATH)
    print("开始检测召回率！")
    print('未被检测出来的位置：')
    for i in range(source_data.shape[0]):
        line_in_source=source_data.iloc[i]
        if line_in_source['Probability']:
            true_num_danger+=1.0
            for j in range(compare_data.shape[0]):
                if j==compare_data.shape[0]:
                    print(line_in_source['Id'] + ' ' + 'not find in compare label')
                if line_in_source['Id']==compare_data.iloc[j]['Id']:
                    if compare_data.iloc[j]['Probability']==1.0:#在预测中的位置是否为1
                        prediction_danger+=1.0
                    else:
                        print(compare_data.iloc[j]['Id'])#把错误预测的位置打出来
                    break #找到了就进行下次循环
    if true_num_danger == prediction_danger:
        print('None')
    print('真实正样本个数:{}'.format(true_num_danger))
    print('成功被预测为正的个数:{}'.format(prediction_danger))
    return prediction_danger/true_num_danger
def get_precesion():
    prediction_exsit = 0.0
    true_exsit = 0.0
    false_count=0.0
    source_data = pd.read_csv(SOURCE_PATH)
    compare_data = pd.read_csv(COMPARE_PATH)
    print("开始检测精准率！")
    print("漏预测的区域为：")
    for i in range(compare_data.shape[0]):
        line_in_compare = compare_data.iloc[i]#预测的位置
        if line_in_compare['Probability'] >= Threshold:
            prediction_exsit += 1.0
            for j in range(source_data.shape[0]):
                if j==source_data.shape[0]:
                    print(line_in_compare['Id']+' '+'not find in source label')
                if line_in_compare['Id']==source_data.iloc[j]['Id']:
                    if source_data.iloc[j]['Probability']==1.0:
                        true_exsit+=1.0
                    else:                  #没有却被预测为存在的位置
                        false_count+=1.0
                        print(line_in_compare['Id'])
                    break
    if false_count==0:
        print('None')
    print('预测为正样本的数量为:{}'.format(prediction_exsit))
    print('预测的正样本中实际为正的数量:{}'.format(true_exsit))
    print('预测的正样本中实际为负的数量:{}'.format(false_count))
    return true_exsit / prediction_exsit
def get_fpr():#事实上为负样本，却被预测为正样本的概率
    true_not_exsit = 0.0
    false_exsit = 0.0
    source_data = pd.read_csv(SOURCE_PATH)
    compare_data = pd.read_csv(COMPARE_PATH)
    print("开始检测误报率！")
    print("负样本被预测为正的位置：")
    for i in range(source_data.shape[0]):
        line_in_source = source_data.iloc[i]
        if line_in_source['Probability'] == 0:#标签中为负样本
            true_not_exsit += 1.0
            for j in range(compare_data.shape[0]):
                if j==compare_data.shape[0]:
                    print(line_in_source['Id'] + ' ' + 'not find in compare label')
                if line_in_source['Id']==compare_data.iloc[j]['Id']:
                    if compare_data.iloc[j]['Probability']!=0:
                        false_exsit += 1.0
                        print(compare_data.iloc[j]['Id'])
                    break
    if false_exsit==0:
        print('None')
    print("实际负样本的个数为：{}".format(true_not_exsit))
    print("负样本中被预测为正的个数为：{}".format(false_exsit))
    return false_exsit / true_not_exsit
def get_accuracy():
    good_prediction = 0.0
    source_data = pd.read_csv(SOURCE_PATH)
    compare_data = pd.read_csv(COMPARE_PATH)
    print("开始检测准确率！")
    print("错误预测的区域：")
    for i in range(source_data.shape[0]):
        line_in_source = source_data.iloc[i]
        for j in range(compare_data.shape[0]):
            if j== compare_data.shape[0]:
                print(line_in_source['Id'] + ' ' + 'not find in compare label')
            if line_in_source['Id']==compare_data.iloc[j]['Id']:
                if line_in_source['Probability']==compare_data.iloc[j]['Probability']:
                    good_prediction+=1.0
                else:
                    print(line_in_source['Id'])
                break
    if good_prediction==source_data.shape[0]:
        print("None")
    print("需要预测的部分总数量为：{}".format(source_data.shape[0]))
    print('正确预测的数量为：{}'.format(good_prediction))
    return good_prediction / source_data.shape[0]

if __name__ == '__main__':
   merge.merge_csv()
   print('召回率为:{:.2f} %'.format(get_recall()*100))
   print('###############################################################')
   print('###############################################################')
   print('精准率为:{:.2f} %'.format(get_precesion() * 100))
   print('###############################################################')
   print('###############################################################')
   print('误检率为:{:.2f} %'.format(get_fpr() * 100))
   print('###############################################################')
   print('###############################################################')
   print('准确率为:{:.2f} %'.format(get_accuracy() * 100))
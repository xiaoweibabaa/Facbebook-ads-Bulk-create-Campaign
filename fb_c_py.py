# encoding='gbk'
# 牛逼轰轰的广告优化师：CYY 创建。      其实一点都不牛逼，非常苦逼
# 如使用感觉不错，请推荐给其他苦逼优化师使用，但是请说明这是CYY的程序
import math
import os
import re
import time
import tkinter as tk
import tkinter.filedialog

import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy
import numpy as np
import pandas as pd
from pandas import DataFrame

# campign类型判断
text1='''
Plase input num(1 or 2):
1. campaign the same creative       
    Tips:   ad name = creative name, 
            adset name = old adset name + creative name,
            campagin name = old campagin name + creative name 

2. campaign mix creative
    Tips:   ad name = creative name, 
            when one adset hanve one ad:
                adset name = old adset name + creative name,
            other:
                adset name = old adset name
            campagin name = old campagin name + 1,2,3......

next step:Choose creative format
'''
print(text1)
cam_tye=input('your choice: ')
while re.findall('^[1-2]$',cam_tye)==[]:
    cam_tye=input('your choice: ')
    
# 素材类型判断
text2='''
Plase Choose creative format(1 or 2):
1. Video 
2. Image

next step:Choose template
'''
print(text2)
cre_frmat=input('your choice: ')
while re.findall('^[1-2]$',cre_frmat)==[]:
    cre_frmat=input('your choice: ')

# 模板读取
print('Choose template')
#########################################################################
root =tk.Tk()
root.withdraw() 
file_path = tkinter.filedialog.askopenfilename(title='Please select your template',filetypes=[('csv', '*.csv'), ('All Files', '*')])
while file_path=="":
    file_path = tkinter.filedialog.askopenfilename(title='Please select your template',filetypes=[('csv', '*.csv'), ('All Files', '*')])
root.destroy()

raw_data=pd.read_csv(r''+file_path+'',encoding='utf-16',sep='\t')
raw_data_backup=raw_data
raw_col=raw_data.columns.to_list()
raw_col.insert(len(raw_col),'image')
raw_col.insert(len(raw_col),'Video File Name')
raw_data=raw_data.reindex(columns=raw_col)

print('read template success')

# 数字判断
campaign_num=len(set(raw_data['Campaign ID']))
adset_num=len(set(raw_data['Ad Set ID']))
ad_num=len(set(raw_data['Ad ID']))
row_num=len(raw_data)

#数据处理 ID清除
raw_data['Campaign ID']=np.nan
raw_data['Ad Set ID']=np.nan
raw_data['Ad ID']=np.nan
raw_data['Video ID']=np.nan
raw_data['Preview Link']=np.nan
raw_data['Instagram Preview Link']=np.nan
raw_data['Permalink']=np.nan
raw_data['Image Hash']=np.nan
#raw_data['Ad Name']=np.nan
#raw_data['Ad Set Name']=np.nan
raw_data['Attribution Spec']=np.nan



print('data clean success')
print('choose your creative')
#######################################################
root =tk.Tk()
root.withdraw() 
cre_path = tkinter.filedialog.askdirectory()
while cre_path=='':
    cre_path = tkinter.filedialog.askdirectory()
root.destroy()
for root, dirs, files in os.walk(r''+cre_path+''):
    pass

#####################################################
if cam_tye=='1':
    if cre_frmat=='1':
        # same+video
        # 复制行
        new_data=DataFrame()
        for i in range(len(files)):
            new_data=new_data.append(raw_data)
            
        # Creative Type 赋值
        new_data['Creative Type']='Video Page Post Ad'
        
        for file_index in range(len(files)):
            # creative name 每step行数 = file
            new_data['Video File Name'][row_num*file_index:row_num*(file_index+1)]=files[file_index]

            # campaign name= oldcampaign name + creatvie name
            new_data['Campaign Name'][row_num*file_index:row_num*(file_index+1)]=new_data['Campaign Name'][row_num*file_index:row_num*(file_index+1)]+'_'+files[file_index]

        # ad_set name = old ad_set name + creatvie name
        new_data['Ad Set Name']=new_data['Ad Set Name']+'_'+new_data['Video File Name']

        # ad name = creative name
        new_data['Ad Name']=new_data['Video File Name']

    else:
        # same+image
        # 复制行
        new_data=DataFrame()
        for i in range(len(files)):
            new_data=new_data.append(raw_data)
            
        # Creative Type 赋值
        new_data['Creative Type']='Link Page Post Ad'

        for file_index in range(len(files)):
            # creative name 每step行数 = file
            new_data['image'][row_num*file_index:row_num*(file_index+1)]=files[file_index]

            # campaign name= oldcampaign name + creatvie name
            new_data['Campaign Name'][row_num*file_index:row_num*(file_index+1)]=new_data['Campaign Name'][row_num*file_index:row_num*(file_index+1)]+'_'+files[file_index]

        # ad_set name = old ad_set name + creatvie name
        new_data['Ad Set Name']=new_data['Ad Set Name']+'_'+new_data['image']

        # ad name = creative name
        new_data['Ad Name']=new_data['image']
        
else:
    if cre_frmat=='1':
        new_data=DataFrame()
        # 恢复广告组名字 此模式不改变广告组名字
        raw_data['Ad Set Name']=raw_data_backup['Ad Set Name']

        for i in range(math.ceil(len(files)/row_num)):
            new_data=new_data.append(raw_data)

        # Creative Type 赋值
        new_data['Creative Type']='Video Page Post Ad'

        # creative name
        new_data['Video File Name'][0:len(files)]=files

        # ad name = creative name
        new_data['Ad Name'][0:len(files)]=files
        #new_data['Ad Set Name'][0:len(files)]=files
        
        # campaign命名 以row_num
        for f_i in range(math.ceil(len(files)/row_num)):
            new_data['Campaign Name'][f_i*row_num:(f_i+1)*row_num] = raw_data['Campaign Name'][0]+'_'+str(f_i+1)
        
        # 一个广告组一个广告的时候，广告组赋值=广告name 其他情况，使用原
        if ad_num==adset_num:
            new_data['Ad Set Name']=new_data['Ad Set Name']+'_'+new_data['Ad Name']

        new_data=new_data.head(len(files))
    else:
        new_data=DataFrame()
        # 恢复广告组名字 此模式不改变广告组名字
        raw_data['Ad Set Name']=raw_data_backup['Ad Set Name']

        for i in range(math.ceil(len(files)/row_num)):
            new_data=new_data.append(raw_data)

        # Creative Type 赋值
        new_data['Creative Type']='Link Page Post Ad'
        # 粘贴文本
        new_data['image'][0:len(files)]=files

        #广告
        new_data['Ad Name'][0:len(files)]=files
        #new_data['Ad Set Name'][0:len(files)]=files

        # campaign命名 以row_num
        for f_i in range(math.ceil(len(files)/row_num)):
            new_data['Campaign Name'][f_i*row_num:(f_i+1)*row_num] = raw_data['Campaign Name'][0]+'_'+str(f_i+1)
        
        # 一个广告组一个广告的时候，广告组赋值=广告name 其他情况，使用原
        if ad_num==adset_num:
            new_data['Ad Set Name']=new_data['Ad Set Name']+'_'+new_data['Ad Name']

        new_data=new_data.head(len(files))
#复制到粘贴板
new_data.to_clipboard(index=False)
print('\n Congratulations! All succeeded \n')
print('\n the copy is successful, please go to FB to paste\n')

try:
    new_data.to_csv(os.path.dirname(file_path)+'//'+os.path.basename(file_path).replace('.csv','')+'_output.csv',encoding='utf-8-sig',index=False)
    print('output: '+os.path.dirname(file_path)+'//'+os.path.basename(file_path).replace('.csv','')+'_output.csv'+'')
except:
    new_data.to_csv(os.path.dirname(file_path)+'//'+os.path.basename(file_path).replace('.csv','')+'_output_2.csv',encoding='utf-8-sig',index=False)
    print('output: '+os.path.dirname(file_path)+'//'+os.path.basename(file_path).replace('.csv','')+'_output_2.csv'+'')

print( '\n © 优化师 CYY 2020 \n')
time.sleep(10)

# © 优化师 CYY 2020

import pandas as pd
# input= pd.read_csv("file:/Users/kripanshubhargava/Desktop/raven-metadata-service/preprocess/input/Testfile1.csv")
# df=input['UN']
# df.dropna(inplace=True)
# total1=len(df)
# sum=0
# for val,cnt in df.value_counts().iteritems():
#     print(val,cnt)
#     if(val==True or val==False):
#         sum=sum+cnt
#
#
# if(sum==total1):
#     print("True")
# else:print("False")

s=[1,2.3,4,5.4,34333]
df=pd.DataFrame(s)
sum=0
total=len(df[0])

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass


    return False
for val,cnt in df[0].value_counts().iteritems():

    if(is_number(val)):
       sum=sum+cnt



if (sum == total):
    print("is numeric")
else: print("is notnumeric")
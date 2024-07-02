import pandas as pd
import matplotlib.pyplot as plt

# 加载数据
data = pd.read_excel('/Users/wangxiaoran/Desktop/推特 选举造假.xlsx')

# 转换发布时间为日期时间格式
data['发布时间'] = pd.to_datetime(data['发布时间'])

# 按时间排序
data = data.sort_values('发布时间')

# 绘制时间序列图
plt.figure(figsize=(10, 6))
plt.plot(data['发布时间'], data['转推数'], label='Retweets')
plt.plot(data['发布时间'], data['点赞数'], label='Likes')
plt.plot(data['发布时间'], data['评论数'], label='Comments')
plt.title('Tweet Activity Over Time')
plt.xlabel('Time')
plt.ylabel('Count')
plt.legend()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# 加载数据
data = pd.read_excel('/Users/wangxiaoran/Desktop/推特 选举造假.xlsx')  # 替换为您的文件路径

# 假设数据中包含列：'user_nickname', 'user_followers', 'user_following', 'comment_text', 'likes', 'retweets'

# 用户影响力评分：简单地以粉丝数作为影响力的代理
data['influence_score'] = data['发布人粉丝数']

# 情绪分析
data['sentiment'] = data['推文文本'].apply(lambda text: TextBlob(text).sentiment.polarity)

# # 分析数据并准备绘图数据
# # 按用户影响力排序并取前10个
# top_influencers = data.sort_values(by='influence_score', ascending=False).head(10)
#
# # 准备情绪分析的数据
# positive_comments = data[data['sentiment'] > 0.5]
# negative_comments = data[data['sentiment'] < -0.5]
#
# # 绘制影响力分布图
# plt.figure(figsize=(10, 6))
# plt.bar(top_influencers['评论用户昵称'], top_influencers['influence_score'], color='grey')
# plt.title('Top 10 Influential Users by Followers')
# plt.xlabel('User Nickname')
# plt.ylabel('Influence Score (Followers)')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# 绘制情绪分析结果
# 计算情绪分布
sentiment_counts = data['sentiment'].apply(lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral').value_counts()

plt.figure(figsize=(8, 5))
sentiment_counts.plot(kind='bar', color=['green', 'blue', 'gray'])
plt.title('Sentiment Analysis of Comments',fontsize=14)
plt.xlabel('Sentiment',fontsize=12)
plt.ylabel('Number of Comments',fontsize=12)
plt.xticks(rotation=0)
plt.show()

data['sentiment_category'] = data['sentiment'].apply(lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral')

# 分组并计算每种情绪类别的转发和点赞平均值
sentiment_summary = data.groupby('sentiment_category')[['转推数', '点赞数']].mean()

# 可视化
fig, ax = plt.subplots(2, 1, figsize=(8, 6))  # 创建两个子图

# 子图1: 平均转发数
ax[0].bar(sentiment_summary.index, sentiment_summary['转推数'], color='skyblue')
ax[0].set_title('Average Retweets by Sentiment Category')
ax[0].set_xlabel('Sentiment Category')
ax[0].set_ylabel('Average Retweets')
ax[0].set_xticks(range(len(sentiment_summary.index)))
ax[0].set_xticklabels(sentiment_summary.index, rotation=45)

# 子图2: 平均点赞数
ax[1].bar(sentiment_summary.index, sentiment_summary['点赞数'], color='salmon')
ax[1].set_title('Average Likes by Sentiment Category')
ax[1].set_xlabel('Sentiment Category')
ax[1].set_ylabel('Average Likes')
ax[1].set_xticks(range(len(sentiment_summary.index)))
ax[1].set_xticklabels(sentiment_summary.index, rotation=45)

# 调整布局和显示图形
plt.tight_layout()
plt.show()
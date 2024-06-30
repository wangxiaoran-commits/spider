# import pandas as pd
# import matplotlib.pyplot as plt
#
# # 加载数据
# data = pd.read_excel('/Users/wangxiaoran/Desktop/cnn 选举造假.xlsx')
#
# # 定义分类
# categories = {
#     "Election Fraud Claims": ["vote rigging", "ballot tampering", "voter fraud", "election interference",
#                               "stolen election", "rigged election", "illegal voting", "voter fraud allegations",
#                               "ballot fraud", "electoral manipulation", "election tampering", "voting discrepancies", "election"],
#     "Voting Process Misinformation": ["voting machines", "ballot mishandling", "voter suppression",
#                                       "polling issues", "polling fraud", "voting errors", "miscounted votes",
#                                       "electoral fraud", "poll tampering", "voting machine error", "vote"],
#     "Misleading Statements by Politicians": ["false claims", "misleading", "deceptive", "untrue",
#                                              "political deception", "false accusations", "misinformation by politicians",
#                                              "political lies", "deceptive campaign", "trump", "biden"],
#     "Legal Challenges and Outcomes": ["lawsuit", "court ruling", "legal challenge", "Supreme Court decisions",
#                                       "legal disputes", "legal battle", "election court cases", "judicial interference",
#                                       "legal ruling on election", "electoral court decision", "court", "case", "trial"],
#     "Social Media Misinformation Spread": ["social media", "fake news", "disinformation", "viral misinformation",
#                                            "online misinformation", "social network lies", "internet fake news",
#                                            "viral deception", "misinformation online", "social media hoaxes", "campaign"]
# }
#
# # 分类文章
# def categorize_article(text):
#     max_category = "Uncategorized"
#     max_count = 0
#     text = str(text).lower()
#     for category, keywords in categories.items():
#         count = sum(keyword in text for keyword in keywords)
#         if count > max_count:
#             max_count = count
#             max_category = category
#     return max_category
#
# # 应用分类函数
# data['Category'] = data['文章'].apply(categorize_article)
#
# # 计算每个分类的文章数
# category_counts = data['Category'].value_counts()
#
# plt.grid(True)
#
# # 绘制结果图表
# fig, ax = plt.subplots(figsize=(8, 4.5))  # 创建图表对象和轴对象
# bars = ax.bar(category_counts.index, category_counts.values, color='cyan')
# plt.title('Analysis of Election-Related Coverage',fontsize=14)
# plt.xlabel('Category')
# plt.ylabel('Number of Articles')
# plt.xticks(rotation=25, fontsize=8)
# plt.subplots_adjust(bottom=0.15)
#
# # 在每个柱子上标注计数
# for bar in bars:
#     yval = bar.get_height()
#     ax.text(bar.get_x() + bar.get_width()/2-0.1, yval, int(yval), va='bottom',fontsize=12)  # va: vertical alignment
#
# plt.grid(False)
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# 加载数据
data = pd.read_excel('/Users/wangxiaoran/Desktop/cnn 选举造假.xlsx')

# 定义分类关键词
categories = {
    "Election Fraud Claims": ["vote rigging", "ballot tampering", "voter fraud", "election interference",
                              "stolen election", "rigged election", "illegal voting", "voter fraud allegations",
                              "ballot fraud", "electoral manipulation", "election tampering", "voting discrepancies", "election"],
    "Voting Process Misinformation": ["voting machines", "ballot mishandling", "voter suppression",
                                      "polling issues", "polling fraud", "voting errors", "miscounted votes",
                                      "electoral fraud", "poll tampering", "voting machine error", "vote"],
    "Misleading Statements by Politicians": ["false claims", "misleading", "deceptive", "untrue",
                                             "political deception", "false accusations", "misinformation by politicians",
                                             "political lies", "deceptive campaign", "trump", "biden"],
    "Legal Challenges and Outcomes": ["lawsuit", "court ruling", "legal challenge", "Supreme Court decisions",
                                      "legal disputes", "legal battle", "election court cases", "judicial interference",
                                      "legal ruling on election", "electoral court decision", "court", "case", "trial"],
    "Social Media Misinformation Spread": ["social media", "fake news", "disinformation", "viral misinformation",
                                           "online misinformation", "social network lies", "internet fake news",
                                           "viral deception", "misinformation online", "social media hoaxes", "campaign"]
}

# 分类文章函数
def categorize_article(text):
    max_category = "Uncategorized"
    max_count = 0
    text = str(text).lower()
    for category, keywords in categories.items():
        count = sum(keyword in text for keyword in keywords)
        if count > max_count:
            max_count = count
            max_category = category
    return max_category

# 应用分类函数
data['Category'] = data['文章'].apply(categorize_article)

# 过滤掉未分类的数据
filtered_data = data[data['Category'] != 'Uncategorized']

# 计算每个分类的文章数
category_counts = filtered_data['Category'].value_counts()

# 绘制结果图表
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(category_counts.index, category_counts.values, color='cyan')
plt.title('Analysis of Election-Related Coverage', fontsize=14)
plt.xlabel('Category')
plt.ylabel('Number of Articles')
plt.xticks(rotation=25, fontsize=8)
plt.subplots_adjust(bottom=0.15)

# 在每个柱子上标注计数
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=12)  # va: vertical alignment

plt.grid(False)
plt.show()
#148未分类
# coding=utf8
import pandas as pd
from flask import *
from flask_cors import CORS  # 导入CORS模块
from gevent import pywsgi


# 读取total_result_pure.csv文件并提取id列的前20条数据以及对应的total_rank字段
total_result = pd.read_csv('./datasets/total_result_pure.csv', encoding='utf-8')
# id_and_rank = total_result[['id', 'total_rank']].head(20)
id_and_rank = total_result[['id', 'total_rank']]

# 读取news_2024-03-02_processed.csv文件
news_data = pd.read_csv('./datasets/Data231202_processed.csv', encoding='utf-8')

# 读取website_Rank_new_FIX.csv文件
website_rank = pd.read_csv('./datasets/website_Rank_new_FIX.csv', encoding='utf-8')

# 根据id列表在news_data中读取对应id的数据
merged_data = pd.merge(id_and_rank, news_data, on='id')

# 根据website_id读取website_Rank_new_FIX.csv文件中的url字段
merged_data = pd.merge(merged_data, website_rank, on='website_id')



# 对字符串类型的字段进行编码转换
def encode_utf8(value):
    if isinstance(value, str):
        return value.encode('utf-8').decode('utf-8')
    return value

string_columns = ['url', 'request_url', 'response_url', 'category1', 'category2', 'title', 'abstract', 'body', 'images', 'md5']
merged_data[string_columns] = merged_data[string_columns].applymap(encode_utf8)


# 使用Flask创建算法接口
app = Flask(__name__)
# app.json.ensure_ascii = False  # 解决中文乱码问题  flask版本2.3.0以上使用
app.config['JSON_AS_ASCII'] = False  # 解决中文乱码问题  flask版本 2.3.0以下使用

CORS(app)  # 添加跨域支持

# 获取“综合”类别的重要新闻
@app.route('/get_data_mixed', methods=['GET'])
def get_data_MIXed():
    # 将每个id对应的数据包装成json格式
    # test_json = [{"artId":20171864,"artTitle":"\n\tচট্টগ্রামে ইফতার সামগ্রী বিতরণ \nদেশের মানুষকে গরিব বানিয়ে দিয়েছে সরকার : ডা: শাহাদাত \n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":710,"afcArtId":20171864,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168120,"artTitle":"\n\nহাইতির প্রধানমন্ত্রী এরিয়েল হেনরির পদত্যাগ\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":653,"afcArtId":20168120,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168002,"artTitle":"\n\nহুমকি পেলে পারমাণবিক অস্ত্র ব্যবহারে প্রস্তুত রাশিয়া : পুতিন\n","artContent":None,"artSpider":"","artType":"আন্তর্জাতিক","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/article/202403/821057_163.jpg\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":641,"afcArtId":20168002,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20349885,"artTitle":"\n\nএমভি আব্দুল্লাহর চিফ অফিসার আতিক উল্লাহ খানের পরিবারের সবাই চিন্তিত\n","artContent":None,"artSpider":"","artType":"দেশ","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":1048,"afcArtId":20349885,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20171711,"artTitle":"\n\nবড়লেখায় পাহাড় কেটে রাস্তা সম্প্রসারণে বেরিয়ে এলো বিরল শিলাখণ্ড \n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":692,"afcArtId":20171711,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20171791,"artTitle":"\n\nপিডব্লিউডি জয়ী\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":702,"afcArtId":20171791,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168169,"artTitle":"\n\nইসলামে কেন রোজার প্রবর্তন\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":664,"afcArtId":20168169,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20349885,"artTitle":"\n\nএমভি আব্দুল্লাহর চিফ অফিসার আতিক উল্লাহ খানের পরিবারের সবাই চিন্তিত\n","artContent":None,"artSpider":"","artType":"দেশ","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":1048,"afcArtId":20349885,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None}]
    result_json = []
    for index, row in merged_data.iterrows():
        data_dict = {
            'artId': row['id'],
            'total_rank': row['total_rank'],
            'websiteUrl': row['url'],
            'website_id': row['website_id'],
            'request_url': row['request_url'],
            'response_url': row['response_url'],
            'artType': row['category1'],
            # 'category2': row['category2'],
            'artTitle': row['title'],
            'abstract': row['abstract'],
            'artContent': row['body'],
            'artTime': row['pub_time'],
            'cole_time': row['cole_time'],
            'artImageUrl': row['images'],
            'language_id': row['language_id'],
            'md5': row['md5'],
            'artCusId': 582,
            # test
            "customer": {"cusId": 582, "cusName": "admin",
                         "cusPass": None,
                         "cusSpider": "",
                         "cusAvatarUrl": "http://localhost:8080/img/Man.png",
                         "cusStyle": "这个人很懒, 什么都没写",
                         "cusGender": 0,
                         "cusTime": "2024-03-14T21:53:09.000+0000", "cusLegal": 0},
            "artFeature": {"afcId": 710, "afcArtId": 20171864,
                           "afcLikeNum": 0, "afcDislikeNum": 0,
                           "afcComNum": 0, "afcRepNum": 0,
                           "afcReadNum": 0,
                           "afcArtTime": None},
            "cusArtBehavior": None
        }
        result_json.append(data_dict)

    # 获取 URL 参数中的参数值
    artType = request.args.get('artType')
    page = request.args.get('page')
    pageSize = request.args.get('pageSize')
    # artType: artType,
    # page: page,
    # pageSize: pageSize
    print(artType)
    print(page)
    print(pageSize)
    # data = {
    #     'code': '200',
    #     'message': 'success',
    #     'news': result_json
    # }
    # response = jsonify(data)
    response = jsonify(result_json)
    # response = jsonify(test_json)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    # return response.data.decode('utf-8')  # 将字节串解码为UTF-8字符串
    return response  # 将字节串解码为UTF-8字符串


# 获取“综合”类别的重要新闻
@app.route('/get_data_by_type', methods=['GET'])
def get_data_ByType():
    # 获取 URL 参数中的参数值
    artType = request.args.get('artType')
    page = request.args.get('page')
    pageSize = request.args.get('pageSize')
    # artType: artType,
    # page: page,
    # pageSize: pageSize
    print(artType)
    print(page)
    print(pageSize)

    if artType != "综合":
        # 筛选类别category1为“test”的数据
        filtered_data = merged_data[merged_data['category1'] == artType]
    else:
        filtered_data = merged_data

    # 读取时读全部 然后选择时按照pageSize进行选择显示
    print(type(pageSize))
    filtered_data = filtered_data.head(int(pageSize))

    # 将每个id对应的数据包装成json格式
    # test_json = [{"artId":20171864,"artTitle":"\n\tচট্টগ্রামে ইফতার সামগ্রী বিতরণ \nদেশের মানুষকে গরিব বানিয়ে দিয়েছে সরকার : ডা: শাহাদাত \n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":710,"afcArtId":20171864,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168120,"artTitle":"\n\nহাইতির প্রধানমন্ত্রী এরিয়েল হেনরির পদত্যাগ\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":653,"afcArtId":20168120,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168002,"artTitle":"\n\nহুমকি পেলে পারমাণবিক অস্ত্র ব্যবহারে প্রস্তুত রাশিয়া : পুতিন\n","artContent":None,"artSpider":"","artType":"আন্তর্জাতিক","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/article/202403/821057_163.jpg\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":641,"afcArtId":20168002,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20349885,"artTitle":"\n\nএমভি আব্দুল্লাহর চিফ অফিসার আতিক উল্লাহ খানের পরিবারের সবাই চিন্তিত\n","artContent":None,"artSpider":"","artType":"দেশ","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":1048,"afcArtId":20349885,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20171711,"artTitle":"\n\nবড়লেখায় পাহাড় কেটে রাস্তা সম্প্রসারণে বেরিয়ে এলো বিরল শিলাখণ্ড \n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":692,"afcArtId":20171711,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20171791,"artTitle":"\n\nপিডব্লিউডি জয়ী\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":702,"afcArtId":20171791,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168169,"artTitle":"\n\nইসলামে কেন রোজার প্রবর্তন\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":664,"afcArtId":20168169,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20349885,"artTitle":"\n\nএমভি আব্দুল্লাহর চিফ অফিসার আতিক উল্লাহ খানের পরিবারের সবাই চিন্তিত\n","artContent":None,"artSpider":"","artType":"দেশ","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":1048,"afcArtId":20349885,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None}]
    result_json = []
    # for index, row in merged_data.iterrows():
    for index, row in filtered_data.iterrows():
        data_dict = {
            'artId': row['id'],
            'total_rank': row['total_rank'],
            'websiteUrl': row['url'],
            'website_id': row['website_id'],
            'request_url': row['request_url'],
            'response_url': row['response_url'],
            'artType': row['category1'],
            # 'category2': row['category2'],
            'artTitle': row['title'],
            'abstract': row['abstract'],
            'artContent': row['body'],
            'artTime': row['pub_time'],
            'cole_time': row['cole_time'],
            'artImageUrl': row['images'],
            'language_id': row['language_id'],
            'md5': row['md5'],
            'artCusId': 582,
            # test
            "customer": {"cusId": 582, "cusName": "admin",
                         "cusPass": None,
                         "cusSpider": "",
                         "cusAvatarUrl": "http://localhost:8080/img/Man.png",
                         "cusStyle": "这个人很懒, 什么都没写",
                         "cusGender": 0,
                         "cusTime": "2024-03-14T21:53:09.000+0000", "cusLegal": 0},
            "artFeature": {"afcId": 710, "afcArtId": 20171864,
                           "afcLikeNum": 0, "afcDislikeNum": 0,
                           "afcComNum": 0, "afcRepNum": 0,
                           "afcReadNum": 0,
                           "afcArtTime": None},
            "cusArtBehavior": None
        }
        result_json.append(data_dict)

    # data = {
    #     'code': '200',
    #     'message': 'success',
    #     'news': result_json
    # }
    # response = jsonify(data)
    response = jsonify(result_json)
    # response = jsonify(test_json)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    # return response.data.decode('utf-8')  # 将字节串解码为UTF-8字符串
    return response  # 将字节串解码为UTF-8字符串

@app.route('/type', methods=['GET'])
def get_Categorys():
    # # 统计category1不同类别的种类数
    # category_counts = merged_data['category1'].value_counts().to_dict()

    # 提取category1列并转换为列表，并去重
    category_list = merged_data['category1'].unique().tolist()

    # 在列表的最前面加入一个元素"综合"
    category_list.insert(0, '综合')

    return jsonify(category_list)

# 返回完整文章内容
@app.route('/main', methods=['GET'])
def get_ArtMain():
    # 获取artId参数的值
    artId = request.args.get('artId')

    # 根据artId筛选数据
    filtered_data = merged_data[merged_data['id'] == int(artId)]

    # 将每个id对应的数据包装成json格式
    # test_json = [{"artId":20171864,"artTitle":"\n\tচট্টগ্রামে ইফতার সামগ্রী বিতরণ \nদেশের মানুষকে গরিব বানিয়ে দিয়েছে সরকার : ডা: শাহাদাত \n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":710,"afcArtId":20171864,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168120,"artTitle":"\n\nহাইতির প্রধানমন্ত্রী এরিয়েল হেনরির পদত্যাগ\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":653,"afcArtId":20168120,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168002,"artTitle":"\n\nহুমকি পেলে পারমাণবিক অস্ত্র ব্যবহারে প্রস্তুত রাশিয়া : পুতিন\n","artContent":None,"artSpider":"","artType":"আন্তর্জাতিক","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/article/202403/821057_163.jpg\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":641,"afcArtId":20168002,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20349885,"artTitle":"\n\nএমভি আব্দুল্লাহর চিফ অফিসার আতিক উল্লাহ খানের পরিবারের সবাই চিন্তিত\n","artContent":None,"artSpider":"","artType":"দেশ","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":1048,"afcArtId":20349885,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20171711,"artTitle":"\n\nবড়লেখায় পাহাড় কেটে রাস্তা সম্প্রসারণে বেরিয়ে এলো বিরল শিলাখণ্ড \n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":692,"afcArtId":20171711,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20171791,"artTitle":"\n\nপিডব্লিউডি জয়ী\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":702,"afcArtId":20171791,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168169,"artTitle":"\n\nইসলামে কেন রোজার প্রবর্তন\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":664,"afcArtId":20168169,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20349885,"artTitle":"\n\nএমভি আব্দুল্লাহর চিফ অফিসার আতিক উল্লাহ খানের পরিবারের সবাই চিন্তিত\n","artContent":None,"artSpider":"","artType":"দেশ","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":1048,"afcArtId":20349885,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None}]
    result_dict = {}
    # for index, row in merged_data.iterrows():
    for index, row in filtered_data.iterrows():
        data_dict = {
            'artId': row['id'],
            'total_rank': row['total_rank'],
            'websiteUrl': row['url'],
            'website_id': row['website_id'],
            'request_url': row['request_url'],
            'response_url': row['response_url'],
            'artType': row['category1'],
            # 'category2': row['category2'],
            'artTitle': row['title'],
            'abstract': row['abstract'],
            'artContent': row['body'],
            'artTime': row['pub_time'],
            'cole_time': row['cole_time'],
            'artImageUrl': row['images'],
            'language_id': row['language_id'],
            'md5': row['md5'],
            'artCusId': 582,
            # test
            "customer": {"cusId": 582, "cusName": "admin",
                         "cusPass": None,
                         "cusSpider": "",
                         "cusAvatarUrl": "http://localhost:8080/img/Man.png",
                         "cusStyle": "这个人很懒, 什么都没写",
                         "cusGender": 0,
                         "cusTime": "2024-03-14T21:53:09.000+0000", "cusLegal": 0},
            "artFeature": {"afcId": 710, "afcArtId": 20171864,
                           "afcLikeNum": 0, "afcDislikeNum": 0,
                           "afcComNum": 0, "afcRepNum": 0,
                           "afcReadNum": 0,
                           "afcArtTime": None},
            "cusArtBehavior": None
        }

        result_dict = data_dict
        # result_json.append(data_dict)

    # data = {
    #     'code': '200',
    #     'message': 'success',
    #     'news': result_json
    # }
    # response = jsonify(data)
    # response = jsonify(result_json)
    response = jsonify(result_dict)
    # response = jsonify(test_json)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    # return response.data.decode('utf-8')  # 将字节串解码为UTF-8字符串
    return response  # 将字节串解码为UTF-8字符串

    # 将筛选出的数据转换为字典形式
    # data_dict = filtered_data.to_dict(orient='records')

    # return jsonify(data_dict)

# 右侧推荐新闻处 随机返回pageSize条新闻
@app.route('/random_art', methods=['GET'])
def get_randomArt():
    # 获取 URL 参数中的参数值
    # artType = request.args.get('artType')
    page = request.args.get('page')
    pageSize = request.args.get('pageSize')
    # artType: artType,
    # page: page,
    # pageSize: pageSize
    # print(artType)
    print(page)
    print(pageSize)

    # 随机选取数据
    sample_data = merged_data.sample(n=min(int(pageSize), len(merged_data)))

    # 将每个id对应的数据包装成json格式
    # test_json = [{"artId":20171864,"artTitle":"\n\tচট্টগ্রামে ইফতার সামগ্রী বিতরণ \nদেশের মানুষকে গরিব বানিয়ে দিয়েছে সরকার : ডা: শাহাদাত \n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":710,"afcArtId":20171864,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168120,"artTitle":"\n\nহাইতির প্রধানমন্ত্রী এরিয়েল হেনরির পদত্যাগ\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":653,"afcArtId":20168120,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168002,"artTitle":"\n\nহুমকি পেলে পারমাণবিক অস্ত্র ব্যবহারে প্রস্তুত রাশিয়া : পুতিন\n","artContent":None,"artSpider":"","artType":"আন্তর্জাতিক","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/article/202403/821057_163.jpg\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":641,"afcArtId":20168002,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20349885,"artTitle":"\n\nএমভি আব্দুল্লাহর চিফ অফিসার আতিক উল্লাহ খানের পরিবারের সবাই চিন্তিত\n","artContent":None,"artSpider":"","artType":"দেশ","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":1048,"afcArtId":20349885,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20171711,"artTitle":"\n\nবড়লেখায় পাহাড় কেটে রাস্তা সম্প্রসারণে বেরিয়ে এলো বিরল শিলাখণ্ড \n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":692,"afcArtId":20171711,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20171791,"artTitle":"\n\nপিডব্লিউডি জয়ী\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":702,"afcArtId":20171791,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20168169,"artTitle":"\n\nইসলামে কেন রোজার প্রবর্তন\n","artContent":None,"artSpider":"","artType":"আজকের পত্রিকা","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":664,"afcArtId":20168169,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None},{"artId":20349885,"artTitle":"\n\nএমভি আব্দুল্লাহর চিফ অফিসার আতিক উল্লাহ খানের পরিবারের সবাই চিন্তিত\n","artContent":None,"artSpider":"","artType":"দেশ","artTags":"","artImageUrl":"[\"https://www.dailynayadiganta.com/resources/img/sitesetup/1_1.png\"]","artTime":"2024-03-13T00:00:00.000+0000","artLegal":0,"artCusId":582,"websiteId":None,"websiteUrl":None,"customer":{"cusId":582,"cusName":"admin","cusPass":None,"cusSpider":"","cusAvatarUrl":"http://localhost:8080/img/Man.png","cusStyle":"这个人很懒, 什么都没写","cusGender":0,"cusTime":"2024-03-14T21:53:09.000+0000","cusLegal":0},"artFeature":{"afcId":1048,"afcArtId":20349885,"afcLikeNum":0,"afcDislikeNum":0,"afcComNum":0,"afcRepNum":0,"afcReadNum":0,"afcArtTime":None},"cusArtBehavior":None}]
    result_json = []
    # for index, row in merged_data.iterrows():
    for index, row in sample_data.iterrows():
        data_dict = {
            'artId': row['id'],
            'total_rank': row['total_rank'],
            'websiteUrl': row['url'],
            'website_id': row['website_id'],
            'request_url': row['request_url'],
            'response_url': row['response_url'],
            'artType': row['category1'],
            # 'category2': row['category2'],
            'artTitle': row['title'],
            'abstract': row['abstract'],
            'artContent': row['body'],
            'artTime': row['pub_time'],
            'cole_time': row['cole_time'],
            'artImageUrl': row['images'],
            'language_id': row['language_id'],
            'md5': row['md5'],
            'artCusId': 582,
            # test
            "customer": {"cusId": 582, "cusName": "admin",
                         "cusPass": None,
                         "cusSpider": "",
                         "cusAvatarUrl": "http://localhost:8080/img/Man.png",
                         "cusStyle": "这个人很懒, 什么都没写",
                         "cusGender": 0,
                         "cusTime": "2024-03-14T21:53:09.000+0000", "cusLegal": 0},
            "artFeature": {"afcId": 710, "afcArtId": 20171864,
                           "afcLikeNum": 0, "afcDislikeNum": 0,
                           "afcComNum": 0, "afcRepNum": 0,
                           "afcReadNum": 0,
                           "afcArtTime": None},
            "cusArtBehavior": None
        }
        result_json.append(data_dict)

    # data = {
    #     'code': '200',
    #     'message': 'success',
    #     'news': result_json
    # }
    # response = jsonify(data)
    response = jsonify(result_json)
    # response = jsonify(test_json)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    # return response.data.decode('utf-8')  # 将字节串解码为UTF-8字符串
    return response  # 将字节串解码为UTF-8字符串


if __name__ == '__main__':
    # app.run(debug=True)
    server = pywsgi.WSGIServer(('127.0.0.1', 9997), app)
    server.serve_forever()
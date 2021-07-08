import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random 


def getInfoByCSDN(tar, nums, whole_len):
    #爬取CSDN的函数
    #args:tar为爬取的目标网站和名字字典列表
    header = {"user-agent": "Mozilla/5.0", "cookie":"uuid_tt_dd=10_37459425890-1625618977533-167909; dc_session_id=10_1625618977533.352233; c_first_ref=cn.bing.com; c_first_page=https%3A//www.csdn.net/; c_segment=5; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1625555559,1625556872,1625561900,1625618982; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22UIBE_day_day_up%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_37459425890-1625618977533-167909!5744*1*UIBE_day_day_up; dc_sid=eccbc958d63e1e10f68c7bcbb71b7cf0; TY_SESSION_ID=cecb974d-0240-49d6-bfbd-0220f724d45f; c_pref=https%3A//cn.bing.com/; c_ref=https%3A//www.csdn.net/; c_page_id=default; dc_tos=qvunmy; log_Id_pv=2; c-login-auto=1; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1625618987; firstDie=1; log_Id_view=5; log_Id_click=2"}
    header["cookie"] = r"uuid_tt_dd=10_37459425890-1625618977533-167909; dc_session_id=10_1625618977533.352233; c_first_ref=cn.bing.com; c_first_page=https%3A//www.csdn.net/; c_segment=5; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1625555559,1625556872,1625561900,1625618982; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22UIBE_day_day_up%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_37459425890-1625618977533-167909!5744*1*UIBE_day_day_up; dc_sid=eccbc958d63e1e10f68c7bcbb71b7cf0; TY_SESSION_ID=cecb974d-0240-49d6-bfbd-0220f724d45f; c_pref=https%3A//cn.bing.com/; c_ref=https%3A//www.csdn.net/; c_page_id=default; dc_tos=qvunmy; log_Id_pv=2; c-login-auto=1; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1625618987; firstDie=1; log_Id_view=5; log_Id_click=2"
    description_lst = []
    num = 0 + nums
    for item in tar:
        time.sleep(random.random()*2)
        try:
            time_now = time.time()
            r = requests.get(item["url"], headers = header).text
            soup = BeautifulSoup(r)
            user_dic = {}
            user_dic["user"] = item["nickName"]
            user_dic["title"] = soup.find("title").text
            first_des = soup.find("p", class_ = "description")
            other = soup.find("div", class_ = "user-profile-head-introduction")
            if other == None and first_des == None:
                print("CSDN:{}无简介".format(user_dic["user"]))        
            elif other == None:
                user_dic["descrip"] = first_des.text
            elif first_des == None:
                user_dic["descrip"] = other.find("p").text
            else:
                user_dic["descrip"] = other.find("p").text + first_des.text
            four_base_info = soup.find("div", class_ = "user-profile-head-info-b")
            if four_base_info == None:
                #说明是B类主页
                head_info_lst = soup.find("div", class_ = "aside-box")
                work_age = head_info_lst.find("span", class_ = "personal-home-page personal-home-years").text
                five_info_lst = head_info_lst.find_all("div", class_ = "data-info d-flex item-tiling")
                five_infos_1 = five_info_lst[0].find_all("dl")
                five_infos_2 = five_info_lst[1].find_all("dl")
                user_dic["访问量"] = five_infos_1[3].find("span").text
                user_dic["博客数"] = five_infos_1[0].find("span").text
                user_dic["排名"] = five_infos_1[2].find("span").text
                user_dic["粉丝数"] = five_infos_2[1].find("span").text
                user_dic["加入时间"] = work_age
                user_dic["积分"] = five_infos_2[0].find("span").text
                user_dic["主页类型"] = "B"
            else:
                four_base_info_lst = soup.find("div", class_ = "user-profile-head-info-b").find_all("div", class_ = "user-profile-statistics-num")
                user_dic["访问量"] = four_base_info_lst[0].text
                user_dic["博客数"] = four_base_info_lst[1].text
                user_dic["排名"] = four_base_info_lst[2].text
                user_dic["粉丝数"] = four_base_info_lst[3].text
                user_dic["加入时间"] = soup.find("li", class_ = "user-general-info-join-csdn").find("span", class_ = "user-general-info-key-word").text
                try:
                    honor = ""
                    honour_lst = soup.find("div", class_ = "aside-common-box-content").find_all("li")
                    for honour in honour_lst:
                        honor += honour.find("div").text
                    user_dic["成就"] = honor
                except AttributeError:
                    print("该用户没有成就")
                try:
                    skill = ""
                    area_block = soup.find("div", class_ = "user-interest-area user-profile-aside-common-box")
                    if area_block == None:
                        print("该用户没有专栏")
                    else:    
                        area_lst = area_block.find_all("li")
                        for area in area_lst:
                            if area.find("div", class_ = "interest-area-name") != None:
                                skill += area.find("div", class_ = "interest-area-name").text
                                skill += ":"
                                small_skill = area.find("div", class_ = "interest-area-sub")
                                if small_skill == None:
                                    continue
                                else:
                                    small_skill_lst = small_skill.find_all("span")
                                    for each_small_skill in small_skill_lst:
                                        skill += each_small_skill.text
                            else:
                                continue
                    user_dic["领域"] = skill
                except AttributeError:
                    print("该用户没有领域信息")
                user_dic["主页类型"] = "A"
            user_dic["url"] = item["url"]
            description_lst.append(user_dic)
            num += 1
            print("CSDN:完成第{}/{}个".format(num, whole_len))
        except AttributeError:
            print("出现属性错误")
            time.sleep(5)
            num += 1
            continue
        except Exception as e:
            print("CSDN:程序出现问题！已返回现爬取结果")
            print(repr(e))
            print("现爬取进度为第{}/{}个".format(num, whole_len))
            break
    return description_lst

name_file = input("请输入待读取UserName文件地址：")
num = input("请输入数据的序号：")
start = input("请输入开始爬取的板块数：")
print(num)
name_lst = list(set(list(pd.read_csv(name_file)["0"])))
tar = []
whole_len = len(name_lst)
for i in range(int(start), len(name_lst) // 10):
    tar = []
    for name in name_lst[i*10:(i+1)*10]:
        now_user = {}
        url= r"https://blog.csdn.net/" + name
        now_user["nickName"] = name
        now_user["url"] = url
        tar.append(now_user)
    # try:
    nums = i*10
    print(nums, i)
    descrip = getInfoByCSDN(tar, nums, whole_len)
    data = pd.DataFrame(descrip, columns = ['user', 'title', 'descrip', '访问量', '博客数', '排名', '粉丝数', '加入时间', '成就',
       '领域', '主页类型', 'url', '积分'])
    data.to_csv(r"data{}.csv".format(num), mode = "a")
    print("写入成功")
    # except:
        # print("出现错误")
        # break

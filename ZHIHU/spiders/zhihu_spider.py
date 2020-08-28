# -*- coding: utf-8 -*-


import scrapy
from scrapy import Request
import json
import sys
from ..items import question_ZhihuItem,answer_ZhihuItem

HEADERS = {
    'cookie':'_zap=cd9b859d-c2ca-4ccf-b355-e0dc35425660; d_c0="AAAYsK_TpxGPTlnzV5L_kej23Geki2aiqKg=|1596100448"; _ga=GA1.2.838386912.1596100451; _xsrf=59e52bfe-76c2-4221-822c-fdf88ed148ba; _gid=GA1.2.184786581.1597297153; capsion_ticket="2|1:0|10:1597305912|14:capsion_ticket|44:ZWZjNzI5MGE5ZDQyNDYyZTk5ZjA2YTY2Mzc4NTVjMTI=|acd96b4837f1f2f17aebdcb8c1d759b8614badc7e3a83170fd7cf19e66a31fcc"; z_c0="2|1:0|10:1597305913|4:z_c0|92:Mi4xOFFqTUhRQUFBQUFBQUJpd3I5T25FU1lBQUFCZ0FsVk5PVUlpWUFEa1dFeDNabUk3UEtRZzk4Tmxwd1U5QlJUbW13|bab39d26561a35c649525e7e980f5dd4f57e8327d3d699bc7896c636e8d1e395"; tshl=; tst=r; q_c1=dda930ef481c4b2aa5e62c418b4aa2be|1597306076000|1597306076000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1597032274,1597297153,1597308468,1597309404; SESSIONID=RCnNPrPFRbVbuSmFQGWttxDVI1OAOpUcPauQPoF3VOU; JOID=UV4TCk6zV5SqfDw2drnUjV3E5Z9i5BT16CpLZj_nMMLHBWleMGpZov9_OTl1YuPhnyioHb4KK_k62KaRaCo9lbQ=; osd=VFwTBkK2VZSmcDk0drXYiF_E6ZNn5hT55C9JZjPrNcDHCWVbMmpVrvp9OTV5Z-HhkyStH74GJ_w42KqdbSg9mbg=; __utma=155987696.838386912.1596100451.1597329949.1597329949.1; __utmc=155987696; __utmz=155987696.1597329949.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1597381376; KLBRSID=9d75f80756f65c61b0a50d80b4ca9b13|1597386414|1597386405',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept-language:':'zh-CN,zh;q=0.9',
    # 'accept-encoding':'gzip, deflate, br',
    'referer':'https://www.zhihu.com/',
    'x-ab-param':'se_videobox=2;tp_topic_tab_new=0-0-0;tp_dingyue_video=0;li_panswer_topic=0;zr_km_answer=open_cvr;se_major=0;se_club_ui=0;li_car_meta=1;li_yxxq_aut=A1;top_universalebook=1;se_v054=0;tp_header_style=1;top_quality=0;li_viptab_name=0;zr_training_first=false;zr_expslotpaid=1;se_wil_act=0;ug_follow_topic_1=2;zw_sameq_sorce=999;se_zp_boost=1;se_v_v005=0;pf_foltopic_usernum=50;se_hi_trunc=0;tp_club_entrance=1;tsp_ad_cardredesign=0;pf_noti_entry_num=2;se_click_v_v=1;se_college=default;tsp_ios_cardredesign=0;li_ebook_gen_search=2;se_entity22=1;ls_video_commercial=0;tp_fenqu_wei=1;pf_fuceng=1;top_v_album=1;li_video_section=0;se_vbert3=0;se_topicfeed=0;se_merge=0;tsp_ioscard2=0;li_svip_tab_search=1;zr_search_paid=1;se_preset=0;tp_m_intro_re_topic=1;tp_flow_ctr=0;pf_newguide_vertical=0;se_major_v2=0;tp_meta_card=0;tp_contents=2;qap_question_visitor= 0;zr_topic_rpc=0;se_adsrank=4;se_searchwiki=0;pf_adjust=1;zr_rec_answer_cp=open;se_usercard=0;tp_club_top=0;tp_discover=1;tp_clubhyb=0;top_test_4_liguangyi=1;li_svip_cardshow=1;zr_intervene=0;se_aa_base=0;se_sug_term=0;se_guess=0;li_answer_card=0;li_sp_mqbk=0;se_whitelist=1;se_v_v006=0;se_v058=0;se_recommend=0;tp_zrec=1;ug_newtag=1;li_catalog_card=1;zr_sim3=0;top_ebook=0;tsp_adcard2=0;tp_topic_style=0;li_topics_search=0;li_vip_verti_search=0;se_auth_src=0;ls_recommend_test=4;zr_training_boost=false;se_v053=1;tp_club_qa_entrance=1;tp_club__entrance2=1;pf_profile2_tab=0;zr_slotpaidexp=8;se_col_boost=1;se_colorfultab=1;se_return_1=0;tp_sft=a;tp_topic_tab=0;tp_club_feed=0;zr_slot_training=2;se_sug_dnn=1;top_root=0;li_paid_answer_exp=0;se_t2sug=1;qap_question_author=0;se_mobilecard=0;tsp_hotlist_ui=3;soc_feed_intelligent=3;soc_notification=1;pf_creator_card=1;ls_videoad=2;li_edu_page=old;qap_labeltype=1;se_v057=0;ls_fmp4=0;li_pl_xj=0;li_yxzl_new_style_a=1;se_ffzx_jushen1=0;se_auth_src2=0',
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-origin',
    'x-ab-pb':'Cg6cCiUKtAq9CicKmwqhChIHAQUAAAYAAA==',
    'x-api-version':'3.0.53',
    'x-requested-with':'fetch',
    'x-zse-83':'3_2.0',
    'x-zse-86':'1.0_aLY0SHH8e_Fx282q1TS0Q7L0nhFYS_SqTG2qUr90FUtY',
}

class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allowed_domains = ['www.zhihu.com']
    # start_urls = ['http://www.zhihu.com/']

    def start_requests(self):
        start_urls = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=3fd6e04ae59bfe887e4ff5d9459bb254&desktop=true&page_number=2&limit=6&action=down&after_id=5&ad_interval=-1'
        for i in range(10):
            yield Request(url=start_urls,callback=self.parse,headers=HEADERS,dont_filter=True,method='GET')

    def parse(self, response):
        # text = response.text
        # print(text)
        # global answer_count
        quwstion_info = json.loads(response.body)
        # print(quwstion_info)
        datas = quwstion_info['data']

        for data in datas:
            item = question_ZhihuItem()
            # 创建时间
            created_time = data.get('created_time')
            item['created_time'] = created_time
            print(created_time)
            # 更新时间
            updated_time = data.get('updated_time')
            item['updated_time'] = updated_time
            print(updated_time)

            target = data.get('target')
            print(target)
            if target:
                questions = target.get('question')
                print(questions)
                # 提问相关内容
                q_content = target.get('content')
                item['q_content'] = q_content
                print(q_content)
                # 节选
                q_excerpt = target.get('excerpt')
                item['q_excerpt'] = q_excerpt
                print(q_excerpt)
                # 新节选
                q_excerpt_new = target.get('excerpt_new')
                item['q_excerpt_new'] = q_excerpt_new
                print(q_excerpt_new)
                # 访问次数
                visited_count = target.get('visited_count')
                item['visited_count'] = visited_count
                print(visited_count)
                # 回答者id
                answer_id = target.get('id')
                item['answer_id'] = answer_id
                print(answer_id)
                # yield item
                # 提问id
                if questions:
                    question_id = questions.get('id')
                    print(question_id)
                    # 提问人姓名
                    item['question_id'] = question_id
                    author = questions.get('author')
                    # 提问标题
                    title = questions.get('title')
                    item['title'] = title
                    print(title)
                    # 回答数
                    answer_count = questions.get('answer_count')
                    item['answer_count'] = answer_count
                    print(answer_count)
                    # 评论数
                    c_count = questions.get('comment_count')
                    item['c_count'] = c_count
                    print(c_count)
                    if author:
                        question_name = author.get('name')
                        print(question_name)
                        item['question_name'] = question_name
                        # 大字标题，提问人座右铭
                        q_headline = author.get('headline')
                        item['q_headline'] = q_headline
                        print(q_headline)

                    yield item
                    for offset in range(3, answer_count, 5):
                        new_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={}&platform=desktop&sort_by=default".format(str(question_id),str(offset))
                        print(new_url)
                        yield Request(url=new_url,callback=self.parse_item1,headers=HEADERS,method='GET')
                    else:
                        pass
                else:
                    pass
            else:
                pass



            # item['question_id'] = question_id
            # item['question_name'] = question_name
            # item['q_headline'] = q_headline
            # item['title'] = title
            # item['q_content'] = q_content
            # item['q_excerpt'] = q_excerpt
            # item['q_excerpt_new'] = q_excerpt_new
            # item['answer_count'] = answer_count
            # item['c_count'] = c_count
            # item['created_time'] = created_time
            # item['updated_time'] = updated_time
            # item['visited_count'] = visited_count
            # item['answer_id'] = answer_id
            # print(item)
            # yield item
            # for offset in range(3, answer_count, 5):
            #     new_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={}&platform=desktop&sort_by=default".format(str(question_id),str(answer_count))
            #     print(new_url)
            #     yield Request(url=new_url,callback=self.parse_item1,headers=HEADERS,method='GET')

    def parse_item1(self,response):
        answer_info = json.loads(response.body)
        print(answer_info)
        datas = answer_info['data']
        for data in datas:
            item = answer_ZhihuItem()

            question = data['question']
            #回复的问题名称
            Rely_q_title = question['title']
            print(Rely_q_title)
            #回复人的姓名
            author = data['author']
            author_name = author['name']
            print(author_name)
            #回复人的标签
            a_headline= author['headline']
            print(a_headline)
            #节选
            a_excerpt = data['excerpt']
            print(a_excerpt)
            #回复内容
            a_content = data['content']
            print(a_content)
            #回复创建时间
            created_time = data['created_time']
            print(created_time)
            #回复更新时间
            updated_time = data['updated_time']
            print(updated_time)
            #点赞数
            comment_count = data['comment_count']
            print(comment_count)

            item['Rely_q_title'] = Rely_q_title
            item['author_name'] = author_name
            item['a_headline'] = a_headline
            item['a_excerpt'] = a_excerpt
            item['a_content'] = a_content
            item['created_time'] = created_time
            item['updated_time'] = updated_time
            item['comment_count'] = comment_count
            yield item

        pass


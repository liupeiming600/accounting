import csv
import os
from datetime import datetime
from collections import defaultdict

# 你提供的原始数据
data = """日期	类型	分类	金额	币种	账户	商户	备注
2025-06-01	支出	外食	780	JPY	三井NL
2025-06-01	支出	日用品	2980	JPY	三井master
2025-06-01	支出	外食	950	JPY	现金
2025-06-01	支出	买菜	819	JPY	乐天Pay
2025-06-02	支出	买菜	1131	JPY	三井NL
2025-06-02	支出	日用品	295	JPY	乐天Pay
2025-06-02	支出	娱乐	500	JPY	三井NL
2025-06-02	支出	外食	1100	JPY	现金
2025-06-02	支出	交通费	636	JPY	suica
2025-06-02	支出	外食	2372	JPY	AmexGold
2025-06-03	支出	外食	2010	JPY	支付宝
2025-06-03	支出	交通费	292	JPY	suica
2025-06-03	支出	外食	1100	JPY	三井Olive
2025-06-04	支出	外食	760	JPY	三井Olive
2025-06-04	支出	医疗	1299	JPY	乐天Pay
2025-06-04	支出	外食	800	JPY	支付宝
2025-06-04	支出	交通费	292	JPY	suica
2025-06-05	支出	外食	550	JPY	三井NL
2025-06-05	支出	外食	1150	JPY	乐天Pay
2025-06-05	支出	日用品	4226	JPY	乐天Pay
2025-06-06	支出	外食	1730	JPY	支付宝
2025-06-06	支出	外食	560	JPY	三井NL
2025-06-07	支出	医疗	1529	JPY	乐天Pay
2025-06-07	支出	日用品	1979	JPY	其他
2025-06-07	支出	外食	540	JPY	乐天Pay
2025-06-08	支出	外食	585	JPY	AmexGold
2025-06-08	支出	日用品	938	JPY	乐天Pay
2025-06-08	支出	外食	780	JPY	三井Olive
2025-06-08	支出	外食	1420	JPY	支付宝
2025-06-08	支出	买菜	298	JPY	乐天Pay
2025-06-08	收入	游戏	3520	JPY
2025-06-08	支出	交通费	356	JPY	suica
2025-06-09	支出	外食	550	JPY	三井NL
2025-06-09	支出	医疗	3364	JPY	乐天Pay
2025-06-09	支出	外食	890	JPY	乐天Pay
2025-06-09	支出	医疗	2080	JPY	乐天Pay
2025-06-10	支出	外食	1480	JPY	现金
2025-06-10	支出	买菜	236	JPY	乐天Pay
2025-06-10	支出	外食	364	JPY	乐天Pay
2025-06-10	支出	买菜	5200	JPY	三井master
2025-06-11	支出	光热费	4873	JPY	AmexGold
2025-06-11	支出	外食	2590	JPY	AmexGold
2025-06-12	支出	外食	769	JPY	三井NL
2025-06-12	支出	买菜	375	JPY	三井NL
2025-06-12	支出	外食	2100	JPY	乐天Pay
2025-06-12	支出	娱乐	950	JPY	乐天Pay
2025-06-12	支出	谷子	1100	JPY	乐天Pay
2025-06-12	支出	交通费	356	JPY	suica
2025-06-13	支出	外食	1733	JPY	乐天Pay
2025-06-13	支出	外食	1200	JPY	三井NL
2025-06-14	支出	外食	710	JPY	三井NL
2025-06-13	支出	娱乐	900	JPY	现金
2025-06-14	支出	外食	1150	JPY	现金
2025-06-14	支出	买菜	340	JPY	乐天Pay
2025-06-14	支出	交通费	1512	JPY	suica
2025-06-15	支出	外食	801	JPY	三井NL
2025-06-15	支出	交通费	733	JPY	suica
2025-06-16	支出	外食	1380	JPY	支付宝
2025-06-17	支出	买菜	4192	JPY	乐天Pay
2025-06-18	支出	旅游	7268	JPY	乐天Master
2025-06-18	支出	买菜	12995	JPY	乐天Master
2025-06-19	支出	日用品	1980	JPY	三井master
2025-06-20	支出	外食	6264	JPY	支付宝
2025-06-20	支出	外食	1160	JPY	乐天Pay
2025-06-21	支出	交通费	356	JPY	suica
2025-06-21	支出	外食	660	JPY	AmexGold
2025-06-21	支出	外食	1980	JPY	乐天Pay
2025-06-21	支出	外食	840	JPY	乐天Pay
2025-06-21	支出	交通费	230	JPY	suica
2025-06-21	支出	买菜	141	JPY	三井NL
2025-06-22	支出	外食	870	JPY	三井NL
2025-06-22	支出	娱乐	1200	JPY	现金
2025-06-22	支出	交通费	824	JPY	suica
2025-06-23	支出	外食	800	JPY	三井NL
2025-06-25	支出	光热费	11724	JPY	AmexGold
2025-06-25	支出	健身房	1100	JPY	AmexGold
2025-06-25	支出	话费网费	1043	JPY	AmexGold
2025-06-25	支出	话费网费	3850	JPY	AmexGold
2025-06-25	支出	房租	117160	JPY	epos
2025-06-26	支出	游戏	1000	JPY	AmexGold
2025-06-26	支出	买菜	3890	JPY	AmexGold
2025-06-27	支出	外食	2810	JPY	乐天Pay
2025-06-27	支出	娱乐	3070	JPY
2025-06-27	支出	交通费	636	JPY	suica
2025-06-27	支出	外食	320	JPY
2025-06-27	支出	外食	1980	JPY	乐天Pay
2025-06-27	支出	买菜	1623	JPY	AmexGold
2025-06-27	支出	游戏	1000	JPY	AmexGold
2025-06-29	支出	交通费	800	JPY	suica
2025-06-29	支出	交通费	6006	JPY	AmexGold
2025-06-29	支出	买菜	22408	JPY	乐天Master
2025-06-30	支出	买菜	609	JPY	乐天Pay
2025-06-30	支出	外食	4123	JPY
2025-06-30	支出	交通费	460	JPY	suica
2025-06-30	支出	游戏	10000	JPY	支付宝
2025-06-30	支出	外食	2281	JPY	三井NL
2025-07-01	支出	外食	1180	JPY	乐天Pay
2025-07-01	支出	娱乐	1750	JPY	乐天Pay
2025-07-01	支出	交通费	460	JPY	suica
2025-07-03	支出	交通费	460	JPY	suica
2025-07-03	支出	外食	4774	JPY	Paypay
2025-07-03	支出	外食	800	JPY	三井NL
2025-07-04	支出	外食	289	JPY	三井NL
2025-07-04	支出	外食	1200	JPY	三井NL
2025-07-04	支出	娱乐	3810	JPY	AmexGold
2025-07-05	支出	外食	2280	JPY	Paypay
2025-07-05	支出	游戏	3380	JPY	Paypay
2025-07-05	支出	交通费	356	JPY	suica
2025-07-06	支出	外食	5500	JPY	Paypay
2025-07-06	支出	交通费	460	JPY	suica
2025-07-06	支出	衣服	1990	JPY	AmexGold
2025-07-07	支出	外食	2043	JPY	AmexGold
2025-07-07	支出	日用品	5900	JPY	AmexGold	Amazon prime
2025-07-07	支出	买菜	265	JPY	三井NL
2025-07-07	支出	外食	1040	JPY	现金
2025-07-07	支出	交通费	320	JPY	三井NL
2025-07-07	支出	交通费	167	JPY	suica
2025-07-07	支出	外食	149	JPY	三井NL
2025-07-08	支出	旅游	9542	JPY		九十九里浜
2025-07-08	支出	光热费	3850	JPY	AmexGold	网费
2025-07-08	支出	衣服	3999	JPY	煤炉卡
2025-07-08	支出	光热费	5880	JPY	AmexGold	水费（2个月）
2025-07-09	支出	外食	1730	JPY	乐天Pay
2025-07-09	支出	娱乐	1300	JPY	乐天Pay
2025-07-09	支出	游戏	2890	JPY	AmexGold
2025-07-11	支出	日用品	9337	JPY	AmexGold
2025-07-10	支出	外食	1450	JPY	AmexGold
2025-07-10	支出	交通费	356	JPY	suica
2025-07-11	支出	光热费	550	JPY	AmexGold	povo
2025-07-12	支出	交通费	460	JPY	suica
2025-07-12	支出	外食	710	JPY	三井NL
2025-07-12	支出	外食	1010	JPY	乐天Pay
2025-07-13	支出	外食	2992	JPY	Paypay
2025-07-13	支出	交通费	726	JPY	suica
2025-07-13	支出	外食	2244	JPY	Paypay
2025-07-13	支出	外食	1047	JPY
2025-07-13	支出	健身房	7500	JPY	AmexGold
2025-07-14	支出	衣服	5200	JPY	煤炉卡
2025-07-14	支出	医疗	2040	JPY	Paypay
2025-07-14	支出	外食	1130	JPY	现金
2025-07-15	支出	买菜	419	JPY	乐天Pay
2025-07-16	支出	外食	1856	JPY	ANAPay
2025-07-16	支出	买菜	14357	JPY	ANAPay
2025-07-17	支出	交通费	230	JPY	suica
2025-07-17	支出	外食	520	JPY	AmexGold
2025-07-20	支出	光热费	12146	JPY	AmexGold
2025-07-19	支出	旅游	43014	JPY		乗鞍岳
2025-07-20	支出	外食	3700	JPY	支付宝
2025-07-20	支出	游戏	2793	JPY
2025-07-20	支出	交通费	460	JPY	suica
2025-07-21	支出	外食	1200	JPY	三井NL
2025-07-22	支出	外食	1070	JPY	现金
2025-07-22	支出	外食	720	JPY	Paypay
2025-07-23	支出	外食	1716	JPY
2025-07-23	支出	交通费	178	JPY	suica
2025-07-24	支出	医疗	3164	JPY	AmexGold
2025-07-24	支出	房租	117160	JPY	epos
2025-07-25	支出	买菜	548	JPY	AmexGold
2025-07-26	支出	外食	3150	JPY	支付宝
2025-07-26	支出	交通费	356	JPY	suica
2025-07-26	支出	娱乐	500	JPY	现金
2025-07-25	支出	外食	402	JPY	乐天Pay
2025-07-25	支出	交通费	1537	JPY	suica
2025-07-27	支出	外食	990	JPY	AmexGold
2025-07-27	支出	外食	2871	JPY	Paypay
2025-07-27	支出	交通费	610	JPY	suica
2025-07-27	支出	娱乐	400	JPY	现金
2025-07-28	支出	买菜	341	JPY	三井NL
2025-07-29	支出	娱乐	1470	JPY
2025-07-29	支出	交通费	356	JPY	suica
2025-07-29	支出	外食	980	JPY	suica
2025-07-30	支出	外食	4000	JPY	Paypay
2025-07-30	支出	交通费	356	JPY	suica
2025-07-31	支出	外食	540	JPY	AmexGold
2025-08-01	支出	外食	4400	JPY	AmexGold
2025-08-01	支出	交通费	636	JPY	suica
2025-08-01	支出	娱乐	10000	JPY	AmexGold
2025-08-02	支出	外食	670	JPY	三井住友银行
2025-08-02	支出	娱乐	7941	JPY	三井master
2025-08-03	支出	外食	1880	JPY	乐天Pay
2025-08-03	支出	交通费	1234	JPY	suica
2025-08-04	支出	光热费	5560	JPY	AmexGold
2025-08-04	支出	外食	520	JPY	AmexGold
2025-08-04	支出	买菜	1593	JPY	乐天Pay
2025-08-05	支出	医疗	7853	JPY
2025-08-05	支出	交通费	466	JPY
2025-08-05	支出	外食	1800	JPY	Paypay
2025-08-05	支出	外食	2379	JPY	AmexGold
2025-08-06	支出	谷子	2370	JPY	煤炉卡
2025-08-06	支出	交通费	475	JPY	suica
2025-08-06	支出	外食	710	JPY	三井NL
2025-08-06	支出	外食	2131	JPY	Paypay
2025-08-06	支出	娱乐	3600	JPY	乐天Pay
2025-08-06	支出	买菜	289	JPY	乐天Pay
2025-08-07	支出	外食	650	JPY	乐天Pay
2025-08-07	支出	交通费	460	JPY	suica
2025-08-07	支出	外食	4764	JPY	Paypay
2025-08-08	支出	外食	1677	JPY
2025-08-08	支出	买菜	397	JPY	乐天Pay
2025-08-09	支出	外食	710	JPY	三井NL
2025-08-09	支出	外食	950	JPY	Paypay
2025-08-09	支出	外食	3430	JPY	乐天Pay
2025-08-10	支出	外食	1330	JPY	Paypay
2025-08-10	支出	外食	520	JPY	AmexGold
2025-08-11	支出	外食	690	JPY	乐天Pay
2025-08-11	支出	日用品	1001	JPY	乐天Pay
2025-08-11	支出	谷子	880	JPY	乐天Pay
2025-08-11	支出	外食	1283	JPY	AmexGold
2025-08-11	支出	日用品	2990	JPY	AmexGold
2025-08-12	支出	外食	1930	JPY	三井NL
2025-08-14	支出	健身房	7876	JPY	AmexGold
2025-08-13	支出	外食	720	JPY	AmexGold
2025-08-13	支出	交通费	460	JPY	suica
2025-08-14	支出	外食	2450	JPY	Paypay
2025-08-14	支出	外食	950	JPY	Paypay
2025-08-14	支出	买菜	160	JPY
2025-08-14	支出	交通费	356	JPY	suica
2025-08-15	支出	外食	900	JPY	AmexGold
2025-08-15	支出	交通费	1142	JPY	suica
2025-08-16	支出	外食	1081	JPY
2025-08-16	支出	买菜	19522	JPY
2025-08-16	支出	交通费	230	JPY
2025-08-17	支出	外食	1757	JPY	三井NL
2025-08-17	支出	外食	1300	JPY	现金
2025-08-18	支出	外食	6050	JPY	AmexGold
2025-08-18	支出	日用品	190	JPY	现金
2025-08-18	支出	交通费	694	JPY	suica
2025-08-19	支出	外食	1350	JPY	现金
2025-08-20	支出	外食	680	JPY	三井NL
2025-08-21	支出	外食	585	JPY	AmexGold
2025-08-20	支出	交通费	1142	JPY	suica
2025-08-20	支出	外食	810	JPY	Paypay
2025-08-21	支出	娱乐	2360	JPY
2025-08-21	支出	外食	1380	JPY	Paypay
2025-08-22	支出	交通费	460	JPY	suica
2025-08-22	支出	买菜	848	JPY
2025-08-23	支出	日用品	5630	JPY
2025-08-23	支出	外食	1100	JPY	现金
2025-08-23	支出	便利店	449	JPY	suica
2025-08-24	支出	外食	3373	JPY	AmexGold
2025-08-24	支出	交通费	1904	JPY	suica
2025-08-22	支出	书籍	1430	JPY	AmexGold
2025-08-25	支出	外食	2107	JPY	乐天Pay
2025-08-25	支出	外食	616	JPY	AmexGold
2025-08-26	支出	外食	1400	JPY	Paypay
2025-08-26	支出	日用品	1700	JPY	乐天Pay
2025-08-26	支出	交通费	356	JPY	suica
2025-08-27	支出	房租	117160	JPY	epos
2025-08-27	支出	外食	1340	JPY	suica
2025-08-27	支出	外食	950	JPY	Paypay
2025-08-28	支出	外食	1650	JPY	Paypay
2025-08-28	支出	外食	495	JPY	AmexGold
2025-08-28	支出	外食	380	JPY	三井NL
2025-08-29	支出	医疗	1950	JPY	AmexGold
2025-08-29	支出	医疗	912	JPY	AmexGold
2025-08-29	支出	外食	6940	JPY	AmexGold
2025-08-29	支出	交通费	460	JPY	suica
2025-08-29	支出	便利店	280	JPY
2025-08-30	支出	旅游	24267	JPY
2025-08-31	支出	外食	1470	JPY	AmexGold
2025-08-31	支出	日用品	2679	JPY	三菱
2025-08-31	支出	交通费	817	JPY	suica
2025-08-31	支出	便利店	539	JPY	suica
2025-09-01	支出	便利店	713	JPY	三井NL
2025-08-25	收入			JPY
2025-09-01	支出	外食	1300	JPY	现金
2025-09-01	支出	便利店	439	JPY	三井NL
2025-09-02	支出	外食	560	JPY	三井Olive
2025-09-03	支出	娱乐	12000	JPY	AmexGold
2025-09-02	支出	便利店	192	JPY	三井NL
2025-09-03	支出	便利店	181	JPY	suica
2025-09-03	支出	交通费	460	JPY	suica
2025-09-04	支出	外食	1000	JPY	三井NL
2025-09-04	支出	交通费	460	JPY	suica
2025-09-04	收入	娱乐	5700	JPY
2025-09-04	支出	便利店	240	JPY	三井NL
2025-09-04	支出	外食	870	JPY	乐天Pay
2025-09-05	支出	外食	500	JPY	三井NL
2025-09-05	支出	外食	5896	JPY	Paypay
2025-09-06	支出	便利店	140	JPY	现金
2025-09-06	支出	交通费	460	JPY	suica
2025-09-06	支出	外食	1010	JPY	suica
2025-09-07	支出	交通费	1193	JPY	suica
2025-09-07	支出	外食	2070	JPY	Paypay
2025-09-08	支出	外食	940	JPY	suica
2025-09-08	支出	衣服	2680	JPY	suica
2025-09-08	支出	话费网费	3850	JPY	AmexGold
2025-09-08	支出	外食	640	JPY	AmexGold
2025-09-08	支出	外食	1550	JPY	现金
2025-09-09	支出	日用品	2539	JPY	AmexGold
2025-09-09	支出	外食	1300	JPY	现金
2025-09-10	支出	便利店	930	JPY	三井NL
2025-09-10	支出	日用品	468	JPY	乐天Pay
2025-09-09	支出	交通费	146	JPY	suica
2025-09-10	支出	外食	540	JPY	三井NL
2025-09-10	支出	话费网费	12980	JPY	AmexGold
2025-09-10	支出	外食	940	JPY	suica
2025-09-10	支出	外食	625	JPY	AmexGold
2025-09-10	支出	交通费	146	JPY	suica
2025-09-10	支出	外食	750	JPY	乐天Pay
2025-09-10	支出	医疗	1580	JPY
2025-09-11	支出	外食	1380	JPY	Paypay
2025-09-11	支出	便利店	181	JPY	suica
2025-09-11	支出	外食	690	JPY	乐天Pay
2025-09-11	支出	交通费	837	JPY	suica
2025-09-13	支出	健身房	7678	JPY	AmexGold
2025-09-14	支出	谷子	1650	JPY	乐天Pay
2025-09-14	支出	衣服	11300	JPY
2025-09-16	支出	日用品	699	JPY	AmexGold
2025-09-16	支出	外食	870	JPY	suica
2025-09-16	支出	外食	770	JPY	三井NL
2025-09-17	支出	旅游	167030	JPY		冲绳旅游（除机票）
2025-09-17	支出	外食	3200	JPY	Paypay
2025-09-17	收入	工资	455000	JPY	三井住友银行
2025-09-17	支出	交通费	816	JPY	suica
2025-09-17	支出	便利店	181	JPY	suica
2025-09-18	支出	交通费	356	JPY	suica
2025-09-18	支出	便利店	218	JPY	suica
2025-09-17	支出	外食	770	JPY	三井NL
2025-09-17	支出	便利店	479	JPY	三井NL
2025-09-18	支出	外食	5150	JPY	ANA卡
2025-09-19	支出	便利店	447	JPY	suica
2025-09-19	支出	便利店	348	JPY	三井NL
2025-09-19	支出	外食	1330	JPY	suica
2025-09-19	支出	便利店	522	JPY	suica
2025-09-20	支出	外食	1070	JPY	三井NL
2025-09-20	支出	交通费	230	JPY	suica
2025-09-20	支出	便利店	159	JPY	suica
2025-09-20	支出	日用品	1204	JPY	suica
2025-09-20	支出	买菜	33000	JPY	三井owners
2025-09-21	支出	外食	420	JPY	三井NL
2025-09-21	支出	交通费	1248	JPY	suica
2025-09-21	支出	便利店	1012	JPY	suica
2025-09-21	支出	便利店	330	JPY	三井NL
2025-09-21	支出	外食	1300	JPY	三井NL
2025-09-21	支出	外食	3200	JPY	Paypay
2025-09-22	支出	外食	990	JPY	suica
2025-09-23	支出	便利店	808	JPY	suica
2025-09-23	支出	便利店	170	JPY	三井NL
2025-09-23	支出	娱乐	2000	JPY	其他
2025-09-24	支出	便利店	638	JPY	三井NL
2025-09-24	支出	买菜	1851	JPY	ANAPay
2025-09-26	支出	交通费	1009	JPY	suica
2025-09-26	支出	便利店	130	JPY	suica
2025-09-26	支出	衣服	13800	JPY	AmexGold
2025-09-27	支出	外食	560	JPY	三井NL
2025-09-28	支出	便利店	476	JPY	suica
2025-09-28	支出	外食	3200	JPY	支付宝
2025-09-28	支出	娱乐	5000	JPY	现金
2025-09-28	支出	交通费	356	JPY	suica
2025-09-28	支出	外食	2600	JPY	Paypay
2025-09-28	支出	便利店	150	JPY	Paypay
2025-09-28	支出	便利店	635	JPY	三井NL
2025-09-29	支出	外食	1850	JPY	suica
2025-09-29	支出	交通费	292	JPY	suica
2025-09-29	支出	便利店	181	JPY	suica
2025-09-29	收入	活动	26240	JPY
2025-09-30	支出	外食	1100	JPY	三井NL
2025-09-30	支出	房租	117160	JPY	epos
"""

# 按月份分组
monthly_data = defaultdict(list)

lines = data.strip().split('\n')[1:]  # 跳过表头
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 5:
        date_str = parts[0]
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            month_key = date.strftime('%Y-%m')
            monthly_data[month_key].append(parts)
        except:
            pass

# 创建目录和CSV文件
base_dir = r'C:\Users\liu\accounting\2025'

for month_key in sorted(monthly_data.keys()):
    records = monthly_data[month_key]

    # 创建CSV文件
    month_num = month_key.split('-')[1]
    csv_file = os.path.join(base_dir, f'{month_num}.csv')

    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['日期', '类型', '分类', '金额', '币种', '账户', '商户', '备注'])

        for record in records:
            # 补齐不足8列的记录
            while len(record) < 8:
                record.append('')
            writer.writerow(record[:8])

    print(f'已创建 {csv_file}，包含 {len(records)} 条记录')

print('\n导入完成！')

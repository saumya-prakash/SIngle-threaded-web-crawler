from modules import *

def load_page(url):         # SSL certificate_verify_failed error to be resolved, happens sometimes

    headers={'User-Agent':'''Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0''',
             'Accept':'''*/*''',
             'Connection':'''close'''}

    #text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8

    req = ur.Request(url=url, headers=headers)

    return ur.urlopen(req)


def url_normalize(cur_page, path):

    #cur_page=cur_page.strip() #may have spaces at the end, but not necessary now
    path=path.strip()   #necessary

    path=encode_space(path)

    b=list(up.urlparse(path))    #'b' parsed into components

    if b[0] not in ['', 'http', 'https']:          #Some other scheme present, like, mailto, javascript, etc.
        return None

    a = list(up.urlparse(cur_page))  # 'a' parsed into components

    if b[2]=='' and b[3]=='' and b[4]=='':      #b[1] to be checked???
        # if b[5]=='':    #Everything is empty; probably an internal link to the same page
        #     return None
        # else:           #Some internal link; may reveal something new
        #     a[5]=b[5]
        #     return up.urlunparse(a)
        return None           #internal link with complete path name (to the same page) to be excluded



    if b[1]!='' and b[1]!=a[1]:   #sub-domain or external site
        # s1=extract_domain(a[1])
        # s2=extract_domain(b[1])
        #
        # if s1==s2:     #sub-domain
        #     if b[0]=='':
        #         b[0]='http://'
        #     return up.urlunparse(b)
        #
        # else:        #external site
        #     return None
        return None

    else:      # b[1]=='' or b[1]==a[1]:  #link belonging to the same domain

        if b[1]==a[1]:       #complete link aready present
            #if b[0]=='':     #set the scheme of 'a' in 'b' (they belong to the same domain
            b[0]=a[0]      #Ensure scheme of 'a' and 'b' are same
            return encode_space(up.urlunparse(b).strip())

        b[0]=a[0]
        b[1]=a[1]

        if b[2][0]=='/':    #search in the 'root' directory
            return up.urlunparse(b)

        if a[2]!='' and a[2][-1]=='/':      #removing the last '/' if present -> to be REVIEWED
            a[2]=a[2][:-1]


        if b[2][:3]=='../' or b[2][:5]=='./../':   #general function for moving up the directory levels
            i=0

            n = len(b[2])
            if b[2][:2]=='./':
                i+=2

            a[2] = remove_fname(a[2])

            while i+2<=n and b[2][i:i+2]=='..':
                a[2] = remove_fname(a[2])
                i+=3

            b[2]='/' + b[2][i:]

            b[2] = a[2]+b[2]

            return up.urlunparse(b)


        if b[2][0:2] == './' or (b[2][0] not in ['/', '.']):  # search in the same directory
            a[2] = remove_fname(a[2])

            if b[2][0] == '.':
                b[2] = b[2][1:]

            if b[2][0] != '/':
                b[2] = '/' + b[2]

            b[2] = a[2] + b[2]

            return up.urlunparse(b)

        print("****", cur_page, path,"****")  #case not found
        return None




def extract_domain(s):
    i=len(s)-1

    while i>=0 and s[i]!='.':
        i-=1

    j=0

    while j<i and s[j]!='.':
        j+=1

    if j==i or i==-1:
        return s

    else:
        return s[j+1:]


def remove_fname(s):
    if s=='':
        return ''

    i=len(s)-1

    while i>=0 and s[i]!='/':
        i-=1

    if i==-1:
        return ''

    else:
        return s[:i]


def encode_space(s):
    res=''
    for i in s:
        if i==' ':
            res = res+'%20'
        else:
            res=res+i
    return res


def cmp_date(l_modified, days_passed=-1):

    if l_modified is None:
        return False

    if days_passed==-1:
        return True

    a = date.today()

    l_modified = list(l_modified[0].split(' '))
    month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

    b = date(int(l_modified[3]), int(month[l_modified[2]]), int(l_modified[1]))

    if (a-b).days <= days_passed:
        return True

    return False

def get_filters():
    s = []
    p = []

    s.append(re.compile('vacanc', re.IGNORECASE))
    s.append(re.compile('job', re.IGNORECASE))
    s.append(re.compile('career', re.IGNORECASE))
    s.append(re.compile('opportunit', re.IGNORECASE))
    # s.append(re.compile('notice', re.IGNORECASE))   #Very generous filter
    # s.append(re.compile('announcement', re.IGNORECASE))
    s.append(re.compile('recruit(?!er(s)?)', re.IGNORECASE))
    s.append(re.compile('position', re.IGNORECASE))
    s.append(re.compile('role', re.IGNORECASE))
    s.append(re.compile('walk( )?(-)?( )?in', re.IGNORECASE))
    s.append(re.compile('interview', re.IGNORECASE))

    p.append(re.compile('result', re.IGNORECASE))

    return (s, p)


#print(url_normalize('http://www.nielit.gov.in/', 'http://nielit.gov.in/sites/all/themes/berry/images/NIELIT-Logo.png'))
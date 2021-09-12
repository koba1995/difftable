#!/usr/bin/env python

DELIMITER=','

import sys
#import 

if len(sys.argv) == 3 :
    #file1 = open(sys.argv[1],'r')
    #file2 = open(sys.argv[1],'r')
    import subprocess
    p = subprocess.Popen(["diff", "-U999999", sys.argv[1], sys.argv[2]], stdout=subprocess.PIPE)
    p.wait()
    diffinput,stderr = p.communicate(input=None)
    diffinput = diffinput.split('\n')
else:
    diffinput = sys.stdin

def difftable(diffinput):
    display_columns = {0:1} #[0,1,2,3,4,5,6,7]
    out = diffline(diffinput, display_columns )
    
    print('changed_line:', display_columns)

    t=""
    for c in out:
        t += '\n'+ c[0] +'\t'
        for i in sorted(display_columns):
            if i < len( c[1] ) :
                t += c[1][i] + '|'
    return t

def diffline(diffinput, changed_col_idx ):
    out=[]
    bef=[]
    aft=[]
    changing=0
    for line in diffinput:
        #print('LINE:', line )
        if not line :
            continue
        d=line[0]
        col=line[1:].replace('\n','').replace('\r','').split(DELIMITER)
        if d==' ':
            if changing :
                bef.append(col)
                changed_block(bef,aft, out, changed_col_idx)
                aft=[]
                bef=[]
            else:
                if len(bef)>0:
                    out.append((' ',bef[0]))
                bef=[col]
            changing=0
        elif d=='-' or d=='<':
            bef.append(col)
            changing=1
        elif d=='+' or d=='>':
            aft.append(col)
            changing=1
        else:
            #print('???>>' + '|'.join(col))
            out.append(('|'.join(col),[]))
            pass
    if changing :
                changed_block(bef,aft, out, changed_col_idx)
                aft=[]
                bef=[]
    else:
                if len(bef)>0:
                    out.append((' ',bef[0]))
    
    return out

    #
def changed_block(before,after, out, changed_col_idx):
#    print(before,after)
    cng_count_a_b=[]
    for ai,a in enumerate(after):
        cng_count_a_b.append([])
        for bi,b in enumerate(before):
            cng_count_a_b[ai].append(compare_line_sum(a,b))
    #print(cng_count_a_b)
    comb_all=[]
    comb(cng_count_a_b, len(after),len(before), 0,0, [],0, comb_all)

    #print(comb_all)

    matchcomb = comb_all[0]
    for cb in comb_all:
        if matchcomb[1] < cb[1]:
            matchcomb = cb
    #
    #print(matchcomb)
    
    last_bi=0
    for ai,a in enumerate(after):
        bm = matchcomb[0][ai]
        for bi in range(last_bi,min(len(before)-1,bm+1)):
            out.append(('-'+str(bi), before[bi]))
        last_bi=min(len(before)-1,bm+1)
        ## get column number that changed ##
        add_changed_col(a,before[bm], changed_col_idx)
        out.append(('+'+str(bm), a))
    for bi in range(last_bi,len(before)-1):
            out.append(('-'+str(bi), before[bi]))
    #last_bi=len(before)-1
    
    #

def add_changed_col(a,b, out):
    for c in range(0,min(len(a),len(b))):
        if (a[c] != b[c]):
            out[c] = 1
def compare_line_sum(a,b):
    count=0
    for c in range(0,min(len(a),len(b))):
        count += 1 if (a[c] == b[c]) else 0
    return count

def comb(allcounts,afterlen,beforelen, afteridx,beforeidx, status,count, out ):
#    print('in ', allcounts,afterlen,beforelen, afteridx,beforeidx, status,count )
    if afteridx<afterlen:
        ai=afteridx+1
        for bi in range(beforeidx,beforelen):
            st = status[:]
            st.append(bi)
            cnt = count + allcounts[afteridx][bi]
            comb(allcounts,afterlen,beforelen, ai,bi, st,cnt, out)
#        print('end',status)
    else:
        out.append((status,count))
#        print('out', status)
        return 0

#
print(difftable(diffinput))


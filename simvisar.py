#!/usr/bin/env python3
'''
Simulated VISAR velocity history from actual velocity history and etalon time delay tau.
Reads velocity history from stdin.  Writes input data to stdout with sim velocity as extra column.
Arguments: tau [timeidx velidx [posidx]]
Time and velocity indices default to 0 and 1 (first two columns).
Position idx defaults to -1 (calculate displacement by integrating velocity).
Ignores comment lines (starting with #).
Assumes self-consistent units: etalon delay tau in same units as time column.

History
- Original (Java) 9/26/12
- Translated to Python2 1/22/21
- Updated to Python3 12/9/22
Damian Swift, LLNL 
'''

import sys

def tabinterp(ftab,x):
   if x<ftab[0][0]: return ftab[0][1]
   n=len(ftab)
   if x>ftab[n-1][0]: return ftab[n-1][1]
   if n==1: return ftab[0][1]
   i0=0; i1=n-2
   while i1>i0+1:
      i=int((i0+i1)/2)
      if x>ftab[i][0]: i0=i
      else: i1=i
   f=(x-ftab[i0][0])/(ftab[i0+1][0]-ftab[i0][0])
   return ftab[i0][1]+f*(ftab[i0+1][1]-ftab[i0][1])

tau=float(sys.argv[1])
it=0; iu=1; ix=-1 # col-index of time, velocity, displacement
if len(sys.argv)>=4:
   it=int(sys.argv[2])
   iu=int(sys.argv[3])
   if len(sys.argv)>=5:
      ix=int(sys.argv[4])

disphist=[]

print('# adding last col: sim visar with etalon delay',tau,'using cols',it,iu,ix)
first=True
x=0.0 # displacement
uold=0.0
minlen=max(it,iu,ix)+1
for line in sys.stdin:
   words=line.split()
   if len(words)>=minlen and not words[0].startswith('#'):
      t=float(words[it])
      u=float(words[iu])
      if ix>=0: x=float(words[ix])
      if first:
         first=False
      else:
         if ix<0: x+=(t-told)*(uold+u)/2
      disphist+=[[t,x]]
      usim=(x-tabinterp(disphist,t-tau))/tau
      print(line[:-1],usim)
      told=t;uold=u;xold=x
   else:
      print(line[:-1])

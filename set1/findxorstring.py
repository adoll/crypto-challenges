import string
import sys
import decodeXor
results = []
for line in sys.stdin:
   results.append(decodeXor.decodeString(line.replace('\n','')))

min = 10000000
champ = ''
i = 1
# number 170, Now that the party is jumping\n
print decodeXor.decodeString("7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f")
for result in results:
   if len(result) > 0:
      if result[0][0] < .02:
         print str(i) + " " + str(result[0:5])
   i += 1

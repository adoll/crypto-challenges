import web
import hmac
import time
import heapq
import random
urls = (
    '/test', 'test'
    )

# get random key
lines = (line for line in open("/usr/share/dict/words"))
word_pairs = ((random.random(), word) for word in lines)
key = heapq.nlargest(1, word_pairs)[0][1]

def insecure_compare(comp1, comp2):
    i = 0
    if len(comp1) != len(comp2): 
        return False
    while i < len(comp1) and i < len(comp2):
        if comp1[i] != comp2[i]:
            return False
        i += 1
        time.sleep(1*.001)
    return True

class test:
    def GET(self):
        user_input = web.input()
        file_name = user_input.file
        sig = user_input.signature
        verify_sig = hmac.hmac_sha1(key, file_name)
        print sig
        print verify_sig

        if not insecure_compare(sig, verify_sig):
            return web.internalerror(self)
        else:
            return 'Success'
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    

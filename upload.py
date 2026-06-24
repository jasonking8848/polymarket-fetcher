import urllib.request, ssl, json, base64
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
TOKEN = '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'
REPO = 'jasonking8848/polymarket-fetcher'
API = 'https://api.github.com/repos/' + REPO
H = {'Authorization':'token '+TOKEN,'User-Agent':'cli','Accept':'application/vnd.github.v3+json'}

# 1. Get latest commit SHA
resp = urllib.request.urlopen(urllib.request.Request(API+'/git/refs/heads/main', headers=H), context=ctx)
sha = json.loads(resp.read())['object']['sha']

# 2. Get the tree SHA from that commit
resp = urllib.request.urlopen(urllib.request.Request(API+'/git/commits/'+sha, headers=H), context=ctx)
tree_sha = json.loads(resp.read())['tree']['sha']

# 3. Create blob for workflow file
with open(r'D:\autoclaw\workspace\polymarket-fetcher\.github\workflows\fetch.yml','r',encoding='utf-8') as f:
    yml = f.read()
data = json.dumps({'content':yml,'encoding':'utf-8'}).encode()
resp = urllib.request.urlopen(urllib.request.Request(API+'/git/blobs', data=data, method='POST', headers=H), context=ctx)
blob_sha = json.loads(resp.read())['sha']

# 4. Create new tree with the .github/workflows/fetch.yml
tree_data = json.dumps({
    'base_tree': tree_sha,
    'tree': [{'path':'.github/workflows/fetch.yml','mode':'100644','type':'blob','sha':blob_sha}]
}).encode()
resp = urllib.request.urlopen(urllib.request.Request(API+'/git/trees', data=tree_data, method='POST', headers=H), context=ctx)
new_tree = json.loads(resp.read())
print('Tree created:', new_tree.get('sha','')[:12])

# 5. Create commit
commit_data = json.dumps({
    'message': 'Add workflow file',
    'tree': new_tree['sha'],
    'parents': [sha]
}).encode()
resp = urllib.request.urlopen(urllib.request.Request(API+'/git/commits', data=commit_data, method='POST', headers=H), context=ctx)
new_sha = json.loads(resp.read())['sha']

# 6. Update ref
ref_data = json.dumps({'sha':new_sha,'force':False}).encode()
resp = urllib.request.urlopen(urllib.request.Request(API+'/git/refs/heads/main', data=ref_data, method='PATCH', headers=H), context=ctx)
print('Workflow uploaded!')
print('Check: https://github.com/jasonking8848/polymarket-fetcher/actions')

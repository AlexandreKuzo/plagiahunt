import requests
import sys
import os
import json
from os.path import join, dirname
from dotenv import load_dotenv


# Init environment
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Check for all arguments
if len(sys.argv) < 3 :
    raise SystemExit

# Start Github getter
print("\nCalling GitHub API")

query = sys.argv[1]+"+in:file+language:"+sys.argv[2]
myHeaders = {
	"Accept": "application/vnd.github+json",
	"Authorization": "Bearer {}".format(os.environ.get('TOKEN'))
}

res = requests.get(os.environ.get("GITHUB_API").format(query), headers=myHeaders)

plagiat = json.loads(res.text)

# Check for result
if plagiat['total_count'] == 0:
    print("No result found")
    raise SystemExit

# Waiting user go according number of results
print("Github gave us {} result(s)".format(plagiat['total_count']))
answer = input("\nLet's Go ? [Yes|no] ")
if answer.lower() in ['n', 'No'] :
    raise SystemExit

# Download files
for item in plagiat['items'] :
    print(item['html_url'])
    url = item['html_url'].replace("https://github.com", "https://raw.githubusercontent.com/")
    url = url.replace("/blob", "")

    res = requests.get(url)

    fp = open(os.environ.get("TMP")+"/"+item['repository']['owner']['login']+"_"+item['name'], "wb")
    fp.write(res.content)
    fp.close()

# Call main engine for search plagiat
print("\nGo to plagiat fiesta")
os.system('python3 engine.py ./tmp js')



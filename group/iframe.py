import requests
from bs4 import BeautifulSoup as bs


## 엔트리 url에서 iframe 추출
# input: (entry) url, width, height
# output: iframe
def get_entry_iframe(url, width, height):
  res = requests.get(url)
  soup = bs(res.text, "html.parser")
  [meta_tag] = soup.select("meta[property='og:image']")
  content = meta_tag.get('content')
  query_id = content.split('/')[-1].split('.')[0]
  embed_url = 'https://playentry.org/iframe/' + query_id
  iframe = "<iframe width='" + str(width) + "' height='" + str(height) + "' src='" + embed_url + "' frameborder='0'></iframe>"
  
  return iframe

## 스크래치 url에서 iframe 추출
# input: (scratch) url, width, height
# output: iframe
def get_scratch_iframe(url, width, height):
  if url[-1] != '/':
    embed_url = url + '/embed'
  else:
    embed_url = url + 'embed'
  iframe = "<iframe src='" + embed_url  + "' allowtransparency='true' width='" + str(width) + "' height='" + str(height) + "' frameborder='0' scrolling='no' allowfullscreen></iframe>"
  return iframe

# url에서 iframe 추출
# input: url, width, height
# output: iframe
# url이 유효하지 않으면 '' return
def get_iframe(url, width, height):
  iframe = ''
  try:
    response = requests.get(url)
    if response.status_code == 200:
      pass
    else:
      return ''
  except: 
      return ''
  if 'scratch' in url:
    iframe = get_scratch_iframe(url, width, height)
  elif 'naver' in url:
    iframe = get_entry_iframe(url, width, height)
  return iframe

def get_img_src(url):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      pass
    else:
      return ''
  except: 
      return ''
  if 'scratch' in url:
    query_id = url.split('/')[-1]
    image_src = "https://cdn2.scratch.mit.edu/get_image/project/" + query_id + "_480x360.png"
  elif 'naver' in url:
    soup = bs(response.text, "html.parser")
    [meta_tag] = soup.select("meta[property='og:image']")
    content = meta_tag.get('content')
    query_id = content.split('/')[-1].split('.')[0]
    image_src = "https://playentry.org/uploads/thumb/" + query_id[0:4]  + "/" + query_id + ".png"
  try:
    response = requests.get(image_src)
    if response.status_code == 200:
      return image_src
    else:
      return ''
  except:
      return ''
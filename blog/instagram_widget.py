import requests

instagram_url = 'https://www.instagram.com/rubyinthewild/media/'

class Instagram:
    def __init__(self, user_url):
        json = requests.get(user_url)
        data = json.json()

        self.image = data['items'][0]['images']['standard_resolution']['url']
        self.caption = data['items'][0]['caption']['text']
        self.post = data['items'][0]['link']

# inst = Instagram(instagram_url)
# print(inst.image)
# print(inst.caption)
# print(inst.post)
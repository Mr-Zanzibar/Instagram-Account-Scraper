import requests
import json

# enter the target profile URL here
profile_url = "https://www.instagram.com/username/"

# make a request to the profile page and get the HTML content
html_content = requests.get(profile_url).text

# find the profile data by searching for the JSON data in the HTML content
profile_data = json.loads(html_content.split("window._sharedData = ")[1].split(";</script>")[0])['entry_data']['ProfilePage'][0]['graphql']['user']

# extract the profile information
username = profile_data['username']
full_name = profile_data['full_name']
bio = profile_data['biography']
followers = profile_data['edge_followed_by']['count']
following = profile_data['edge_follow']['count']
is_private = profile_data['is_private']
profile_pic_url = profile_data['profile_pic_url']

# if the profile is private, make a request to the profile's media endpoint to get the media data
if is_private:
    media_url = "https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables={\"id\":\"" + profile_data['id'] + "\",\"first\":50}"
    media_data = json.loads(requests.get(media_url).text)['data']['user']['edge_owner_to_timeline_media']
else:
    media_data = profile_data['edge_owner_to_timeline_media']

# extract all the photo URLs from the media data
photo_urls = []
for node in media_data['edges']:
    photo_url = node['node']['display_url']
    photo_urls.append(photo_url)

print("Profile Information:")
print("Username: " + username)
print("Full Name: " + full_name)
print("Bio: " + bio)
print("Followers: " + str(followers))
print("Following: " + str(following))
print("Is Private: " + str(is_private))
print("Profile Picture URL: " + profile_pic_url)

print("\nPhoto URLs:")
for url in photo_urls:
    print(url)

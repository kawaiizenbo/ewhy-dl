import json, wget, os, re, requests

base_url = "https://content.services.pbskids.org/v2/kidspbsorg/"

if not os.path.exists("download/"):
    os.mkdir("download")
index_json = json.loads(requests.get(base_url + "home").content)

index = 0
for category in index_json["order"]:
    if category == "kids-livestream":
        continue
    print(f"{index}. {index_json['collections'][category]['title']}")
    index += 1

raw_index = input("Select Category: ")
int_index = int(raw_index)
if int_index > len(index_json["order"]) - 1:
    print("Invalid index")
    exit(0)
print("")

show_idx = 0
for show in index_json['collections'][index_json['order'][int_index]]['content']:
    print(f"{show_idx}. {show['title']}")
    show_idx += 1

raw_show = input("Select Show: ")
int_show = int(raw_show)
if int_show > len(index_json['collections'][index_json['order'][int_index]]['content']):
    print("Invalid index")
    exit(0)
print("")

slug = index_json['collections'][index_json['order'][int_index]]['content'][int_show]["slug"]
show_json = json.loads(requests.get(base_url + "programs/" + slug).content)

print("aa: All Episodes and Clips")
print("\nca: All Clips")
clip_idx = 0
for c in show_json["collections"]["clips"]["content"]:
    print(f"c{clip_idx}. {c['title']}")
    clip_idx += 1

print("\nea: All Episodes")
ep_idx = 0
for c in show_json["collections"]["episodes"]["content"]:
    print(f"e{ep_idx}. {c['title']}")
    ep_idx += 1

ca = False
ea = False

raw_ec = input("Select Episode or Clip: ")
match raw_ec:
    case "aa":
        ca = True
        ea = True
    case "ca":
        ca = True
    case "ea":
        ea = True
    case _:
        ca = False
        ea = False
try:
    if raw_ec.startswith('e'):
        int_ec = int(raw_ec.removeprefix('e'))
        if int_ec > len(show_json["collections"]["episodes"]["content"]):
            print("Invalid index")
            exit(0)
        c = show_json["collections"]["episodes"]["content"][int_ec]
        filename = re.sub('[\\/:*?\"\"<>|]', "_", c['title']) + ".mp4"
        if not os.path.exists(filename):
            print(f"Downloading {c['title']}")
            wget.download(c["mp4"], "download/" + filename)
        else:
            print("File already exists.")
    elif raw_ec.startswith('c'):
        int_ec = int(raw_ec.removeprefix('c'))
        if int_ec > len(show_json["collections"]["clips"]["content"]):
            print("Invalid index")
            exit(0)
        c = show_json["collections"]["clips"]["content"][int_ec]
        filename = re.sub('[\\/:*?\"\"<>|]', "_", c['title']) + ".mp4"
        if not os.path.exists(filename):
            print(f"Downloading {c['title']}")
            wget.download(c["mp4"], "download/" + filename)
        else:
            print("File already exists.")
except:
    if ca:
        for c in show_json["collections"]["clips"]["content"]:
            filename = re.sub('[\\/:*?\"\"<>|]', "_", c['title']) + ".mp4"
            if not os.path.exists(filename):
                print(f"\nDownloading {c['title']}")
                wget.download(c["mp4"], "download/" + filename)

    if ea:
        for c in show_json["collections"]["episodes"]["content"]:
            filename = re.sub('[\\/:*?\"\"<>|]', "_", c['title']) + ".mp4"
            if not os.path.exists(filename):
                print(f"\nDownloading {c['title']}")
                wget.download(c["mp4"], "download/" + filename)

print("\ndone, have fun :)")

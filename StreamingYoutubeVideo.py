import numpy as np


class Video:
    def __init__(self, id, size):
        self.id = id
        self.size = size


class Endpoint:
    def __init__(self, id, lat_to_datacent, num_of_caches):
        self.lat_to_datacent = lat_to_datacent
        self.VN = []
        self.CL = []
        self.id = id
        self.num_of_caches = num_of_caches


class Cache:
    def __init__(self, id, size):
        self.id = id
        self.videos = []
        self.size = size
        self.cur_size = 0
        self.num_of_ep = 0
        self.cache_ep_list = []

    def __lt__(self, other):
        return self.num_of_ep < other.num_of_ep


def main():
    inp = get_data('me_at_the_zoo.in')
    ep_list, video_list, cache_list = arrange_input(inp)

    for ch in cache_list:
        ch.num_of_ep, ch.cache_ep_list = find_num_of_ep_for_cache(ch.id, ep_list)
        #print("Cache:"+str(ch.id)+" Num of ep:"+str(ch.num_of_ep))

    cache_list.sort(reverse=True)

    p_pair = np.zeros((len(video_list), len(cache_list)))
    for ch in cache_list:
        # print("Cache:"+str(ch.id)+" Num of ep:"+str(ch.num_of_ep)+" Ln of ep list:"+str(len(ch.cache_ep_list)))
        for v in video_list:
            for e in ch.cache_ep_list:
                val_vn = find_vn(e, v.id)
                val_cl = find_cl(e, ch.id)
                #print(val_vn)
                #print(val_cl)
                p_pair[v.id][ch.id] += val_vn * (e.lat_to_datacent - val_cl)

    # print(p_pair)

    for p in range(len(video_list)*len(cache_list)):
        indexes = np.argwhere(p_pair.max() == p_pair)
        #print(indexes)
        i = indexes[0][0]
        j = indexes[0][1]
        if p_pair[i][j] == 0:
            break
        if cache_list[j].cur_size + video_list[i].size < cache_list[j].size and p_pair[i][j] > 0:
            cache_list[j].videos.append(video_list[i])
            cache_list[j].cur_size += video_list[i].size

        p_pair[i, j] = 0

    cs = []
    for ch in cache_list:
        if len(ch.videos) > 0:
            cs.append(ch)

    output = str(len(cs))+"\n"

    for c in cs:
        output += str(c.id)+" "
        for v in c.videos:
            output += str(v.id)+" "
        output += "\n"

    f = open('output_me_at_the_zoo.out', 'w')

    f.write(output)
    f.close()




def find_vn(ep, vid):
    for e in ep.VN:
        if vid == e[0].id:
            return e[1]

    return 0


def find_cl(ep, cid):
    for e in ep.CL:
        if cid == e[0]:
            return e[1]
    return 0

def find_num_of_ep_for_cache(cache_id, ep_list):
    num_of_ep = 0
    cache_ep_list = []
    for ep in ep_list:
        for cl in ep.CL:
            if cl[0] == cache_id:
                num_of_ep += 1
                cache_ep_list.append(ep)


    return num_of_ep, cache_ep_list

def arrange_input(inp):
    first_line = inp[0]
    num_of_videos = int(first_line[0])
    num_of_endpoints = int(first_line[1])
    num_of_reqdes = int(first_line[2])
    num_of_caches = int(first_line[3])
    size_of_caches = int(first_line[4])


    cache_list = []
    for c in range(num_of_caches):
        cache_list.append(Cache(c, size_of_caches))

    # print("Video #:"+ str(num_of_videos))
    # print("# of Endpoints" + str(num_of_endpoints))
    # print("# of req dest: " + str(num_of_reqdes))
    # print("# of caches:"+ str(num_of_caches))
    # print("size of caches:"+ str(size_of_caches))

    idx = 0
    video_line = inp[1]
    video_list = []

    # Handles videos
    for v in video_line:
        ex_video = Video(idx, v)
        video_list.append(ex_video)
        idx += 1

    idx = 2

    ep_list = []
    for ep in range(num_of_endpoints):
        ep_list.append(Endpoint(ep, int(inp[idx][0]), int(inp[idx][1])))
        idx += 1
        for ch in range(ep_list[ep].num_of_caches):
            ep_list[ep].CL.append([int(inp[idx][0]), int(inp[idx][1])])
            idx += 1

    for req in range(num_of_reqdes):
        ep_list[int(inp[idx][1])].VN.append([video_list[int(inp[idx][0])], int(inp[idx][2])])
        idx += 1

    return ep_list, video_list, cache_list


def get_data(dir):
    text = []
    with open(dir, 'r') as f:
        for line in f:
            token = line.split()
            temp = []
            for each in token:
                if each.isdigit():
                    each = float(each)
                temp.append(each)
            text.append(temp)
    return text


if __name__ == '__main__':
    main()

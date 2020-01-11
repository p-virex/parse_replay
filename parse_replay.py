import json
import os
import struct
from pprint import pprint


def parse_replay(file_path):
    result_blocks = dict()

    with open(file_path, 'rb') as f:
        f.seek(4)
        blocks = struct.unpack('I', f.read(4))[0]
        block_num = 1
        block_pointer = {}
        block_size = {}
        start_point = 8

        assert not blocks == 0, 'num_blocks == 0'
        assert not blocks > 4, 'num_blocks > 4'

        while blocks >= 1:

            f.seek(start_point)
            size = f.read(4)
            block_size[block_num] = struct.unpack('I', size)[0]
            block_pointer[block_num] = start_point + 4
            start_point = block_pointer[block_num] + block_size[block_num]
            block_num += 1
            blocks -= 1
            for i in block_size:
                f.seek(block_pointer[i])
                block = f.read(int(block_size[i]))
                if 'arenaUniqueID' not in str(block):
                    block_dict = re_iter_data(json.loads(block))
                    result_blocks['battle_info'] = block_dict
                else:

                    block_dict = re_iter_data(json.loads(block))
                    result_blocks['battle_result'] = block_dict[0]
        pprint(result_blocks)


def re_iter_data(data):
    re_iter = data
    if isinstance(data, dict):
        re_iter = {re_iter_data(key): re_iter_data(value) for key, value in data.items()}
    elif isinstance(data, (list, tuple, set)):
        re_iter = [re_iter_data(element) for element in data]
    return re_iter


if __name__ == '__main__':
    path_replay = 'C:\\Games\\World_of_Tanks_RU\\replays'
    name_replay = '20191213_1853_sweden-S01_Strv_74_A2_95_lost_city_ctf.wotreplay'
    parse_replay(os.path.join(path_replay, name_replay))

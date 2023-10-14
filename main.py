from compileSol import *
from createImage import *
import tensorflow as tf
from grad_cam_heatmap import get_vulnerability_location

# 사용자에게 function을 출력해줄 함수
def find_function_start(index, source):
    # 현재 인덱스에서부터 "function" 키워드를 찾음
    start = index
    while start > 0 and source[start] != 'f':
        start -= 1

    # "function" 키워드를 찾았을 경우, 함수의 시작을 찾음
    if source[start:start + 8] == "function":
        return start

    return None


def main():
    # file_path = "E:/sol/buggy1_0x2c2a721d303dc4273725c6aa8704ec8d1d3d17b1.sol" 67%
    file_path = "E:/sol/buggy1_0xc24c64b9909f0b2f947f2f36bc7d46ae848599e0.sol"
    with open(file_path, "r") as file:
        source = file.read()

    version = extract_compiler_version(source)
    if version[0] == '^':
        version = version[1:]
    select_version(version)

    compiled_sol = compile_source(source)
    keys = compiled_sol.keys()

    for key in keys:
        contract_interface = compiled_sol[key]
        contract_name = key.split(':')[1]
        print('contract name: ', contract_name)
        asm = contract_interface['asm']
        bytecode = contract_interface['bin']
        if (asm is None) or (bytecode is None):
            continue

        pixel_colors = create_pixels(bytecode)
        if len(pixel_colors) != 10000:
            continue
        create_image(contract_name, pixel_colors)
        model = tf.keras.models.load_model('my_model1.h5')

        image_path = contract_name + '.png'
        pred, idxs = get_vulnerability_location(image_path, model)
        if pred < 0.5:
            continue
        print(pred)
        print(idxs)

        filtered_asm1 = [d for d in asm['.code'] if d.get('name') != "tag"]
        filtered_asm1.append({'begin': 0, 'end': 0, 'name': 'STOP'})
        filtered_asm2 = [d for d in asm['.data']['0']['.code'] if d.get('name') != "tag"]
        asms = filtered_asm1 + filtered_asm2

        for index in idxs:
            if index >= len(asms):
                continue
            begin = asms[index].get('begin')
            end = asms[index].get('end')

            function_start = find_function_start(begin, source)

            print('---------------------------------------------------')
            print('opcode idx:', index)
            print('begin:', begin)
            print('end:', end)
            print('---------------------------------------------------')
            print('Begin line:', source.count('\n', 0, begin) + 1)
            print('End line:', source.count('\n', 0, end) + 1)
            print('source:\n', source[begin:end + 1])
            print('---------------------------------------------------')
            # 함수 출력
            if function_start is not None:
                # 함수 전체를 출력
                function_end = end
                function_source = source[function_start:function_end + 1]
                print('Function source:')
                print(function_source)
            else:
                print('Function not found')

main()
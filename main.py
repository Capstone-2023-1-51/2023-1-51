import glob
import createImage
import compileSol
import os
from keras.models import load_model
def preprocessing(folder_path):
    versions = set()  # 설치된 버전
    files = glob.glob(folder_path + '/*.sol')
    file_num = 1
    version = '0.4.26'
    compileSol.install_version(version)
    compileSol.select_version(version)
    for file in files:
        print(file)
        version_in_use = version
        version = compileSol.extract_compiler_version(file)
        if version is None:
            continue
        if version[0] == '^':
            version = '0.4.26'

        if version != version_in_use:
            if version not in versions:
                compileSol.install_version(version)
                versions.add(version)

            compileSol.select_version(version)

        try:
            compiled_sol = compileSol.compile_source_file(file)
        except Exception as e:
            with open('./exception/compile/' + str(file_num), 'w') as f:
                s = version + '\n' + file + '\n' + str(e)
                f.write(s)
            continue

        keys = compiled_sol.keys()
        for key in keys:
            label = 0
            strs = key.split(':')
            bin_file_path = folder_path + '/bin/' + str(file_num) + strs[1] + '.bin'

            for function in compiled_sol[key]['abi']:
                if 'name' in function.keys():
                    if function['name'].startswith('reenbug'):  # 컨트랙트 내에 'reenbug'로 시작하는 이름의 함수 존재
                        label = 1
                        break

            bytecode = compiled_sol[key]['bin']
            with open(bin_file_path, 'w') as f:
                f.write(bytecode)

            file_name = str(file_num) + strs[1]
            try:
                pixel_colors = createImage.create_pixels(bytecode)
            except Exception as e:
                with open('./exception/img/' + str(file_num), 'w') as f:
                    f.write(version + '\n' + file + '\n' + str(e))
                continue

            if len(pixel_colors) != 10000:
                continue

            if label == 0:
                file_name = './images/no/' + str(file_num) + strs[1]
            else:
                file_name = './images/yes/' + str(file_num) + strs[1]

            createImage.create_image(file_name, pixel_colors)
        file_num = file_num + 1


def main():
    #folder_path = 'E:/sol'
    #preprocessing(folder_path)
    # # 모델 로딩
    # model = load_model('my_model.h5')
    #
    # # 이미지 폴더 경로
    # image_folder = './images/yes'
    # class_index = 1  # 클래스 인덱스 설정 (예: "yes" 클래스)
    #
    # # 이미지 폴더 내의 모든 이미지 파일에 대해 Grad-CAM 시각화
    # for image_name in os.listdir(image_folder):
    #     image_path = os.path.join(image_folder, image_name)
    #     visualize_grad_cam(image_path, model, class_index)
    #

main()

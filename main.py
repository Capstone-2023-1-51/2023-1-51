import glob
import createImage
import compileSol

def main():
    versions = set()    # 설치된 버전
    folder_path = 'E:/sol'
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
            with open('./exception'+file_num+'.txt', 'w') as f:
                s = version + '\n' + file + '\n' + str(e)
                f.write(s)
            continue

        keys = compiled_sol.keys()
        for key in keys:
            label = '0'
            strs = key.split(':')
            bin_file_path = folder_path + '/bin/' + str(file_num) + strs[1] + '.bin'

            for function in compiled_sol[key]['abi']:
                if 'name' in function.keys():
                    if function['name'].startswith('reenbug'):  # 컨트랙트 내에 'reenbug'로 시작하는 이름의 함수 존재
                        label = '1'
                        break

            bytecode = compiled_sol[key]['bin']
            with open(bin_file_path, 'w') as f:
                f.write(bytecode)

            file_name = str(file_num) + strs[1]
            try:
                pixel_colors = createImage.create_pixels(bytecode)
            except Exception as e:
                with open('./exception' + str(file_num), 'w') as f:
                    f.write(version + '\n' + file + '\n' + str(e))
                continue
            createImage.create_image(file_name, pixel_colors)
        file_num = file_num + 1


main()

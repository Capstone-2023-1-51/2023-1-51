import subprocess
import glob
from solcx import compile_source
import re

# 소스코드 컴파일
def compile_source_file(file_path):
    with open(file_path, 'r', encoding='UTF8') as f:
        source = f.read()
    return compile_source(source)


# 솔리디티 컴파일러 버전 추출
def extract_compiler_version(sol_file_path):
    with open(sol_file_path, 'r', encoding='UTF8') as file:
        solidity_code = file.read()

        # 정규식 패턴으로 pragma 문 또는 컴파일러 지시어를 찾습니다.
        pragma_pattern = re.compile(r'pragma\s+solidity\s+["\']?([^\s"\'\;]+)["\']?\s*;', re.IGNORECASE)
        matches = pragma_pattern.findall(solidity_code)

        if matches:
            # pragma 문 또는 컴파일러 지시어에서 버전 정보 추출
            compiler_version = matches[0]
            return compiler_version
        else:
            return None


# 솔리디티 컴파일러 해당 버전 설치
def install_version(version):
    cmd_command = f"solc-select install {version}"
    install_process = subprocess.Popen(cmd_command, stdout=subprocess.PIPE, shell=True)
    output, error = install_process.communicate()
    print(output.decode())


# 솔리디티 컴파일러 버전 선택
def select_version(version):
    cmd_command = f"solc-select use {version}"
    select_process = subprocess.Popen(cmd_command, stdout=subprocess.PIPE, shell=True)
    output, error = select_process.communicate()
    print(output.decode())


# 솔리디티 컴파일러 버전 확인
def check_version():
    check_cmd = "solc --version"
    check_process = subprocess.Popen(check_cmd, stdout=subprocess.PIPE, shell=True)
    output, error = check_process.communicate()
    print(output.decode())


def compile_solidity(folder_path):
    versions = set()    # 설치된 버전
    files = glob.glob(folder_path + '/*.sol')

    file_num = 1
    version = '0.4.26'
    select_version(version)

    for file in files:
        print(file)
        version_in_use = version
        version = extract_compiler_version(file)
        if version is None:
            continue
        if version[0] == '^':
            version = '0.4.26'

        if version != version_in_use:
            if version not in versions:
                install_version(version)
                versions.add(version)

            select_version(version)

        compiled_sol = compile_source_file(file)
        keys = compiled_sol.keys()
        for key in keys:
            label = '0,'
            strs = key.split(':')
            bin_file_path = folder_path + '/bin/' + str(file_num) + strs[1] + '.bin'

            for function in compiled_sol[key]['abi']:
                if 'name' in function.keys():
                    if function['name'].startswith('reenbug'):  # 컨트랙트 내에 'reenbug'로 시작하는 이름의 함수 존재
                        label = '1,'
                        break

            bytecode = label + compiled_sol[key]['bin']
            with open(bin_file_path, 'w') as f:
                f.write(bytecode)

        file_num = file_num + 1


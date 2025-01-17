import cpuinfo
import psutil
try:
    import GPUtil
except ImportError:
    print("GPUtil 라이브러리가 설치되어 있지 않습니다. GPU 정보를 보려면 'pip install GPUtil'을 통해 설치하세요.")
    GPUtil = None

def get_system_info():
    # CPU 정보
    info = cpuinfo.get_cpu_info()
    cpu_name = info.get('brand_raw', '알 수 없는 CPU')
    
    # RAM 용량 (byte -> GB 변환)
    total_memory_gb = psutil.virtual_memory().total / (1024**3)
    
    # GPU 정보
    gpu_names = []
    if GPUtil is not None:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_names.append(gpu.name)

    print(f"CPU 이름: {cpu_name}")
    print(f"RAM 용량: {total_memory_gb:.2f} GB")
    
    if gpu_names:
        for idx, name in enumerate(gpu_names, start=1):
            print(f"GPU #{idx} 이름: {name}")
    else:
        print("GPU 정보를 가져올 수 없습니다. (GPUtil 미설치 or GPU 미감지)")

if __name__ == "__main__":
    get_system_info()

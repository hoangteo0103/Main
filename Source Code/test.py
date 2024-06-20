import time
import logging
from rarCracker.main import RarCracker

def time_rar_cracker(file_path, start, stop, charset, workers):
    # Khởi tạo RarCracker
    cracker = RarCracker(file_path=file_path, start=start, stop=stop, charset=charset, workers=workers)

    # Đo thời gian bắt đầu
    start_time = time.time()

    # Thực hiện cracking
    password = cracker.crack(callback=lambda log: print(log))

    # Đo thời gian kết thúc
    end_time = time.time()

    # Tính toán thời gian thực hiện
    elapsed_time = end_time - start_time

    return password, elapsed_time

def run_tests():
    # Đường dẫn đến file RAR cần kiểm tra
    file_path = 'thread.rar'

    # Thiết lập các bài kiểm tra với các tham số khác nhau
    test_cases = [
        {'start': 1, 'stop': 3, 'charset': '0123456789', 'workers': 2},
        {'start': 1, 'stop': 4, 'charset': 'abcdefghijklmnopqrstuvwxyz', 'workers': 4},
        {'start': 1, 'stop': 5, 'charset': '0123456789abcdefghijklmnopqrstuvwxyz', 'workers': 6},
        {'start': 1, 'stop': 6, 'charset': '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'workers': 8},
        {'start': 1, 'stop': 7, 'charset': '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 'workers': 10},
        # Thêm các bài kiểm tra khác nếu cần
    ]

    # Chạy từng bài kiểm tra và lưu kết quả
    results = []
    for i, params in enumerate(test_cases):
        print(f"Running test {i + 1} with parameters: {params}")
        password, elapsed_time = time_rar_cracker(file_path, **params)
        results.append({
            'test': i + 1,
            'params': params,
            'password': password,
            'elapsed_time': elapsed_time,
        })

    # In kết quả của từng bài kiểm tra
    for result in results:
        print(f"Test {result['test']}:")
        print(f"  Parameters: {result['params']}")
        print(f"  Password found: {result['password']}")
        print(f"  Elapsed time: {result['elapsed_time']:.2f} seconds")
        print()

if __name__ == "__main__":
    run_tests()

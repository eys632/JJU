import threading
import time
import matplotlib.pyplot as plt
from starcraft_env.starcraft import SCV, CommandCenter, Mineral

def simulate_mining(mineral_field, command_center, mineral_quantity, mineral_distance, time_step=1):
    total_time = 0
    scv_count_history = []
    mineral_depletion_history = []
    total_minerals_history = []

    def scv_work(scv):
        nonlocal total_time
        while command_center.total_minerals < mineral_quantity and mineral_field.amount > 0:
            # 각 작업에 대해 time_step에 맞는 비율만큼 진행
            total_time += scv.travel_time(mineral_distance) * time_step
            scv.harvest(mineral_field)
            time.sleep(30 * time_step)  # time_step에 따라 대기 시간 조정
            total_time += scv.travel_time(mineral_distance) * time_step
            scv.deliver(command_center)  # store 함수 내에서 미네랄을 저장하도록 처리
            time.sleep(30 * time_step)

    def command_center_work():
        while command_center.total_minerals < mineral_quantity and mineral_field.amount > 0:
            # 커맨드 센터의 주기적인 SCV 생산
            time.sleep(10 * time_step)  # time_step에 맞게 대기 시간 조정
            command_center.produce_scv()

            # 기록
            scv_count_history.append(len(command_center.scv_list))
            mineral_depletion_history.append(mineral_field.amount)
            total_minerals_history.append(command_center.total_minerals)

    # 초기 SCV 4기 생성
    for i in range(1):
        initial_scv = SCV(id=i+1)
        command_center.scv_list.append(initial_scv)
        threading.Thread(target=scv_work, args=(initial_scv,), daemon=True).start()

    # 커맨드 센터의 작업을 별도의 스레드에서 실행
    threading.Thread(target=command_center_work, daemon=True).start()

    # SCV 작업이 끝날 때까지 대기
    while command_center.total_minerals < mineral_quantity and mineral_field.amount > 0:
        # 새로 생성된 SCV를 작업에 추가
        if len(command_center.scv_list) > 4:
            new_scv = command_center.scv_list[-1]
            threading.Thread(target=scv_work, args=(new_scv,), daemon=True).start()

        time.sleep(10 * time_step)

    # 모든 SCV 작업이 끝날 때까지 대기
    for thread in threading.enumerate():
        if thread is not threading.main_thread():
            thread.join()

    return total_time, scv_count_history, mineral_depletion_history, total_minerals_history


# 초기화
mineral_field = Mineral(100000)
command_center = CommandCenter()

# 시뮬레이션 실행
mineral_distance = 30
required_minerals = 50000
time_step = 0.001

total_time_taken, scv_count_history, mineral_depletion_history, total_minerals_history = simulate_mining(
    mineral_field, command_center, required_minerals, mineral_distance, time_step)

# 결과 출력
print(f"총 {required_minerals} 미네랄 채굴에 걸린 시간: {total_time_taken}초")

# 그래프 그리기
time_steps = range(len(scv_count_history))

plt.figure(figsize=(15, 5))

# SCV count graph
plt.subplot(1, 3, 1)
plt.plot(time_steps, scv_count_history, color='b')
plt.xlabel('Time (seconds)')
plt.ylabel('Number of SCVs')
plt.title('SCV Count Over Time')

# Mineral depletion graph
plt.subplot(1, 3, 2)
plt.plot(time_steps, mineral_depletion_history, color='r')
plt.xlabel('Time (seconds)')
plt.ylabel('Mineral Amount')
plt.title('Mineral Depletion Over Time')

# Total minerals in command center graph
plt.subplot(1, 3, 3)
plt.plot(time_steps, total_minerals_history, color='g')
plt.xlabel('Time (seconds)')
plt.ylabel('Total Minerals in Command Center')
plt.title('Total Minerals Stored in Command Center Over Time')

plt.tight_layout()
plt.show()
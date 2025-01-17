import time

class SCV:
    def __init__(self):
        self.speed = 1  # m/s
        self.gather_speed = 10  # minerals per trip

    def gather(self, distance):
        # 왕복 시간 계산
        round_trip_time = 2 * (distance / self.speed)
        return round_trip_time

    def collect_minerals(self):
        return self.gather_speed

class CommandCenter:
    def __init__(self, initial_minerals, initial_scv):
        self.minerals = initial_minerals  # Initial minerals in command center
        self.scv_count = initial_scv  # Initial SCV count
        self.scv_cost = 50  # Cost of producing one SCV
        self.scv_production_time = 10  # Time to produce one SCV (in seconds)
        self.production_timer = 0  # Timer for SCV production

    def produce_scv(self):
        if self.minerals >= self.scv_cost:
            self.minerals -= self.scv_cost
            self.scv_count += 1
            return True
        return False

def simulation(initial_minerals=100_000, initial_scv=1, goal_minerals=50_000):
    # Constants
    mineral_distance = 30  # Distance to minerals in meters

    # Initial conditions
    total_minerals = initial_minerals  # Total available minerals
    command_center = CommandCenter(initial_minerals=0, initial_scv=initial_scv)  # 명령 센터 인스턴스 생성
    scv = SCV()  # SCV 인스턴스 생성
    time_elapsed = 0  # Time counter in seconds

    while command_center.minerals < goal_minerals:
        # Gather minerals
        gather_time = scv.gather(mineral_distance)
        minerals_collected = scv.collect_minerals()

        # Update total minerals and command center minerals
        if total_minerals >= minerals_collected:
            total_minerals -= minerals_collected
            command_center.minerals += minerals_collected
        else:
            command_center.minerals += total_minerals
            total_minerals = 0

        # SCV 생산 로직
        command_center.production_timer += gather_time  # 생산 타이머 업데이트
        if command_center.production_timer >= command_center.scv_production_time:
            command_center.produce_scv()  # SCV 생산
            command_center.production_timer = 0  # 타이머 초기화

        # Increment time
        time_elapsed += gather_time  # Increment by the time it took to gather

        # Print progress every 100 seconds
        if time_elapsed % 100 == 0:
            print(f"Time: {time_elapsed}s, Command Center Minerals: {command_center.minerals:.2f}, SCVs: {command_center.scv_count}")

    print(f"Goal reached! Time taken: {time_elapsed} seconds")

# 사용자가 원하는 초기 값으로 시뮬레이션 실행
initial_minerals = 100_000  # 초기 광물 수
initial_scv = 1  # 초기 SCV 수
goal_minerals = 50_000  # 목표 광물 수

simulation(initial_minerals=initial_minerals, initial_scv=initial_scv, goal_minerals=goal_minerals)

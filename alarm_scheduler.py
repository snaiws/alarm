import json
import os
import subprocess


def load_alarm_info(json_file):
    """JSON 파일에서 알람 정보 로드"""
    with open(json_file, "r", encoding="utf-8") as f:  # UTF-8로 파일 읽기
        data = json.load(f)
    return data["alarms"]


def schedule_alarm_tasks(alarms, script_path):
    """
    Windows 작업 스케줄러에 알람 작업 등록
    :param alarms: 알람 리스트 (time, sound, message 포함)
    :param script_path: 실행할 스크립트 경로
    """
    for alarm in alarms:
        task_name = f"Alarm_{alarm['time'].replace(':', '_')}"
        time = alarm["time"]
        sound = alarm["sound"]
        message = alarm["message"]

        # 작업 등록 명령어 생성
        command = (
            f"schtasks /create /tn {task_name} /tr "
            f"\"python {script_path} --sound {sound} --message '{message}'\" "
            f"/sc once /st {time} /f"
        )

        # 작업 등록 실행
        try:
            subprocess.run(command, check=True, shell=True)
            print(f"알람 등록 성공: {task_name} ({time})")
        except subprocess.CalledProcessError as e:
            print(f"알람 등록 실패: {task_name} ({time}) - {e}")


def remove_all_scheduled_tasks():
    """기존 알람 작업 제거"""
    try:
        tasks = subprocess.check_output("schtasks /query /fo LIST", shell=True, text=True)
        for line in tasks.splitlines():
            if line.startswith("TaskName:") and "Alarm_" in line:
                task_name = line.split(":")[1].strip()
                subprocess.run(f"schtasks /delete /tn {task_name} /f", shell=True, check=True)
                print(f"알람 작업 삭제됨: {task_name}")
    except subprocess.CalledProcessError as e:
        print(f"작업 삭제 중 오류 발생: {e}")


if __name__ == "__main__":
    json_file = "alarm_info.json"  # 알람 정보를 저장한 JSON 파일 경로
    alarms = load_alarm_info(json_file)

    # 현재 스크립트 경로
    script_path = os.path.abspath("./alarm_action.py")

    # 기존 작업 제거 후 새로운 작업 등록
    remove_all_scheduled_tasks()
    schedule_alarm_tasks(alarms, script_path)

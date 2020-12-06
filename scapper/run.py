from crawlers import run_glassdoor, run_indeed
from concurrent.futures import ProcessPoolExecutor, as_completed
# import threading
from utils import db_conn


def r_method(some_string):
    if some_string == "run_indeed":
        print(f"running {some_string}(True) functions")
        return eval(f"{some_string}(True)")
    else:
        print(f"running {some_string}() functions")
        return eval(f"{some_string}()")


def insert_to_db(payload):
    try:
        db = db_conn()
        db.insert(payload)
        print("insert_finished")
    except:
        print("couldn't")


def run():
    run_methods = ["run_indeed", "run_glassdoor"]
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(r_method, i): i for i in run_methods}
        for future in as_completed(futures):
            payload = future.result()
            # print(payload)
            insert_to_db(payload)


if __name__ == "__main__":
    run()

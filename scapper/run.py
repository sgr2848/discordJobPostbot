from crawlers.glassdoor import run_glassdoor
from crawlers.indeed import run_indeed
# from db_barell import get_db
from concurrent.futures import ProcessPoolExecutor
def r_method(some_string):
    print(f"running {some_string} functions")
    eval(some_string)
def run():
    run_methods = ["run_indeed","run_glassdoor"]
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(r_method, f"{i}()"): i for i in run_methods}
if __name__ == "__main__":
    run()
    run_indeed()
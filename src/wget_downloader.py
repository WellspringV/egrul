import subprocess
import time

def run_cmd(cmd, *args, verbose=False, **kwargs):
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True
        )
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip(), end='\r')
        rc = process.poll()
        if verbose:
            print(f"Command exited with status {rc}")
    except OSError as e:
        raise
    except Exception as e:
        raise


def wget_data(url,  max_retries=3):
    retry_delay = 1
    filename = url.split('/')[-1]
    for attempt in range(max_retries):
        try:  
            run_cmd(f"wget -cO - {url} > {filename}", verbose=False)
            return
        except Exception:
            time.sleep(retry_delay)
            retry_delay *= 2
    raise Exception("Maximum retry attempts reached")


if __name__ == "__main__":    
    url = 'https://ofdata.ru/open-data/download/egrul.json.zip'    
    wget_data(url)

    
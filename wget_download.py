import subprocess

def run_cmd(cmd, verbose=False, *args, **kwargs):
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
        print(f"Error executing command '{cmd}': {e}")
    except Exception as e:
        print(f"Error executing command '{cmd}': {e}")



if __name__ == "__main__":        
    run_cmd('echo "Wait download!"', verbose=True)
    run_cmd("wget -cO - https://ofdata.ru/open-data/download/egrul.json.zip > egrul.json.zip", verbose=True)
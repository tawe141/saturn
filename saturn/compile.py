import glob
import subprocess
import json
import os


def convert_ipynb_to_html(filepath: str) -> None:
    output_directory = filepath.split('/')
    del output_directory[-1]
    output_directory[0] = 'site'
    output_directory = '/'.join(output_directory)
    command = ("jupyter nbconvert --to html --output-dir %s --template basic %s" % (output_directory, filepath)).split()
    process = subprocess.run(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    if process.returncode != 0:
        raise RuntimeWarning('Notebook %s failed to convert to html.' % filepath,
                             process.stdout,
                             process.stderr)


def compile_notebooks(force=False):
    to_convert = []
    notebooks = glob.glob('notebooks/**/*.ipynb', recursive=True)
    modified_times = [os.stat(i).st_mtime for i in notebooks]
    current_mtimes = dict(zip(notebooks, modified_times))

    if os.path.isfile('ipynb_mtimes.json') and force is False:
        last_mtimes = json.load(open('ipynb_mtimes.json', 'r'))

        # add all new notebooks
        to_convert.extend(
            [k for k in set(current_mtimes) - set(last_mtimes)]
        )

        # then add all the ones that were modified
        to_convert.extend(
            [k for k in last_mtimes.keys() if current_mtimes[k] != last_mtimes[k]]
        )
    else:
        to_convert = notebooks

    if len(to_convert) == 0:
        print('No notebooks modified or created since the last compile.')
        return
    print('%i notebooks modified or created. Converting the following to HTML:' % len(to_convert))

    for n in to_convert:
        convert_ipynb_to_html(n)

    json.dump(current_mtimes, open('ipynb_mtimes.json', 'w'), indent='\t')
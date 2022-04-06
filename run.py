#!/usr/bin/env python3

import os
import argparse
import subprocess as sp
from pathlib import Path


APPS = ['blackscholes', 'fft', 'inversek2j', 'jmeint', 'jpeg', 'kmeans', 'sobel']
dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

def checkProc(rc: int, err_str: str):
    if rc != 0:
        raise Exception(err_str)
    return

def makeApp(app: str):
    print(f'Making {app}')

    app_dir = dir_path / 'applications' / app

    if not Path(app_dir / 'log').exists():
        os.mkdir(Path(app_dir / 'log'))

    with open(Path(app_dir / 'log' / 'Make.log'), 'w+') as log_file:
        proc = sp.Popen(
            ['make'],
            cwd=app_dir, stdout=log_file, stderr=log_file
        )
        proc.wait()
        checkProc(proc.returncode, 'Make failed')

    print(f'Make successful')

def cleanApp(app: str):
    print(f'Cleaning {app}')

    app_dir = dir_path / 'applications' / app

    if not Path(app_dir / 'log').exists():
        os.mkdir(app_dir / 'log')

    with open(Path(app_dir / 'log' / 'clean.log'), 'w+') as log_file:
        proc = sp.Popen(
            ['make', 'clean'], 
            cwd=app_dir, stdout=log_file, stderr=log_file
        )
        proc.wait()
        checkProc(proc.returncode, 'Clean failed')

    print(f'Clean successful')

def runApp(app: str):
    print(f'Running {app}')
    app_dir = Path(dir_path / 'applications' / app)

    print('#1: Collecting the training data')
    proc = sp.Popen(['bash', 'run_observation.sh'], cwd=app_dir)
    proc.wait()
    checkProc(proc.returncode, 'Run failed')

    print('#2: Aggregating the training data')
    proc = sp.Popen(['python3', '../../scripts/dataConv.py',
        './train.data/output/bin'], cwd=app_dir)
    proc.wait()
    checkProc(proc.returncode, 'Run failed')

    print('#3: Getting the compile parameters')
    proc = sp.Popen(['python3', '../../scripts/comm_to_json.py', app],
        cwd=app_dir)
    proc.wait()
    checkProc(proc.returncode, 'Run failed')

    print('#4: Exploring different NN topologies')
    with open(Path(app_dir / 'log' / f'{app}_training.log'), 'w+') as log_file:
        proc = sp.Popen(['python3', '../../scripts/train.py', app],
            cwd=app_dir, stdout=log_file, stderr=log_file)
        proc.wait()
        checkProc(proc.returncode, 'Run failed')

    print('#5: Finding the best NN topology')
    proc = sp.Popen(['python3', '../../scripts/find_best_NN.py', app],
        cwd=app_dir)
    proc.wait()
    checkProc(proc.returncode, 'Run failed')

    print('#6: Replacing the code with the NN')
    proc = sp.Popen(['python3', '../../scripts/parrotConv.py', app],
        cwd=app_dir)
    proc.wait()
    checkProc(proc.returncode, 'Run failed')

    print('#7: Compiling the code with the NN')
    with open(Path(app_dir / 'log' / 'Make_nn.log'), 'w+') as log_file:
        proc = sp.Popen(['make', '-f', 'Makefile_nn'],
            cwd=app_dir, stdout=log_file, stderr=log_file)
        proc.wait()
        checkProc(proc.returncode, 'Run failed')

    print('#8: Running the code on the test data')
    proc = sp.Popen(['bash', 'run_NN.sh'],
        cwd=app_dir)
    proc.wait()
    checkProc(proc.returncode, 'Run failed')

    print('Run successful')

def setupApp(app: str):
    print(f'Setup {app}')

    app_dir = dir_path / 'applications' / app

    if Path(app_dir).is_dir():
        raise FileExistsError(f'{app_dir} already exists!')

    # base directory
    os.mkdir(Path(app_dir))
    # fann configs
    os.mkdir(Path(app_dir) / 'fann.config')
    # log
    os.mkdir(Path(app_dir) / 'log')
    # nn.configs
    os.mkdir(Path(app_dir) / 'nn.configs')
    # src
    os.mkdir(Path(app_dir) / 'src')
    # NN src
    os.mkdir(Path(app_dir) / 'src.nn')
    # train data
    os.mkdir(Path(app_dir) / 'train.data')
    # input and ouput
    os.mkdir(Path(app_dir) / 'train.data' / 'input')
    os.mkdir(Path(app_dir) / 'train.data' / 'output')
    os.mkdir(Path(app_dir) / 'train.data' / 'output' / 'fann.data')
    os.mkdir(Path(app_dir) / 'train.data' / 'output' / 'bin')
    # test data
    os.mkdir(Path(app_dir) / 'test.data')
    # input and ouput
    os.mkdir(Path(app_dir) / 'test.data' / 'input')
    os.mkdir(Path(app_dir) / 'test.data' / 'output')

    print('Setup successful')

def main(args: dict):

    if args.cmd == 'setup':
        setupApp(args.application)
        return

    if args.application not in APPS and args.application != 'all':
        raise ValueError(f'{args.application} is not a valid application')

    if args.cmd == 'clean':
        if args.application == 'all':
            for app in APPS:
                cleanApp(app)
        else:
            cleanApp(args.application)
    elif args.cmd == 'make':
        if args.application == 'all':
            for app in APPS:
                makeApp(app)
        else:
            makeApp(args.application)
    elif args.cmd == 'run':
        if args.application == 'all':
            for app in APPS:
                runApp(app)
        else:
            runApp(args.application)
    else:
        raise ValueError(f'{args.cmd} is not a valid command')

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', help="Command to execute: clean, make, run, setup")
    parser.add_argument('application', 
        help=f"Application to utilize: {', '.join(APPS)}")

    args = parser.parse_args()

    main(args)
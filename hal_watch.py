"""
See step-by-step running of the vm. Hit enter at each step.
"""

import sys

import ansi
import hal_vm

def main(filename, inputs):
    run(hal_vm.load(filename, inputs))

def run(vm):
    while True:
        sys.stdout.write(ansi.clear_screen)
        vm.show()
        sys.stdin.read(1)
        try:
            vm.step()
        except hal_vm.Halt as e:
            print(e)
            break

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

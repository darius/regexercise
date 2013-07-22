"""
See step-by-step running of the vm. Hit enter at each step.
"""

import ansi
import hal_vm

def run(filename, inputs):
    vm = hal_vm.load(filename, inputs)
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
    import sys
    run(sys.argv[1], sys.argv[2])
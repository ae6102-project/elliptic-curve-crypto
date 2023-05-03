from automan.api import (
    Automator,
    Problem,
    mdict,
    Simulation,
    opts2path,
    filter_cases
)
from matplotlib import pyplot as plt
import numpy as np


class Basic(Problem):
    def get_name(self):
        return 'Basic'

    def setup(self):
        base_cmd = 'python basic_algo_wrapper.py '
        self.curve = ["P-192", "P-224", "P-256", "P-384", "Basic"]
        self.algo = ["DnA", "rDnA", "ML", "JDnA"]
        self.scalar = [10, 100, 500, 1000, 2000]
        opts = mdict(curve=self.curve, algo=self.algo, scalar=self.scalar)
        print(opts)
        self.cases = [
            Simulation(
                root=self.input_path(opts2path(kw)),
                base_command=base_cmd,
                **kw
            )
            for kw in opts
        ]

    def run(self):
        self.make_output_dir()
        y_axes_res = {}
        for curve in self.curve:
            plt.figure()
            filtered_cases = filter_cases(self.cases, curve=curve)
            input = [open(case.input_path('stdout.txt'), 'r').read().strip()
                     for case in filtered_cases]
            y_axes_res[curve] = [float(i) for i in input]
            for itera, algo in enumerate(self.algo):
                arrname = []
                for j, scalar in enumerate(self.scalar):
                    arrname.append(y_axes_res[curve][j+itera*len(self.scalar)])
                print(algo, self.scalar, arrname)
                plt.plot(self.scalar, arrname)
            plt.xlabel('Value of scalar')
            plt.ylabel('Time')
            plt.title(f'{curve}')
            plt.legend(self.algo)
            plt.savefig(f'./basic_plots/curve/{curve}.png')

        for algo in self.algo:
            plt.figure()
            filtered_cases = filter_cases(self.cases, algo=algo)
            input = [open(case.input_path('stdout.txt'), 'r').read().strip()
                     for case in filtered_cases]
            y_axes_res[algo] = [float(i) for i in input]
            for itera, curve in enumerate(self.curve):
                arrname = []
                for j, scalar in enumerate(self.scalar):
                    arrname.append(y_axes_res[algo][j+itera*len(self.scalar)])
                plt.plot(self.scalar, arrname)
            plt.xlabel('Value of Scalar')
            plt.ylabel('Time')
            plt.title(f'{algo}')
            plt.legend(self.curve)
            plt.savefig(f'./basic_plots/algo/{algo}.png')


if __name__ == '__main__':
    automator = Automator(
        simulation_dir='outputs',
        output_dir='manuscript/figures',
        all_problems=[Basic]
    )
    automator.run()

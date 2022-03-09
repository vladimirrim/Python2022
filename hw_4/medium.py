import logging
import math
import multiprocessing
import timeit
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

logging.basicConfig(filename='artifacts/medium_logs.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def integrate_worker(f, a, step, iter_start, iter_end, logger):
    if logger is not None:
        logger.info(f'Start task for iters from {iter_start} to {iter_end}')

    acc = 0
    for i in range(iter_start, iter_end):
        acc += f(a + i * step) * step

    if logger is not None:
        logger.info(f'End task for iters from {iter_start} to {iter_end}')
    return acc


def integrate(f, a, b, *, n_jobs=1, executor=None, logger=None, n_iter=1000):
    step = (b - a) / n_iter
    if executor is None:
        return integrate_worker(f, a, step, 0, n_iter, logger)
    else:
        acc = 0
        res = []
        job_step = n_iter // n_jobs
        with executor(max_workers=n_jobs) as pool:
            for i in range(n_jobs - 1):
                res.append(pool.submit(integrate_worker, f, a, step, i * job_step, (i + 1) * job_step, logger))
            res.append(pool.submit(integrate_worker, f, a, step, job_step * (n_jobs - 1), n_iter, logger))

            for r in res:
                acc += r.result()
    return acc


def run_exp(n, t, executor, f):
    f.write(f'-----------Exp: {n} {t}-----------\n')
    f.write(
        f'{timeit.timeit(lambda: integrate(math.cos, 0, math.pi / 2, n_iter=1000000, n_jobs=n, executor=executor), number=1)} seconds\n')


if __name__ == '__main__':
    integrate(math.cos, 0, math.pi / 2, n_iter=100000, n_jobs=10, executor=ProcessPoolExecutor, logger=logger)
    with open('artifacts/medium_cmp.txt', 'w') as f:
        for n in range(1, 2 * multiprocessing.cpu_count() + 1):
            run_exp(n, 'threads', ThreadPoolExecutor, f)
            run_exp(n, 'processes', ProcessPoolExecutor, f)

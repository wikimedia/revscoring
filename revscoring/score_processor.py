import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import cpu_count

from more_itertools import chunked

from . import dependencies
from .datasources import Datasource

logger = logging.getLogger(__name__)


class ScoreProcessor:

    IO_WORKER_MULTIPLIER = 0.25
    MIN_IO_WORKERS = 2
    MAX_IO_WORKERS = 10

    def __init__(self, scoring_model, extractor, cpu_workers=None,
                 io_workers=None, batch_size=50):
        self.scoring_model = scoring_model
        self.extractor = extractor
        self.cpu_workers = \
            int(cpu_workers) if cpu_workers is not None else cpu_count()
        self.batch_size = int(batch_size)

        if io_workers is not None:
            self.io_workers = int(io_workers)
        else:
            self.io_workers = max(self.MIN_IO_WORKERS,
                                  min(self.MAX_IO_WORKERS,
                                      int(self.cpu_workers *
                                          self.IO_WORKER_MULTIPLIER)))

        logger.info("Starting up IO thread pool with {0} workers"
                    .format(self.io_workers))
        self.scores_ex = ThreadPoolExecutor(max_workers=self.io_workers)
        logger.info("Starting up CPU thread pool with {0} workers"
                    .format(self.cpu_workers))
        self.process_ex = ProcessPoolExecutor(max_workers=self.cpu_workers)

        roots = dependencies.dig(self.scoring_model.features)
        self.root_datasources = [d for d in roots if isinstance(d, Datasource)]

    def __enter__(self):
        return self

    def __exit__(self):
        self.scores_executor.shutdown()
        self.process_executor.shutdown()

    def score(self, rev_ids, caches=None, cache=None):
        if isinstance(rev_ids, int):
            rev_ids = [rev_ids]

        batches = batch_rev_caches(chunked(rev_ids, self.batch_size), caches,
                                   cache)

        for batch_scores in self.scores_ex.map(self._score_batch, batches):
            for score in batch_scores:
                yield score

    def _score_batch(self, batch_rev_cache):
        id_batch, caches, cache = batch_rev_cache
        logger.debug("running _score_batch() on {0} rev_ids"
                     .format(len(id_batch)))
        error_values = self.extractor.extract(
            id_batch, self.root_datasources, caches=caches, cache=cache)
        e_r_caches = self._group_error_root_caches(
            id_batch, error_values, caches, cache)

        rev_scores = self.process_ex.map(self._process_score, e_r_caches)
        return list(rev_scores)

    def _group_error_root_caches(self, id_batch, error_values, caches, cache):
        for rev_id, (error, vals) in zip(id_batch, error_values):
            if error:
                score_cache = {}
                scoring_model = None
                extractor = None
            else:
                score_cache = {}
                score_cache.update(cache or {})
                score_cache.update((caches or {}).get(rev_id, {}))
                score_cache.update({rd: rv for rd, rv in
                                    zip(self.root_datasources, vals)})
                scoring_model = self.scoring_model
                extractor = self.extractor

            yield (rev_id, scoring_model, extractor, score_cache, error)

    @classmethod
    def _process_score(cls, e_r_caches):
        rev_id, scoring_model, extractor, cache, error = e_r_caches
        logger.debug("running _process_score() on {0}".format(rev_id))

        if error is None:

            try:
                feature_values = list(extractor.solve(
                    scoring_model.features, cache=cache))
            except Exception as error:
                logger.debug("An error occured during feature extraction")
                raise error
                return rev_id, error_score(error)

            try:
                score = scoring_model.score(feature_values)
                return rev_id, score
            except Exception as error:
                logger.debug("An error occured during scoring")
                return rev_id, error_score(error)
        else:
            return rev_id, error_score(error)


def error_score(error):
    error_type = error.__class__.__name__
    message = str(error)

    return {'type': error_type, 'message': message}


def sub_dict(d, keys):
    if d is None:
        return None
    else:
        return {k: d[k] for k in keys if k in d}


def batch_rev_caches(batches, caches, cache):
    for batch in batches:
        batch = list(batch)
        yield (batch, sub_dict(caches, batch), cache)

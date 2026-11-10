"""Finite three-binary-cue routeability benchmark — exact enumeration, not animals.

R selects which independently sampled leaf cue (U or V) determines target.
R is revealed in both arms; contingent requests a leaf after R, precommit
binds a first leaf before R, and can request the other after seeing R.
Only the restricted information-first comparator is proven here.
"""
from itertools import product
from math import isfinite


def worlds():
    return tuple(product((0, 1), repeat=3))


def target(r,u,v):
    if any(type(k) is not int or k not in (0, 1) for k in (r,u,v)):
        raise ValueError('NO_GO_INVALID_EXPERIMENTAL_WORLD')
    return u if r==0 else v


def contingent_first_leaf(r):
    if type(r) is not int or r not in (0,1):
        raise ValueError('NO_GO_INVALID_ROOT_VALUE')
    return 'U' if r==0 else 'V'


def precommit_leaf_queries(r,first):
    if first not in ('U','V'):
        raise ValueError('NO_GO_INVALID_FIRST_LEAF_REQUEST')
    return 1 if first==contingent_first_leaf(r) else 2


def benchmark(cost=0.1):
    if not isinstance(cost,(int,float)) or not isfinite(cost) or cost<0 or cost>=0.5:
        raise ValueError('NO_GO_BAD_ILLUSTRATIVE_COST_OR_GUESS_THRESHOLD')
    case=worlds()
    assert len(case)==8
    active=sum(1 for _ in case)/len(case)
    static={k:sum(precommit_leaf_queries(r,k) for r,u,v in case)/len(case)
            for k in ('U','V')}
    if static!={'U':1.5,'V':1.5}:raise AssertionError('NOT_THE_BALANCED_SOURCE_TASK')
    ordinary=min(static.values())
    return {
      'status':'EXACT_RESTRICTED_PRECOMMIT_QUERY_BENCHMARK',
      'n_worlds':len(case),
      'root_is_common_in_both_arms':True,
      'contingent_leaf_queries':active,
      'precommit_leaf_queries':ordinary,
      'total_information_queries_with_root':{'contingent':1+active,'precommit':1+ordinary},
      'query_saving':ordinary-active,
      'illustrative_query_cost_in_reward_units':cost,
      'full_accuracy_toy_payoff_difference':cost*(ordinary-active),
      'full_certainty_without_guessing_assumed_only_for_math':True,
      'comparison_is_restricted_first_leaf_precommit_not_universal_static_bound':True,
      'observed_animal_result':False}

if __name__=='__main__':
    import json
    print('STAGE15_EXACT_TASK_BENCHMARK '+json.dumps(benchmark(),sort_keys=True))

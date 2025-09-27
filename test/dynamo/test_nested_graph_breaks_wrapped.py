# Owner(s): ["module: dynamo"]
import unittest

import torch
import torch._dynamo.test_case
import torch._dynamo.testing
from torch._dynamo.testing import make_test_cls_with_patches


try:
    from . import test_ctx_manager
except ImportError:
    import test_ctx_manager


test_classes = {}


def make_nested_cls(cls, strong):
    config = torch._dynamo.config

    if strong:
        # A strong nested graph break test - will graph break at every leaf function's return
        test_class = make_test_cls_with_patches(
            cls,
            "NestedGraphBreaksStrong",
            "_nested_graph_breaks_strong",
            (config, "nested_graph_breaks", True),
            (config, "debug_force_nested_calls", True),
            (config, "debug_force_graph_break_on_leaf_return", True),
            (config, "debug_disable_compile_counter", True),
            xfail_prop="_expected_failure_nested_graph_breaks_strong",
        )
    else:
        test_class = make_test_cls_with_patches(
            cls,
            "NestedGraphBreaks",
            "_nested_graph_breaks",
            (config, "nested_graph_breaks", True),
            (config, "debug_force_nested_calls", True),
            (config, "debug_disable_compile_counter", True),
            xfail_prop="_expected_failure_nested_graph_breaks",
        )

    test_classes[test_class.__name__] = test_class
    # REMOVING THIS LINE WILL STOP TESTS FROM RUNNING
    globals()[test_class.__name__] = test_class
    test_class.__module__ = __name__


tests = [
    test_ctx_manager.CtxManagerTests,
]

strong_tests = []
test = None
for test in tests:
    make_nested_cls(test, False)

for test in strong_tests:
    make_nested_cls(test, True)

del test

xfails = [
    # multiple exit due to nested graph break in decorator
    # NestedGraphBreaksStrongCtxManagerTests.test_disable_saved_tensors_hooks_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_disable_saved_tensors_hooks_prev_disabled_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_disable_saved_tensors_hooks_prev_disabled_nested_nested_graph_breaks_strong,  # noqa: F821
    # graph break in context manager __init__
    # NestedGraphBreaksStrongCtxManagerTests.test_generic_context_manager_CustomizedCtxManager_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_generic_context_manager_customized_ctx_manager_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_generic_context_manager_with_graph_break_CustomizedCtxManager_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_generic_context_manager_with_graph_break_customized_ctx_manager_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_generic_ctx_manager_with_graph_break_CustomizedCtxManagerWithGraphBreak_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_generic_ctx_manager_with_graph_break_customized_ctx_manager_with_graph_break_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_nested_generic_context_manager_CustomizedCtxManager_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_nested_generic_context_manager_customized_ctx_manager_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_nested_generic_context_manager_with_graph_break_CustomizedCtxManager_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_nested_generic_context_manager_with_graph_break_customized_ctx_manager_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_return_context_manager_nested_graph_breaks_strong,  # noqa: F821
    # NestedGraphBreaksStrongCtxManagerTests.test_return_context_manager_with_graph_break_nested_graph_breaks_strong,  # noqa: F821
    # recursion limit exceeded
    # NestedGraphBreaksStrongCtxManagerTests.test_cuda_stream_compared_with_constant_nested_graph_breaks_strong,  # noqa: F821
]


case = None

for case in xfails:
    unittest.expectedFailure(case)

del case, xfails

if __name__ == "__main__":
    from torch._dynamo.test_case import run_tests

    run_tests()

from semantic_kernel import Kernel


class KernelRouter:
    def __init__(self, kernel: Kernel) -> None:
        self.kernel = kernel

    def run_function(self, function, input_text: str):
        return self.kernel.run(function, input_text)

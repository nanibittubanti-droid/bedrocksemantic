import logging

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.bedrock import BedrockTextCompletion

from app.config import Config

logger = logging.getLogger(__name__)


class SemanticKernelRuntime:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.kernel: Kernel | None = None
        self.completion: BedrockTextCompletion | None = None

    def initialize(self) -> None:
        logger.debug("Initializing Semantic Kernel runtime")
        self.kernel = Kernel()
        self.completion = BedrockTextCompletion(
            model=self.config.model_id,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            endpoint=self.config.bedrock_endpoint,
            region=self.config.aws_region,
        )
        self.kernel.add_text_completion("bedrock", self.completion)

    def get_kernel(self) -> Kernel:
        if self.kernel is None:
            raise RuntimeError("Semantic Kernel is not initialized")
        return self.kernel

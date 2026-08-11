from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE
from .incidents import STATE
from .tracing import observe

@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


class FakeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model
        self.cache: dict[str, FakeResponse] = {}

    @observe(as_type="span")
    def generate(self, prompt: str) -> FakeResponse:
        if prompt in self.cache:
            # Trả về từ cache với 0 token (Cost Optimization)
            cached_resp = self.cache[prompt]
            return FakeResponse(text=cached_resp.text, usage=FakeUsage(0, 0), model=self.model)

        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        answer = (
            "Starter answer. Teams should improve this output logic and add better quality checks. "
            "Use retrieved context and keep responses concise."
        )
        resp = FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)
        self.cache[prompt] = resp
        return resp

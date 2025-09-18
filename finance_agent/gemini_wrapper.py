import os
import json
import inspect
import logging
from dotenv import load_dotenv
from typing import Any, Dict, List, Callable, Optional
from google.generativeai.types import GenerationConfig
import google.generativeai as genai

logger = logging.getLogger(__name__)

load_dotenv()
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"

USE_REAL = bool(os.getenv(GEMINI_API_KEY_ENV, "").strip())

if USE_REAL:
    try:
        genai.configure(api_key=os.getenv(GEMINI_API_KEY_ENV))
    except Exception as e:
        logger.warning("Failed to import google.generativeai - falling back to MOCK. Error: %s", e)
        USE_REAL = False


def _callable_to_schema(func: Callable) -> Dict:
    """
    Build a simple JSON schema for function parameters based on signature.
    Defaults to string for unknown annotations.
    """
    sig = inspect.signature(func)
    props = {}
    required = []
    for name, param in sig.parameters.items():
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        ann = param.annotation
        if ann == inspect._empty:
            t = "string"
        elif ann in (str,):
            t = "string"
        elif ann in (int,):
            t = "integer"
        elif ann in (float,):
            t = "number"
        elif ann in (bool,):
            t = "boolean"
        else:
            t = "string"
        props[name] = {"type": t, "description": f"Parameter {name} of {func.__name__}"}
        if param.default == inspect._empty:
            required.append(name)
    schema = {"type": "object", "properties": props}
    if required:
        schema["required"] = required
    return schema


class GeminiWrapper:
    """
    Wrapper: if GEMINI_API_KEY provided and google.generativeai importable -> real calls
    Otherwise uses a deterministic MOCK LLM for dev / testing.
    """

    def __init__(self, model: str = "gemini-2.0-flash"):
        self.model_name = model
        self.use_real = USE_REAL
        if self.use_real:
            try:
                self.model = genai.GenerativeModel(model)
            except Exception as e:
                logger.error("Failed to init GenerativeModel: %s", e)
                self.use_real = False
                self.model = None
        else:
            self.model = None

    def _build_functions_metadata(self, tools: List[Callable]) -> List[Dict]:
        metas = []
        for t in tools:
            metas.append(
                {
                    "name": getattr(t, "__name__", str(t)),
                    "description": (t.__doc__ or "").strip(),
                    "parameters": _callable_to_schema(t),
                }
            )
        return metas

    def _mock_generate(self, messages: List[Dict], tools: Optional[List[Callable]] = None) -> Dict[str, Any]:
        """
        A very small deterministic mock LLM.
        """
        joined = " ".join(m.get("content", "") for m in messages).lower()
        out = {"text": None, "function_call": None, "raw": None}

        # detect subquestion generation intent
        if "json array of subquestions" in joined or "json list of subquestions" in joined:
            json_out = {"subquestions": [
                {"id": 1, "question": "What is the ticker for FPT?", "depends_on": []},
                {"id": 2, "question": "What is the current price of {{TICKER_FROM_Q1}}?", "depends_on": [1]}
            ]}
            out["text"] = json.dumps(json_out)
            return out

        # detect tool request
        if tools and ("price" in joined or "giá" in joined):
            tool_name = getattr(tools[0], "__name__", None)
            if tool_name:
                out["function_call"] = {"name": tool_name, "arguments": {"ticker": "MOCK"}}
                return out

        out["text"] = "[-] Mock answer: cannot do complex reasoning in mock mode."
        return out

    def generate(
        self,
        messages: List[Dict],
        tools: Optional[List[Callable]] = None,
        temperature: float = 0.0,
        max_output_tokens: int = 1024,
        function_call: str = "auto"
    ) -> Dict[str, Any]:
        """
        Gọi model Gemini hoặc mock.
        Trả về dict: {'text': str|None, 'function_call': dict|None, 'raw': raw_response}
        """
        if not self.use_real or not self.model:
            return self._mock_generate(messages, tools)

        try:
            # gom tất cả messages thành chuỗi cho Gemini
            user_input = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

            resp = self.model.generate_content(
                user_input,
                generation_config=GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens
                )
            )

            out = {"text": None, "function_call": None, "raw": resp}
            out["text"] = getattr(resp, "text", None)
            return out

        except Exception as e:
            logger.error("Error calling real Gemini SDK: %s. Falling back to MOCK.", e)
            return self._mock_generate(messages, tools)

    async def agenerate(self, *args, **kwargs):
        import asyncio
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: self.generate(*args, **kwargs))

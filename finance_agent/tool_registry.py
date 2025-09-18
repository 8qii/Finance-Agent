import inspect
from dataclasses import dataclass, field
from typing import Callable, Dict, Any


def _callable_to_schema(func: Callable) -> Dict[str, Any]:
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


@dataclass
class ToolMeta:
    """Metadata for each registered tool."""
    name: str
    description: str
    func: Callable
    parameters_schema: Dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    """Central registry for all tools."""

    def __init__(self):
        self._tools: Dict[str, ToolMeta] = {}

    def register(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters_schema: Dict[str, Any] = None,
    ):
        """Register a tool into the registry."""
        if parameters_schema is None:
            parameters_schema = _callable_to_schema(func)
        meta = ToolMeta(
            name=name,
            description=description,
            func=func,
            parameters_schema=parameters_schema,
        )
        self._tools[name] = meta

    def get(self, name: str) -> ToolMeta:
        return self._tools.get(name)

    def list_tools(self) -> Dict[str, ToolMeta]:
        return self._tools


# -----------------------
# Global registry instance
# -----------------------
registry = ToolRegistry()

# Example tool registrations
# Bạn import các tool thực tế của bạn vào đây
from .tools.chart import generate_price_chart
from .tools.fundamentals import get_fundamentals
from .tools.google_search import google_search
from .tools.news import search_news
from .tools.pdf_parse import parse_financial_report
from .tools.ratios import calculate_ratios
from .tools.stock_price import get_stock_price
from .tools.stock_symbol import get_stock_symbol

# Register all tools
registry.register(
    name="generate_price_chart",
    description="Generate a price chart for a given stock ticker",
    func=generate_price_chart,
)
registry.register(
    name="get_fundamentals",
    description="Retrieve fundamental information for a stock ticker",
    func=get_fundamentals,
)
registry.register(
    name="google_search",
    description="Perform a Google search and return snippets",
    func=google_search,
)
registry.register(
    name="search_news",
    description="Search for the latest financial news about a stock ticker or company.",
    func=search_news,
)
registry.register(
    name="parse_financial_report",
    description="Parse PDF financial report and extract sections",
    func=parse_financial_report,
)
registry.register(
    name="calculate_ratios",
    description="Calculate financial ratios (EPS, P/E, ROE) given stock price, net income, equity, and shares outstanding.",
    func=calculate_ratios,
)
registry.register(
    name="get_stock_price",
    description="Fetch current or historical stock price for a ticker",
    func=get_stock_price,
)
registry.register(
    name="get_stock_symbol",
    description="Find stock ticker symbol from a company name",
    func=get_stock_symbol,
)

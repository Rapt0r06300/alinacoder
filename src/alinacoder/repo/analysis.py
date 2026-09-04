from __future__ import annotations
from dataclasses import dataclass
import ast
from pathlib import Path

@dataclass(frozen=True, slots=True)
class DataFlowEdge:
    kind: str
    line: int
    symbol: str

class RepositoryAnalyzer:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()

    def _path(self, relative: str) -> Path:
        path=(self.root/relative).resolve(); path.relative_to(self.root); return path

    def data_flow(self, relative: str, symbol: str) -> list[DataFlowEdge]:
        tree=ast.parse(self._path(relative).read_text(encoding='utf-8'), filename=relative)
        out:list[DataFlowEdge]=[]
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id==symbol:
                kind='define' if isinstance(node.ctx,(ast.Store,ast.Param)) else 'read' if isinstance(node.ctx,ast.Load) else 'delete'
                out.append(DataFlowEdge(kind,getattr(node,'lineno',0),symbol))
            elif isinstance(node, ast.arg) and node.arg==symbol:
                out.append(DataFlowEdge('define',getattr(node,'lineno',0),symbol))
        out.sort(key=lambda e:(e.line,e.kind))
        return out

    def impacted_tests(self, changed_paths: set[str]) -> set[str]:
        modules={Path(p).with_suffix('').as_posix().replace('/','.') for p in changed_paths if p.endswith('.py')}
        stems={Path(p).stem for p in changed_paths if p.endswith('.py')}
        impacted:set[str]=set()
        for path in self.root.rglob('*.py'):
            rel=path.relative_to(self.root).as_posix()
            name=path.name
            if not (name.startswith('test_') or name.endswith('_test.py') or '/tests/' in '/'+rel):
                continue
            try: tree=ast.parse(path.read_text(encoding='utf-8'),filename=rel)
            except (SyntaxError,UnicodeDecodeError): continue
            imports:set[str]=set()
            for node in ast.walk(tree):
                if isinstance(node,ast.Import): imports.update(alias.name for alias in node.names)
                elif isinstance(node,ast.ImportFrom) and node.module: imports.add(node.module)
            if any(any(i==m or i.startswith(m+'.') for i in imports) for m in modules) or any(s in {i.split('.')[0] for i in imports} for s in stems):
                impacted.add(rel)
        return impacted

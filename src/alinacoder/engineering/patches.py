from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChangeImpact:
    files: set[str]
    tests: set[str]


class ChangeImpactSimulator:
    def __init__(self, *, dependencies: dict[str, set[str]], tests_by_file: dict[str, set[str]]) -> None:
        self.dependencies = {k:set(v) for k,v in dependencies.items()}
        self.tests_by_file = {k:set(v) for k,v in tests_by_file.items()}

    def analyze(self, changed_files: set[str]) -> ChangeImpact:
        files = set(changed_files)
        progressed = True
        while progressed:
            progressed = False
            for src, dependents in self.dependencies.items():
                if src in files:
                    for dep in dependents:
                        if dep not in files:
                            files.add(dep)
                            progressed = True
        tests: set[str] = set()
        for path in files:
            tests |= self.tests_by_file.get(path, set())
        return ChangeImpact(files, tests)


@dataclass(frozen=True)
class CandidatePatch:
    changed_paths: set[str]
    behavioral_contracts: dict[str, str]
    required_tests: set[str]

    def ready_for_verification(self, *, executed_tests: set[str]) -> bool:
        return bool(self.changed_paths) and bool(self.behavioral_contracts) and self.required_tests <= executed_tests

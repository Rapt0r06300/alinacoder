from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class AgentSpec:
    agent_id: str
    specialty: str
    lineage: str
    provider: str
    capabilities: frozenset[str] = field(default_factory=frozenset)
    failure_domain: str = ""


class FencingRegistry:
    def __init__(self) -> None:
        self._epochs: dict[str, int] = {}

    def issue(self, resource: str) -> int:
        token = self._epochs.get(resource, 0) + 1
        self._epochs[resource] = token
        return token

    def validate(self, resource: str, token: int) -> bool:
        return self._epochs.get(resource, 0) == token


@dataclass(frozen=True)
class ResourceLease:
    resource: str
    owner: str
    fence: int
    mode: str
    state_version: int


class LeaseManager:
    def __init__(self) -> None:
        self.fences = FencingRegistry()
        self._leases: dict[str, ResourceLease] = {}

    def acquire(self, resource: str, owner: str, *, mode: str, state_version: int) -> ResourceLease:
        if mode not in {"read", "write", "resource"}:
            raise ValueError("invalid lease mode")
        current = self._leases.get(resource)
        if current and current.owner != owner and (mode == "write" or current.mode == "write"):
            raise RuntimeError("conflicting lease")
        lease = ResourceLease(resource, owner, self.fences.issue(resource), mode, state_version)
        self._leases[resource] = lease
        return lease

    def admit_write(self, lease: ResourceLease, *, current_state_version: int) -> bool:
        return (
            lease.mode in {"write", "resource"}
            and self.fences.validate(lease.resource, lease.fence)
            and lease.state_version == current_state_version
        )

    def release(self, lease: ResourceLease) -> None:
        if self._leases.get(lease.resource) == lease:
            del self._leases[lease.resource]


@dataclass(frozen=True)
class ProposedChange:
    agent_id: str
    path: str
    exports: dict[str, str] = field(default_factory=dict)
    requires: dict[str, str] = field(default_factory=dict)
    writes: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class SemanticConflict:
    symbol: str
    producer_path: str
    consumer_path: str
    producer_contract: str
    consumer_contract: str


class SemanticConflictDetector:
    def detect(self, changes: Iterable[ProposedChange]) -> list[SemanticConflict]:
        changes = list(changes)
        exports: dict[str, tuple[str, str]] = {}
        conflicts: list[SemanticConflict] = []
        for change in changes:
            for symbol, contract in change.exports.items():
                previous = exports.get(symbol)
                if previous and previous[1] != contract:
                    conflicts.append(SemanticConflict(symbol, previous[0], change.path, previous[1], contract))
                exports[symbol] = (change.path, contract)
        for change in changes:
            for symbol, required in change.requires.items():
                producer = exports.get(symbol)
                if producer and producer[1] != required:
                    conflicts.append(SemanticConflict(symbol, producer[0], change.path, producer[1], required))
        return list(
            {
                (c.symbol, c.producer_path, c.consumer_path, c.producer_contract, c.consumer_contract): c
                for c in conflicts
            }.values()
        )


@dataclass(frozen=True)
class VoteResult:
    verdict: str
    independent_votes: int
    lineage_verdicts: dict[str, tuple[str, float]]


class IndependentVoteAggregator:
    def aggregate(self, votes: Iterable[tuple[AgentSpec, str, float]]) -> VoteResult:
        by_lineage: dict[str, tuple[str, float]] = {}
        for agent, verdict, confidence in votes:
            previous = by_lineage.get(agent.lineage)
            if previous is None or confidence > previous[1]:
                by_lineage[agent.lineage] = (verdict, confidence)
        weighted: dict[str, float] = {}
        for verdict, confidence in by_lineage.values():
            weighted[verdict] = weighted.get(verdict, 0.0) + confidence
        if any(verdict == "FAIL" and confidence >= 0.9 for verdict, confidence in by_lineage.values()):
            final = "FAIL"
        elif weighted:
            final = max(weighted.items(), key=lambda item: (item[1], item[0]))[0]
        else:
            final = "INCONCLUSIVE"
        return VoteResult(final, len(by_lineage), by_lineage)


class CouncilPolicy:
    def __init__(self, minimum_margin: float = 0.05) -> None:
        self.minimum_margin = minimum_margin

    def should_debate(
        self,
        *,
        expected_terminal_gain: float,
        criticality: float,
        latency_cost: float,
        resource_cost: float,
    ) -> bool:
        return expected_terminal_gain * max(0.0, criticality) - latency_cost - resource_cost >= self.minimum_margin


class TopologyRouter:
    def route(self, *, nodes: list[str], edges: list[tuple[str, str]], coupling: float) -> str:
        if len(nodes) <= 1:
            return "single"
        if edges or coupling >= 0.6:
            return "sequential"
        if len(nodes) >= 4 and coupling >= 0.3:
            return "hierarchical"
        return "parallel"


@dataclass(frozen=True)
class TopologyValueObservation:
    topology: str
    net_terminal_gain: float
    enabled: bool
    verdict: str


class TopologyValueAudit:
    """Fail closed when a multi-agent topology does not prove net terminal value."""

    def __init__(self, min_terminal_gain: float = 0.03) -> None:
        self.min_terminal_gain = min_terminal_gain
        self._observations: dict[str, TopologyValueObservation] = {}

    def observe(
        self,
        *,
        topology: str,
        baseline_terminal_success: float,
        topology_terminal_success: float,
        latency_penalty: float,
        resource_penalty: float,
    ) -> TopologyValueObservation:
        net_gain = topology_terminal_success - baseline_terminal_success - latency_penalty - resource_penalty
        enabled = net_gain + 1e-12 >= self.min_terminal_gain
        verdict = "KEEP_PROVEN_VALUE" if enabled else "DISABLE_NO_PROVEN_VALUE"
        observation = TopologyValueObservation(topology, net_gain, enabled, verdict)
        self._observations[topology] = observation
        return observation

    def is_enabled(self, topology: str) -> bool:
        observation = self._observations.get(topology)
        return bool(observation and observation.enabled)

    def observation(self, topology: str) -> TopologyValueObservation | None:
        return self._observations.get(topology)


@dataclass(frozen=True)
class ConflictNotification:
    target_agent: str
    resource: str
    reason: str
    new_state_version: int


class ConflictNotificationPlane:
    def __init__(self) -> None:
        self._notifications: dict[str, list[ConflictNotification]] = {}

    def publish(self, notification: ConflictNotification) -> None:
        self._notifications.setdefault(notification.target_agent, []).append(notification)

    def drain(self, agent_id: str) -> list[ConflictNotification]:
        return self._notifications.pop(agent_id, [])


class SpecialistRegistry:
    def __init__(self, agents: Iterable[AgentSpec] = ()) -> None:
        self._agents = {agent.agent_id: agent for agent in agents}

    def register(self, agent: AgentSpec) -> None:
        self._agents[agent.agent_id] = agent

    def eligible(self, capability: str) -> list[AgentSpec]:
        return [
            agent
            for agent in self._agents.values()
            if capability in agent.capabilities or agent.specialty == capability
        ]

    def select_diverse(self, capability: str, *, desired: int) -> list[AgentSpec]:
        if desired <= 0:
            return []
        candidates = sorted(self.eligible(capability), key=lambda agent: agent.agent_id)
        selected: list[AgentSpec] = []
        seen_lineages: set[str] = set()
        seen_domains: set[str] = set()
        while candidates and len(selected) < desired:
            candidate = max(
                candidates,
                key=lambda agent: (
                    int(agent.lineage not in seen_lineages),
                    int((agent.failure_domain or agent.provider) not in seen_domains),
                    -len(agent.capabilities),
                    agent.agent_id,
                ),
            )
            candidates.remove(candidate)
            selected.append(candidate)
            seen_lineages.add(candidate.lineage)
            seen_domains.add(candidate.failure_domain or candidate.provider)
        return selected


class Orchestrator:
    def __init__(self, registry: SpecialistRegistry, topology_router: TopologyRouter | None = None) -> None:
        self.registry = registry
        self.topology_router = topology_router or TopologyRouter()

    def plan_topology(self, tasks: list[dict]) -> str:
        nodes = [str(task["id"]) for task in tasks]
        edges = [(str(a), str(b)) for task in tasks for a, b in task.get("edges", [])]
        coupling = max((float(task.get("coupling", 0.0)) for task in tasks), default=0.0)
        return self.topology_router.route(nodes=nodes, edges=edges, coupling=coupling)

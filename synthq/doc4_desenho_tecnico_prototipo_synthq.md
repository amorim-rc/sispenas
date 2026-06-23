# DOCUMENTO 4 — DESENHO TÉCNICO DO PROTÓTIPO
## SynthQ — Motor de Otimização de Circuitos Quânticos via ZX-Calculus

**Versão:** 1.0 | **Data:** Junho/2026
**Autores:** Luccas Cavicchioli (CEO) + Leandro Moraes (CTO)
**Classificação:** Confidencial — contém descrição de IP proprietário

---

# 1. VISÃO GERAL DA ARQUITETURA

## 1.1. Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SYNTHQ ENGINE v1.0                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐    ┌──────────────┐    ┌──────────┐    ┌──────────┐ │
│  │          │    │              │    │          │    │          │ │
│  │  PARSER  │───▶│  ZX ENGINE   │───▶│ EXPORTER │───▶│ METRICS  │ │
│  │          │    │              │    │          │    │          │ │
│  └──────────┘    └──────────────┘    └──────────┘    └──────────┘ │
│       ▲               ▲                   │               │       │
│       │               │                   │               │       │
│  OpenQASM 3.0    Grafo ZX            OpenQASM 3.0    Relatório    │
│  Qiskit IR       (rustworkx)         Qiskit Circuit  JSON/PDF     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                          API LAYER (FastAPI)                         │
│  POST /optimize  │  GET /metrics  │  POST /batch  │  GET /health   │
└─────────────────────────────────────────────────────────────────────┘
```

## 1.2. Fluxo de Dados (Pipeline Completa)

```
Input (OpenQASM)
      │
      ▼
┌─────────────┐
│ 1. PARSING  │  Converte OpenQASM → Representação interna
│             │  (Qiskit QuantumCircuit → lista de gates)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 2. DECOMP   │  Decompõe gates arbitrários em Clifford+T
│             │  (RZ(θ) → sequência de H, S, T, T†, CNOT)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 3. ZX CONV  │  Converte circuito Clifford+T → Grafo ZX
│             │  (cada gate → spider/hadamard box)
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│ 4. SIMPLIFICAÇÃO ZX (core proprietário) │
│                                         │
│  4a. Spider Fusion                      │
│  4b. π-Commutation                     │
│  4c. Bialgebra Rule                     │
│  4d. Phase Gadget Optimization          │
│  4e. Interior Clifford Reduction        │
│  4f. Local Complementation              │
│  4g. Pivot Rule                         │
│                                         │
│  [Heurística de ordenação proprietária] │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────┐
│ 5. EXTRACT  │  Extrai circuito do grafo ZX simplificado
│             │  (graph-like → circuit via CNOT extraction)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 6. EXPORT   │  Converte para formato de saída
│             │  (Qiskit Circuit → OpenQASM 3.0)
└──────┬──────┘
       │
       ▼
Output (OpenQASM otimizado + métricas)
```

---

# 2. COMPONENTES DETALHADOS

## 2.1. Parser (Módulo `synthq.parser`)

**Responsabilidade:** Aceitar circuitos em múltiplos formatos e normalizar para representação interna.

**Formatos suportados (v1.0):**
- OpenQASM 2.0
- OpenQASM 3.0
- Qiskit QuantumCircuit (objeto Python direto)

**Código base (já construível):**

```python
# synthq/parser/qasm_parser.py

from qiskit import QuantumCircuit
from qiskit.qasm3 import loads as qasm3_loads
from qiskit.qasm2 import loads as qasm2_loads
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class Gate:
    """Representação interna de uma porta quântica."""
    name: str           # 'h', 's', 't', 'tdg', 'cx', 'rz', etc.
    qubits: Tuple[int, ...]  # índices dos qubits
    params: Tuple[float, ...] = ()  # parâmetros (ex: ângulo de RZ)


@dataclass
class ParsedCircuit:
    """Circuito parseado em representação interna."""
    n_qubits: int
    gates: List[Gate]
    metadata: dict  # informações originais (nome, versão QASM, etc.)

    @property
    def gate_count(self) -> int:
        return len(self.gates)

    @property
    def depth(self) -> int:
        """Calcula profundidade do circuito."""
        layers = [0] * self.n_qubits
        for gate in self.gates:
            max_layer = max(layers[q] for q in gate.qubits)
            for q in gate.qubits:
                layers[q] = max_layer + 1
        return max(layers)


def parse_qasm(qasm_string: str) -> ParsedCircuit:
    """
    Parseia string OpenQASM (2.0 ou 3.0) para representação interna.
    Detecta versão automaticamente.
    """
    # Detecção de versão
    if qasm_string.strip().startswith("OPENQASM 3"):
        qc = qasm3_loads(qasm_string)
    else:
        qc = qasm2_loads(qasm_string)

    return _qiskit_to_parsed(qc)


def parse_qiskit(qc: QuantumCircuit) -> ParsedCircuit:
    """Converte QuantumCircuit do Qiskit para representação interna."""
    return _qiskit_to_parsed(qc)


def _qiskit_to_parsed(qc: QuantumCircuit) -> ParsedCircuit:
    """Conversão interna de QuantumCircuit → ParsedCircuit."""
    gates = []
    for instruction in qc.data:
        op = instruction.operation
        qubits = tuple(qc.find_bit(q).index for q in instruction.qubits)
        params = tuple(float(p) for p in op.params)
        gates.append(Gate(name=op.name.lower(), qubits=qubits, params=params))

    return ParsedCircuit(
        n_qubits=qc.num_qubits,
        gates=gates,
        metadata={
            "name": qc.name,
            "original_depth": qc.depth(),
            "original_gate_count": qc.size(),
        }
    )
```

---

## 2.2. Decompositor Clifford+T (Módulo `synthq.decompose`)

**Responsabilidade:** Decompor portas arbitrárias (RZ, RX, RY, U3, etc.) em sequências do gate set Clifford+T = {H, S, S†, T, T†, CNOT}.

**Base científica:** Utiliza o algoritmo de síntese gridsynth (Ross & Selinger, 2016) para rotações de ângulo arbitrário, com precisão configurável ε.

**Código base (já construível):**

```python
# synthq/decompose/clifford_t.py

from typing import List, Tuple
from synthq.parser.qasm_parser import Gate, ParsedCircuit
import numpy as np

# Conjunto Clifford+T
CLIFFORD_GATES = {'h', 's', 'sdg', 'cx', 'cz', 'x', 'y', 'z', 'id'}
T_GATES = {'t', 'tdg'}
CLIFFORD_T_SET = CLIFFORD_GATES | T_GATES


def is_clifford_t(gate: Gate) -> bool:
    """Verifica se a porta já está no gate set Clifford+T."""
    return gate.name in CLIFFORD_T_SET


def decompose_rz(angle: float, precision: float = 1e-10) -> List[Gate]:
    """
    Decompõe RZ(θ) em sequência Clifford+T.

    Para ângulos especiais (múltiplos de π/4), usa decomposição exata.
    Para ângulos gerais, usa aproximação gridsynth com precisão ε.

    Retorna lista de Gates de 1 qubit (placeholder qubit=0).
    """
    # Normaliza ângulo para [0, 2π)
    angle = angle % (2 * np.pi)

    # Casos exatos (múltiplos de π/4)
    EXACT_ANGLES = {
        0.0: [],
        np.pi / 4: [Gate('t', (0,))],
        np.pi / 2: [Gate('s', (0,))],
        3 * np.pi / 4: [Gate('s', (0,)), Gate('t', (0,))],
        np.pi: [Gate('z', (0,))],
        5 * np.pi / 4: [Gate('z', (0,)), Gate('t', (0,))],
        3 * np.pi / 2: [Gate('sdg', (0,))],
        7 * np.pi / 4: [Gate('tdg', (0,))],
    }

    for exact_angle, decomp in EXACT_ANGLES.items():
        if abs(angle - exact_angle) < precision:
            return decomp

    # Para ângulos gerais: usar síntese aproximada
    # NOTA: Esta é a interface para o algoritmo gridsynth/Ross-Selinger
    # A implementação completa requer aritmética sobre Z[1/√2, i]
    return _gridsynth_approximate(angle, precision)


def _gridsynth_approximate(angle: float, epsilon: float) -> List[Gate]:
    """
    Síntese aproximada via algoritmo gridsynth.

    ⚠️ GAP CIENTÍFICO #1: Implementação completa requer:
    - Aritmética exata sobre o anel Z[1/√2, i]
    - Fatoração em Z[ω] (anel dos inteiros de Eisenstein generalizado)
    - Busca em rede (lattice) para encontrar aproximação ótima
    - Complexidade: O(log(1/ε)) portas T

    IMPLEMENTAÇÃO PROVISÓRIA: usa Qiskit solovay_kitaev para fase de protótipo.
    Substituir por implementação proprietária baseada em pygridsynth.
    """
    from qiskit.transpiler.passes import SolovayKitaev
    from qiskit import QuantumCircuit as QC
    from qiskit.circuit.library import RZGate

    # Circuito temporário com RZ
    temp_qc = QC(1)
    temp_qc.rz(angle, 0)

    # Decompor via Solovay-Kitaev (placeholder — substituir)
    skd = SolovayKitaev(recursion_degree=3)
    decomposed = skd(temp_qc)

    # Converter resultado para nosso formato
    gates = []
    for inst in decomposed.data:
        op = inst.operation
        gates.append(Gate(name=op.name.lower(), qubits=(0,), params=tuple(op.params)))

    return gates


def decompose_circuit(circuit: ParsedCircuit, precision: float = 1e-10) -> ParsedCircuit:
    """
    Decompõe circuito inteiro para gate set Clifford+T.

    Portas que já estão em Clifford+T passam inalteradas.
    Portas parametrizadas (RZ, RX, RY, U3) são decompostas.
    """
    decomposed_gates = []

    for gate in circuit.gates:
        if is_clifford_t(gate):
            decomposed_gates.append(gate)
        elif gate.name == 'rz':
            rz_decomp = decompose_rz(gate.params[0], precision)
            # Remapear qubits
            for g in rz_decomp:
                decomposed_gates.append(
                    Gate(name=g.name, qubits=gate.qubits, params=g.params)
                )
        elif gate.name == 'rx':
            # RX(θ) = H · RZ(θ) · H
            q = gate.qubits
            decomposed_gates.append(Gate('h', q))
            rz_decomp = decompose_rz(gate.params[0], precision)
            for g in rz_decomp:
                decomposed_gates.append(Gate(g.name, q, g.params))
            decomposed_gates.append(Gate('h', q))
        elif gate.name == 'ry':
            # RY(θ) = S† · H · RZ(θ) · H · S
            q = gate.qubits
            decomposed_gates.append(Gate('sdg', q))
            decomposed_gates.append(Gate('h', q))
            rz_decomp = decompose_rz(gate.params[0], precision)
            for g in rz_decomp:
                decomposed_gates.append(Gate(g.name, q, g.params))
            decomposed_gates.append(Gate('h', q))
            decomposed_gates.append(Gate('s', q))
        else:
            # Porta não reconhecida — manter como está (warning)
            decomposed_gates.append(gate)

    return ParsedCircuit(
        n_qubits=circuit.n_qubits,
        gates=decomposed_gates,
        metadata={**circuit.metadata, "decomposed": True}
    )
```

---

## 2.3. Motor ZX (Módulo `synthq.zx_engine`) — CORE PROPRIETÁRIO

**Responsabilidade:** Converter circuito Clifford+T para grafo ZX, aplicar simplificações, e extrair circuito otimizado.

**Base científica:**
- ZX-Calculus (Coecke & Duncan, 2011)
- Simplificação completa (Kissinger & van de Wetering, 2020)
- Extração de circuito (Backens et al., 2021)

**Código base (já construível — usa PyZX como base):**

```python
# synthq/zx_engine/core.py

import pyzx as zx
from pyzx import Circuit as ZXCircuit
from pyzx.graph import Graph
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class OptimizationResult:
    """Resultado da otimização ZX."""
    original_graph: Graph
    optimized_graph: Graph
    original_t_count: int
    optimized_t_count: int
    original_total_gates: int
    optimized_total_gates: int
    original_depth: int
    optimized_depth: int
    reduction_t_count_pct: float
    reduction_total_pct: float
    passes_applied: list


class ZXEngine:
    """
    Motor de otimização baseado em ZX-Calculus.

    Aplica uma sequência de passes de simplificação ao grafo ZX
    para minimizar o T-count preservando a equivalência unitária.
    """

    def __init__(self, strategy: str = "full"):
        """
        Args:
            strategy: Estratégia de otimização.
                - "full": Aplicar todas as simplificações disponíveis
                - "light": Apenas regras básicas (mais rápido)
                - "aggressive": Incluir heurísticas experimentais
        """
        self.strategy = strategy
        self._passes_applied = []

    def circuit_to_zx(self, qasm_string: str) -> Graph:
        """Converte circuito OpenQASM para grafo ZX."""
        circuit = zx.Circuit.from_qasm(qasm_string)
        graph = circuit.to_graph()
        return graph

    def simplify(self, graph: Graph) -> Graph:
        """
        Aplica pipeline de simplificação ao grafo ZX.

        A ORDEM DE APLICAÇÃO DAS REGRAS É O IP PROPRIETÁRIO.
        """
        self._passes_applied = []
        g = graph.copy()

        if self.strategy == "light":
            return self._light_simplify(g)
        elif self.strategy == "full":
            return self._full_simplify(g)
        elif self.strategy == "aggressive":
            return self._aggressive_simplify(g)
        else:
            raise ValueError(f"Estratégia desconhecida: {self.strategy}")

    def _light_simplify(self, g: Graph) -> Graph:
        """Simplificação leve — apenas regras básicas."""
        # 1. Spider fusion (combinar spiders adjacentes da mesma cor)
        zx.simplify.spider_simp(g)
        self._passes_applied.append("spider_fusion")

        # 2. Identidade (remover spiders com fase 0)
        zx.simplify.id_simp(g)
        self._passes_applied.append("identity_removal")

        return g

    def _full_simplify(self, g: Graph) -> Graph:
        """
        Simplificação completa — sequência otimizada de regras.

        Baseado em: Kissinger & van de Wetering (2020),
        "Reducing the number of non-Clifford gates in quantum circuits"
        """
        # Fase 1: Converter para graph-like form
        zx.simplify.to_graph_like(g)
        self._passes_applied.append("to_graph_like")

        # Fase 2: Simplificação interior (Clifford interior)
        zx.simplify.interior_clifford_simp(g)
        self._passes_applied.append("interior_clifford")

        # Fase 3: Full reduce (ponto fixo de todas as regras)
        zx.simplify.full_reduce(g)
        self._passes_applied.append("full_reduce")

        # Fase 4: Phase teleportation (otimização adicional de fases)
        # ⚠️ HEURÍSTICA PROPRIETÁRIA: ordem e condições de aplicação
        self._phase_teleportation(g)
        self._passes_applied.append("phase_teleportation")

        return g

    def _aggressive_simplify(self, g: Graph) -> Graph:
        """
        Simplificação agressiva — inclui heurísticas experimentais.

        ⚠️ GAP CIENTÍFICO #2: Heurísticas de ordenação ótima.
        """
        # Todas as passes de full_simplify
        g = self._full_simplify(g)

        # Passes adicionais experimentais
        # T-count targeted: tentar todas as permutações de regras locais
        # e manter a que minimiza T-count
        self._greedy_t_reduction(g)
        self._passes_applied.append("greedy_t_reduction")

        return g

    def _phase_teleportation(self, g: Graph) -> None:
        """
        Phase teleportation: move fases T através do grafo para
        possibilitar fusões adicionais.

        ⚠️ PARCIALMENTE IMPLEMENTADO — requer pesquisa adicional
        para definir condições ótimas de teleportação.
        """
        # Implementação básica usando PyZX
        zx.simplify.pivot_simp(g)

    def _greedy_t_reduction(self, g: Graph) -> None:
        """
        Heurística greedy: aplica transformações locais e
        mantém apenas as que reduzem T-count.

        ⚠️ GAP CIENTÍFICO #3: Critério de parada ótimo e
        busca local vs. global.
        """
        # Placeholder — implementação completa é pesquisa ativa
        pass

    def extract_circuit(self, graph: Graph) -> ZXCircuit:
        """
        Extrai circuito do grafo ZX simplificado.

        Usa algoritmo de extração por CNOT (Backens et al., 2021).
        """
        return zx.extract_circuit(graph.copy())

    def optimize(self, qasm_string: str) -> OptimizationResult:
        """
        Pipeline completa: QASM → ZX → Simplificação → Extração → Métricas.
        """
        # 1. Converter para grafo ZX
        original_circuit = zx.Circuit.from_qasm(qasm_string)
        original_graph = original_circuit.to_graph()
        original_t_count = zx.tcount(original_graph)

        # 2. Simplificar
        optimized_graph = self.simplify(original_graph)
        optimized_t_count = zx.tcount(optimized_graph)

        # 3. Extrair circuito
        extracted = self.extract_circuit(optimized_graph)

        # 4. Métricas
        return OptimizationResult(
            original_graph=original_graph,
            optimized_graph=optimized_graph,
            original_t_count=original_t_count,
            optimized_t_count=optimized_t_count,
            original_total_gates=len(original_circuit.gates),
            optimized_total_gates=len(extracted.gates),
            original_depth=original_circuit.depth(),
            optimized_depth=extracted.depth(),
            reduction_t_count_pct=(
                (original_t_count - optimized_t_count) / original_t_count * 100
                if original_t_count > 0 else 0.0
            ),
            reduction_total_pct=(
                (len(original_circuit.gates) - len(extracted.gates))
                / len(original_circuit.gates) * 100
                if len(original_circuit.gates) > 0 else 0.0
            ),
            passes_applied=self._passes_applied.copy(),
        )
```

---

## 2.4. Exportador (Módulo `synthq.exporter`)

**Responsabilidade:** Converter circuito otimizado de volta para formatos padrão.

```python
# synthq/exporter/qasm_exporter.py

import pyzx as zx
from pyzx import Circuit as ZXCircuit


def to_qasm2(circuit: ZXCircuit) -> str:
    """Exporta para OpenQASM 2.0."""
    return circuit.to_qasm()


def to_qasm3(circuit: ZXCircuit) -> str:
    """
    Exporta para OpenQASM 3.0.

    Converte via Qiskit (ZXCircuit → Qiskit → QASM3).
    """
    from qiskit.qasm3 import dumps
    qc = _zx_to_qiskit(circuit)
    return dumps(qc)


def _zx_to_qiskit(circuit: ZXCircuit):
    """Converte circuito PyZX para Qiskit QuantumCircuit."""
    from qiskit import QuantumCircuit

    qasm_str = circuit.to_qasm()
    from qiskit.qasm2 import loads
    return loads(qasm_str)
```

---

## 2.5. Módulo de Métricas (Módulo `synthq.metrics`)

**Responsabilidade:** Calcular e reportar métricas de otimização.

```python
# synthq/metrics/reporter.py

from dataclasses import dataclass, asdict
from typing import Optional
import json
from datetime import datetime


@dataclass
class OptimizationReport:
    """Relatório completo de otimização."""
    # Identificação
    circuit_name: str
    timestamp: str
    engine_version: str = "1.0.0"
    strategy: str = "full"

    # Métricas originais
    original_qubits: int = 0
    original_t_count: int = 0
    original_t_depth: int = 0
    original_gate_count: int = 0
    original_depth: int = 0

    # Métricas otimizadas
    optimized_t_count: int = 0
    optimized_t_depth: int = 0
    optimized_gate_count: int = 0
    optimized_depth: int = 0

    # Reduções
    reduction_t_count_pct: float = 0.0
    reduction_t_depth_pct: float = 0.0
    reduction_gate_count_pct: float = 0.0
    reduction_depth_pct: float = 0.0

    # Performance
    processing_time_seconds: float = 0.0
    passes_applied: list = None

    # Economia estimada
    estimated_cost_saving_per_shot_usd: Optional[float] = None
    estimated_annual_saving_usd: Optional[float] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, default=str)

    def summary(self) -> str:
        """Resumo legível para humanos."""
        return (
            f"═══ SynthQ Optimization Report ═══\n"
            f"Circuito: {self.circuit_name}\n"
            f"Qubits: {self.original_qubits}\n"
            f"─────────────────────────────────\n"
            f"T-count:    {self.original_t_count} → {self.optimized_t_count} "
            f"({self.reduction_t_count_pct:+.1f}%)\n"
            f"Gate count: {self.original_gate_count} → {self.optimized_gate_count} "
            f"({self.reduction_gate_count_pct:+.1f}%)\n"
            f"Depth:      {self.original_depth} → {self.optimized_depth} "
            f"({self.reduction_depth_pct:+.1f}%)\n"
            f"─────────────────────────────────\n"
            f"Tempo: {self.processing_time_seconds:.2f}s\n"
            f"Passes: {', '.join(self.passes_applied or [])}\n"
        )
```

---

## 2.6. API Layer (Módulo `synthq.api`)

```python
# synthq/api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import time

from synthq.zx_engine.core import ZXEngine

app = FastAPI(
    title="SynthQ API",
    description="Quantum Circuit T-count Optimization via ZX-Calculus",
    version="1.0.0",
)


class OptimizeRequest(BaseModel):
    """Requisição de otimização."""
    qasm: str = Field(..., description="Circuito em OpenQASM 2.0 ou 3.0")
    strategy: str = Field(default="full", description="Estratégia: light, full, aggressive")
    output_format: str = Field(default="qasm2", description="Formato de saída: qasm2, qasm3")


class OptimizeResponse(BaseModel):
    """Resposta da otimização."""
    optimized_qasm: str
    original_t_count: int
    optimized_t_count: int
    reduction_pct: float
    original_gate_count: int
    optimized_gate_count: int
    processing_time_ms: float
    passes_applied: list


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize_circuit(request: OptimizeRequest):
    """
    Otimiza um circuito quântico para redução de T-count.

    Recebe OpenQASM, retorna circuito otimizado + métricas.
    """
    try:
        engine = ZXEngine(strategy=request.strategy)

        start = time.time()
        result = engine.optimize(request.qasm)
        elapsed_ms = (time.time() - start) * 1000

        # Extrair circuito em formato solicitado
        from synthq.exporter.qasm_exporter import to_qasm2, to_qasm3
        extracted = engine.extract_circuit(result.optimized_graph)

        if request.output_format == "qasm3":
            output_qasm = to_qasm3(extracted)
        else:
            output_qasm = to_qasm2(extracted)

        return OptimizeResponse(
            optimized_qasm=output_qasm,
            original_t_count=result.original_t_count,
            optimized_t_count=result.optimized_t_count,
            reduction_pct=result.reduction_t_count_pct,
            original_gate_count=result.original_total_gates,
            optimized_gate_count=result.optimized_total_gates,
            processing_time_ms=elapsed_ms,
            passes_applied=result.passes_applied,
        )

    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Erro ao processar circuito: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
```

---

# 3. STACK TECNOLÓGICA COMPLETA

## 3.1. Dependências

```toml
# pyproject.toml

[project]
name = "synthq"
version = "1.0.0"
description = "Quantum Circuit T-count Optimization via ZX-Calculus"
requires-python = ">=3.11"

[project.dependencies]
# Core
pyzx = ">=0.8.0"              # ZX-Calculus engine (base)
rustworkx = ">=0.14.0"        # Grafos de alta performance (Rust backend)
numpy = ">=1.26.0"            # Computação numérica
mpmath = ">=1.3.0"            # Aritmética de precisão arbitrária

# Quantum SDKs
qiskit = ">=1.1.0"            # Parsing/exportação OpenQASM
qiskit-aer = ">=0.14.0"       # Simulação para verificação de corretude

# API
fastapi = ">=0.111.0"         # Framework web
uvicorn = ">=0.30.0"          # Servidor ASGI
pydantic = ">=2.7.0"          # Validação de dados

# Utilitários
rich = ">=13.0"               # Output formatado (CLI/notebooks)
loguru = ">=0.7.0"            # Logging estruturado

[project.optional-dependencies]
dev = [
    "pytest >= 8.0",
    "pytest-cov >= 5.0",
    "hypothesis >= 6.100",     # Property-based testing
    "ruff >= 0.4.0",           # Linter + formatter
    "mypy >= 1.10",            # Type checking
]
```

## 3.2. Estrutura do Repositório

```
synthq/
├── pyproject.toml
├── README.md
├── LICENSE                     # Proprietário (não open-source)
├── .github/
│   └── workflows/
│       ├── ci.yml              # Testes + lint em cada PR
│       └── benchmark.yml       # Benchmark automatizado semanal
├── src/
│   └── synthq/
│       ├── __init__.py
│       ├── parser/
│       │   ├── __init__.py
│       │   └── qasm_parser.py
│       ├── decompose/
│       │   ├── __init__.py
│       │   └── clifford_t.py
│       ├── zx_engine/
│       │   ├── __init__.py
│       │   ├── core.py            # Motor principal (IP)
│       │   ├── rules.py           # Regras ZX individuais
│       │   └── heuristics.py      # Heurísticas de ordenação (IP)
│       ├── exporter/
│       │   ├── __init__.py
│       │   └── qasm_exporter.py
│       ├── metrics/
│       │   ├── __init__.py
│       │   └── reporter.py
│       └── api/
│           ├── __init__.py
│           └── main.py
├── tests/
│   ├── test_parser.py
│   ├── test_decompose.py
│   ├── test_zx_engine.py
│   ├── test_exporter.py
│   ├── test_correctness.py     # Verificação de equivalência unitária
│   └── conftest.py             # Fixtures (circuitos de teste)
├── benchmarks/
│   ├── circuits/               # Circuitos de referência (QASM)
│   │   ├── qft_5.qasm
│   │   ├── qft_8.qasm
│   │   ├── grover_4.qasm
│   │   ├── vqe_h2.qasm
│   │   ├── vqe_lih.qasm
│   │   ├── qaoa_maxcut_p1.qasm
│   │   ├── qaoa_maxcut_p2.qasm
│   │   ├── bernstein_vazirani_6.qasm
│   │   ├── random_clifford_t_10.qasm
│   │   └── toffoli_cascade_5.qasm
│   ├── run_benchmark.py
│   └── results/                # Resultados (gerados)
├── notebooks/
│   ├── demo_synthq.ipynb       # Demo para vídeo/inscrição
│   └── benchmark_analysis.ipynb
└── docs/
    └── architecture.md
```

---

# 4. GAPS CIENTÍFICOS A PRODUZIR NA EMPRESA

## 4.1. Gap #1 — Síntese Clifford+T Ótima para Rotações Arbitrárias

**Descrição:** Implementar algoritmo de síntese que encontre a decomposição com MENOR T-count possível para rotações de ângulo arbitrário RZ(θ).

**Estado da arte:**
- Ross & Selinger (2016): 3·log₂(1/ε) + O(log·log(1/ε)) portas T para 1 qubit
- Yamamoto & Yoshioka (2026, pygridsynth): Extensão para n qubits com T-count (21/8·4ⁿ - 9/2·2ⁿ + 9)·log₂(1/ε)

**O que falta implementar:**
- Aritmética exata sobre o anel Z[1/√2, i] (número algébrico)
- Algoritmo de fatoração eficiente em Z[ω₈]
- Busca em rede (lattice search) para encontrar ponto ótimo
- Integração com pipeline ZX (usar resultado da síntese como input para simplificação)

**Complexidade:** Alta — requer 4-8 semanas de trabalho dedicado do CTO
**Impacto:** Reduz T-count na etapa ANTES da simplificação ZX (efeitos compostos)
**Referências:** Ross & Selinger 2016, Kliuchnikov et al. 2023, Yamamoto & Yoshioka 2026

---

## 4.2. Gap #2 — Heurísticas de Ordenação de Regras ZX

**Descrição:** Determinar a ORDEM ÓTIMA de aplicação das regras de simplificação ZX para maximizar redução de T-count.

**Problema:** O ZX-Calculus é confluente (qualquer ordem chega ao mesmo resultado) apenas para certas subclasses de grafos. Para grafos gerais, a ordem de aplicação importa — algumas sequências levam a mínimos locais subótimos.

**Estado da arte:**
- PyZX usa ordem fixa (full_reduce = spider → bialgebra → interior_clifford → pivot, repetido até ponto fixo)
- Kissinger & van de Wetering (2020) provam confluência apenas para "graph-like" ZX-diagrams
- Nenhum trabalho publicado explora otimização da sequência para circuitos industriais

**O que falta pesquisar:**
- Benchmarking exaustivo de todas as permutações de regras em circuitos-alvo
- Aprendizado por reforço (RL) para descobrir sequências ótimas por classe de circuito
- Heurísticas adaptativas: analisar estrutura do grafo e escolher sequência dinamicamente
- Critério de "desistência" — quando parar de simplificar

**Complexidade:** Muito alta — pesquisa genuinamente original, potencial publicação
**Impacto:** Pode adicionar 10-30% de redução além do que PyZX full_reduce já faz
**Referências:** Kissinger & van de Wetering 2020, Duncan et al. 2020

---

## 4.3. Gap #3 — Extração de Circuito sem Ancillas

**Descrição:** Melhorar o algoritmo de extração de circuito do grafo ZX simplificado para NÃO introduzir ancilla qubits.

**Problema:** O algoritmo padrão de extração (usado por PyZX) pode introduzir qubits auxiliares adicionais ao converter grafo ZX de volta para circuito. Isso é indesejável porque:
- Aumenta largura do circuito (mais qubits necessários)
- Hardware quântico tem qubits limitados
- Cliente espera circuito com o MESMO número de qubits

**Estado da arte:**
- Backens et al. (2021): Extração via CNOT synthesis — pode introduzir ancillas
- Yamamoto & Yoshioka (2026): pygridsynth é "ancilla-free" para síntese, mas não para extração de grafos ZX gerais
- Kissinger & van de Wetering: Provam que extração ancilla-free é possível para "graph-like" ZX-diagrams com Gauss elimination

**O que falta pesquisar:**
- Condições necessárias e suficientes para extração ancilla-free
- Algoritmo de eliminação gaussiana adaptado para preservar otimalidade de T-count
- Trade-off: menos ancillas vs. mais gates (qual é preferível para o cliente?)
- Implementação eficiente para grafos grandes (>20 qubits)

**Complexidade:** Alta — combina álgebra linear e teoria de grafos
**Impacto:** Crítico para usabilidade (clientes não aceitam circuitos com mais qubits)
**Referências:** Backens et al. 2021, de Beaudrap & Horsman 2020

---

## 4.4. Gap #4 — Benchmarking Industrial e Validação End-to-End

**Descrição:** Validar empiricamente que a redução de T-count se traduz em economia REAL quando o circuito é executado em QPU.

**Problema:** A teoria prevê que menos portas T = menor custo, mas:
- O mapeamento físico (after SynthQ) pode introduzir overhead que anula ganhos
- Noise models diferentes podem beneficiar circuitos com mais ou menos T-gates
- Pricing das plataformas pode não ser exatamente proporcional ao T-count

**O que falta fazer:**
- Executar circuitos originais e otimizados em QPU real (IBM Quantum, IonQ via AWS Braket)
- Medir: fidelidade do resultado, tempo de execução, custo cobrado
- Confirmar que otimização ZX + transpilação subsequente > transpilação sozinha
- Construir suite de benchmarks com circuitos industriais reais (não apenas acadêmicos)
- Publicar resultados para credibilidade

**Complexidade:** Média (mais operacional que científica)
**Impacto:** Fundamental para validação de mercado (resposta à Pergunta 6 do Anexo B)
**Dependência:** Acesso a QPU (via IBM Quantum Network Academic ou AWS Braket Credits)

---

# 5. ROADMAP TÉCNICO (16 SEMANAS — 4 SPRINTS)

## Sprint 1 (Semanas 1-4): Fundação

| Semana | Entregável | Responsável |
|--------|-----------|-------------|
| 1 | Setup repositório + CI/CD + dependências | Leandro |
| 1 | Parser OpenQASM 2.0 funcional + testes | Leandro |
| 2 | Decompositor Clifford+T (ângulos exatos) funcional | Leandro |
| 2 | Integração com PyZX: circuito → grafo ZX → full_reduce → extração | Leandro |
| 3 | Pipeline completa end-to-end (QASM in → QASM out) | Leandro |
| 3 | Testes de corretude (verificar equivalência unitária via simulação) | Leandro |
| 4 | Módulo de métricas (T-count, depth, gate count) | Leandro |
| 4 | **DEMO**: Notebook Jupyter demonstrando pipeline em 3-5 circuitos | Leandro |

**Entregável do Sprint 1:** Protótipo funcional demonstrável para vídeo de inscrição.

## Sprint 2 (Semanas 5-8): Motor v1

| Semana | Entregável | Responsável |
|--------|-----------|-------------|
| 5 | Benchmark suite: 10 circuitos de referência em QASM | Leandro |
| 5 | Rodar benchmark comparativo (SynthQ vs PyZX vs Qiskit transpiler) | Leandro |
| 6 | Decompositor: suporte a RZ de ângulo geral (via Solovay-Kitaev provisório) | Leandro |
| 6 | Suporte a OpenQASM 3.0 (parsing + export) | Leandro |
| 7 | API REST básica (FastAPI, endpoint /optimize) | Leandro |
| 7 | Containerização Docker | Leandro |
| 8 | Documentação técnica (README, docstrings, exemplos) | Leandro |
| 8 | **RELEASE**: Motor v1.0 — pipeline completa, API funcional, 10 benchmarks | Leandro |

## Sprint 3 (Semanas 9-12): Otimizações Avançadas

| Semana | Entregável | Responsável |
|--------|-----------|-------------|
| 9 | Implementação de phase gadget optimization (além do PyZX padrão) | Leandro |
| 9 | Heurística v1 de ordenação de regras (testes A/B em benchmark suite) | Leandro |
| 10 | Pesquisa: implementação parcial de gridsynth próprio (Gap #1) | Leandro |
| 10 | Expandir benchmark para 20 circuitos (incluir VQE e QAOA industriais) | Leandro |
| 11 | Otimização de extração: minimizar ancillas na conversão ZX→circuito | Leandro |
| 11 | Adicionar T-depth como métrica secundária de otimização | Leandro |
| 12 | Performance profiling + otimização de hot paths | Leandro |
| 12 | **RELEASE**: Motor v1.1 — performance 2x melhor, suporte a 20 qubits | Leandro |

## Sprint 4 (Semanas 13-16): Validação e Produtização

| Semana | Entregável | Responsável |
|--------|-----------|-------------|
| 13 | Validação em QPU real (IBM Quantum ou AWS Braket) | Leandro |
| 13 | Relatório de economia real vs. teórica | Leandro + Luccas |
| 14 | Dashboard de métricas para cliente (resultado visual) | Leandro |
| 14 | Proposta de patente: redigir reivindicações com apoio jurídico | Luccas |
| 15 | Primeiro PoC com circuito real de cliente | Ambos |
| 15 | Preprint arXiv: resultados de benchmark + metodologia | Leandro |
| 16 | Polish: API documentada (Swagger), onboarding guide, exemplos | Ambos |
| 16 | **RELEASE**: Motor v1.2 — validado em QPU, pronto para PoC comercial | Ambos |

---

# 6. TESTES E VERIFICAÇÃO DE CORRETUDE

## 6.1. Princípio Fundamental

> Todo circuito otimizado DEVE ser matematicamente equivalente ao original.
> Se o motor introduz QUALQUER erro, o produto é inútil.

## 6.2. Estratégia de Testes

```python
# tests/test_correctness.py — EXEMPLO

import numpy as np
import pyzx as zx
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from hypothesis import given, strategies as st

from synthq.zx_engine.core import ZXEngine


def circuits_are_equivalent(qasm_original: str, qasm_optimized: str, tolerance: float = 1e-8) -> bool:
    """
    Verifica equivalência unitária entre dois circuitos.

    Calcula a matriz unitária de ambos e verifica se são iguais
    (a menos de fase global).
    """
    from qiskit.quantum_info import Operator

    op_original = Operator(QuantumCircuit.from_qasm_str(qasm_original))
    op_optimized = Operator(QuantumCircuit.from_qasm_str(qasm_optimized))

    return op_original.equiv(op_optimized, rtol=tolerance)


def test_qft_5_equivalence():
    """O circuito QFT-5 otimizado é equivalente ao original."""
    with open("benchmarks/circuits/qft_5.qasm") as f:
        original_qasm = f.read()

    engine = ZXEngine(strategy="full")
    result = engine.optimize(original_qasm)
    optimized_circuit = engine.extract_circuit(result.optimized_graph)
    optimized_qasm = optimized_circuit.to_qasm()

    assert circuits_are_equivalent(original_qasm, optimized_qasm)


@given(st.integers(min_value=2, max_value=6))
def test_random_circuits_equivalence(n_qubits):
    """
    Property-based test: qualquer circuito aleatório Clifford+T
    mantém equivalência após otimização.
    """
    # Gerar circuito aleatório
    random_circuit = zx.generate.cliffordT(n_qubits, depth=20, p_t=0.3)
    original_qasm = random_circuit.to_qasm()

    engine = ZXEngine(strategy="full")
    result = engine.optimize(original_qasm)
    optimized_circuit = engine.extract_circuit(result.optimized_graph)
    optimized_qasm = optimized_circuit.to_qasm()

    assert circuits_are_equivalent(original_qasm, optimized_qasm)
```

## 6.3. Níveis de Teste

| Nível | O que testa | Como | Frequência |
|-------|------------|------|-----------|
| Unitário | Cada módulo isoladamente | pytest, mocks | Cada commit |
| Integração | Pipeline end-to-end | Circuitos de referência | Cada PR |
| Corretude | Equivalência unitária | Simulação de matriz unitária | Cada PR |
| Property-based | Circuitos aleatórios | hypothesis (1000+ testes) | CI diário |
| Benchmark | Performance e redução | Suite de 10-20 circuitos | Semanal |
| Validação QPU | Equivalência em hardware real | Execução IBM Quantum | Mensal |

---

# 7. CONSIDERAÇÕES DE PROPRIEDADE INTELECTUAL

## 7.1. O que é IP proprietário (não publicar/não open-source):

1. **Heurísticas de ordenação de regras** (Gap #2): a sequência específica em que aplicamos as transformações ZX para maximizar T-count reduction em circuitos industriais
2. **Condições de aplicação** de cada regra: quando e como decidimos aplicar phase teleportation, pivot, complementation local
3. **Critérios de parada**: algoritmo de decisão sobre quando a simplificação atingiu ponto ótimo
4. **Pipeline de integração**: como combinamos síntese gridsynth + simplificação ZX + extração ancilla-free
5. **Dados de benchmark privados**: resultados em circuitos de clientes

## 7.2. O que é publicável (gera credibilidade + citações):

1. **Resultados de benchmark** em circuitos públicos (sem revelar como)
2. **Metodologia geral** de avaliação de compiladores quânticos
3. **Contribuições teóricas** sobre confluência de ZX, condições de extração, etc.
4. **Comparações** com state-of-the-art (PyZX, pytket, Qiskit)

## 7.3. Patente potencial:

**Título:** "Sistema e método para otimização automatizada de circuitos quânticos em gate set Clifford+T via transformações categóricas em grafos ZX com heurísticas de ordenação adaptativa"

**Reivindicações centrais:**
1. Método de redução de T-count via simplificação de grafo ZX com pipeline de N passes em ordem determinada por análise estrutural do grafo
2. Sistema de API para otimização de circuitos quânticos com garantia de corretude e métricas de economia
3. Algoritmo de extração de circuito ancilla-free a partir de grafo ZX simplificado

---

*Fim do Documento 4 — Desenho Técnico do Protótipo SynthQ v1.0*
*Confidencial — contém descrição de IP proprietário.*

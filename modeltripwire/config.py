from __future__ import annotations

import os
from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel, ConfigDict, Field


class ConfigBaseModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())


class ProviderConfig(ConfigBaseModel):
    type: str = "mock"
    model_name: str = "mock-safe-v1"
    openai_api_key_env: str = "OPENAI_API_KEY"
    anthropic_api_key_env: str = "ANTHROPIC_API_KEY"


class DatasetConfig(ConfigBaseModel):
    path: str = "data/prompts/baseline_adversarial_prompts.json"


class OutputConfig(ConfigBaseModel):
    directory: str = "outputs/latest"
    sqlite_path: str = "outputs/latest/modeltripwire.db"


class TripwireConfig(ConfigBaseModel):
    enabled: List[str] = Field(default_factory=list)


class ScoringConfig(ConfigBaseModel):
    enable_rule_based: bool = True
    enable_llm_judge: bool = False
    llm_judge_model: str = "judge-beta-v1"


class ReportingConfig(ConfigBaseModel):
    title: str
    research_question: str


class AppConfig(ConfigBaseModel):
    provider: ProviderConfig
    dataset: DatasetConfig
    output: OutputConfig
    tripwires: TripwireConfig
    scoring: ScoringConfig
    reporting: ReportingConfig

    def resolve_output_directory(self, root: Path) -> Path:
        return (root / self.output.directory).resolve()

    def resolve_sqlite_path(self, root: Path) -> Path:
        return (root / self.output.sqlite_path).resolve()

    def resolve_dataset_path(self, root: Path) -> Path:
        return (root / self.dataset.path).resolve()


def load_config(config_path: str | Path) -> AppConfig:
    with Path(config_path).open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    return AppConfig.model_validate(raw)


def read_env_var(name: str) -> str | None:
    return os.getenv(name)

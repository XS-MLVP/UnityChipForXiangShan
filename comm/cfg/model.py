__all__ = [
    "RTLConfig",
    "TestConfig",
    "OutputConfig",
    "ReportConfig",
    "ReportInformationConfig",
    "ReportInformationMetaConfig",
    "ReportInformationUserConfig",
    "LogConfig",
    "DocResultConfig",
    "UnityChipConfig"
]

from pydantic import BaseModel, PositiveInt, HttpUrl, Field

from .custom_type import TemplateString


class RTLConfig(BaseModel):
    base_url: HttpUrl = Field(alias="base-url")
    version: str
    cache_dir: TemplateString = Field(alias="cache-dir")


class TestConfig(BaseModel):
    skip_tags: list[str] = Field(alias="skip-tags")
    run_tags: list[str] = Field(alias="run-tags")
    skip_cases: list[str] = Field(alias="skip-cases")
    run_cases: list[str] = Field(alias="run-cases")
    skip_exceptions: list[str] = Field(alias="skip-exceptions")


class OutputConfig(BaseModel):
    out_dir: TemplateString = Field(alias="out-dir")


class ReportInformationUserConfig(BaseModel):
    name: str
    email: str


class ReportInformationMetaConfig(BaseModel):
    version: TemplateString


class ReportInformationConfig(BaseModel):
    title: TemplateString
    user: ReportInformationUserConfig
    line_greate: int = PositiveInt()
    meta: ReportInformationMetaConfig


class ReportConfig(BaseModel):
    report_dir: TemplateString = Field(alias="report-dir")
    report_name: TemplateString = Field(alias="report-name")
    information: ReportInformationConfig = Field(alias="information")


class LogConfig(BaseModel):
    root_level: str = Field(alias="root-level")
    term_level: str = Field(alias="term-level")
    file_dir: TemplateString = Field(alias="file-dir")
    file_name: TemplateString = Field(alias="file-name")
    file_level: str = Field(alias="file-level")


class DocResultConfig(BaseModel):
    disable: bool
    dutree: TemplateString
    result_name: TemplateString = Field(alias="result-name")
    report_link: TemplateString = Field(alias="report-link")


class UnityChipConfig(BaseModel):
    # Exclude filed
    load_path: str = Field(default="", exclude=True)
    no_waveform: bool = Field(default=False, exclude=True)
    no_code_cov: bool = Field(default=False, exclude=True)
    no_func_cov: bool = Field(default=False, exclude=True)
    # Field from configure file
    rtl: RTLConfig
    test: TestConfig
    output: OutputConfig
    report: ReportConfig
    log: LogConfig
    doc_result: DocResultConfig = Field(alias="doc-result")

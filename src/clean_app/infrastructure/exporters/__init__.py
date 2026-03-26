from clean_app.infrastructure.exporters.base import DataExporter
from clean_app.infrastructure.exporters.csv_exporter import CsvExporter
from clean_app.infrastructure.exporters.excel_exporter import ExcelExporter

EXPORTERS: dict[str, type[DataExporter]] = {
    "csv": CsvExporter,
    "excel": ExcelExporter,
}


def get_exporter(format_type: str) -> DataExporter:
    exporter_class = EXPORTERS.get(format_type.lower())
    if exporter_class is None:
        supported = ", ".join(EXPORTERS.keys())
        raise ValueError(f"Unsupported format: {format_type}. Supported: {supported}")
    return exporter_class()

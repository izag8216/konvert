"""CSV format handler."""

import csv
import io

from .base import BaseFormat


class CsvFormat(BaseFormat):
    """Handle CSV serialization and deserialization.

    CSV is tabular, so conversion assumes list-of-dicts (each row = dict).
    """

    def load(self, content: str) -> list[dict]:
        reader = csv.DictReader(io.StringIO(content))
        return [dict(row) for row in reader]

    def dump(self, data: object, pretty: bool = False) -> str:
        if not isinstance(data, list):
            data = [data] if isinstance(data, dict) else [{"value": data}]

        if not data:
            return ""

        output = io.StringIO()
        if isinstance(data[0], dict):
            keys = list(data[0].keys())
            writer = csv.DictWriter(output, fieldnames=keys)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        else:
            writer = csv.writer(output)
            for row in data:
                writer.writerow([row])

        return output.getvalue()

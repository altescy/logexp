from __future__ import annotations
import typing as tp


class Table:
    _MIN_MAX_COLUMN_WIDTH = 3

    def __init__(self, columns: tp.List[str], max_column_width: int = None) -> None:
        if max_column_width is not None and max_column_width < Table._MIN_MAX_COLUMN_WIDTH:
            raise ValueError(
                f"max_column_widh must be larger than"
                f"{Table._MIN_MAX_COLUMN_WIDTH}: {max_column_width}"
            )

        self._columns = columns
        self._max_column_width = max_column_width
        self._items: tp.List[tp.Dict[str, tp.Any]] = []

    def __getitem__(self, columns: tp.List[str]) -> Table:
        table = Table(columns=columns, max_column_width=self._max_column_width)
        for item in self._items:
            table.add(item)
        return table

    @staticmethod
    def _get_padded_column_value(value: str, width: int) -> str:
        if len(value) > width:
            assert len(value) >= Table._MIN_MAX_COLUMN_WIDTH
            value = value[:width - 2] + ".."

        return f"{value:{width}}"

    @staticmethod
    def _get_column_value_str(value: tp.Any) -> str:
        if isinstance(value, str):
            return repr(value)[1:-1]
        return repr(value)

    def _get_column_widths(self) -> tp.Dict[str, int]:
        column_widths: tp.Dict[str, int] = {}
        for col in self.columns:
            column_values = [x[col] for x in self._items]
            column_value_strings = [self._get_column_value_str(x) for x in column_values]

            column_width = max(len(x) for x in column_value_strings + [col])

            if self._max_column_width is not None:
                column_width = min(column_width, self._max_column_width)

            column_widths[col] = column_width
        return column_widths

    @property
    def columns(self) -> tp.List[str]:
        return self._columns

    def add(self, item: tp.Dict[str, tp.Any]) -> None:
        self._items.append({col: item[col] for col in self.columns})

    def sort(self, column: str, desc: bool = False) -> None:
        self._items = sorted(self._items, key=lambda x: x[column], reverse=desc)

    def print(self) -> None:
        column_widths = self._get_column_widths()

        print(
            " ".join(
                self._get_padded_column_value(col, column_widths[col])
                for col in self.columns
            )
        )
        print(" ".join("=" * column_widths[col] for col in self.columns))
        for item in self._items:
            print(
                " ".join(
                    self._get_padded_column_value(
                        self._get_column_value_str(item[col]),
                        column_widths[col]
                    )
                    for col in self.columns
                )
            )

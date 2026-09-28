from PyQt6.QtCore import Qt, QRectF, QLineF
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QBrush
from PyQt6.QtWidgets import QWidget


class FretboardWidget(QWidget):
    """Visualiza una ventana fija del mástil de guitarra.

    El modelo musical conserva el orden sexta -> primera. La capa visual
    invierte las cuerdas para mostrar primera cuerda arriba y sexta abajo.

    El traste 0 (cuerda al aire) no es un traste físico: se representa en
    una zona independiente a la izquierda de la cejilla. El primer traste
    empieza inmediatamente después de la cejilla.
    """

    OPEN_STRING_WIDTH = 82.0
    NUT_WIDTH = 10.0
    FRET_LINE_WIDTH = 3.0
    STRING_LINE_WIDTH = 3.0
    VISIBLE_FRETS = 15  # cantidad de trastes físicos visibles (1..15)
    NOTE_RADIUS_FACTOR = 0.36

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tuning = None
        self._positions = []
        self._total_frets = 24
        self._view_start = 0  # 0 = cuerdas al aire + 1..15; luego 1..15, etc.
        self._root_name = ""
        self.setMinimumHeight(390)

    @property
    def view_start(self):
        return self._view_start

    def max_view_start(self):
        # Con 24 trastes y 15 visibles, la última ventana es 10..24.
        return max(0, self._total_frets - self.VISIBLE_FRETS + 1)

    def set_data(self, tuning, positions, total_frets: int, root_name: str):
        self._tuning = tuning
        self._positions = positions
        self._total_frets = max(1, total_frets)
        self._root_name = root_name
        self._view_start = min(self._view_start, self.max_view_start())
        self.update()

    def set_view_start(self, start: int):
        self._view_start = max(0, min(start, self.max_view_start()))
        self.update()

    def move_view(self, delta: int):
        self.set_view_start(self._view_start + delta)

    def can_move_left(self):
        return self._view_start > 0

    def can_move_right(self):
        return self._view_start < self.max_view_start()

    def visible_range(self):
        """Devuelve el rango de trastes físicos que se está mostrando."""
        if self._view_start == 0:
            return 0, min(self._total_frets, self.VISIBLE_FRETS)

        end = min(
            self._total_frets,
            self._view_start + self.VISIBLE_FRETS - 1,
        )
        return self._view_start, end

    def _visible_frets(self):
        """Cantidad de celdas de trastes físicos visibles."""
        return min(
            self.VISIBLE_FRETS,
            max(1, self._total_frets - max(1, self._view_start) + 1),
        )

    def _fret_origin_x(self, left):
        # Cuando se ve el traste 0, la cejilla es el borde izquierdo de
        # la zona de trastes. Cuando se navega, el primer traste visible
        # ocupa inmediatamente el borde izquierdo.
        if self._view_start == 0:
            return left + self.OPEN_STRING_WIDTH + self.NUT_WIDTH
        return left

    def _note_x(self, fret, origin, fret_width):
        if fret == 0 and self._view_start == 0:
            # Centro de la zona de cuerda al aire.
            return origin - self.NUT_WIDTH - self.OPEN_STRING_WIDTH * 0.5

        first_fret = 1 if self._view_start == 0 else self._view_start
        cell_index = fret - first_fret
        return origin + (cell_index + 0.5) * fret_width

    def paintEvent(self, event):
        if not self._tuning:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = float(self.width())
        height = float(self.height())

        left = 20.0
        right = 20.0
        top = 54.0
        bottom = 74.0  # más espacio para los números de traste

        board_height = max(220.0, height - top - bottom)
        board_bottom = top + board_height

        painter.fillRect(
            QRectF(0.0, 0.0, width, height),
            QColor("#1f1f1f"),
        )

        origin = self._fret_origin_x(left)
        fret_area_width = max(200.0, width - right - origin)
        visible = self._visible_frets()
        fret_width = fret_area_width / max(1, visible)

        # Madera del diapasón.
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#D9B37A")))
        painter.drawRect(
            QRectF(origin, top, fret_area_width, board_height)
        )

        string_count = len(self._tuning.strings)
        string_gap = board_height / max(1, string_count - 1)

        # Cejilla: separa físicamente las cuerdas al aire del traste 1.
        if self._view_start == 0:
            nut_x = left + self.OPEN_STRING_WIDTH
            painter.setPen(
                QPen(QColor("#E6E6E6"), self.NUT_WIDTH)
            )
            painter.drawLine(
                QLineF(nut_x, top, nut_x, board_bottom)
            )

        # Líneas de trastes. En la vista inicial la primera línea es la
        # cejilla; las siguientes son los límites de 1, 2, ... 15.
        painter.setPen(
            QPen(QColor("#6D6D6D"), self.FRET_LINE_WIDTH)
        )
        for i in range(visible + 1):
            x = origin + i * fret_width
            painter.drawLine(
                QLineF(x, top, x, board_bottom)
            )

        # Cuerdas. El modelo es sexta -> primera; visualmente se invierte.
        for model_index, open_note in enumerate(self._tuning.strings):
            visual_index = string_count - 1 - model_index
            y = top + visual_index * string_gap

            painter.setPen(
                QPen(QColor("#C8C8C8"), self.STRING_LINE_WIDTH)
            )
            painter.drawLine(
                QLineF(origin, y, origin + fret_area_width, y)
            )

            # Etiqueta de cuerda a la izquierda.
            painter.setPen(QColor("#E8E8E8"))
            painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            label = f"{model_index + 1}ª {open_note.name}"
            painter.drawText(
                QRectF(0.0, y - 13.0, left - 8.0, 26.0),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                label,
            )

        # Números de traste: siempre se dibujan debajo del diapasón,
        # nunca encima de las notas de la sexta/primera cuerda.
        painter.setPen(QColor("#D0D0D0"))
        painter.setFont(QFont("Arial", 10))

        first_fret = 1 if self._view_start == 0 else self._view_start
        last_fret = min(
            self._total_frets,
            first_fret + visible - 1,
        )

        for fret in range(first_fret, last_fret + 1):
            x = self._note_x(fret, origin, fret_width)
            painter.drawText(
                QRectF(
                    x - 24.0,
                    board_bottom + 20.0,
                    48.0,
                    24.0,
                ),
                Qt.AlignmentFlag.AlignCenter,
                str(fret),
            )

        self._draw_inlays(
            painter,
            origin,
            top,
            board_height,
            fret_width,
            visible,
        )

        radius = min(
            24.0,
            max(
                14.0,
                min(fret_width * self.NOTE_RADIUS_FACTOR, string_gap * 0.38),
            ),
        )

        # Notas. El traste 0 es especial; los demás usan celdas 1..N.
        for item in self._positions:
            if item.fret > self._total_frets:
                continue

            if self._view_start == 0:
                if item.fret < 0 or item.fret > visible:
                    continue
            else:
                if item.fret < self._view_start:
                    continue
                if item.fret > self._view_start + visible - 1:
                    continue

            visual_index = string_count - 1 - item.string_index
            y = top + visual_index * string_gap
            x = self._note_x(item.fret, origin, fret_width)

            fill = QColor("#C92A2A" if item.is_root else "#145A91")
            painter.setBrush(QBrush(fill))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(
                QRectF(
                    x - radius,
                    y - radius,
                    radius * 2.0,
                    radius * 2.0,
                )
            )

            painter.setPen(QColor("#FFFFFF"))
            painter.setFont(
                QFont(
                    "Arial",
                    max(9, int(radius * 0.62)),
                    QFont.Weight.Bold,
                )
            )
            painter.drawText(
                QRectF(
                    x - radius,
                    y - radius,
                    radius * 2.0,
                    radius * 2.0,
                ),
                Qt.AlignmentFlag.AlignCenter,
                item.note.name,
            )

    def _draw_inlays(
        self,
        painter,
        origin,
        top,
        height,
        fret_width,
        visible,
    ):
        painter.setBrush(QBrush(QColor("#8C6D39")))
        painter.setPen(Qt.PenStyle.NoPen)

        first_fret = 1 if self._view_start == 0 else self._view_start
        last_fret = min(
            self._total_frets,
            first_fret + visible - 1,
        )

        for fret in (3, 5, 7, 9, 15, 17, 19, 21):
            if first_fret <= fret <= last_fret:
                cell_index = fret - first_fret
                x = origin + (cell_index + 0.5) * fret_width
                y = top + height / 2.0
                painter.drawEllipse(
                    QRectF(x - 6.0, y - 6.0, 12.0, 12.0)
                )

        for fret in (12, 24):
            if first_fret <= fret <= last_fret and self._total_frets >= fret:
                cell_index = fret - first_fret
                x = origin + (cell_index + 0.5) * fret_width
                painter.drawEllipse(
                    QRectF(
                        x - 6.0,
                        top + height * 0.34 - 6.0,
                        12.0,
                        12.0,
                    )
                )
                painter.drawEllipse(
                    QRectF(
                        x - 6.0,
                        top + height * 0.66 - 6.0,
                        12.0,
                        12.0,
                    )
                )

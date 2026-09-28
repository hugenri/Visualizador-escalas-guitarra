from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from data.scales import SCALES
from domain.note import NOTE_NAMES_SHARP, Note
from domain.tuning import STANDARD_TUNING
from services.fretboard_service import FretboardService
from ui.fretboard_widget import FretboardWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de escalas para guitarra")
        self.resize(1280, 720)
        self.setMinimumSize(1050, 600)

        self.service = FretboardService()

        # Controles de selección
        self.root_combo = QComboBox()
        self.root_combo.addItems(NOTE_NAMES_SHARP)

        self.scale_combo = QComboBox()
        for scale in SCALES.values():
            self.scale_combo.addItem(scale.name, scale.id)

        self.total_frets_combo = QComboBox()
        self.total_frets_combo.addItems(["22", "24"])
        self.total_frets_combo.setCurrentText("24")

        self.info = QLabel()
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        controls = QFormLayout()
        controls.setVerticalSpacing(12)
        controls.addRow("Tonalidad:", self.root_combo)
        controls.addRow("Escala:", self.scale_combo)
        controls.addRow("Trastes totales:", self.total_frets_combo)

        control_widget = QWidget()
        control_widget.setLayout(controls)
        control_widget.setMaximumWidth(330)

        # Controles de navegación
        self.left_button = QPushButton("◀")
        self.right_button = QPushButton("▶")
        self.left_button.setFixedSize(52, 38)
        self.right_button.setFixedSize(52, 38)

        self.range_label = QLabel()
        self.range_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.range_label.setMinimumWidth(250)

        nav = QHBoxLayout()
        nav.setSpacing(12)
        nav.addWidget(self.left_button)
        nav.addWidget(self.range_label)
        nav.addWidget(self.right_button)

        # Configuración del diseño principal
        self.fretboard = FretboardWidget()

        header = QHBoxLayout()
        header.addWidget(control_widget)
        header.addWidget(self.info, 1)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)
        layout.addLayout(header)
        layout.addLayout(nav)
        layout.addWidget(self.fretboard, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Conexiones de señales
        self.root_combo.currentIndexChanged.connect(self.update_view)
        self.scale_combo.currentIndexChanged.connect(self.update_view)
        self.total_frets_combo.currentIndexChanged.connect(self.update_view)

        self.left_button.clicked.connect(lambda: self.move_view(-1))
        self.right_button.clicked.connect(lambda: self.move_view(1))

        self.update_view()

    def update_view(self):
        root = Note.from_name(self.root_combo.currentText())
        scale = SCALES[self.scale_combo.currentData()]
        total = int(self.total_frets_combo.currentText())

        positions = self.service.positions(STANDARD_TUNING, root, scale, total)
        self.fretboard.set_data(STANDARD_TUNING, positions, total, root.name)
        self.update_navigation()

        self.info.setText(
            f"<span style='font-size: 24px; font-weight: bold;'>{root.name} {scale.name}</span><br>"
            f"<span style='font-size: 13px;'>Rojo = tónica · Azul = notas de la escala</span>"
        )

    def move_view(self, delta):
        self.fretboard.move_view(delta)
        self.update_navigation()

    def update_navigation(self):
        start, end = self.fretboard.visible_range()
        prefix = "Cuerdas al aire" if start == 0 else f"Traste {start}"
        self.range_label.setText(f"{prefix}  •  {start}–{end}")
        self.left_button.setEnabled(self.fretboard.can_move_left())
        self.right_button.setEnabled(self.fretboard.can_move_right())


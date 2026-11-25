import sys
from PySide6.QtCore import QTimer, Qt, QUrl
from PySide6.QtGui import QColor, QPixmap, QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from Body import Body

APP_STYLESHEET = """
QWidget {
    background-color: #12161f;
    color: #eef2f7;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}

QFrame#card {
    background-color: #1a202c;
    border: 1px solid #2b3548;
    border-radius: 14px;
}

QFrame#bridge_bar {
    background-color: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 8px;
}

QLabel#title_label {
    font-size: 18px;
    font-weight: 700;
    color: #f8fafc;
}

QLabel#section_label {
    font-size: 12px;
    font-weight: 600;
    color: #94a3b8;
}

QDoubleSpinBox, QComboBox {
    background-color: #0f131b;
    color: #f1f5f9;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 6px 8px;
    font-weight: 600;
}

QDoubleSpinBox:read-only {
    background-color: #1e293b;
    color: #fde047;
    border: 1px solid #475569;
}

QSlider::groove:vertical {
    background: #1e293b;
    width: 10px;
    border-radius: 5px;
    border: 1px solid #334155;
}

QSlider::handle:vertical {
    background: #f8fafc;
    border: 2px solid #38bdf8;
    height: 18px;
    margin: 0 -6px;
    border-radius: 9px;
}

QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 700;
}

QPushButton:hover {
    background-color: #3b82f6;
}

QPushButton:pressed {
    background-color: #1d4ed8;
}

QPushButton#toggle_btn {
    background-color: #16a34a;
    font-size: 14px;
}

QPushButton#toggle_btn:hover {
    background-color: #22c55e;
}

QPushButton#toggle_btn:checked {
    background-color: #dc2626;
}

QPushButton#toggle_btn:checked:hover {
    background-color: #ef4444;
}

QPushButton#secondary_btn {
    background-color: #263042;
    border: 1px solid #3b4a63;
}

QPushButton#secondary_btn:hover {
    background-color: #334158;
}
"""


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About - Heat Transfer")
        self.resize(440, 480)
        self.setStyleSheet(APP_STYLESHEET)

       
        self.image_path = "elmo.jpg"
        self.author_name = "Ziv Taieb"
        self.author_email = "ziv.taieb@s.afeka.ac.il"
        self.linkedin_url = "www.linkedin.com/in/ziv-taieb-604192316"
        self.github_url = ""

        self.setupUI()

    def open_linkedin(self):
        QDesktopServices.openUrl(QUrl(self.linkedin_url))

    def open_github(self):
        QDesktopServices.openUrl(QUrl(self.github_url))

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(12)

        title = QLabel("Heat Conduction Simulator")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignCenter)

        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(140, 140)
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(
                pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            self.image_label.setStyleSheet("border-radius: 12px;")
        else:
            self.image_label.setText("Add Image\n(profile.png)")
            self.image_label.setStyleSheet(
                "background-color: #0f172a; border: 2px dashed #475569; "
                "border-radius: 12px; color: #94a3b8; font-weight: 600;"
            )

        image_row = QHBoxLayout()
        image_row.addStretch()
        image_row.addWidget(self.image_label)
        image_row.addStretch()

        name_label = QLabel(self.author_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #f8fafc;")

        email_label = QLabel(self.author_email)
        email_label.setAlignment(Qt.AlignCenter)
        email_label.setStyleSheet("font-size: 13px; color: #94a3b8;")

        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(12)

        self.linkedin_button = QPushButton("LinkedIn")
        self.linkedin_button.setStyleSheet(
            "QPushButton { background-color: #0a66c2; }"
            "QPushButton:hover { background-color: #0077b5; }"
        )
        self.linkedin_button.clicked.connect(self.open_linkedin)

        self.github_button = QPushButton("GitHub")
        self.github_button.setObjectName("secondary_btn")
        self.github_button.clicked.connect(self.open_github)

        buttons_row.addWidget(self.linkedin_button)
        buttons_row.addWidget(self.github_button)

        card_layout.addWidget(title)
        card_layout.addSpacing(4)
        card_layout.addLayout(image_row)
        card_layout.addWidget(name_label)
        card_layout.addWidget(email_label)
        card_layout.addSpacing(10)
        card_layout.addLayout(buttons_row)

        layout.addWidget(card)


class GraphWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Graph Window")
        self.resize(780, 480)
        self.setStyleSheet(APP_STYLESHEET)
        self.setupUI()

    def setupUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(14)

        plot_card = QFrame()
        plot_card.setObjectName("card")
        plot_layout = QVBoxLayout(plot_card)
        plot_layout.setContentsMargins(10, 10, 10, 10)

        self.figure = Figure(figsize=(5.5, 4.2), facecolor="#1a202c")
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#0f131b")
        self.ax.set_title("Temperature vs. Time", color="#f8fafc", fontsize=12, fontweight="bold")
        self.ax.set_xlabel("Time (s)", color="#cbd5e1")
        self.ax.set_ylabel("Temperature (°C)", color="#cbd5e1")
        self.ax.tick_params(colors="#cbd5e1")
        for spine in self.ax.spines.values():
            spine.set_color("#334155")
        self.ax.grid(True, linestyle="--", alpha=0.25, color="#94a3b8")

        self.canvas = FigureCanvasQTAgg(self.figure)
        plot_layout.addWidget(self.canvas)

        controls_card = QFrame()
        controls_card.setObjectName("card")
        controls_card.setFixedWidth(210)
        controls_layout = QVBoxLayout(controls_card)
        controls_layout.setContentsMargins(16, 18, 16, 18)
        controls_layout.setSpacing(12)

        select_label = QLabel("Select Body to Plot")
        select_label.setObjectName("section_label")

        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2", "Both Bodies"])

        self.draw_button = QPushButton("Draw")
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("secondary_btn")
        self.export_button = QPushButton("Export to CSV")
        self.export_button.setObjectName("secondary_btn")

        controls_layout.addWidget(select_label)
        controls_layout.addWidget(self.body_combo)
        controls_layout.addSpacing(8)
        controls_layout.addWidget(self.draw_button)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.export_button)
        controls_layout.addStretch()

        main_layout.addWidget(plot_card, stretch=1)
        main_layout.addWidget(controls_card)

class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heat Transfer")
        self.resize(860, 560)
        self.setStyleSheet(APP_STYLESHEET)

        # add other window variables here
        self.graph_window = GraphWindow(self)
        self.about_window = AboutWindow()

        # add other needed variables
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        # initialize the timer
        self.timer = QTimer()

        self.setupUI()

    def _create_body_panel(self, title_text, default_temp, default_color):
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        header = QLabel(title_text)
        header.setObjectName("title_label")
        header.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(header)

        visual_row = QHBoxLayout()
        visual_row.setSpacing(14)

        slider = QSlider(Qt.Vertical)
        slider.setRange(0, 200)
        slider.setValue(int(default_temp))
        slider.setMinimumHeight(180)

        body_box = QFrame()
        body_box.setMinimumSize(130, 180)
        body_box.setStyleSheet(
            f"background-color: {default_color}; border-radius: 14px; border: 2px solid #f8fafc;"
        )

        visual_row.addStretch()
        visual_row.addWidget(slider)
        visual_row.addWidget(body_box)
        visual_row.addStretch()
        card_layout.addLayout(visual_row)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(8)

        temp_label = QLabel("Temp.")
        temp_label.setObjectName("section_label")
        temp_display = QDoubleSpinBox()
        temp_display.setRange(0.0, 200.0)
        temp_display.setDecimals(1)
        temp_display.setValue(default_temp)
        temp_display.setSuffix(" °C")
        temp_display.setReadOnly(True)
        temp_display.setButtonSymbols(QDoubleSpinBox.NoButtons)

        mass_label = QLabel("Mass")
        mass_label.setObjectName("section_label")
        mass_spin = QDoubleSpinBox()
        mass_spin.setRange(0.1, 10000.0)
        mass_spin.setDecimals(2)
        mass_spin.setValue(10.0)
        mass_spin.setSuffix(" kg")

        cap_label = QLabel("H. Cap.")
        cap_label.setObjectName("section_label")
        cap_spin = QDoubleSpinBox()
        cap_spin.setRange(0.01, 1000.0)
        cap_spin.setDecimals(2)
        cap_spin.setValue(0.4)
        cap_spin.setSuffix(" J/kg°C")

        grid.addWidget(temp_label, 0, 0)
        grid.addWidget(temp_display, 0, 1)
        grid.addWidget(mass_label, 1, 0)
        grid.addWidget(mass_spin, 1, 1)
        grid.addWidget(cap_label, 2, 0)
        grid.addWidget(cap_spin, 2, 1)

        card_layout.addLayout(grid)

        return card, slider, body_box, temp_display, mass_spin, cap_spin


        self.setupUI()

    def setupUI(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(14)

        top_bar = QHBoxLayout()
        app_title = QLabel("HEAT CONDUCTION STUDIO")
        app_title.setObjectName("title_label")

        self.about_button = QPushButton("About")
        self.about_button.setObjectName("secondary_btn")
        self.about_button.clicked.connect(self.about_window.show)

        top_bar.addWidget(app_title)
        top_bar.addStretch()
        top_bar.addWidget(self.about_button)
        root_layout.addLayout(top_bar)

        stage_layout = QHBoxLayout()
        stage_layout.setSpacing(12)

        left_card, self.left_slider, self.left_body_box, self.left_temp_spin, self.left_mass_spin, self.left_cap_spin = (
            self._create_body_panel("Body 1", 200.0, "#ef4444")
        )

        center_panel = QVBoxLayout()
        center_panel.setSpacing(10)

        cond_card = QFrame()
        cond_card.setObjectName("card")
        cond_layout = QVBoxLayout(cond_card)
        cond_layout.setContentsMargins(12, 12, 12, 12)
        cond_layout.setSpacing(6)

        cond_label = QLabel("Conductivity")
        cond_label.setObjectName("section_label")
        cond_label.setAlignment(Qt.AlignCenter)

        self.conductivity_spin = QDoubleSpinBox()
        self.conductivity_spin.setRange(0.01, 500.0)
        self.conductivity_spin.setDecimals(2)
        self.conductivity_spin.setValue(1.0)
        self.conductivity_spin.setSuffix(" J/s°C")

        cond_layout.addWidget(cond_label)
        cond_layout.addWidget(self.conductivity_spin)

        bridge = QFrame()
        bridge.setObjectName("bridge_bar")
        bridge.setFixedHeight(22)

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("toggle_btn")
        self.start_button.setCheckable(True)
        self.start_button.setMinimumHeight(44)

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setMinimumHeight(40)
        self.graphs_button.clicked.connect(self.graph_window.show)

        center_panel.addStretch()
        center_panel.addWidget(cond_card)
        center_panel.addWidget(bridge)
        center_panel.addSpacing(8)
        center_panel.addWidget(self.start_button)
        center_panel.addWidget(self.graphs_button)
        center_panel.addStretch()

        right_card, self.right_slider, self.right_body_box, self.right_temp_spin, self.right_mass_spin, self.right_cap_spin = (
            self._create_body_panel("Body 2", 0.0, "#111827")
        )

        stage_layout.addWidget(left_card, stretch=1)
        stage_layout.addLayout(center_panel)
        stage_layout.addWidget(right_card, stretch=1)
        root_layout.addLayout(stage_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
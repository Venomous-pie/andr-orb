from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QSizeGrip, QSizePolicy
)
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QUrl
from config import PANEL_WIDTH, PANEL_HEIGHT

from PyQt6.QtWebEngineWidgets import QWebEngineView
import markdown

GRIP_SIZE = 8

class ResizeHandle(QWidget):
    def __init__(self, parent, edge):
        super().__init__(parent)
        self.edge = edge
        self.setMouseTracking(True)
        self._drag_start = None
        self._start_geo = None

        cursors = {
            "left":        Qt.CursorShape.SizeHorCursor,
            "right":       Qt.CursorShape.SizeHorCursor,
            "top":         Qt.CursorShape.SizeVerCursor,
            "bottom":      Qt.CursorShape.SizeVerCursor,
            "top-left":    Qt.CursorShape.SizeFDiagCursor,
            "top-right":   Qt.CursorShape.SizeBDiagCursor,
            "bottom-left": Qt.CursorShape.SizeBDiagCursor,
            "bottom-right":Qt.CursorShape.SizeFDiagCursor,
        }
        self.setCursor(cursors[edge])

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_start = e.globalPosition().toPoint()
            self._start_geo = self.window().geometry()

    def mouseMoveEvent(self, e):
        if self._drag_start is None:
            return
        delta = e.globalPosition().toPoint() - self._drag_start
        geo = QRect(self._start_geo)
        dx, dy = delta.x(), delta.y()

        if "right" in self.edge:
            geo.setRight(geo.right() + dx)
        if "bottom" in self.edge:
            geo.setBottom(geo.bottom() + dy)
        if "left" in self.edge:
            geo.setLeft(geo.left() + dx)
        if "top" in self.edge:
            geo.setTop(geo.top() + dy)

        min_w, min_h = self.window().minimumSize().width(), self.window().minimumSize().height()
        if geo.width() >= min_w and geo.height() >= min_h:
            self.window().setGeometry(geo)

    def mouseReleaseEvent(self, e):
        self._drag_start = None
        self._start_geo = None

class ChatPanel(QWidget):
    message_sent = pyqtSignal(str)
    collapsed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(280, 360)
        self.resize(PANEL_WIDTH, PANEL_HEIGHT)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self._drag_pos = None
        self._build_ui()
        self.hide()
    
    def get_min_btn_pos(self):
        return self.min_btn.mapToGlobal(self.min_btn.rect().center())

    def _build_ui(self):
        self.setStyleSheet("""
            QWidget#panel {
                background-color: rgba(20, 20, 30, 230);
                border-radius: 5px;
                border: 1px solid rgba(100, 180, 255, 120);
            }
            QTextEdit {
                background: transparent;
                color: #e0e0e0;
                font-size: 13px;
                border: none;
            }
            QLineEdit {
                background: rgba(255,255,255,20);
                color: white;
                border: 1px solid rgba(100,180,255,150);
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QPushButton#send_btn {
                background: rgba(100, 180, 255, 180);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 13px;
            }
            QPushButton#send_btn:hover {
                background: rgba(100, 180, 255, 255);
            }
            QPushButton#min_btn {
                background: transparent;
                color: rgba(200,200,200,180);
                border: none;
                font-size: 16px;
            }
            QPushButton#min_btn:hover { color: white; }
            QSizeGrip {
                background: transparent;
                width: 16px;
                height: 16px;
            }
        """)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.inner = QWidget(self)
        self.inner.setObjectName("panel")
        inner_layout = QVBoxLayout(self.inner)
        inner_layout.setContentsMargins(14, 10, 14, 14)
        inner_layout.setSpacing(8)

        # header (drag handle)
        header = QHBoxLayout()
        self.title = QLabel("✦ Orb")
        self.title.setStyleSheet("color: rgba(100,180,255,255); font-weight: bold; font-size: 14px;")
        self.min_btn = QPushButton("−")
        self.min_btn.setObjectName("min_btn")
        self.min_btn.setFixedSize(28, 28)
        self.min_btn.clicked.connect(self.collapse)
        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.min_btn)
        inner_layout.addLayout(header)

        # chat history
        self.history_box = QTextEdit()
        self.history_box.setReadOnly(True)
        inner_layout.addWidget(self.history_box, stretch=1)

        # input row
        input_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Say something...")
        self.input_field.returnPressed.connect(self._send)
        send_btn = QPushButton("Send")
        send_btn.setObjectName("send_btn")
        send_btn.clicked.connect(self._send)
        input_row.addWidget(self.input_field)
        input_row.addWidget(send_btn)
        inner_layout.addLayout(input_row)

        # size grip bottom-right
        grip_row = QHBoxLayout()
        grip_row.addStretch()
        grip = QSizeGrip(self)
        grip_row.addWidget(grip)
        inner_layout.addLayout(grip_row)

        outer.addWidget(self.inner)
        
        self._add_resize_handles()

    # --- drag via header ---
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint()

    def mouseMoveEvent(self, e):
        if self._drag_pos:
            delta = e.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = e.globalPosition().toPoint()

    def mouseReleaseEvent(self, e):
        self._drag_pos = None

    def resizeEvent(self, e):
        self.inner.resize(self.size())
        super().resizeEvent(e)

    def _send(self):
        text = self.input_field.text().strip()
        if text:
            self.input_field.clear()
            self.message_sent.emit(text)

    def append_message(self, role, text):
        color = "#64b4ff" if role == "user" else "#b0ffb0"
        label = "You" if role == "user" else "Orb"
        self.history_box.append(
            f'<span style="color:{color};font-weight:bold;">{label}:</span> '
            f'<span style="color:#e0e0e0;">{text}</span><br>'
        )

    def set_thinking(self, thinking: bool):
        if thinking:
            self.history_box.append(
                '<span style="color:gray;font-style:italic;">Orb is thinking...</span>'
            )

    def expand(self, orb_pos, orb_size):
        x = orb_pos.x() + orb_size + 8
        y = orb_pos.y() - (self.height() // 2) + (orb_size // 2)
        self.move(x, y)
        self.show()
        self.inner.resize(self.size())

    def collapse(self):
        self.hide()
        self.collapsed.emit()

    def _add_resize_handles(self):
        g = GRIP_SIZE
        edges = ["left", "right", "top", "bottom",
                 "top-left", "top-right", "bottom-left", "bottom-right"]
        self._handles = [ResizeHandle(self, edge) for edge in edges]
        self._reposition_handles()

    def _reposition_handles(self):
        g = GRIP_SIZE
        w, h = self.width(), self.height()
        positions = {
            "left":         QRect(0,      g,      g,      h-2*g),
            "right":        QRect(w-g,    g,      g,      h-2*g),
            "top":          QRect(g,      0,      w-2*g,  g),
            "bottom":       QRect(g,      h-g,    w-2*g,  g),
            "top-left":     QRect(0,      0,      g,      g),
            "top-right":    QRect(w-g,    0,      g,      g),
            "bottom-left":  QRect(0,      h-g,    g,      g),
            "bottom-right": QRect(w-g,    h-g,    g,      g),
        }
        for handle in self._handles:
            handle.setGeometry(positions[handle.edge])
            handle.raise_()


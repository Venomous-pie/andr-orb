from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QBrush, QRadialGradient, QPen
from config import ORB_SIZE

class Orb(QWidget):
    double_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool 
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(ORB_SIZE, ORB_SIZE)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

        self._drag_pos = None
        self._thinking = False
        self._pulse = 0
        self._pulse_dir = 1

        self._timer = QTimer()
        self._timer.timeout.connect(self._tick_pulse)
        self._timer.start(30)

        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - ORB_SIZE - 40, screen.height() - ORB_SIZE - 60)
        self.show()

    def set_thinking(self, thinking: bool):
        self._thinking = thinking

    def _tick_pulse(self):
        if self._thinking:
            self._pulse += self._pulse_dir * 4
            if self._pulse >= 80 or self._pulse <= 0:
                self._pulse_dir *= -1
        else:
            self._pulse = max(0, self._pulse - 3)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx, cy = ORB_SIZE // 2, ORB_SIZE // 2
        r = ORB_SIZE // 2 - 2

        grad = QRadialGradient(cx - r * 0.3, cy - r * 0.3, r * 1.2)
        base_alpha = 200 + self._pulse
        grad.setColorAt(0.0, QColor(160, 210, 255, min(255, base_alpha)))
        grad.setColorAt(0.5, QColor(80, 150, 240, min(255, base_alpha - 20)))
        grad.setColorAt(1.0, QColor(40, 80, 180, min(255, base_alpha - 40)))

        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        if self._thinking:
            glow = QColor(100, 200, 255, 60 + self._pulse)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(glow, 3))
            painter.drawEllipse(cx - r - 4, cy - r - 4, (r + 4) * 2, (r + 4) * 2)

    def mouseDoubleClickEvent(self, e):
        self.double_clicked.emit()

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

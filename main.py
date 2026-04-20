import sys
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal

from orb import Orb
from panel import ChatPanel
from brain import Brain
from voice import speak
from config import ORB_SIZE, PANEL_WIDTH

class Worker(QObject):
    response_ready = pyqtSignal(str)

    def __init__(self, brain):
        super().__init__()
        self.brain = brain

    def process(self, text):
        def run():
            reply = self.brain.ask(text)
            self.response_ready.emit(reply)
        threading.Thread(target=run, daemon=True).start()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    brain = Brain()
    orb = Orb()
    panel = ChatPanel()
    worker = Worker(brain)

    def on_double_click():
        if panel.isVisible():
            panel.collapse()
        else:
            orb_center = orb.mapToGlobal(orb.rect().center())
            panel.move(
                orb_center.x() - (PANEL_WIDTH - 14 - 28 // 2) + ORB_SIZE // 2,
                orb_center.y() - 10 - ORB_SIZE // 2
            )
            panel.show()
            orb.hide()

    def startup_greet():
        reply = brain.greet()
        panel.append_message("assistant", reply)
        speak(reply)
        
    threading.Thread(target=startup_greet, daemon=True).start()

    def on_collapsed():
        btn_pos = panel.get_min_btn_pos()
        orb.move(btn_pos.x() - ORB_SIZE // 2, btn_pos.y() - ORB_SIZE // 2)
        orb.show()

    def on_message(text):
        panel.append_message("user", text)
        orb.set_thinking(True)
        panel.set_thinking(True)
        worker.process(text)

    def on_response(reply):
        orb.set_thinking(False)
        panel.append_message("assistant", reply)
        speak(reply)

    orb.double_clicked.connect(on_double_click)
    panel.message_sent.connect(on_message)
    panel.collapsed.connect(on_collapsed)
    worker.response_ready.connect(on_response)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

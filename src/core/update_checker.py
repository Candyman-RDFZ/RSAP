from PySide6.QtCore import QUrl, QObject, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class UpdateChecker(QObject):
	finished = Signal(str)
	error = Signal(str)

	def __init__(self, parent):
		super().__init__()
		self.manager = QNetworkAccessManager(parent)
		self._reply = None
	
	def chk(self):
		if self._reply is not None:
			return
		request = QNetworkRequest('https://candyman33.cc/p/RSAP/ver.json')
		self._reply = self.manager.get(request)
		self._reply.finished.connect(self.on_finished)

	def abort(self):
		if self._reply is None:
			return
		self._reply.finished.disconnect(self.on_finished)
		self._reply.abort()
		self._reply.deleteLater()
		self._reply = None

	def on_finished(self):
		reply = self._reply
		self._reply = None
		if reply is None:
			self.error.emit('Empty reply.')
		if reply.error() != QNetworkReply.NetworkError.NoError:
			self.error.emit(reply.errorString())
			return
		data = bytes(reply.readAll())
		text = data.decode('utf-8', errors='replace')
		self.finished.emit(text)
		reply.deleteLater()
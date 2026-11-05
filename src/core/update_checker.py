from PySide6.QtCore import QUrl, QObject
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class UpdateChecker:
	def __init__(self, parent):
		self.manager = QNetworkAccessManager(parent)
		self._reply = None
	
	def chk(self, callback):
		if self._reply is not None:
			return
		request = QNetworkRequest('https://candyman33.cc/p/RSAP/ver.json')
		self._reply = self.manager.get(request)
		self._reply.finished.connect(lambda: self.on_finished(callback))

	def on_finished(self, callback):
		reply = self._reply
		self._reply = None
		if reply is None:
			callback(-1)
			return
		if reply.error() != QNetworkReply.NetworkError.NoError:
			callback(-1)
			return
		data = bytes(reply.readAll())
		text = data.decode('utf-8', errors='replace')
		callback(text)
		reply.deleteLater()
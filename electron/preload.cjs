 const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  readExcel: () => ipcRenderer.invoke('read-excel'),
  saveExcel: (data) => ipcRenderer.invoke('save-excel', data)
})

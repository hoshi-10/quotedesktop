console.log('✅ preload loaded')
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  readExcel: () => ipcRenderer.invoke('read-excel'),
  saveExcel: (data) => ipcRenderer.invoke('save-excel', data),
  selectAndReadExcel: () => ipcRenderer.invoke('select-and-read-excel')
})
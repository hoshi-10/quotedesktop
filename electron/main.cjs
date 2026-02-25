const { ipcMain, app,BrowserWindow } = require('electron')
const fs = require('fs')
const path = require('path')
const XLSX = require('xlsx')

let mainWindow

const excelPath = path.join(app.getPath('documents'), 'data.xlsx')

ipcMain.handle('read-excel', async () => {
  try {
    if (!fs.existsSync(excelPath)) return []

    const workbook = XLSX.readFile(excelPath)
    const sheet = workbook.Sheets[workbook.SheetNames[0]]
    const data = XLSX.utils.sheet_to_json(sheet, { defval: '' })

    return data
  } catch (error) {
    console.error('读取失败:', error)
    return []
  }
})

ipcMain.handle('save-excel', async (event, data) => {
  try {
    const headers = [
      'id',
      'content',
      'quantity',
      'price',
      'subtotal',
      'material',
      'size',
      'handler',
      'remark'
    ]

    const worksheet = XLSX.utils.json_to_sheet(data, { header: headers })
    const workbook = XLSX.utils.book_new()

    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1')
    XLSX.writeFile(workbook, excelPath)

    return true
  } catch (error) {
    console.error('保存失败:', error)
    return false
  }
})
function createWindow(){
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })

  mainWindow.loadURL('http://localhost:5173')
}
app.whenReady().then(() => {
  createWindow()
})
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

const { app, BrowserWindow } = require("electron");
function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
  });
  
  let {PythonShell} = require('python-shell')
  PythonShell.run("app.py", function (err, results) {
    if (err) console.log(err);
  });
  win.loadURL("http://127.0.0.1:5000")

}

app.whenReady().then(() => {
  createWindow();
});

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});

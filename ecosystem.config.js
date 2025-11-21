//This file is for deploying app to production using tool pm2
module.exports = {
  apps: [{
    name: "aiTravelMate-be",
    script: "app.py",
    cwd: __dirname,  //current working directory same as this file
    interpreter: "./.venv/bin/python",
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: "500M",  
    kill_timeout: 5000,  // Give process 5 seconds to shutdown gracefully
    wait_ready: false,  // Don't wait for ready event - uvicorn doesn't emit it
    listen_timeout: 0,  // Disable listen timeout check
    shutdown_with_message: false,  // Don't wait for shutdown message
    env: {
      PYTHONUNBUFFERED: "1",  // Important for real-time logs
      ENV: "production"
    },
    error_file: "./logs/python-err.log",
    out_file: "./logs/python-out.log",
    time: true
  }]
};
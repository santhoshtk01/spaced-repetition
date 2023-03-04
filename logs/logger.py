# Function to add logs to the log file.
def addLog(log: str) -> None:
    with open('logs.txt', 'a') as logFile:
        logFile.write(log + '\n')

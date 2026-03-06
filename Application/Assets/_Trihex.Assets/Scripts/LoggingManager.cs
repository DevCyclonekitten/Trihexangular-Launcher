using UnityEngine;
using System;

public class LogHandler : ILogHandler
{
    private ILogHandler m_DefaultHandler = Debug.unityLogger.logHandler;
    
    public void LogFormat(LogType logType, UnityEngine.Object context, string format, params object[] args)
    {

        string prefix = $"[{DateTime.Now:HH:mm:ss}] ";
        m_DefaultHandler.LogFormat(logType, context, prefix + format, args);
    }

    public void LogException(Exception exception, UnityEngine.Object context)
    {
        m_DefaultHandler.LogException(exception, context);
    }
}
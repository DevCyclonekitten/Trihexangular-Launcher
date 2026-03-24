using UnityEditor;
using UnityEngine.Rendering;

public class OpenGLES2BuildScript
{
    [MenuItem("OpenGLES/Force GLES2 Build Settings")]
    public static void ForceGLES2()
    {
        GraphicsDeviceType[] apis = { GraphicsDeviceType.OpenGLES2 };
        PlayerSettings.SetGraphicsAPIs(BuildTarget.StandaloneLinux64, apis);
        
        // This prints the active APIs to your Console window
        var currentAPIs = PlayerSettings.GetGraphicsAPIs(BuildTarget.StandaloneLinux64);
        foreach (var api in currentAPIs)
        {
            UnityEngine.Debug.Log("MidiBox Active API: " + api.ToString());
        }
    }
}
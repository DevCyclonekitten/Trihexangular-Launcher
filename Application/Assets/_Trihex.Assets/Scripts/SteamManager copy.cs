using System;
using System.IO;
using System.Text;
using UnityEngine;

public class SteamManager : MonoBehaviour{

    public static void AddGameToSteamLibrary(string gameName, string exePath)
    {
        if (!File.Exists(exePath)){
            Debug.LogError($"[SteamShortcut] Executable not found at: {exePath}");
            return;
        }

        string gameDir = Path.GetDirectoryName(exePath);
        string steamUserDataDir = "/home/deck/.local/share/Steam/userdata/";
        if (!Directory.Exists(steamUserDataDir))
        {
            Debug.LogError("[SteamShortcut] Steam userdata directory not found. Ensure this is running on SteamOS.");
            return;
        }

        string[] userDirs = Directory.GetDirectories(steamUserDataDir);
        if (userDirs.Length == 0)
        {
            Debug.LogError("[SteamShortcut] No active Steam user profiles detected.");
            return;
        }
        string shortcutsPath = Path.Combine(userDirs[0], "config", "shortcuts.vdf");

        try{
            byte[] shortcutPayload = CreateShortcutBlock(gameName, exePath, gameDir);
            if (!File.Exists(shortcutsPath)){
                using (BinaryWriter bw = new BinaryWriter(File.Create(shortcutsPath)))
                {
                    bw.Write((byte)0x00); // Start marker
                    bw.Write(Encoding.ASCII.GetBytes("shortcuts"));
                    bw.Write((byte)0x00);
                    bw.Write(shortcutPayload);
                    bw.Write((byte)0x08); // End marker
                    bw.Write((byte)0x08); // End marker
                }
            }
            else
            {
                // Append to an existing shortcuts file safely
                byte[] fileBytes = File.ReadAllBytes(shortcutsPath);
                
                // Find the structural end markers at the tail of the file to splice into
                int insertIndex = fileBytes.Length - 2; 
                
                using (MemoryStream ms = new MemoryStream())
                {
                    ms.Write(fileBytes, 0, insertIndex);
                    ms.Write(shortcutPayload, 0, shortcutPayload.Length);
                    ms.WriteByte(0x08);
                    ms.WriteByte(0x08);

                    File.WriteAllBytes(shortcutsPath, ms.ToArray());
                }
            }

            Debug.Log($"[SteamShortcut] Successfully added '{gameName}' to Steam shortcuts. Change will take effect after restarting Steam.");
        }
        catch (Exception ex)
        {
            Debug.LogError($"[SteamShortcut] Failed writing to VDF file: {ex.Message}");
        }
    }

    /// <summary>
    /// Generates Valve's binary KeyValues data structure for a shortcut entry.
    /// </summary>
    private static byte[] CreateShortcutBlock(string name, string exe, string dir)
    {
        using (MemoryStream ms = new MemoryStream())
        using (BinaryWriter bw = new BinaryWriter(ms))
        {
            // Unique entry key index string (using timestamps prevents index collisions)
            string entryIndex = DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString();

            bw.Write((byte)0x00); // Entry type object
            bw.Write(Encoding.ASCII.GetBytes(entryIndex));
            bw.Write((byte)0x00);

            // 1. AppName string field
            bw.Write((byte)0x01); 
            bw.Write(Encoding.ASCII.GetBytes("AppName"));
            bw.Write((byte)0x00);
            bw.Write(Encoding.UTF8.GetBytes(name));
            bw.Write((byte)0x00);

            // 2. Exe string field (wrapped in quotes for system safety)
            bw.Write((byte)0x01);
            bw.Write(Encoding.ASCII.GetBytes("Exe"));
            bw.Write((byte)0x00);
            bw.Write(Encoding.UTF8.GetBytes($"\"{exe}\""));
            bw.Write((byte)0x00);

            // 3. StartDir string field (Forces execution inside its local directory context)
            bw.Write((byte)0x01);
            bw.Write(Encoding.ASCII.GetBytes("StartDir"));
            bw.Write((byte)0x00);
            bw.Write(Encoding.UTF8.GetBytes($"\"{dir}/\"")); // Valve expectations favor trailing slashes
            bw.Write((byte)0x00);

            // 4. Default structural fields required to satisfy the file parser layout
            WriteEmptyStringField(bw, "icon");
            WriteEmptyStringField(bw, "ShortcutPath");
            WriteEmptyStringField(bw, "LaunchOptions");
            
            // IsDev boolean field (false)
            bw.Write((byte)0x02);
            bw.Write(Encoding.ASCII.GetBytes("IsDev"));
            bw.Write((byte)0x00);
            bw.Write(0); 

            // Close current index map
            bw.Write((byte)0x08);

            return ms.ToArray();
        }
    }

    private static void WriteEmptyStringField(BinaryWriter bw, string fieldName)
    {
        bw.Write((byte)0x01);
        bw.Write(Encoding.ASCII.GetBytes(fieldName));
        bw.Write((byte)0x00);
        bw.Write((byte)0x00);
    }
}
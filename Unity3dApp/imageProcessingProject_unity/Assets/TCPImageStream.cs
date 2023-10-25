using System;
using UnityEngine;
using System.Threading;
using System.Net.Sockets;
using System.IO;
using System.Collections.Concurrent;
using UnityEngine.UI;

public class TCPImageStream : MonoBehaviour
{
    Thread m_NetworkThread;
    bool m_NetworkRunning;
    ConcurrentQueue<byte[]> dataQueue = new ConcurrentQueue<byte[]>();
    Texture2D tex2 = new Texture2D(640, 400, TextureFormat.RGB24, false);
    private void OnEnable()
    {
        m_NetworkRunning = true;
        m_NetworkThread = new Thread(NetworkThread);
        m_NetworkThread.Start();
        
    }
    private void OnDisable()
    {
        m_NetworkRunning = false;
        if (m_NetworkThread != null)
        {
            if (!m_NetworkThread.Join(100))
            {
                m_NetworkThread.Abort();
            }
        }
    }
    private void NetworkThread()
    {
        TcpClient client = new TcpClient();
        client.Connect("127.0.0.1", 12345);
        using (var stream = client.GetStream())
        {
            BinaryReader reader = new BinaryReader(stream);
            try
            {
                Debug.Log("try read");
                while (m_NetworkRunning && client.Connected && stream.CanRead)
                {
                    // int length = reader.ReadInt32();
                    // print(length);
                    int length = 360000;
                    byte[] dataLen = reader.ReadBytes(4);
                    
                    Int32 len = BitConverter.ToInt32(dataLen, 0);
                    Debug.Log("length: " + len);
                    byte[] data = reader.ReadBytes(len);
                    if(data.Length!=0)
                        print(data.Length);
                    dataQueue.Enqueue(data);
                }
            }
            catch(Exception ex)
            {
                Debug.Log("ex");
                Debug.LogException(ex, this);
            }
        }
    }
 
    public Material mat;
    public Texture2D tex = null;
 
    void Update()
    {
        byte[] data;
        if (dataQueue.Count > 0 && dataQueue.TryDequeue(out data))
        {
            if (data.Length > 0)
            {
                Debug.Log("inside texture update");
                if (tex == null)
                    tex = new Texture2D(640, 640);
                print(tex.LoadImage(data));
                tex.Apply();
                GetComponent<Renderer>().material.SetTexture("_MainTex", tex);
            }
        }
    }
}
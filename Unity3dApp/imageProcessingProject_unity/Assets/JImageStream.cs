using System;
using UnityEngine;
using System.Threading;
using System.Net.Sockets;
using System.IO;
using System.Collections.Concurrent;
using UnityEngine.UI;

public class JImageStream : MonoBehaviour
{
    public ScoreCounter scoreCounter;
    Thread m_NetworkThread;
    bool m_NetworkRunning;
    ConcurrentQueue<byte[]> dataQueue = new ConcurrentQueue<byte[]>();
    Texture2D tex2 = new Texture2D(640, 400, TextureFormat.RGB24, false);
    public GraphManager graph;
    public PatternDisplay patternDisplay;
    public ScoreCounter totalCnt;
    public ScoreCounter comboCnt;
    public MiniGame miniGame;
    private Int32 patternNum;

    private Int32 totalCounter;
    private Int32 comboCounter;
        
    private Int32 score;
    private Int32 combo;
    private Int32 bonus;
    private Int32 targetPosX;
    private Int32 targetPosY;
    private Int32 targetBonus;
    private Int32 targetCounter;
    private Int32 imgSize;
    private Int32[] xBalls;
    private Int32[] yBalls;
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
        xBalls = new int[4];
        yBalls = new int[4];
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
                    
                    patternNum = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    patternDisplay.showPattern((PatternDisplay.Pattern)patternNum);
                    totalCounter = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    totalCnt.updateCounter(totalCounter);
                    comboCounter = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    comboCnt.updateCounter(comboCounter);
                    
                    score = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    combo = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    scoreCounter.updateCounter(score, combo);
                    
                    bonus = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    targetPosX = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    targetPosY = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    
                    targetBonus = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    targetCounter = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    miniGame.updateVals(targetPosX, targetPosY, targetBonus, targetCounter);
                    for (int i = 0; i < xBalls.Length; i++)
                    {
                        xBalls[i] = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                        yBalls[i] = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                    }
                    graph.updateGraph(xBalls[0],yBalls[0],xBalls[1],yBalls[1],xBalls[2],yBalls[2],xBalls[3],yBalls[3]);
                    imgSize = BitConverter.ToInt32(reader.ReadBytes(4), 0);
                 
                    byte[] data = reader.ReadBytes(imgSize);
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
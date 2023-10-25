using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using UnityEngine.UI;

public class MyStreamer : MonoBehaviour
{
    // private Texture tex;
    Texture2D tex = new Texture2D(500, 500, TextureFormat.PVRTC_RGBA4, false);
    void Start()
    {
        StartCoroutine(GetText());
        // GetComponent<RawImage>().texture = tex;
    }

    IEnumerator GetText()
    {
        
        using (UnityWebRequest uwr = UnityWebRequestTexture.GetTexture("http://127.0.0.1:8080/video_feed"))
        // using (UnityWebRequest uwr = UnityWebRequest.Get("http://127.0.0.1:8080/video_feed"))
        {
            Debug.Log("texture 1");
            yield return uwr.SendWebRequest();
            Debug.Log("texture 2");
            if (uwr.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(uwr.error);
            }
            else
            {
                Debug.Log("texture was found");
                // LoadRawTextureData(uwr.Ge)
                // Get downloaded asset bundle
                Debug.Log(uwr);
                // GetComponent<RawImage>().texture = DownloadHandlerTexture.GetContent(uwr);
                  
            }
        }
    }
}
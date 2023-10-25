using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlusSpawner : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject plusSticker;
    private PlusSticker sticker;
    public AudioClip coinSound; 
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void spawn(int value)
    {
        sticker = GameObject.Instantiate(plusSticker,transform).GetComponent<PlusSticker>();
        sticker.show(value);
        Destroy(sticker,1);
        GetComponent<AudioSource>().PlayOneShot(coinSound);
    }
}

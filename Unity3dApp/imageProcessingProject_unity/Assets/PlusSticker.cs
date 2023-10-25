using System.Collections;
using System.Collections.Generic;
using DG.Tweening;
using TMPro;
using UnityEditor.Experimental.GraphView;
using UnityEngine;

public class PlusSticker : MonoBehaviour
{
    // Start is called before the first frame update
    public bool great;
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void show(int value)
    {
        if (!great)
            GetComponent<TextMeshPro>().SetText('+'+value.ToString());
        
        transform.DOMoveY(transform.position.y + 3, 0.6f);
        GetComponent<TextMeshPro>().DOFade(0, 0.6f);
        
    }

}

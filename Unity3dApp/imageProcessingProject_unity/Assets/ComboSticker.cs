using System.Collections;
using System.Collections.Generic;
using DG.Tweening;
using UnityEngine;

public class ComboSticker : MonoBehaviour
{
    // Start is called before the first frame update
    private Vector3 initPos;
    public float ShakeStrengh;
    public int ShakeVibrito;
    public float duration;
    private bool DoCombo1 = false;
    void Start()
    {
        initPos = transform.position;
        // ShowCombo();
    }

    // Update is called once per frame
    void Update()
    {
        if (DoCombo1)
        {
            DoCombo1 = false;
            transform.position = initPos;
            transform.DOMoveY(10, 1.2f).SetEase(Ease.OutBounce);
            transform.DOShakeScale(duration,ShakeStrengh,ShakeVibrito);
            Invoke(nameof(outCombo), duration-0.6f);
        }
            
    }

    public void ShowCombo()
    {
        DoCombo1 = true;
    }

    void outCombo()
    {
        transform.DOMoveY(40, 1.2f).SetEase(Ease.OutCubic);
    }
}

using System.Collections;
using System.Collections.Generic;
using DG.Tweening;
using TMPro;
using UnityEditor.U2D;
using UnityEngine;

public class MiniGame : MonoBehaviour
{
    // Start is called before the first frame update
    private int lastX =-1;
    private int lastY =-1;
    private int targetScore=0;
    private int targetCount=0;
    
    private int newLastX =-1;
    private int newLastY =-1;
    private int newTargetScore=0;
    private int newTargetCount=0;
    
    private Vector3 initPos;
    private Vector3 endPos;
    private bool gameOn=false;
    public TextMeshPro textScore;
    public TextMeshPro textCount;
    public PlusSpawner greatSpawner;
    public AudioClip successSound;
    public AudioClip miniGameSound;
    
    private bool doUpdate = false;
    void Start()
    {
        initPos = transform.position;
        endPos = new Vector3(initPos.x, initPos.y - 15, initPos.z);

    }

    // Update is called once per frame
    void Update()
    {
        if (doUpdate)
        {
            doUpdate = false;
            doUpdateVals(newLastX, newLastY, newTargetScore, newTargetCount);
            
        }
    }

    public void updateVals(int x, int y, int targetScore1, int targetCount1)
    {
        if (x != lastX)
        {
            newLastX = x;
            newLastY = y;
            newTargetCount = targetCount1;
            newTargetScore = targetScore1;
            doUpdate = true;
        }
    }
    
    void doUpdateVals(int x, int y,int targetScore1,int targetCount1)
    {
        textScore.SetText(targetScore1.ToString());
        textCount.SetText(targetCount1.ToString());
        
        if (x == -1 && gameOn)
        {
            transform.DOMove(initPos, 1.4f).SetEase(Ease.InBounce);
            gameOn = false;
            return;
        }

        if (x != -1 && !gameOn)
        {
            transform.DOMove(endPos, 1.4f).SetEase(Ease.InBounce);
            GetComponent<AudioSource>().PlayOneShot(miniGameSound);
            gameOn = true;
        }
        
        
        if (this.targetScore != targetScore1)
        {
             // newScore ,might be 0
             if(targetScore1!=0)
                  GetComponent<AudioSource>().PlayOneShot(successSound);
             this.targetScore = targetScore1;
             this.targetCount = targetCount1;
        }

        lastX = x;
        lastY = y;

    }
}

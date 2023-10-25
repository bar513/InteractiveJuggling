using System.Collections;
using System.Collections.Generic;
using DG.Tweening;
using TMPro;
using UnityEngine;
using UnityEngine.SocialPlatforms.Impl;

public class ScoreCounter : MonoBehaviour
{
    // Start is called before the first frame update
    public TextMeshPro textMesh;
    public PlusSpawner plusSpawner;
    public ComboSticker comboSticker1;
    public ComboSticker comboSticker2;
    public AudioClip combo1;
    public AudioClip combo2;
    public bool spawnPlus;
    public int score = 0;
    int testCounter = 0;
    private int oldScore=0;
    private int lastCombo = 0;
    void Start()
    {
        // updateCounter(120, 100);
    }

    // Update is called once per frame
    void Update()
    {
        
        // if (Random.Range(0, 10000) > 9990)
        // {
        //     testCounter += 1;
        //     UpdateScore(testCounter);
        // }
        if (oldScore != score)
        {
            if (lastCombo != 0 && spawnPlus)
            {
                comboSticker1.ShowCombo();
                GetComponent<AudioSource>().PlayOneShot(combo1);
                lastCombo = 0;
            }
            //play sound
            textMesh.SetText(score.ToString());
            // transform.DOPunchRotation(new Vector3(5, 3, 0), 0.3f,1,0.8f);
            if (spawnPlus)
                plusSpawner.spawn(score - oldScore);

            oldScore = score;
            
        }
    }

    void UpdateScore(int newScore)
    {
        if (newScore != score)
        {
            oldScore = score;
            score = newScore;
            
        }
    }

    public void updateCounter(int score, int combo=0)
    {
        lastCombo = combo;
        UpdateScore(score);
        

    }
}

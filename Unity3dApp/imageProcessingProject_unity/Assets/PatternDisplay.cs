using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.Video;

public class PatternDisplay : MonoBehaviour
{


    public enum Pattern
    {
        UNKNOWN = 0,
        ONE_BALL_ONE_HAND = 1,
        ONE_BALL_TWO_HANDS = 2,
        TWO_BALLS_ONE_HAND = 3,
        TWO_BALLS_TWO_HANDS = 4,
        THREE_BALLS_CACADE = 5,
        THREE_BALLS_CACADE_WIDE = 6,
        THREE_BALLS_FOUNTAIN = 7,
        THREE_BALLS_ONE_ABOVE = 8,
        THREE_BALLS_ONE_ELEVATOR = 9,
        FOUR_BALLS_ASYNC = 10,
        FOUR_BALLS_SYNC = 11    
    }

    private string[] patternNames =
    {
        "Nothing", "1 up down", "1 between hands", "2 up down", "2 both hands sync", "3 cascade", "3 cascade wide",
        "3 fountain", "3 one above", "3 elevator", "4 async", "4 sync"
    };

    private Pattern currentPattern = Pattern.UNKNOWN;

    public VideoClip[] clips;

    public Jeffect effect;

    public TextMeshPro textMesh;

    private bool shouldShowPattern = false;
    // Start is called before the first frame update
    void Start()
    {
        // Invoke("testShowPattern",4);    
    }

    void testShowPattern()
    {
        showPattern(Pattern.ONE_BALL_TWO_HANDS);
    }
    

    // Update is called once per frame
    void Update()
    {
        if (shouldShowPattern)
        {
            shouldShowPattern = false;
            doShowPattern(currentPattern);
        }
            
    }

    public void showPattern(Pattern newPattern)
    {
        if (currentPattern != newPattern)
        {
            currentPattern = newPattern;
            shouldShowPattern = true;
        }
    }

    void doShowPattern(Pattern newPattern)
    {
        GetComponent<VideoPlayer>().clip = clips[(int)currentPattern];
        effect.showEffect();
        textMesh.SetText(patternNames[(int)currentPattern]);
        
    }
}

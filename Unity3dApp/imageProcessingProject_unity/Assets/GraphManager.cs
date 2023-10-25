using System.Collections;
using System.Collections.Generic;
using DG.Tweening;
using UnityEngine;

public class GraphManager : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject[] nodes;
    public Transform graphCam;
    private Vector3 initPos;
    private float xOffest=0;
    private float cameraOffset = -14;
    
    private bool shouldUpdateGraph = false;
    private int[] xArr;
    private int[] yArr;
    void Start()
    {
        initPos = transform.position;
        xArr = new[] { -1, -1, -1, -1 };
        yArr = new[] { -1, -1, -1, -1 };

    }

    // Update is called once per frame
    void Update()
    {
        if (shouldUpdateGraph)
        {
            shouldUpdateGraph = false;
            addNodes();
        }
    }

    public void updateGraph(int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4)
    {
        xArr[0] = x1;
        xArr[1] = x2;
        xArr[2] = x3;
        xArr[3] = x4;
        
        yArr[0] = y1;
        yArr[1] = y2;
        yArr[2] = y3;
        yArr[3] = y4;
        shouldUpdateGraph = true;
    }
    private void addNodes()
    {
        if(xArr[0]!=-1)
            addNode(0, xArr[0], yArr[0]);
        if(xArr[1]!=-1)
            addNode(1, xArr[1], yArr[1]);
        if(xArr[2]!=-1)
            addNode(2, xArr[2], yArr[2]);
        if(xArr[3]!=-1)
            addNode(3, xArr[3], yArr[3]);
        moveGraph();
    }
    private void addNode(int id, int x, int y)
    {
         Destroy(Instantiate(nodes[id],new Vector3(initPos.x+ xOffest,initPos.y - y/10f, initPos.z ),Quaternion.identity),2);
    }

    private void moveGraph()
    {
        xOffest += 1;
        graphCam.DOMoveX(initPos.x + xOffest + cameraOffset, 0.06f);
    }
}

# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

from OCC.Core.gp import gp_Pnt, gp_Trsf
from OCC.Core.Geom import Geom_CartesianPoint

from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeCircle
from OCC.Core.AIS import AIS_Shape, AIS_Point, AIS_Circle
from OCC.Core.BRepBuilderAPI import  BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform 
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool

from OCC.Core.TopAbs import (TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL,
                      TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE)

from scene import (SceneGetNative, SceneDrawCircle3, SceneDrawShape, SceneDrawPoint,
                   SceneDrawLabel, SceneLayer, SceneLevelUp, SceneLevelDown,
                   SceneScreenInit, SceneScreenStart, SceneDrawAxis)

from math import cos, sin, pi

# todo 
# Переименовать переменные с указанием типа
# Cделать базовую окружность шире 

def cylPnt(x, y, z, r, a, h):
    angle = a / 180 * pi 
    return gp_Pnt(x + r*cos(angle), y +r*sin(angle), z+h)

def PaintDaoShape(r, l):
  
    # base points    
    r2 = r/2
    
    p1 = gp_Pnt(0,0,0)      
    p2 = cylPnt(0,r2, 0 , r2, 90 + 90 + 45, 0)      
    p3 = gp_Pnt(-r2,r2,0)      
    p4 = cylPnt(0,r2, 0 , r2, 90 + 45, 0)      
    p5 = gp_Pnt(0,r,0)      
    p6 = gp_Pnt(r,0,0)      
    p7 = gp_Pnt(0,-r,0)      
    p8 = gp_Pnt(r2,-r2,0)      
 
    # base circle
    SceneLayer('info')
    SceneDrawCircle3('circle', p5,p6,p7)
  
    # base dao
    arc1 =  GC_MakeArcOfCircle(p1,p2,p3).Value()
    arc2 =  GC_MakeArcOfCircle(p3,p4,p5).Value()
    arc3 =  GC_MakeArcOfCircle(p5,p6,p7).Value()
    arc4 =  GC_MakeArcOfCircle(p7,p8,p1).Value()
 
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(arc4).Edge()
  
    wireDaoBase = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    SceneLayer('base')
    SceneDrawShape('dao_base', wireDaoBase)
    
    # dao with offset
    offset = BRepOffsetAPI_MakeOffset()
    offset.AddWire(wireDaoBase)
    offset.Perform(-l)
    wireDao = offset.Shape()  
    SceneLayer('main')
    SceneDrawShape('dao', wireDao)
    
    # mirrored dao
    transform = gp_Trsf()
    transform.SetMirror(gp_Pnt(0,0,0))
    
    wireDaoMirr =  BRepBuilderAPI_Transform(wireDao, transform).Shape()
    SceneLayer('info')
    SceneDrawShape('dao_mirr', wireDaoMirr)
    
def DetectBasePoints(name)     :
    
    dao = SceneGetNative(name)
    shape = dao.Shape()
    exp = TopExp_Explorer(shape, TopAbs_VERTEX)
    i = 0
    while (exp.More()):
       vertex = exp.Current()
       tool = BRep_Tool()
       pnt = tool.Pnt(vertex)
       SceneLayer('base')
       if i % 2 == 0:
          vind =  str(int(i/2))
          vname =  name+'_vertex_'+ vind
          SceneDrawPoint(vname, pnt)
          SceneDrawLabel(vname, 'p'+vind)
       i += 1 
       exp.Next()
  
  
if __name__ == '__main__':
    
    SceneScreenInit()
    
    SceneDrawAxis('axis')
    
    SceneLevelDown('dao_draw')
  
    PaintDaoShape(5,0.3)
    DetectBasePoints('dao')
    
    SceneLevelUp()
    
    SceneScreenStart()

